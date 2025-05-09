import random
import pgzrun

WIDTH = 200
HEIGHT = 400
TITLE = "Tetris Clone"

GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 20

score = 0
game_over = False
fall_delay = 30  # frames
fall_counter = 0

# Tetromino shapes
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
          [1, 1, 1]]
}

COLORS = {
    'I': (0, 255, 255),
    'O': (255, 255, 0),
    'T': (128, 0, 128),
    'S': (0, 255, 0),
    'Z': (255, 0, 0),
    'J': (0, 0, 255),
    'L': (255, 165, 0)
}

grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def new_piece():
    shape = random.choice(list(SHAPES.keys()))
    return {
        'shape': shape,
        'matrix': SHAPES[shape],
        'x': GRID_WIDTH // 2 - len(SHAPES[shape][0]) // 2,
        'y': 0
    }

current_piece = new_piece()

def rotate(matrix):
    return [list(row)[::-1] for row in zip(*matrix)]

def can_move(piece, dx, dy, new_matrix=None):
    m = new_matrix if new_matrix else piece['matrix']
    for y, row in enumerate(m):
        for x, cell in enumerate(row):
            if cell:
                nx = piece['x'] + x + dx
                ny = piece['y'] + y + dy
                if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT:
                    return False
                if ny >= 0 and grid[ny][nx]:
                    return False
    return True

def lock_piece(piece):
    global grid
    for y, row in enumerate(piece['matrix']):
        for x, cell in enumerate(row):
            if cell:
                ny = piece['y'] + y
                nx = piece['x'] + x
                if ny >= 0:
                    grid[ny][nx] = piece['shape']
    sounds.line.play()
    clear_lines()

def clear_lines():
    global score, grid
    new_grid = [row for row in grid if any(cell is None for cell in row)]
    lines_cleared = GRID_HEIGHT - len(new_grid)
    score += lines_cleared * 100
    for _ in range(lines_cleared):
        new_grid.insert(0, [None] * GRID_WIDTH)
    grid[:] = new_grid

def update():
    global fall_counter, current_piece, game_over

    if game_over:
        return

    fall_counter += 1
    if fall_counter >= fall_delay:
        fall_counter = 0
        if can_move(current_piece, 0, 1):
            current_piece['y'] += 1
        else:
            lock_piece(current_piece)
            if current_piece['y'] <= 0:
                sounds.gameover.play()
                game_over = True
            current_piece = new_piece()

def draw():
    screen.fill((0, 0, 0))
    draw_grid()
    draw_piece(current_piece)
    screen.draw.text(f"Score: {score}", (5, 5), color="white")
    if game_over:
        screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=40, color="red")

def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell = grid[y][x]
            if cell:
                draw_cell(x, y, COLORS[cell])
            screen.draw.rect(Rect((x*CELL_SIZE, y*CELL_SIZE), (CELL_SIZE, CELL_SIZE)), (40, 40, 40))

def draw_piece(piece):
    for y, row in enumerate(piece['matrix']):
        for x, cell in enumerate(row):
            if cell:
                draw_cell(piece['x'] + x, piece['y'] + y, COLORS[piece['shape']])

def draw_cell(x, y, color):
    screen.draw.filled_rect(Rect((x*CELL_SIZE, y*CELL_SIZE), (CELL_SIZE, CELL_SIZE)), color)

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
