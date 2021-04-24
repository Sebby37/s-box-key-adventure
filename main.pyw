import pygame, random, os, traceback, sys
from assets.classes import *
pygame.init()

# Try fix the error that disallows me from using pygame.mixer

try:
    # Window initialization
    window = pygame.display.set_mode((800, 600))
    pygame.display.set_icon(pygame.image.load(resource_path("assets\\key.png")))
    pygame.display.set_caption("The S&Box Key Adventure!")
    clock = pygame.time.Clock()
    global_timer = 0
    checkpoint = 0

    # Other screens
    def screen(img, music = None, won = False):
        pygame.mixer.music.stop()
        global window, global_timer, clock
        bg_img = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (800, 600))
        wait_timer = 0
        if music is not None:
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)
            pass
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and wait_timer > 15:
                    if not won:
                        main()
                    else:
                        pygame.quit()
                        sys.exit(0)
            wait_timer += 1
            window.blit(bg_img, (0, 0))
            clock.tick(60)
            pygame.display.update()
            window.fill((255, 255, 255))



    # Main gameplay loop
    def main():
        global global_timer, window, clock, checkpoint
        pygame.mixer.music.stop()
        # Image loading
        bg_img = pygame.transform.scale(pygame.image.load(resource_path("assets\\gm_construct.jpg")).convert_alpha(), (800, 600))

        '''Class initialization'''
        # Player
        player = Sprite(window, 375, 275, 50, 50, resource_path("assets\\player.png"))
        player_speed = 10
        keys = {
            "up" : False,
            "down" : False,
            "left" : False,
            "right" : False
        }

        # Garry
        garry = Sprite(window, 0, 0, 100, 100, resource_path("assets\\garry.jpg"))
        bullet_array = []
        garry_attacks_count = 0

        # Token thing I guess (you collect these to win the game)
        token_imgs = [resource_path(f"assets\\powerup{i}.png") for i in range(1, 5)]
        token_img_index = checkpoint  # 0 otherwise
        token = Sprite(window, random.randint(100, 600), random.randint(100, 400), 100, 100, token_imgs[token_img_index])
        token_collected = True

        pygame.mixer.music.load(resource_path("assets\\Your Best Nightmare (Alternative Mix) - Undertale.mp3"))
        pygame.mixer.music.play(-1)
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    #---DEBUG\\CHEATS---#
                    if event.key == pygame.K_MINUS:
                        screen(resource_path("assets\\win_screen.png"), resource_path("assets\\Half Life Original Soundtrack - Track 6 - CreditsClosing Theme.mp3"), won=True)
                    if event.key == pygame.K_EQUALS:
                        screen(resource_path("assets\\intro_screen.png"), resource_path("assets\\Gala Premiere.mp3"))
                    if event.key == pygame.K_BACKSPACE:
                        screen(resource_path("assets\\lose_screen.png"), resource_path("assets\\Half Life 2-Combine Theme.mp3"))
            #
            if checkpoint >= 4:
                screen(resource_path("assets\\win_screen.png"), resource_path("assets\\Half Life Original Soundtrack - Track 6 - CreditsClosing Theme.mp3"), won=True)

            # For the garry attacks, we will have an attack manager to make the attack types more random
            garry_attacks_count = garry_attack_1(garry, bullet_array, global_timer, window, garry_attacks_count)
            for bullet in bullet_array:
                bullet.update()
                if bullet.y <= -50 or bullet.y >= 600:
                    del bullet_array[bullet_array.index(bullet)]
                if bullet.rect.colliderect(player.rect):
                    screen(resource_path("assets\\lose_screen.png"), resource_path("assets\\Half Life 2-Combine Theme.mp3"))
            
            if garry.rect.colliderect(player.rect):
                    screen(resource_path("assets\\lose_screen.png"), resource_path("assets\\Half Life 2-Combine Theme.mp3"))

            if garry_attacks_count >= 4 and token_collected:
                token_collected = False

            if not token_collected:
                token.update()
                if player.rect.colliderect(token.rect):
                    token_collected = True
                    token_img_index += 1
                    checkpoint = token_img_index
                    token.x = random.randint(100, 600)
                    token.y = random.randint(100, 400)
                    try:
                        token.change_image(token_imgs[token_img_index])
                    except:
                        screen(resource_path("assets\\win_screen.png"), resource_path("assets\\Half Life Original Soundtrack - Track 6 - CreditsClosing Theme.mp3"), won=True)
                    garry_attacks_count = 0
            
            disp_text(window, 0, 0, f"How impressed Garry is with you: {round((checkpoint/4)  * 100)}%")
            
            player_update_func(events, player, keys, player_speed)
            #
            global_timer += 1
            clock.tick(60)
            pygame.display.update()
            window.fill((255, 255, 255))
            window.blit(bg_img, (0, 0))


    if __name__ == "__main__":
        screen(resource_path("assets\\intro_screen.png"), resource_path("assets\\Gala Premiere.mp3"))
except Exception as e:
    # Debug
    open("traceback.txt", "w+").write(f"{e}\n{traceback.format_exc()}")