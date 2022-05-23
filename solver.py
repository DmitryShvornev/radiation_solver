import meshio
from data import Node
from data import Element
import numpy as np
import math

# постоянная Стефана-Больцмана
SIGMA_0 = 5.67 * 10**(-8)

# излучательная способность
EPSILON = 0.7

#температура
THETA = 300

def get_rad_vector(center_left, center_right):
    rx = center_left.x - center_right.x
    ry = center_left.y - center_right.y
    rz = center_left.z - center_right.z
    r = Node(rx, ry, rx)
    return r

def get_scalar_comp(vector_left, vector_right):
    comp = vector_left.x * vector_right.x + vector_left.y * vector_right.y + vector_left.z * vector_right.z
    return comp
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

    def create_local_matrix(self, element):
        E = (1 / 12) * element.get_square() * np.ones((3,3))
        Weight = 0
        current_center = element.get_center()
        current_square = element.get_square()
        for elem in self.mesh_elements:
            if (not element.is_equal_to(elem)):
                target_center = elem.get_center()
                target_square = elem.get_square()
                r = get_rad_vector(target_center, current_center)
                k_N = get_scalar_comp(r, target_center)
                k_M = get_scalar_comp(r, current_center)
                dist = target_center.get_distance(current_center)
                Weight += k_M * k_N * target_square / (dist**2)
        Weight *= current_square / (math.pi * 12)     
        K = Weight * np.ones((3,3))
        M = E - K
        return M

    def create_local_vector(self, element):
        return (1 / 3) * SIGMA_0 * EPSILON * (THETA**4) * element.get_square() * np.ones((3,1))

    def create_global_matrix():
        pass

    def create_global_vector():
        pass

    def solve_global_SLAE():
        pass

    def print_to_mv2():
        pass



solver = Solver("mesh_final.msh")
solver.mesh_preprocessing()
