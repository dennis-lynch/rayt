import math

from rayt_python.hittable import HitRecord
from rayt_python.ray import Ray
from rayt_python.vec3 import Color, dot
from rayt_python.utils import random_double


class Material:
    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> bool:
        raise NotImplementedError


class Lambertian(Material):
    def __init__(self, albedo: Color) -> None:
        self.albedo = albedo

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> bool:
        scatter_direction = rec.normal + random_unit_vector()
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return True


class Metal(Material):
    def __init__(self, a: Color, f: float) -> None:
        self.albedo = a
        self.fuzz = f if f < 1 else 1

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> bool:
        reflected = reflect(unit_vector(r_in.direction()), rec.normal)
        scattered = Ray(rec.p, reflected + fuzz * random_in_unit_sphere())
        attenuation = albedo
        return dot(scattered.direction(), rec.normal) > 0


class Dielectric(Material):
    def __init__(self, ri: float) -> None:
        self.ref_idx = ri

    def scatter(
        self, r_in: Ray, rec: HitRecord, attenuation: Color, scattered: Ray
    ) -> bool:
        attenuation = Color(1.0, 1.0, 1.0)
        etai_over_etat = 1.0 / ref_idx if rec.front_face else ref_idx
        unit_direction = unit_vector(r_in.direction())
        cos_theta = fmin(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)

        if etai_over_etat * sin_theta > 1.0:
            reflected = reflect(unit_direction, rec.normal)
            scattered = Ray(rec.p, reflected)
            return True

        reflected_prob = schlick(cos_theta, etai_over_etat)
        if random_double() < reflected_prob:
            reflected = reflect(unit_direction, rec.normal)
            scattered = Ray(rec.p, reflected)
            return True

        refracted = refract(unit_direction, rec.normal, etai_over_etat)
        scattered = Ray(rec.p, refracted)
        return True