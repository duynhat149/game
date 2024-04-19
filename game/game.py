import random
import pygame
import sys

# Khởi tạo pygame
pygame.init()

# Tạo màn hình
screen = pygame.display.set_mode((432, 640))
pygame.display.set_caption("Flappy Bird")

# Tạo đồng hồ để giới hạn tốc độ khung hình
clock = pygame.time.Clock()

# Tạo hàm vẽ sàn
def draw_floor():
    screen.blit(floor, (floor_x_pos, 600))
    screen.blit(floor, (floor_x_pos + 432, 600))

# Tạo hàm tạo ống
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(500, random_pipe_pos - 200))
    return bottom_pipe, top_pipe

# Tạo hàm di chuyển ống 
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

# Tạo hàm vẽ ống
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 768:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

# Định nghĩa hàm game_over để hiển thị thông báo và kết thúc trò chơi
def game_over():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(216, 320))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  # Delay để hiển thị thông báo game over trong 2 giây
     
    pygame.quit()
    sys.exit()

# Load hình ảnh và chuyển đổi kích thước 2x
bg = pygame.image.load('game/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

floor = pygame.image.load('game/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

bird = pygame.image.load('game/assets/yellowbird-midflap.png').convert()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 384))

pipe_surface = pygame.image.load('game/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Tạo sự kiện thêm ống
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [300, 400, 500]

# Thiết lập các biến về chuyển động
gravity = 0.25
bird_movement = 0

# Vòng lặp chính của trò chơi
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = -6
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

    # Di chuyển và vẽ con chim
    bird_movement += gravity
    bird_rect.centery += bird_movement

    # Kiểm tra va chạm với ống
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            game_over()

    # Kiểm tra va chạm với đáy hoặc trần
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        game_over()

    # Hiển thị hình ảnh nền
    screen.blit(bg, (0, 0))

    # Di chuyển và vẽ ống
    pipe_list = move_pipe(pipe_list)
    draw_pipe(pipe_list)

    # Di chuyển và vẽ sàn
    floor_x_pos -= 1
    draw_floor()

    # Đặt lại vị trí sàn khi nó di chuyển hết màn hình
    if floor_x_pos <= -432:
        floor_x_pos = 0

    # Di chuyển và vẽ con chim
    screen.blit(bird, bird_rect)

    # Cập nhật màn hình
    pygame.display.update()

    # Giới hạn tốc độ khung hình
    clock.tick(30)
