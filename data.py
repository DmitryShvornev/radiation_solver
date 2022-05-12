class Node:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{[self.x, self.y, self.z]}"


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