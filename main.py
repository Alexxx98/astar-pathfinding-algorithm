import pygame
from models import Node
from settings import WIDTH, HEIGHT, FPS, WHITE, BLACK


pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()


def main():
    running = True
    holding = False
    nodes = get_grid()
    start = None
    end = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Left click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                holding = True
            # Right click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                # If status == 0 next clicked node becomes start node, if status == 1, next node clicked node is end node
                status = 0

                # Check if start node is already on the grid and check which node suits mouse position
                for row in nodes:
                    for node in row:
                        if node.is_start():
                            status = 1

                        if mouse_pos[0] in range(
                            node.x, node.x + node.width
                        ) and mouse_pos[1] in range(node.y, node.y + node.height):
                            clicked_node = node

                if status == 0:
                    clicked_node.make_start()
                    start = clicked_node
                else:
                    clicked_node.make_end()
                    end = clicked_node

            if event.type == pygame.MOUSEMOTION:
                if holding:
                    mouse_pos = pygame.mouse.get_pos()
                    for row in nodes:
                        for node in row:
                            if mouse_pos[0] in range(
                                node.x, node.x + node.width
                            ) and mouse_pos[1] in range(node.y, node.y + node.height):
                                node.make_wall()
            if event.type == pygame.MOUSEBUTTONUP:
                holding = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                for row in nodes:
                    for node in row:
                        node.update_neighbours(nodes)
                pathfinder(start, end, nodes)
                create_path(start, end, nodes)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for row in nodes:
                    for node in row:
                        node.reset()

        draw_grid(nodes)

        clock.tick(FPS)

    pygame.quit()


def get_grid():
    nodes = []
    node_width = 20
    node_height = 20
    rows = WIDTH // node_width
    cols = HEIGHT // node_height
    for row in range(rows):
        nodes.append([])
        for col in range(cols):
            nodes[row].append(Node(row, col, node_width, node_height))
    return nodes


def draw_grid(nodes):
    for row in nodes:
        for node in row:
            # Fill node with color
            pygame.draw.rect(
                WINDOW, node.color, pygame.Rect(node.x, node.y, node.width, node.height)
            )
            # Draw black for every node
            pygame.draw.rect(
                WINDOW, BLACK, pygame.Rect(node.x, node.y, node.width, node.height), 1
            )

    # Update screen
    pygame.display.flip()


def h_score(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def pathfinder(start, end, nodes):
    open_set = []
    open_set.append(start)

    start.g_score = 0
    start.f_score = h_score(start.get_pos(), end.get_pos())

    while open_set:
        current_node = open_set[0]
        for node in open_set:
            if node.f_score < current_node.f_score:
                current_node = node

        open_set.remove(current_node)

        if current_node == end:
            return

        for neighbour in current_node.neighbours:
            if neighbour.f_score == float("inf") and not neighbour.is_wall():
                neighbour.g_score = current_node.g_score + 1
                neighbour.f_score = neighbour.g_score + h_score(
                    neighbour.get_pos(), end.get_pos()
                )
                neighbour.parent = current_node
                if neighbour != end:
                    neighbour.make_open()
                open_set.append(neighbour)

        draw_grid(nodes)


def create_path(start, end, nodes):
    current_node = end
    while current_node != start:
        current_node = current_node.parent
        if current_node != start:
            current_node.make_path()
        draw_grid(nodes)


if __name__ == "__main__":
    main()
