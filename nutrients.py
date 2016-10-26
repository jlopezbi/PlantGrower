import bpy
import numpy as np
import random
import math
# NOTE: working here to set up particles system


class ParticleSystem(object):
    ''' composed of world an a set of particles.
    perhaps this is the main simulation
    '''

    def __init__(self, num_particles, world):
        self.world = world
        self.randomness_of_motion = 0.0  # [0, 1.0]
        #NOTE: probs should make magnitude of trend motion some multiple of particle radius
        self.trend_motion_vec = np.array((0.0,0.0,-0.3))
        self.radius = .6
        self.num_particles = num_particles
        self.particles = []
        self._init_particles()

    def _init_particles(self):
        #perhaps adding all the particles to the top plane and the running
        #the simulation causes some odd stuff to happen right at the beginning
        # i.e. a ton of particles colliding in a small time frame. How to space it out?
        for i in range(self.num_particles):
            position = self.world.get_a_spawn_location()
            self.particles.append(
                Particle(position, self.radius, self.trend_motion_vec))

    def show_particles(self):
        for p in self.particles:
            p.show()

    def move_particles(self):
        '''
        sends command to all particles to
        move
        '''
        for p in self.particles:
            p.move(self.randomness_of_motion)

    def re_spawn_escaped_particles(self):
        #NOTE: working here, just need to try out running alot of particles
        #This is trivial solution. if it ends up being slow consider seraching for some sort of spatial data structure to solve problem
        '''
        particles that have escaped the world are moved back to spawn_plane
        '''
        for p in self.particles:
            if not self.world.particle_is_inside(p):
                new_pos = self.world.get_a_spawn_location()
                p.set_position(new_pos)

    def re_spawn_particle(self,particle):
        '''
        moves particle back to spawn location
        '''
        new_pos = self.world.get_a_spawn_location()
        particle.set_position(new_pos)


    def show_case_particle_motion(self,steps=10):
        init_pos = (0.,0.,0.)
        p1 = Particle(init_pos,self.radius,self.trend_motion_vec)
        for i in range(steps):
            p1.move(self.randomness_of_motion)
            p1.show()

class Particle(object):

    def __init__(self, position, radius, trend_velocity):
        self.position = np.array(position)
        self.radius = radius
        self.trend_velocity = np.array(trend_velocity)

    def _get_trend_speed(self):
        return np.linalg.norm(self.trend_velocity)
    
    def set_position(self,new_position):
        self.position = np.array(new_position)

    def move(self, randomness=0.5):
        '''
        randomness is in range [0,1] for random brownian-like motion
        '''
        magnitude = self._get_trend_speed() 
        displacement_vec = self.trend_velocity*(1.-randomness) + self._get_random_vector(magnitude)*randomness
        displacement_vec = self.trend_velocity*(1.-randomness) + self._get_random_vector(magnitude)*randomness
        self.position += displacement_vec


    def show(self):
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        # bpy.ops.object.empty_add(type='SPHERE',radius=self.radius,location=(x,y,z))
        bpy.ops.surface.primitive_nurbs_surface_sphere_add(
            radius=self.radius, location=(x, y, z))

    def _get_random_vector_biased(self, speed):
        '''
        depricated function using traingular distribution to
        bias movement
        '''
        self.peak_inclination = math.pi * grav_factor
        inclination = random.triangular(
            0, math.pi + .00001, self.peak_inclination)
        azimuth = random.uniform(0, math.pi * 2.0)
        velX = speed * math.sin(azimuth) * math.cos(inclination)
        velY = speed * math.sin(azimuth) * math.sin(inclination)
        velZ = speed * math.cos(inclination)
        return np.array([velX, velY, velZ])
    
    def _get_random_vector(self,magnitude=1.0):
        '''
        '''
        padding = .00001
        inclination = random.uniform(0, math.pi)
        azimuth = random.uniform(0, math.pi * 2.0)
        X = magnitude * math.sin(azimuth) * math.cos(inclination)
        Y = magnitude * math.sin(azimuth) * math.sin(inclination)
        Z = magnitude * math.cos(inclination)
        return np.array([X, Y, Z])

