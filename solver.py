import meshio
from data import Node
from data import Element

class Solver:
    
    def __init__(self, mesh_filename):
        self.mesh_filename = mesh_filename
        self.mesh_elements = []
        self.mesh_nodes = []

    def mesh_preprocessing(self):
        mesh = meshio.read(self.mesh_filename)
        elements_data = mesh.cells_dict['triangle']
        points_data = mesh.points
        
        for elem in elements_data:
            nodes = []
            for point_num in elem:
                node = Node(*points_data[point_num])
                nodes.append(node)
                self.mesh_nodes.append(node)
            element = Element(*nodes)
            self.mesh_elements.append(element)



mesh = meshio.read("mesh1.msh")
print(mesh.points)
solver = Solver("mesh1.msh")
solver.mesh_preprocessing()
