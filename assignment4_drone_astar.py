import heapq
import time

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def get_neighbors(pos, grid):
    dirs = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []
    for dx, dy in dirs:
        nx, ny = pos[0]+dx, pos[1]+dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != "#":
            neighbors.append((nx, ny))
    return neighbors

def cost(grid, pos):
    val = grid[pos[0]][pos[1]]
    return int(val) if val.isdigit() else 1

def a_star(grid, start, goal):
    open_set = [(0, start)]
    came_from = {}
    g = {start: 0}
    f = {start: heuristic(start, goal)}
    visited = set()
    node_count = 0

    while open_set:
        _, current = heapq.heappop(open_set)
        node_count += 1  # Hitung setiap node yang diproses
        if current == goal:
            return reconstruct(came_from, start, goal), node_count

        visited.add(current)

        for neighbor in get_neighbors(current, grid):
            temp_g = g[current] + cost(grid, neighbor)
            if neighbor not in g or temp_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + heuristic(neighbor, goal)
                if neighbor not in visited:
                    heapq.heappush(open_set, (f[neighbor], neighbor))
    return None, node_count

def reconstruct(came_from, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(came_from[path[-1]])
    path.reverse()
    return path

def print_grid(grid, path):
    grid_copy = [row[:] for row in grid]
    for x, y in path:
        if grid_copy[x][y] not in "SG":
            grid_copy[x][y] = "*"
    for row in grid_copy:
        print("".join(row))

def run_assignment4():
    grid = [
        list("S123#"),
        list("23459"),
        list("12345"),
        list("45678"),
        list("9#876"),
        list("9876G")
    ]
    start = find(grid, "S")
    goal = find(grid, "G")

    # Catat waktu mulai
    t0 = time.perf_counter()

    path, node_count = a_star(grid, start, goal)
    
    # Catat waktu selesai
    t1 = time.perf_counter()

    print("\nAssignment 4 - A* Path (Drone Navigation):")
    if path:
        print_grid(grid, path)
    else:
        print("No path found.")

    # Hitung waktu eksekusi dalam milidetik
    exec_time = (t1 - t0) * 1000

    print(f"Execution Time: {exec_time:.4f} ms")
    print(f"Nodes Explored: {node_count}")

    return exec_time, node_count

def find(grid, symbol):
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == symbol:
                return (i, j)