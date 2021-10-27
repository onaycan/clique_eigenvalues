import itertools
from clique_classes import VERTEX
from clique_classes import EDGE

def update_edges(_edges,_vertices):
    for e in _edges.values():
        e.vertices[0].coords=_vertices[e.vertices[0].id].coords
        e.vertices[1].coords=_vertices[e.vertices[1].id].coords
        e.cog=[0.0,0.0]
        e.cog[0]=(e.vertices[0].coords[0]+e.vertices[1].coords[0])*0.5
        e.cog[1]=(e.vertices[0].coords[1]+e.vertices[1].coords[1])*0.5
        
def update_perturbated_edges(_edges,_vertices):
    for e in _edges.values():
        e.vertices[0].pcoords=_vertices[e.vertices[0].id].pcoords
        e.vertices[1].pcoords=_vertices[e.vertices[1].id].pcoords
        
def assembly_K(_K,_edges):
    for e in _edges.values():
        eft={}
        for k in range(4):
            eft[k]=(e.vertices[k/2].id-1)*2+k%2

        for l in eft.keys():
            for r in eft.keys():
                _K[eft[l]][eft[r]]=_K[eft[l]][eft[r]]+e.K[l][r]
        
    

def assembly_perturbated_K(_pK,_edges):
    for e in _edges.values():
        eft={}
        for k in range(4):
            eft[k]=(e.vertices[k/2].id-1)*2+k%2

        for l in eft.keys():
            for r in eft.keys():
                _pK[eft[l]][eft[r]]=_pK[eft[l]][eft[r]]+e.pK[l][r]                
                
def brute_force_max_clique(_vertices,_edges):
    edge_pairs=[]
    for edge in _edges.values():
        edge_pairs.append(edge.pair)
    #print edge_pairs
    vertex_array=[]
    for vertex in _vertices.values():
        vertex_array.append(vertex.id)
    numberofvertices=len(vertex_array)
    finish_flag=False
    for i in range(0,numberofvertices-2):
        current_clique_size=numberofvertices-i
        current_clique_combinations=itertools.combinations(vertex_array,current_clique_size)
        #print current_clique_size
        for current_clique_combination in current_clique_combinations:
            current_edge_combinations=list(itertools.combinations(current_clique_combination,2))
            if not set(current_edge_combinations)-set(edge_pairs):
                #print current_clique_size,current_edge_combinations
                final_edge_combinations=current_edge_combinations
                finish_flag=True
                break
            if finish_flag:
                break
        if finish_flag:
            break
    print final_edge_combinations,len(final_edge_combinations)
    clique_vertices={}
    for final_edge_combination in final_edge_combinations:
        clique_vertices[final_edge_combination[0]]=1
        clique_vertices[final_edge_combination[1]]=1
    for vertex in clique_vertices.keys():
        print vertex
            #for current_edge_combination in current_edge_combinations:
                #print set(current_edge_combination)-set(edge_pairs)
            #   print current_edge_combination
            
def evaluate_system_cog(_edges):
    cog=[0.0,0.0]
    total_moment=[0.0,0.0]
    cog=[0.0,0.0]
    total_weight=0.0
    for edge in _edges.values():
        total_weight=total_weight+edge.length
        for i in range(2):
            total_moment[i]=total_moment[i]+edge.length*edge.cog[i]
       
    cog[0]=total_moment[0]/total_weight
    cog[1]=total_moment[1]/total_weight
    return cog
        
