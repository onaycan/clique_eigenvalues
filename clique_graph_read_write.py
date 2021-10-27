import itertools
import math
import xlsxwriter
import random
from clique_classes import VERTEX
from clique_classes import EDGE
from xlsxwriter.utility import xl_rowcol_to_cell
from numpy import linalg as LA
import numpy as np

def read_coordinates(_coordfile,_vertices):
    #coordfile=open("./coords.txt","r")
    coord_lines=_coordfile.read().splitlines()
    for line in coord_lines:
        current_id=int(line.split()[0])
        current_x=float(line.split()[1])
        current_y=float(line.split()[2])
        coords=[]
        coords.append(current_x)
        coords.append(current_y)
        current_vertex=VERTEX()
        current_vertex.define_vertex(current_id,coords)
        _vertices[current_id]=current_vertex
        
        
def read_graph(_vertices,_edges,_graphfile):

    #graph_file=open("./graph.txt","r")
    graph_lines=_graphfile.read().splitlines()
    for line in graph_lines:
        current_edge_id=line.split()[0]
        current_vertexA_id=int(line.split()[1])
        current_vertexB_id=int(line.split()[2])
        #print current_edge_id,current_vertexA_id,current_vertexB_id
        coordsA=[random.uniform(0.0,10.0),random.uniform(0.0,10.0)]
        coordsB=[random.uniform(0.0,10.0),random.uniform(0.0,10.0)]
        #coordsA=[random.uniform(0.0,10.0),0.0]
        #coordsB=[random.uniform(0.0,10.0),0.0]
        
        current_vertexA=VERTEX()
        current_vertexA.define_vertex(current_vertexA_id,coordsA)
        current_vertexB=VERTEX()
        current_vertexB.define_vertex(current_vertexB_id,coordsB)
        _vertices[current_vertexA_id]=current_vertexA
        _vertices[current_vertexB_id]=current_vertexB
        current_edge=EDGE()
        current_vertices=[]
        current_vertices.append(current_vertexA)
        current_vertices.append(current_vertexB)
        current_edge.define_edge(current_edge_id,current_vertices)
        _edges[current_edge_id]=current_edge
    
def write_graph(_edges,_ndof,_wb,_ws):
    
    row=2
    column=1
    chart = _wb.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
    _ws.write(row-1,column-1,"vertex of edge")
    _ws.write(row-1,column,"edge")
    _ws.write(row-1,column+1,"X of vertex of edge")
    _ws.write(row-1,column+2,"Y of vertex of edge")
    
    edge_row=2
    edge_column=4
    _ws.write(edge_row-1,edge_column,"edge")
    _ws.write(edge_row-1,edge_column+1,"edge initial length")
    _ws.write(edge_row-1,edge_column+2,"edge final length")
    _ws.write(edge_row-1,edge_column+3,"edge length difference in %")
    for e in sorted(_edges.values()):
        _ws.write(row,column-1,(e.vertices[0].id))
        _ws.write(row+1,column-1,(e.vertices[1].id))
        _ws.write(row,column,"edge "+str(e.id)+" vertex A")
        
        _ws.write(row+1,column,"edge "+str(e.id)+" vertex B")
        #_ws.write(row,column+1,e.vertices[0].coords[0])
        #x of vertex A
        formula="=VLOOKUP(A"+str(row+1)+", I3:ZI10000, 2, 0)+VLOOKUP(A"+str(row+1)+", I3:ZI10000, B1*2+4, 0)"
        _ws.write_formula(row,column+1,formula)
        #_ws.write(row,column+2,e.vertices[0].coords[1])
        #y of vertex A
        formula="=VLOOKUP(A"+str(row+1)+", I3:ZI10000, 3, 0)+VLOOKUP(A"+str(row+1)+", I3:ZI10000, B1*2+5, 0)"
        _ws.write_formula(row,column+2,formula)
        #_ws.write(row+1,column+1,e.vertices[1].coords[0])
        #x of vertex B
        formula="=VLOOKUP(A"+str(row+2)+", I3:ZI10000, 2, 0)+VLOOKUP(A"+str(row+2)+", I3:ZI10000, B1*2+4, 0)"
        _ws.write_formula(row+1,column+1,formula)
        #_ws.write(row+1,column+2,e.vertices[1].coords[1])
        #y of vertex B
        formula="=VLOOKUP(A"+str(row+2)+", I3:ZI10000, 3, 0)+VLOOKUP(A"+str(row+2)+", I3:ZI10000, B1*2+5, 0)"
        _ws.write_formula(row+1,column+2,formula)
        name=str(e.id)
        x_interval="=graph_topology!"+"C"+str(row+1)+":C"+str(row+2)
        y_interval="=graph_topology!"+"D"+str(row+1)+":D"+str(row+2)
        chart.add_series({
        'name':       name,
        'categories': x_interval,
        'values':     y_interval,
        'marker': {'type': 'circle','size': 11},})
        
        #writing the edge length to compare the energy values
        _ws.write(edge_row,edge_column,int(e.id))
        _ws.write(edge_row,edge_column+1,float(e.length))
        cell_of_Ax=xl_rowcol_to_cell(row,column+1)
        cell_of_Bx=xl_rowcol_to_cell(row+1,column+1)
        cell_of_Ay=xl_rowcol_to_cell(row,column+2)
        cell_of_By=xl_rowcol_to_cell(row+1,column+2)
        formula="=SQRT(("+cell_of_Ax+"-"+cell_of_Bx+")*"+"("+cell_of_Ax+"-"+cell_of_Bx+")+"+"("+cell_of_Ay+"-"+cell_of_By+")*"+"("+cell_of_Ay+"-"+cell_of_By+"))"
        _ws.write_formula(edge_row,edge_column+2,formula)
        cell_of_Li=xl_rowcol_to_cell(edge_row,edge_column+1)
        cell_of_Lf=xl_rowcol_to_cell(edge_row,edge_column+2)
        formula="=("+cell_of_Lf+"-"+cell_of_Li+")/"+cell_of_Li+"*100"
        _ws.write_formula(edge_row,edge_column+3,formula)
        edge_row=edge_row+1
        row=row+2
    #chart.set_style(12)
    chart.set_x_axis({'min': -8, 'max': 8})
    chart.set_y_axis({'min': -8, 'max': 8})
    _ws.insert_chart('H20', chart) 
    

def write_global_K(_ndof,_debugfile,_K):
    for r in range(_ndof):
        for c in range(_ndof):
            _debugfile.write(str(_K[r][c])+"\t")
        _debugfile.write("\n")

def write_eigenvalues(_ndof,_debugfile,_real_values_to_vectors):
    for e in _real_values_to_vectors.keys():
        _debugfile.write(str(e)+"\n")
        _debugfile.write(str(_real_values_to_vectors[e])+"\n")
        
def write_graph_eigenvectors(_edges,_vertices,_wb,_ws,_real_values_to_vectors):
        row=2
        column=8
        _ws.write(row-1,column,"vertex")
        _ws.write(row-1,column+1,"X of vertex")
        _ws.write(row-1,column+2,"Y of vertex")
        for vertex in _vertices.values():
            _ws.write(row,column,vertex.id)
            _ws.write(row,column+1,vertex.coords[0])
            _ws.write(row,column+2,vertex.coords[1])
            row=row+1
        row=2
        column=column+3
        
        _ws.write(row-2,column,"eigenvector: "+str(0))
        _ws.write(row-2,column+1,"eigenvalue: "+str(0))
        _ws.write(row-1,column,"u of vertex")
        _ws.write(row-1,column+1,"v of vertex")
        for vertex in _vertices.values():
            _ws.write(row,column,0.0)
            _ws.write(row,column+1,0.0)
            row=row+1
        row=2
        column=column+2
        
        counter=1
        for v in sorted(_real_values_to_vectors.keys()):
            _ws.write(row-2,column,"eigenvector: "+str(counter))
            counter=counter+1
            _ws.write(row-2,column+1,"eigenvalue: "+str(v))
            _ws.write(row-1,column,"u of vertex")
            _ws.write(row-1,column+1,"v of vertex")
            for vertex in _vertices.values():
                _ws.write(row,column,_real_values_to_vectors[v][(vertex.id-1)*2])
                _ws.write(row,column+1,_real_values_to_vectors[v][(vertex.id-1)*2+1])
                row=row+1
            column=column+2
            row=2


        _ws.set_column(0,100,30)

def read_objective_eigenvector(_ndof):
    objective_vector=np.zeros(_ndof,dtype=float)
    #for i in range(_ndof):
    #    objective_vector.append(0.0)
    
    file=open("objective_eigenvector.txt",'r')
    lines=file.read().splitlines()
    for line in lines:
        current_id=int(line.split()[0])
        current_dof=int(line.split()[1])
        objective_vector[(current_id-1)*2+(current_dof-1)]=1.0
    objective_vector=objective_vector/LA.norm(objective_vector)   
    return objective_vector
        
        
        
def generate_complete_graph(_graphfile,_coordfile,_numberofvertices,_radius):
	angle=math.pi*2.0/_numberofvertices
	vertex_ids=[]
	for i in range(_numberofvertices):
		random_dist=random.uniform(0.0,10.0)
		_coordfile.write(str(i+1)+"\t"+str(_radius*math.cos(i*angle*random_dist))+"\t"+str(_radius*math.sin(i*angle*random_dist))+"\n")
		vertex_ids.append(i+1)
	combinations=itertools.combinations(vertex_ids,2)
	edge_iterator=1
	iterator=1
	for combination in combinations:
		_graphfile.write(str(edge_iterator)+"\t")
		for connectivity in combination:
			_graphfile.write(str(connectivity)+"\t")
		_graphfile.write("\n")
		edge_iterator=edge_iterator+1
		
        
def generate_arbitrary_graph(_graphfile,_coordfile,_numberofvertices,_numberofedges,_radius):
	angle=math.pi*2.0/_numberofvertices
	vertex_ids=[]
	for i in range(_numberofvertices):
		_coordfile.write(str(i+1)+"\t"+str(_radius*math.cos(i*angle))+"\t"+str(_radius*math.sin(i*angle))+"\n")
		vertex_ids.append(i+1)
	combinations=itertools.combinations(vertex_ids,2)
	edge_iterator=1
	for i in range(_numberofedges):
		_graphfile.write(str(edge_iterator)+"\t")
		numbers = range(0,_numberofvertices)  # list(range(5)) in Python 3
		random.shuffle(numbers)
		_graphfile.write(str(numbers.pop()+1)+"\t"+str(numbers.pop()+1))
		_graphfile.write("\n")
		edge_iterator=edge_iterator+1


	