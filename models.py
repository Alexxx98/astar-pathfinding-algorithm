from settings import WHITE, BLACK, BLUE, GREEN, YELLOW, BROWN


class Node:
    def __init__(self, row, col, width, height):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * height
        self.width = width
        self.height = height
        self.parent = None
        self.neighbours = []
        self.color = WHITE
        self.g_score = float("inf")
        self.f_score = float("inf")

    def __repr__(self):
        return f"{self.row, self.col}"

    def make_wall(self):
        self.color = BLACK

    def make_open(self):
        self.color = GREEN

    def make_start(self):
        self.color = BLUE

    def make_end(self):
        self.color = BROWN

    def make_path(self):
        self.color = YELLOW

    def is_wall(self):
        return self.color == BLACK

    def is_open(self):
        return self.color == GREEN

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == BROWN

    def is_path(self):
        return self.color == YELLOW

    def get_pos(self):
        return (self.row, self.col)

    def update_neighbours(self, nodes):
        """Take 4 nodes that are connected to current node"""
        for row in nodes:
            for node in row:
                row, col = node.get_pos()
                if self.row == row and abs(self.col - col) == 1:
                    self.neighbours.append(node)
                elif abs(self.row - row) == 1 and self.col == col:
                    self.neighbours.append(node)

    def reset(self):
        self.color = WHITE
        self.parent = None
        self.neighbours = []
        self.g_score = float("inf")
        self.f_score = float("inf")
