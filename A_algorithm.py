import time

import pygame
import heapq

# Khởi tạo màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Khởi tạo kích thước màn hình
WIDTH = 25
HEIGHT = 25
MARGIN = 5
WINDOW_SIZE = [760, 760]

# Khởi tạo ma trận
grid = []
for row in range(25):
    grid.append([])
    for column in range(25):
        grid[row].append(0)

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("A* Pathfinding")
clock = pygame.time.Clock()

# Hàm tính toán khoảng cách giữa hai điểm
def distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# Hàm tìm đường A*
def astar(start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: distance(start, end)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end:
            path = []
            while current in came_from:
                path.insert(0, current)  # Thay vì sử dụng append, bạn sử dụng insert để chèn giá trị vào đầu danh sách
                current = came_from[current]
            return path

        for neighbor in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor_pos = (current[0] + neighbor[0], current[1] + neighbor[1])

            if neighbor_pos[0] < 0 or neighbor_pos[0] >= len(grid) or neighbor_pos[1] < 0 or neighbor_pos[1] >= len(grid[0]):
                continue

            if grid[neighbor_pos[0]][neighbor_pos[1]] != 0:
                continue

            tentative_g_score = g_score[current] + distance(current, neighbor_pos)

            if neighbor_pos not in g_score or tentative_g_score < g_score[neighbor_pos]:
                came_from[neighbor_pos] = current
                g_score[neighbor_pos] = tentative_g_score
                f_score[neighbor_pos] = tentative_g_score + distance(neighbor_pos, end)
                heapq.heappush(open_set, (f_score[neighbor_pos], neighbor_pos))

# Hàm vẽ lưới
def draw_grid():
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            color = WHITE
            if grid[row][column] == 1:
                color = BLACK
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

    # Vẽ điểm ban đầu màu xanh
    pygame.draw.rect(screen, GREEN, [(MARGIN + WIDTH) * start_point[1] + MARGIN, (MARGIN + HEIGHT) * start_point[0] + MARGIN, WIDTH, HEIGHT])
    # Vẽ điểm đích màu đỏ
    pygame.draw.rect(screen, RED, [(MARGIN + WIDTH) * end_point[1] + MARGIN, (MARGIN + HEIGHT) * end_point[0] + MARGIN, WIDTH, HEIGHT])


# Hàm vẽ đường đi
def draw_path(path):
    for i, point in enumerate(path):
        if i == len(path) - 1:
            pygame.draw.rect(screen, BLUE,[(MARGIN + WIDTH) * start_point[1] + MARGIN, (MARGIN + HEIGHT) * start_point[0] + MARGIN,WIDTH, HEIGHT])
            pygame.draw.rect(screen, GREEN, [(MARGIN + WIDTH) * point[1] + MARGIN, (MARGIN + HEIGHT) * point[0] + MARGIN, WIDTH, HEIGHT])
        else:
            pygame.draw.rect(screen, BLUE, [(MARGIN + WIDTH) * point[1] + MARGIN, (MARGIN + HEIGHT) * point[0] + MARGIN, WIDTH, HEIGHT])


# Hàm chạy chương trình
def run_astar(start, end):
    path = astar(start, end)

    done = False
    i = 0  # Chỉ số bước đi trong đường đi
    clock = pygame.time.Clock()
    elapsed_time = 0  # Thời gian đã trôi qua

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(BLACK)
        draw_grid()

        elapsed_time += clock.get_time()

        if elapsed_time >= 100:  # Nếu đã trôi qua ít nhất 1 giây
            elapsed_time = 0  # Đặt lại thời gian

            if i < len(path) - 1:
                i += 1
            else:
                done = True

        # Vẽ các bước đi đã được tìm thấy
        draw_path(path[:i + 1])
        pygame.display.flip()

        clock.tick(60)



# Điểm bắt đầu và kết thúc
start_point = (0, 0)
end_point = (22, 1)

# Thực thi chương trình
run_astar(start_point, end_point)

pygame.quit()
