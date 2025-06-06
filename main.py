
import pygame as pg
import pytmx
# from pygame.examples.video import backgrounds

pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
FPS = 80
TILE_SCALE = 3


class Platform(pg.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super(Platform, self).__init__()

        self.image = pg.transform.scale(image, (width * TILE_SCALE, height * TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SCALE
        self.rect.y = y * TILE_SCALE


class Player(pg.sprite.Sprite):
    def __init__(self, map_width, map_height):
        super(Player, self).__init__()
        self.load_animations()
        self.current_animation = self.move_animation_right
        self.image = self.current_animation[0]
        self.current_image = 0

        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)  # Начальное положение персонажа

        # Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 2
        self.is_jumping = False
        self.map_width = 30 * 48 * TILE_SCALE
        self.map_height = 20 * 48 * TILE_SCALE

        self.timer = pg.time.get_ticks()
        self.interval = 200

    def load_animations(self):
        tile_scale = 4
        tile_size = 32

        self.idle_animation_right = []

        num_images = 5
        spritesheet = pg.image.load("sprites/Sprite Pack 3/2 - Twiggy/Idle (32 x 32).png")

        for i in range(num_images):
            x = i * tile_size  # Начальная координата X изображения в спрайтшите
            y = 0  # Начальная координата Y изображения в спрайтшите
            rect = pg.Rect(x, y, tile_size, tile_size)  # Прямоугольник, который определяет область изображения
            image = spritesheet.subsurface(rect)  # Вырезаем изображение из спрайтшита
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.idle_animation_right.append(image)  # Добавляем изображение в список

        self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]

        self.move_animation_right = []

        num_images = 6
        spritesheet = pg.image.load("sprites/Sprite Pack 3/2 - Twiggy/Running (32 x 32).png")

        for i in range(num_images):
            x = i * tile_size  # Начальная координата X изображения в спрайтшите
            y = 0  # Начальная координата Y изображения в спрайтшите
            rect = pg.Rect(x, y, tile_size, tile_size)  # Прямоугольник, который определяет область изображения
            image = spritesheet.subsurface(rect)  # Вырезаем изображение из спрайтшита
            image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
            self.move_animation_right.append(image)  # Добавляем изображение в список

        self.move_animation_left = [pg.transform.flip(image, True, False) for image in self.move_animation_right]

    def update(self, platforms):
        # Обработка ввода
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not self.is_jumping:
            self.jump()

        if keys[pg.K_a]:
            if self.current_animation != self.move_animation_left:
                self.current_animation = self.move_animation_left
                self.current_image = 0

            self.velocity_x = -10
        elif keys[pg.K_d]:
            if self.current_animation != self.move_animation_right:
                self.current_animation = self.move_animation_right
                self.current_image = 0

            self.velocity_x = 10
        else:
            if self.current_animation not in (self.idle_animation_right, self.idle_animation_left):
                if self.current_animation == self.move_animation_right:
                    self.current_animation = self.idle_animation_right
                elif self.current_animation == self.move_animation_left:
                    self.current_animation = self.idle_animation_left
                else:
                    self.current_animation = self.idle_animation_left
                self.current_image = 0

            self.velocity_x = 0

        # Применение гравитации
        self.velocity_y += self.gravity

        # Предотвращение выхода за пределы карты по горизонтали
        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x

        self.rect.y += self.velocity_y

        # Проверка на коллизии с платформами
        for platform in platforms:
            if pg.sprite.collide_mask(self, platform):
                if self.velocity_y > 0:
                    self.rect.y = platform.rect.y - self.rect.height
                    self.velocity_y = 0
                elif self.velocity_y < 0:
                    self.rect.y = platform.rect.y + platform.rect.height
                    self.velocity_y = 0
                self.is_jumping = False

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

    def jump(self):
        # Прыжок (установка вертикальной скорости вверх)
        self.velocity_y = -45  # Вы можете изменить это значение для высоты прыжка
        self.is_jumping = True
    #
    #
    #     self.idle_animation_right = []
    #     self.idle_animation_left = []
    #
    #     self.move_animation_right = []
    #     self.move_animation_left = []
    #
    #     self.load_animations()
    #
    #     self.current_animation = self.idle_animation_right
    #     self.image = self.current_animation[0]
    #     self.current_image = 0
    #
    #     self.rect = self.image.get_rect()
    #     self.rect.center = (200, 100)  # Начальное положение персонажа
    #
    #     # Начальная скорость и гравитация
    #     self.velocity_x = 0
    #     self.velocity_y = 0
    #     self.gravity = 2
    #     self.is_jumping = False
    #     self.map_width = map_width * TILE_SCALE
    #     self.map_height = map_height * TILE_SCALE
    #
    #     self.timer = pg.time.get_ticks()
    #     self.interval = 200
    #
    # def load_animations(self):
    #     tile_size = 32
    #     tile_scale = 3
    #
    #     # self.idle_animation_right = []
    #     # self.move_animation_right = []
    #
    #     num_images = 2
    #     # running_num_images = 4
    #     spritesheet = pg.image.load("sprites/Sprite Pack 2/2 - Mr. Mochi/Idle (32 x 32).png")
    #     # spritesheet2 = pg.image.load("sprites/Sprite Pack 2/2 - Mr. Mochi/Running (32 x 32).png")
    #     # print(spritesheet2)
    #
    #     for i in range(num_images):
    #         x = i * tile_size
    #         y = 0
    #         rect = pg.Rect(x, y, tile_size, tile_size)
    #         image = spritesheet.subsurface(rect)
    #         image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
    #         self.idle_animation_right.append(image)
    #     self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]
    #
    #     # self.move_animation_right = []
    #
    #     running_num_images = 4
    #     spritesheet = pg.image.load("sprites/Sprite Pack 2/2 - Mr. Mochi/Running (32 x 32).png")
    #
    #     for i in range(running_num_images):
    #         x = i * tile_size
    #         print("x")
    #         y = 0
    #         rect = pg.Rect(x, y, tile_size, tile_scale)
    #         image = spritesheet.subsurface(rect)
    #         image = pg.transform.scale(image, (tile_size * tile_scale, tile_size * tile_scale))
    #         self.move_animation_right.append(image)
    #     print(self.move_animation_right)
    #     self.move_animation_left = [pg.transform.flip(image, True, False) for image in self.move_animation_right]
    #     # self.idle_animation_left = [pg.transform.flip(image, True, False) for image in self.idle_animation_right]
    #
    #
    # def update(self, platforms):
    #     keys = pg.key.get_pressed()
    #     if keys[pg.K_SPACE] and not self.is_jumping:
    #         self.jump()
    #     if keys[pg.K_a]:
    #
    #         if self.current_animation != self.move_animation_left:
    #             self.current_animation = self.move_animation_left
    #             self.current_image = 0
    #
    #         self.velocity_x = -5
    #     elif keys[pg.K_d]:
    #         if self.current_animation != self.move_animation_right:
    #             self.current_animation = self.move_animation_right
    #             self.current_image = 0
    #         self.velocity_x = 5
    #     else:
    #         if self.current_animation not in (self.idle_animation_right, self.idle_animation_left):
    #             if self.current_animation == self.move_animation_right:
    #                 self.current_animation = self.idle_animation_right
    #             elif self.current_animation == self.move_animation_left:
    #                 self.current_animation = self.idle_animation_left
    #             else:
    #                 self.current_animation = self.idle_animation_left
    #             self.current_image = 0
    #         # if self.current_animation == self.move_animation_right:
    #         #     self.current_animation = self.idle_animation_right
    #         #     self.current_image = 0
    #         # elif self.current_animation == self.move_animation_left:
    #         #     self.current_animation == self.idle_animation_left
    #         #     self.current_image = 0
    #
    #         self.velocity_x = 0
    #
    #     new_x = self.rect.x + self.velocity_x
    #     if 0 <= new_x <= self.map_width - self.rect.width:
    #         self.rect.x = new_x
    #
    #     self.velocity_y += self.gravity
    #     self.rect.y += self.velocity_y
    #     for platform in platforms:
    #
    #         if platform.rect.collidepoint(self.rect.midbottom):
    #             self.rect.bottom = platform.rect.top
    #             self.velocity_y = 0
    #             self.is_jumping = False
    #
    #         if platform.rect.collidepoint(self.rect.midtop):
    #             self.rect.top = platform.rect.bottom
    #             self.velocity_y = 0
    #         if platform.rect.collidepoint(self.rect.midright):
    #             self.rect.right = platform.rect.left
    #         if platform.rect.collidepoint(self.rect.midleft):
    #             self.rect.left = platform.rect.right
    #
    #     if pg.time.get_ticks() - self.timer > self.interval:
    #         self.current_image += 1
    #         if self.current_image >= len(self.current_animation):
    #             self.current_image = 0
    #         self.image = self.current_animation[self.current_image]
    #         self.timer = pg.time.get_ticks()
    #
    # def jump(self):
    #     self.velocity_y = -30
    #     self.is_jumping = True
    #


class Game:
    def __init__(self):


        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Платформер")
        self.clock = pg.time.Clock()
        self.is_running = False

        self.background = pg.image.load("background2.png")
        self.background = pg.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))


        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        self.tmx_map = pytmx.load_pygame("maps/Tilesetmap1version.tmx")


        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE



        self.player = Player(self.map_pixel_width, self.map_pixel_height)
        self.all_sprites.add(self.player)

        for layer in self.tmx_map:
            for x, y, gid in layer:
                tile = self.tmx_map.get_tile_image_by_gid(gid)



                if tile:
                    platform = Platform(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight,
                                        self.tmx_map.tilewidth,
                                        self.tmx_map.tileheight)

                    self.all_sprites.add(platform)
                    self.platforms.add(platform)

        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 4



        self.run()

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

        keys = pg.key.get_pressed()

        # if keys[pg.K_LEFT]:
        #     self.camera_x += self.camera_speed
        # if keys[pg.K_RIGHT]:
        #     self.camera_x -= self.camera_speed
        # if keys[pg.K_UP]:
        #     self.camera_y += self.camera_speed
        # if keys[pg.K_DOWN]:
        #     self.camera_y -= self.camera_speed

    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()
        quit()

    # def event(self):
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             self.is_running = False
    #
    #     keys = pg.key.get_pressed()

    def update(self):
        self.player.update(self.platforms)

        self.camera_x = self.player.rect.x - SCREEN_WIDTH // 2
        self.camera_y = self.player.rect.y - SCREEN_HEIGHT // 2
        self.camera_x = max(0, min(self.camera_x, self.map_pixel_width - SCREEN_WIDTH))
        self.camera_y = max(0, min(self.camera_y, self.map_pixel_height - SCREEN_HEIGHT))


    def draw(self):


        pg.display.flip()
        # self.screen.fill("light blue")
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.background, (0,0))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, -self.camera_y))


if __name__ == "__main__":
    game = Game()