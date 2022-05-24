import meshio
from data import Node
from data import Element
import numpy as np
import math
import os
import os.path

# постоянная Стефана-Больцмана
SIGMA_0 = 5.67 * 10**(-8)

# излучательная способность
EPSILON = 0.7

#температура
THETA = 573

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
        for point in points_data:
            node = Node(*point)
            self.mesh_nodes.append(node)
        
        for elem in elements_data:
            nodes = []
            for point_num in elem:
                node = self.mesh_nodes[point_num]
                node.globalID = point_num
                nodes.append(node)
            element = Element(*nodes)
            element.globalIDs = [element.i_node.globalID, element.j_node.globalID, element.k_node.globalID]
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
                Weight +=  k_M * k_N * target_square / (dist**2)
        Weight *= current_square / (math.pi * 12)     
        K = (1 - EPSILON) * Weight * np.ones((3,3))
        M = E - K
        return M

    def create_local_vector(self, element):
        return (1 / 3) * SIGMA_0 * EPSILON * (THETA**4) * element.get_square() * np.ones((3,1))

    def create_global_SLAE(self):
        G = np.zeros((len(self.mesh_nodes), len(self.mesh_nodes)))
        H = np.zeros((len(self.mesh_nodes), 1))
        for elem in self.mesh_elements:
            M = self.create_local_matrix(elem)
            F = self.create_local_vector(elem)
            for i in range(3):
                i_gl = elem.globalIDs[i]
                H[i_gl] += F[i]
                for j in range(3):
                    j_gl = elem.globalIDs[j]
                    G[i_gl, j_gl] += M[i, j]
        return G, H


    def solve_global_SLAE(self):
        G, H = self.create_global_SLAE()
        self.Q = np.linalg.solve(G, H)
        return self.Q

    def print_to_mv2(self):
        q = [elem[0] for elem in self.Q.tolist()]
        print(q)
        with open("./result_mke.txt",'w') as file:
            file.write(str(len(self.mesh_nodes))+' 3 1 q \n')
            for i in range(len(self.mesh_nodes)):
                file.write(str(i + 1) + ' ' + str(self.mesh_nodes[i].x) + ' ' + str(self.mesh_nodes[i].y) + ' ' + str(self.mesh_nodes[i].z) + ' ' + str(q[i]) + '\n')
            file.write(str(len(self.mesh_elements)) + ' 3 3 BC_id mat_id mat_id_Out\n')
            for i in range(len(self.mesh_elements)):
                file.write(str(i + 1) + ' ' + str(self.mesh_elements[i].globalIDs[0] + 1) + ' ' + str(self.mesh_elements[i].globalIDs[1] + 1) + ' ' + str(self.mesh_elements[i].globalIDs[2] + 1) + ' ' + str(1) + ' ' + str(1) + ' ' + str(0) + '\n')
        file.close()
        if os.path.exists("./result_mke.mv2"):
            os.remove("./result_mke.mv2")
        os.rename("./result_mke.txt","./result_mke.mv2")


solver = Solver("mesh_final.msh")
solver.mesh_preprocessing()
solver.solve_global_SLAE()
solver.print_to_mv2()
