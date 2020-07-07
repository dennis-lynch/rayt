use crate::vec3::{Point3, Vec3};

pub struct Ray {
    pub origin: Point3,
    pub direction: Vec3,
}

impl Ray {
    pub(crate) fn new(origin: Point3, direction: Vec3) -> Self {
        Self { origin, direction }
    }

    pub(crate) fn at(self, t: f64) -> Point3 {
        self.origin + t * self.direction
    }
}