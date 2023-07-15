import pygame
from pygame.locals import *

# 화면 크기 설정
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# 색깔 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 250)

# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("arkanoid-oneni")

clock = pygame.time.Clock()

# 패들 정보 초기화
paddle_width = 0.15 * SCREEN_WIDTH
paddle_height = 0.025 * SCREEN_HEIGHT
paddle_x = (SCREEN_WIDTH - paddle_width) // 2
paddle_y = SCREEN_HEIGHT - paddle_height - 10
paddle_speed = 8

# 공 정보 초기화
ball_radius = 0.015 * SCREEN_WIDTH
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed_x = 3
ball_speed_y = 3

# 벽돌 정보 초기화
brick_rows = 3
brick_cols = 10
brick_gap = 4
brick_width = (SCREEN_WIDTH - (brick_gap * (brick_cols - 1))) // brick_cols
brick_height = 0.025 * SCREEN_HEIGHT
bricks = []
for row in range(brick_rows):
    for col in range(brick_cols):
        brick_x = col * (brick_width + brick_gap)
        brick_y = row * (brick_height + brick_gap) + brick_gap
        bricks.append(pygame.Rect(brick_x, brick_y, brick_width, brick_height))

# 게임 상태
lives = 3
game_over = False
start_image = pygame.image.load('game_start.png')
end_image = pygame.image.load('game_end.png')
start_rect = start_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
end_rect = end_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

def show_life_notification():
    screen.blit(start_image, start_rect)
    lives_text = font.render(f"Life Lost! Lives: {lives}", True, WHITE)
    text_rect = lives_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(lives_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(1000)

# 폰트 초기화
font = pygame.font.Font(None, 30)

# 게임 시작 팝업
screen.blit(start_image, start_rect)
pygame.display.flip()
pygame.time.wait(3000)

# 게임 루프
while not game_over:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            paddle_x -= paddle_speed
        if keys[K_RIGHT]:
            paddle_x += paddle_speed

        # 패들 이동 범위 제한
        if paddle_x < 0:
            paddle_x = 0
        if paddle_x > SCREEN_WIDTH - paddle_width:
            paddle_x = SCREEN_WIDTH - paddle_width

        if ball_speed_x == 0 and ball_speed_y == 0:
            # 게임 시작 전, 공을 패들 위에 고정
            ball_x = paddle_x + paddle_width // 2
            ball_y = paddle_y - ball_radius

            # 스페이스바를 누르면 공이 움직이도록 설정
            if keys[K_SPACE]:
                ball_speed_x = 4
                ball_speed_y = -4

        # 공 이동
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # 벽과의 충돌 체크
        if ball_x <= 0 or ball_x >= SCREEN_WIDTH - ball_radius:
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        # 바닥에 닿았을 때 생명 감소
        if ball_y >= SCREEN_HEIGHT - ball_radius:
            lives -= 1
            if lives == 0:
                game_over = True
            else:
                show_life_notification()
                ball_speed_x = 0
                ball_speed_y = 0
                ball_x = paddle_x + paddle_width // 2
                ball_y = paddle_y - ball_radius

        # 패들과의 충돌 체크
        if paddle_x < ball_x < paddle_x + paddle_width and paddle_y < ball_y < paddle_y + paddle_height:
            ball_speed_y = -ball_speed_y

        # 벽돌과의 충돌 체크
        for brick in bricks[:]:
            if brick.colliderect(pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
                bricks.remove(brick)
                break

        # 화면에 그리기
        pygame.draw.rect(screen, SKY_BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

        for brick in bricks:
            pygame.draw.rect(screen, SKY_BLUE, brick)

        # 생명 표시
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (10, 10))

        # 게임 종료 체크
        if len(bricks) == 0:
            screen.blit(end_image, end_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            game_over = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
