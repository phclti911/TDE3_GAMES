import pgzrun
import random

WIDTH = 200
HEIGHT = 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Cores e peças
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
}

COLORS = {
    'I': (0, 255, 255),
    'O': (255, 255, 0),
    'T': (128, 0, 128),
    'S': (0, 255, 0),
    'Z': (255, 0, 0),
    'J': (0, 0, 255),
    'L': (255, 165, 0),
}

grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
score = 0
game_over = False

def new_piece():
    shape = random.choice(list(SHAPES.keys()))
    return {
        'shape': shape,
        'matrix': SHAPES[shape],
        'x': GRID_WIDTH // 2 - len(SHAPES[shape][0]) // 2,
        'y': 0
    }

current_piece = new_piece()
fall_time = 0
fall_speed = 30  # frames

def rotate(matrix):
    return [list(row)[::-1] for row in zip(*matrix)]

def can_move(piece, dx, dy, new_matrix=None):
    m = new_matrix if new_matrix else piece['matrix']
    for y, row in enumerate(m):
        for x, val in enumerate(row):
            if val:
                new_x = piece['x'] + x + dx
                new_y = piece['y'] + y + dy
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                    return False
                if new_y >= 0 and grid[new_y][new_x]:
                    return False
    return True

def lock_piece():
    global grid
    for y, row in enumerate(current_piece['matrix']):
        for x, val in enumerate(row):
            if val:
                gx = current_piece['x'] + x
                gy = current_piece['y'] + y
                if 0 <= gy < GRID_HEIGHT:
                    grid[gy][gx] = current_piece['shape']

def clear_lines():
    global grid, score
    new_grid = []
    lines = 0
    for row in grid:
        if all(row):
            lines += 1
        else:
            new_grid.append(row)
    for _ in range(lines):
        new_grid.insert(0, [None] * GRID_WIDTH)
    grid = new_grid
    score += lines * 100

def update():
    global fall_time, current_piece, game_over

    if game_over:
        return

    fall_time += 1
    if fall_time >= fall_speed:
        fall_time = 0
        if can_move(current_piece, 0, 1):
            current_piece['y'] += 1
        else:
            lock_piece()
            clear_lines()
            current_piece = new_piece()
            if not can_move(current_piece, 0, 0):
                game_over = True

def draw():
    screen.clear()
    draw_grid()
    draw_piece()
    screen.draw.text(f"Score: {score}", (5, 5), color="white")
    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="red")

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            val = grid[y][x]
            if val:
                screen.draw.filled_rect(
                    Rect((x * CELL_SIZE, y * CELL_SIZE), (CELL_SIZE, CELL_SIZE)),
                    COLORS[val]
                )

def draw_piece():
    for y, row in enumerate(current_piece['matrix']):
        for x, val in enumerate(row):
            if val:
                px = current_piece['x'] + x
                py = current_piece['y'] + y
                if py >= 0:
                    screen.draw.filled_rect(
                        Rect((px * CELL_SIZE, py * CELL_SIZE), (CELL_SIZE, CELL_SIZE)),
                        COLORS[current_piece['shape']]
                    )

def on_key_down(key):
    global current_piece
    if game_over:
        return
    if key == keys.LEFT and can_move(current_piece, -1, 0):
        current_piece['x'] -= 1
    elif key == keys.RIGHT and can_move(current_piece, 1, 0):
        current_piece['x'] += 1
    elif key == keys.DOWN and can_move(current_piece, 0, 1):
        current_piece['y'] += 1
    elif key == keys.UP:
        rotated = rotate(current_piece['matrix'])
        if can_move(current_piece, 0, 0, rotated):
            current_piece['matrix'] = rotated

pgzrun.go()
