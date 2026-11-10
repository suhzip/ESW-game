
import math
import time
import random

from PIL import Image, ImageDraw, ImageFont
from Joystick import Joystick

# LCD 및 조이스틱 초기화
joystick = Joystick()

WIDTH = joystick.width
HEIGHT = joystick.height

# 화면 중심
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# 행성 및 궤도 설정
PLANET_RADIUS = 35
ORBIT_RADIUS = 75

# 우주선 설정
angle = -math.pi / 2
rotation_speed = 2.0

# 배경 별 생성
random.seed(42)
stars = [
    (random.randint(0, WIDTH - 1),
     random.randint(0, HEIGHT - 1))
    for _ in range(35)
]

# 버튼 입력 확인 (눌림 = False)
def pressed(button):
    return not button.value


def draw_game():
    global angle

    # 검은색 배경
    image = Image.new("RGB", (WIDTH, HEIGHT), (5, 8, 25))
    draw = ImageDraw.Draw(image)

    # 별
    for x, y in stars:
        draw.point((x, y), fill=(180, 190, 220))

    # 원형 궤도
    draw.ellipse(
        (
            CENTER_X - ORBIT_RADIUS,
            CENTER_Y - ORBIT_RADIUS,
            CENTER_X + ORBIT_RADIUS,
            CENTER_Y + ORBIT_RADIUS
        ),
        outline=(70, 80, 120),
        width=2
    )

    # 행성
    draw.ellipse(
        (
            CENTER_X - PLANET_RADIUS,
            CENTER_Y - PLANET_RADIUS,
            CENTER_X + PLANET_RADIUS,
            CENTER_Y + PLANET_RADIUS
        ),
        fill=(100, 70, 200),
        outline=(170, 130, 255),
        width=3
    )

    # 행성 장식
    draw.ellipse(
        (CENTER_X - 18, CENTER_Y - 12,
         CENTER_X - 5, CENTER_Y + 1),
        fill=(130, 100, 230)
    )

    # 우주선 위치 계산
    ship_x = CENTER_X + ORBIT_RADIUS * math.cos(angle)
    ship_y = CENTER_Y + ORBIT_RADIUS * math.sin(angle)

    # 우주선 삼각형
    size = 11

    points = [
        (ship_x + size * math.cos(angle),
         ship_y + size * math.sin(angle)),

        (ship_x + size * math.cos(angle + 2.5),
         ship_y + size * math.sin(angle + 2.5)),

        (ship_x + size * math.cos(angle - 2.5),
         ship_y + size * math.sin(angle - 2.5))
    ]

    draw.polygon(points, fill=(70, 230, 255))

    # 상단 제목
    draw.text((8, 8), "ORBIT PANIC", fill=(255, 255, 255))

    # 하단 조작 안내
    draw.text((8, HEIGHT - 18), "L/R: MOVE  A: DASH", fill=(180, 180, 180))

    # LCD 출력
    joystick.disp.image(image)


def main():
    global angle

    print("ORBIT PANIC START!")

    previous_time = time.monotonic()

    try:
        while True:
            current_time = time.monotonic()
            dt = min(current_time - previous_time, 0.1)
            previous_time = current_time

            speed = rotation_speed

            # A 버튼: 대시
            if pressed(joystick.button_A):
                speed *= 2.5

            # 왼쪽 회전
            if pressed(joystick.button_L):
                angle -= speed * dt

            # 오른쪽 회전
            if pressed(joystick.button_R):
                angle += speed * dt

            angle %= 2 * math.pi

            # B 버튼: 종료
            if pressed(joystick.button_B):
                print("GAME EXIT")
                break

            draw_game()
            time.sleep(0.02)

    except KeyboardInterrupt:
        print("프로그램 종료")


if __name__ == "__main__":
    main()
