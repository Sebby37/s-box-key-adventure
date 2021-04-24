import pygame, os, sys

class Sprite:
    def __init__(self, window, x, y, width, height, image, extra_update_func = None, args = None):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x - 5, self.y - 5, self.width - 5, self.height - 5)
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (self.width, self.height))
        self.extra_update_func = extra_update_func
        self.args = args
    def change_image(self, image):
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (self.width, self.height))
    def update(self):
        if self.extra_update_func is not None:
            self.extra_update_func(self, self.args)

        self.rect = pygame.Rect(self.x - 5, self.y - 5, self.width - 5, self.height - 5)
        self.window.blit(self.image, self.rect.topleft)

# What a yucky function :(
def player_update_func(events, player, keys, player_speed):
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                keys["up"] = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys["down"] = True
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                keys["left"] = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                keys["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                keys["up"] = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys["down"] = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                keys["left"] = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                keys["right"] = False
    ''' Player stuff '''
    # Movement
    if keys["up"]:
        player.y -= player_speed
    if keys["down"]:
        player.y += player_speed
    if keys["left"]:
        player.x -= player_speed
    if keys["right"]:
        player.x += player_speed
    # Edge guarding
    if player.x < 0:
        player.x += player_speed
    if player.y < 0:
        player.y += player_speed
    if player.x > 800 - player.width:
        player.x -= player_speed
    if player.y > 600 - player.height:
        player.y -= player_speed
    # Final update
    player.update()

def bullet_behavior_1(bullet, args):
    garry_y = args[0]
    if garry_y == 0:
        bullet.y += 8
    elif garry_y >= 500:
        bullet.y -= 8

def garry_attack_1(garry, bullet_array, global_timer, window, garry_attacks_count):
    if garry.y <= 0 and garry.x < 700:
        garry.x += 7
        if global_timer % 15 == 0:
            bullet_array.append(Sprite(window, garry.x, garry.y, 50, 50, resource_path("assets\\punch.png"), bullet_behavior_1, [garry.y]))

    if garry.x >= 700 and garry.y != 500:
        garry.y += 20

    if garry.y >= 500 and garry.x > 0:
        garry.x -= 7
        if global_timer % 15 == 0:
            bullet_array.append(Sprite(window, garry.x, garry.y, 50, 50, resource_path("assets\\punch.png"), bullet_behavior_1, [garry.y]))

    if garry.x <= 0 and garry.y != 0:
        garry.y -= 50
    
    if garry.x <= 0 and garry.y <= 00:
        garry_attacks_count += 1
    
    garry.update()
    
    return garry_attacks_count

def disp_text(window, x, y, text):
    font = pygame.font.SysFont("Comic Sans MS", 20)
    surface = font.render(text, False, (0, 0, 0))
    window.blit(surface, (x, y))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

'''

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)'''