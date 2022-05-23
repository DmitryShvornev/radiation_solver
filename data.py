import math
class Node:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{[self.x, self.y, self.z]}"

    def get_distance(self, node):
        return math.sqrt((self.x - node.x)**2 + (self.y - node.y)**2 + (self.z - node.z)**2)


class Element:

    def __init__(self, i_node, j_node, k_node):
        self.i_node = i_node
        self.j_node = j_node
        self.k_node = k_node

    def __str__(self):
        return f"{[[self.i_node.x, self.i_node.y, self.i_node.z], [self.j_node.x, self.j_node.y, self.j_node.z], [self.k_node.x, self.k_node.y, self.k_node.z]]}"

    def get_center(self):
        x = (self.i_node.x + self.j_node.x + self.k_node.x) / 3
        y = (self.i_node.y + self.j_node.y + self.k_node.y) / 3
        z = (self.i_node.z + self.j_node.z + self.k_node.z) / 3
        center = Node(x, y, z)
        return center

    def is_equal_to(self, element):
        cond_x = self.i_node.x == element.i_node.x and self.j_node.x == element.j_node.x and self.k_node.x == element.k_node.x
        cond_y = self.i_node.y == element.i_node.y and self.j_node.y == element.j_node.y and self.k_node.y == element.k_node.y
        cond_z = self.i_node.z == element.i_node.z and self.j_node.z == element.j_node.z and self.k_node.z == element.k_node.z
        return cond_x and cond_y and cond_z

    def get_square(self):
        Xi = self.i_node.x
        Yi = self.i_node.y
        Xj = self.j_node.x
        Yj = self.j_node.y
        Xk = self.k_node.x
        Yk = self.k_node.y
        return abs((Xj - Xi) * (Yk - Yi) - (Xk - Xi * (Yj - Yi))) / 2
    
    def get_normal(self):
        Xi = self.i_node.x
        Yi = self.i_node.y
        Zi = self.i_node.z
        Xj = self.j_node.x
        Yj = self.j_node.y
        Zj = self.j_node.z
        Xk = self.k_node.x
        Yk = self.k_node.y
        Zk = self.j_node.z
        nx = (Yj - Yi) * (Zk - Zi) - (Zj - Zi) * (Yk - Yi)
        ny = (Zj - Zi) * (Xk - Xi) - (Xj - Xi) * (Zj - Zi)
        nz = (Xj - Xi) * (Yk - Yi) - (Yj - Yi) * (Xk - Xi) 
        normal = Node(nx, ny, nz)
        return normal