import math
from numpy import linalg as LA
import numpy as np


class VERTEX:
    def define_vertex(self,_id,_coords):
        self.id=_id
        self.coords=_coords
        self.pcoords=_coords
    def perturbate_coords(self,_dof,perturbation):
        #self.pcoords=self.coords
        self.pcoords[_dof]=self.coords[_dof]+perturbation
    def set_pcoords(self):
        self.pcoords=self.coords
    def update_coords(self,_h):
        self.coords[0]=self.coords[0]+_h[(self.id-1)*2]
        self.coords[1]=self.coords[1]+_h[(self.id-1)*2+1]

class EDGE:
    def define_edge(self,_id,_vertices):
        self.id=_id
        self.vertices=_vertices
    def define_angle_length_K(self):
        delta_x=(self.vertices[1].coords[0]-self.vertices[0].coords[0])
        delta_y=(self.vertices[1].coords[1]-self.vertices[0].coords[1])
        self.length=math.sqrt(delta_x*delta_x+delta_y*delta_y)
        self.c=delta_x/self.length
        self.s=delta_y/self.length
        c=self.c
        s=self.s
        self.K=np.array(
        ([c*c,s*c,-1.0*c*c,-1.0*s*c],
        [s*c,s*s,-1.0*s*c,-1.0*s*s],
        [-1.0*c*c,-1.0*s*c,c*c,s*c],
        [-1.0*s*c,-1.0*s*s,s*c,s*s]),dtype=float)
        for i in range(4):
            for j in range(4):
                self.K[i][j]=self.K[i][j]/self.length
    def define_pangle_plength_pK(self):
        delta_x=(self.vertices[1].pcoords[0]-self.vertices[0].pcoords[0])
        delta_y=(self.vertices[1].pcoords[1]-self.vertices[0].pcoords[1])
        self.plength=math.sqrt(delta_x*delta_x+delta_y*delta_y)
        self.c=delta_x/self.plength
        self.s=delta_y/self.plength
        c=self.c
        s=self.s
        self.pK=np.array(
        ([c*c,s*c,-1.0*c*c,-1.0*s*c],
        [s*c,s*s,-1.0*s*c,-1.0*s*s],
        [-1.0*c*c,-1.0*s*c,c*c,s*c],
        [-1.0*s*c,-1.0*s*s,s*c,s*s]),dtype=float)
        for i in range(4):
            for j in range(4):
                self.pK[i][j]=self.pK[i][j]/self.plength
    def store_vertex_pairs(self):
        first=self.vertices[0].id
        second=self.vertices[1].id
        self.pair=(first,second)
        if second<first:
            self.pair=(second,first)
        

