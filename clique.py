

import os 
import sys
import time 
import math
import xlrd
import random
import xlsxwriter
import clique_graph_read_write
import clique_classes
import clique_global_functions
import clique_optimization_functions

from numpy import linalg as LA
import numpy as np


debugfile=open("debugfile.log","w")
wb = xlsxwriter.Workbook('graph.xlsx')

graphfile=open("graph.txt","w")
coordfile=open("coord.txt","w")
numberofvertices=10
numberofedges=20
radius=5.0
clique_graph_read_write.generate_complete_graph(graphfile,coordfile,numberofvertices,radius)
#clique_graph_read_write.generate_arbitrary_graph(graphfile,coordfile,numberofvertices,numberofedges,radius)
graphfile.close()
coordfile.close()
graphfile=open("graph.txt","r")
coordfile=open("coord.txt","r")

ws = wb.add_worksheet("graph_topology")
    
vertices={}
edges={}

clique_graph_read_write.read_graph(vertices,edges,graphfile)
clique_graph_read_write.read_coordinates(coordfile,vertices)
clique_global_functions.update_edges(edges,vertices)
ndof=len(vertices.keys())*2

for e in edges.values():
    e.define_angle_length_K()
clique_graph_read_write.write_graph(edges,ndof,wb,ws)
    
s=(ndof,ndof)
K=np.zeros(s)
clique_global_functions.assembly_K(K,edges)
#clique_graph_read_write.write_global_K(ndof,debugfile,K)
eigenvalues, eigenvectors = LA.eigh(K)
real_values_to_vectors={}
for e in range(ndof):
    real_values_to_vectors[float(eigenvalues[e])]=eigenvectors[:,e]
clique_graph_read_write.write_graph_eigenvectors(edges,vertices,wb,ws,real_values_to_vectors)
wb.close()
#clique_graph_read_write.write_eigenvalues(ndof,debugfile,real_values_to_vectors)
#objective_vector=clique_graph_read_write.read_objective_eigenvector(ndof)
for e in edges.values():
    e.store_vertex_pairs()
    #print e.pair
cog=clique_global_functions.evaluate_system_cog(edges)
print cog
clique_global_functions.brute_force_max_clique(vertices,edges)
'''
clique_graph_read_write.write_graph_eigenvectors(edges,vertices,wb,ws,real_values_to_vectors)
current_eigenvector=eigenvectors[:,ndof-1]
objective_vector=clique_graph_read_write.read_objective_eigenvector(ndof)
f=clique_optimization_functions.objective_function(objective_vector,current_eigenvector)
print f
perturbation=0.1
delf_delv,del2f_delv2=clique_optimization_functions.evaluate_h(ndof,vertices,edges,perturbation,objective_vector,current_eigenvector)
x_upd=np.array([0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01])
f_x_pl_xupd=f+np.dot(delf_delv,x_upd)+np.dot(np.dot(del2f_delv2,x_upd),x_upd)*0.5
print f_x_pl_xupd


for vertex in vertices.values():
    vertex.update_coords(x_upd)
clique_global_functions.update_edges(edges,vertices)
s=(ndof,ndof)
K=np.zeros(s)
for e in edges.values():
    e.define_angle_length_K()
clique_global_functions.assembly_K(K,edges)
eigenvalues, eigenvectors = LA.eigh(K)
current_eigenvector=eigenvectors[:,ndof-1]
current_objective=clique_optimization_functions.objective_function(objective_vector,current_eigenvector)
print current_objective

'''
'''

divergence=True
perturbation=0.1
current_eigenvector=eigenvectors[:,ndof-1]
iterations=0
while (divergence and iterations<1000):
    current_search=clique_optimization_functions.evaluate_h(ndof,vertices,edges,perturbation,objective_vector,current_eigenvector)
    #print current_search
    #current_search=current_search/LA.norm(current_search)*2.0   
    for vertex in vertices.values():
        vertex.update_coords(current_search)
    #print current_search
    clique_global_functions.update_edges(edges,vertices)
    s=(ndof,ndof)
    K=np.zeros(s)
    for e in edges.values():
        e.define_angle_length_K()
    clique_global_functions.assembly_K(K,edges)
    eigenvalues, eigenvectors = LA.eigh(K)
    current_eigenvector=eigenvectors[:,ndof-1]
    current_objective=clique_optimization_functions.objective_function(objective_vector,current_eigenvector)
    #print objective_vector
    #print current_eigenvector
    if math.fabs(current_objective)<0.01:
        divergence=False
    print math.fabs(current_objective)
    iterations=iterations+1
real_values_to_vectors={}
for e in range(ndof):
    real_values_to_vectors[float(eigenvalues[e])]=eigenvectors[:,e]
clique_graph_read_write.write_eigenvalues(ndof,debugfile,real_values_to_vectors)
clique_graph_read_write.write_graph(edges,ndof,wb,ws)
clique_graph_read_write.write_graph_eigenvectors(edges,vertices,wb,ws,real_values_to_vectors)
'''
wb.close()  
