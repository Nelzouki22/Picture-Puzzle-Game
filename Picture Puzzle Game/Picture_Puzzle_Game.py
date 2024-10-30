import pygame
import random
import tkinter as tk
from tkinter import filedialog

# إعداد واجهة tkinter لاختيار الصورة
tk.Tk().withdraw()
image_path = filedialog.askopenfilename(title="اختر صورة اللغز", filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])

if not image_path:
    raise FileNotFoundError("لم يتم اختيار صورة!")

# تهيئة Pygame
pygame.init()

# إعداد حجم الشاشة
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Picture Puzzle Game")

# تحميل الصورة وتحديد حجم الشبكة
image = pygame.image.load(image_path)
image = pygame.transform.scale(image, (WIDTH, HEIGHT))  # ضبط حجم الصورة
ROWS, COLS = 4, 4  # حجم شبكة اللغز
TILE_SIZE = WIDTH // COLS  # حجم المربعات

# تقطيع الصورة إلى مربعات مع إضافة مربع فارغ
tiles = []
positions = []
empty_tile = (COLS - 1, ROWS - 1)  # آخر مربع سيكون فارغًا
for row in range(ROWS):
    for col in range(COLS):
        rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if (col, row) != empty_tile:
            tile_image = image.subsurface(rect).copy()
            tiles.append(tile_image)
        else:
            tiles.append(None)  # المربع الفارغ
        positions.append((col, row))

# خلط المربعات عشوائيًا
random.shuffle(positions)

# دالة لرسم المربعات
def draw_tiles():
    for i, pos in enumerate(positions):
        tile_image = tiles[i]
        if tile_image:
            x, y = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE
            screen.blit(tile_image, (x, y))

# دالة للعثور على موقع المربع الفارغ
def get_empty_tile_position():
    for i, pos in enumerate(positions):
        if tiles[i] is None:
            return pos
    return None

# دالة للتحقق إذا كانت اللعبة قد حُلت
def check_win():
    for i, pos in enumerate(positions):
        correct_pos = (i % COLS, i // COLS)
        if pos != correct_pos:
            return False
    return True

# الحلقة الأساسية للعبة
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # عند النقر، نحاول تحريك المربع إذا كان بجانب المربع الفارغ
            mx, my = pygame.mouse.get_pos()
            col, row = mx // TILE_SIZE, my // TILE_SIZE
            empty_pos = get_empty_tile_position()

            # تحقق من أن المربع المجاور هو المربع الفارغ
            if (abs(col - empty_pos[0]) == 1 and row == empty_pos[1]) or (abs(row - empty_pos[1]) == 1 and col == empty_pos[0]):
                # تبادل المربع مع المربع الفارغ
                empty_index = positions.index(empty_pos)
                clicked_index = positions.index((col, row))
                positions[empty_index], positions[clicked_index] = positions[clicked_index], positions[empty_index]

    # تحديث الشاشة
    screen.fill((255, 255, 255))  # لون الخلفية
    draw_tiles()
    pygame.display.flip()

    # التحقق من حالة الفوز
    if check_win():
        print("تهانينا! لقد حليت اللغز!")
        running = False

pygame.quit()
