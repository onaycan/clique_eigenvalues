import xlsxwriter
import random
from clique_classes import VERTEX
from clique_classes import EDGE
from xlsxwriter.utility import xl_rowcol_to_cell
from numpy import linalg as LA
import numpy as np
import clique_global_functions

def objective_function(_objective_vector,_current_eigenvector):
	return LA.norm(_objective_vector-_current_eigenvector)
	
def evaluate_h(_ndof,_vertices,_edges,perturbation,_objective_vector,_current_eigenvector):
	delf_delv=np.zeros(_ndof,dtype=float)
	del2f_delv2=np.zeros((_ndof,_ndof),dtype=float)
	
	for i in range(_ndof):
		#_vertices[i/2+1].pcoords=_vertices[i/2+1].coords
		_vertices[i/2+1].perturbate_coords(i%2,perturbation)
		clique_global_functions.update_perturbated_edges(_edges,_vertices)
		for e in _edges.values():
			e.define_pangle_plength_pK()		
		s=(_ndof,_ndof)
		pK=np.zeros(s)
		clique_global_functions.assembly_perturbated_K(pK,_edges)
		eigenvalues, eigenvectors = LA.eigh(pK)
		current_peigenvector=eigenvectors[:,_ndof-1]
		#print _current_eigenvector
		#print current_peigenvector
		plu_f=objective_function(_objective_vector,current_peigenvector)
		f=objective_function(_objective_vector,_current_eigenvector)
		#print plu_f, f
		delf_delv[i]=(plu_f-f)/perturbation
		for vertex in _vertices.values():
			vertex.set_pcoords()
		for j in range(_ndof):
			 _vertices[j/2+1].perturbate_coords(j%2,-perturbation)
			 clique_global_functions.update_perturbated_edges(_edges,_vertices)
			 for e in _edges.values():
				e.define_pangle_plength_pK()
			 s=(_ndof,_ndof)
			 pK=np.zeros(s)
			 clique_global_functions.assembly_perturbated_K(pK,_edges)
			 eigenvalues, eigenvectors = LA.eigh(pK)
			 current_peigenvector=eigenvectors[:,_ndof-1]
			 min_f=objective_function(_objective_vector,current_peigenvector)
			 del2f_delv2[i][j]=(plu_f-2.0*f+min_f)/perturbation/perturbation
			 for vertex in _vertices.values():
				vertex.set_pcoords()
	
	#return delf_delv,del2f_delv2
	#h = np.linalg.solve(del2f_delv2, -delf_delv)
	mu=1.0
	iterations=0
	if LA.det(del2f_delv2)>0.0:
		del2f_delv2=del2f_delv2+np.identity(_ndof)*1000.0
	
	while(LA.det(del2f_delv2)<0.0):
		del2f_delv2=del2f_delv2+np.identity(_ndof)*mu
		mu=mu*2
		iterations=iterations+1
	#print LA.det(del2f_delv2)
	h = np.linalg.solve(del2f_delv2, -delf_delv)
	return h
	#return -delf_delv
		
