from math import sin
import pygame, random
import time, re



def base_movement(window, base_img, var_x):
    window.blit(base_img, (var_x,245))
    window.blit(base_img, (var_x + 288,245))


def dragon_movement(window, dragon_img, dragon_rect):
    window.blit(dragon_img, dragon_rect)

def badguy_movement(window, badguys, badguy_img):
    for badguy in badguys:
        badguy.centerx -= 2
        badguy.centery += 4 * sin(random.uniform(0.0, 6.28))
        badguy.centery = max(badguy.centery, 15) 
        window.blit(badguy_img, badguy)

def tree_movement(window, trees, tree_img):
    for tree in trees:
        tree.centerx -= 5
    for tree in trees:
        window.blit(tree_img, tree)

def fireball_movement(window, fireballs, fireball_img):
    for fireball in fireballs:
        fireball.centerx +=10
    for fireball in fireballs:
        window.blit(fireball_img, fireball)
        

def text_objects(text, font):
    text_surface = font.render(text, True,(0,0,0))
    return text_surface, text_surface.get_rect()

def read_high_score():
    high_score = open("HighScore", "r").read()  
    return int (re.sub(r'[^a-zA-Z0-9]', '', high_score))

def new_high_score(game_points, high_score):
    if game_points > high_score:
        high_score = game_points
        new_high_score = open("HighScore", "w")
        new_high_score.write(str (high_score))
    return high_score

# def rotate_dragon(dragon,dragon_angle):
    # new_dragon = pygame.transform.rotozoom(dragon, -dragon_angle * 3, 1)
    # return new_dragon

def collision(trees, badguys, dragon_rect):
    for tree in trees:
        if tree.colliderect(dragon_rect):
            print("Collided")
            return True
    for badguy in badguys:
        if badguy.colliderect(dragon_rect):
            print("Collided")
            return True

    if dragon_rect.top <= -10:
        print("Exceeded upper limit.")

    if dragon_rect.bottom >= 255:
        print("Exceeded lower limit.")

def collision2(fireballs, badguys, game_points):
    fireballs_to_delete = []
    badguys_to_delete = []
    for fireball in fireballs:
        for badguy in badguys:
            if fireball.colliderect(badguy):
                print("Badguy dies")
                fireballs_to_delete.append(fireball)
                badguys_to_delete.append(badguy)
                print(fireballs_to_delete)
                print(badguys_to_delete)
                game_points = game_points + 100
                print(game_points)
    try:
        for fireball in fireballs_to_delete:
            fireballs.remove(fireball)
        for badguy in badguys_to_delete:
            badguys.remove(badguy)
    except:
        pass
    return game_points




                    


def end_screen(window, game_points, POINTS):
    bkg_img = pygame.image.load("images/background.jpg")
    window.blit(bkg_img, (0,0))
    large_text = pygame.font.Font('freesansbold.ttf',75)
    small_text = pygame.font.Font('freesansbold.ttf',25)
    pygame.time.set_timer(POINTS, 0)
    
    total_points_text, total_points_text_rect = text_objects("Final Score: " + str(game_points), small_text)
    total_points_text_rect.center = (256,20)
    window.blit(total_points_text, total_points_text_rect)

    title_text, title_text_rect = text_objects("Try again?", large_text)
    title_text_rect.center = (256,130)
    window.blit(title_text, title_text_rect)

    yes_text, yes_text_rect = text_objects("Yes", large_text)
    yes_text_rect.center = (150, 200)
    window.blit(yes_text, yes_text_rect)
    
    no_text, no_text_rect = text_objects("No", large_text)
    no_text_rect.center = (350, 200)
    window.blit(no_text, no_text_rect)
    

def reset(dragon_img):  
    var_x = 0
    dragon_rect = dragon_img.get_rect(center = (150, 288/2))
    dragon_new_pos = 40
    game_points = 0
    list_of_trees = []
    list_of_badguys = []
    list_of_fireballs = []

    TIMER = pygame.USEREVENT
    pygame.time.set_timer(TIMER, 1000)

    BADTIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(BADTIMER, 5036 )
    
    DRAGONFLAP =   pygame.USEREVENT + 2
    pygame.time.set_timer(DRAGONFLAP, 500)

    POINTS = pygame.USEREVENT + 3
    pygame.time.set_timer(POINTS, 100)

    GRAVITYTIMER = pygame.USEREVENT + 4
    pygame.time.set_timer(GRAVITYTIMER, 0)

    #main loop
    clock = pygame.time.Clock()
    running = True
    collided = False    
    return var_x, dragon_rect, dragon_new_pos, game_points, list_of_trees, list_of_badguys, list_of_fireballs, clock, running, collided


def game_build():
    
    pygame.init()
    window = pygame.display.set_mode((512, 288))
    bkg_img = pygame.image.load("images/background.jpg")   
    var_x = 0
    pygame.mixer.init()
    pygame.mixer.music.load("music/DragonRoostIslandMusic.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    points_text = pygame.font.Font('freesansbold.ttf',30)
    game_points = 0
    high_score = read_high_score()
    points_text, points_text_rect = text_objects(str(game_points), points_text)
    points_text_rect.center = (50,5)
    window.blit(points_text, points_text_rect)
    high_text = pygame.font.Font('freesansbold.ttf',25)
    high_text, high_text_rect = text_objects(str(high_score), high_text)
    high_text_rect.center = (350,15)
    window.blit(high_text, high_text_rect)
    
    dragon_downflap = pygame.image.load("images/FlappyDragon1.png")
    dragon_upflap = pygame.image.load("images/FlappyDragon2.png")
    dragon_frames = [dragon_downflap, dragon_upflap]
    dragon_index = 0
    dragon_img = dragon_frames[dragon_index]
    dragon_img = pygame.transform.scale(dragon_img, (int(dragon_img.get_width() * 0.15), int(dragon_img.get_height() * 0.15)))
    dragon_rect = dragon_img.get_rect(center = (150, 288/2))
    badguy_img = pygame.image.load("images/Batman_0.png")
    badguy_img = pygame.transform.scale(badguy_img, (int(badguy_img.get_width() * 0.65), int(badguy_img.get_height() * 0.65)))
    fireball_img = pygame.image.load("images/fireball_2.png")
    list_of_badguys = []
    list_of_fireballs = []
    g_force = 1.2
    dragon_new_pos = 40
    tree_img = pygame.image.load("images/three_d_tree.png")
    # tree_img = pygame.transform.scale(tree_img, (int(tree_img.get_width()), int(tree_img.get_height())))
    list_of_trees =[]
    base_img = pygame.image.load("images/ground.jpg")

    TIMER = pygame.USEREVENT
    pygame.time.set_timer(TIMER, 1240)

    BADTIMER = pygame.USEREVENT + 1
    pygame.time.set_timer(BADTIMER, 5036)

    DRAGONFLAP =   pygame.USEREVENT + 2
    pygame.time.set_timer(DRAGONFLAP, 500)

    POINTS = pygame.USEREVENT + 3
    pygame.time.set_timer(POINTS, 100)

    GRAVITYTIMER = pygame.USEREVENT + 4
    pygame.time.set_timer(GRAVITYTIMER, 0)

    #main loop
    clock = pygame.time.Clock()
    running = True
    collided = False
    
    while running:
        #window.fill((200,100,50))



        #event loop
        dragon_y_delta = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # dragon_y_delta -= 15
                    g_force = -g_force
                    pygame.time.set_timer(GRAVITYTIMER, 1500)


                if event.key == pygame.K_n:
                    running = False
                if event.key == pygame.K_y:
                    print("restart")
                    var_x, dragon_rect, dragon_new_pos, game_points, list_of_trees, list_of_badguys, list_of_fireballs, clock, running, collided = reset(dragon_img)
            if event.type == TIMER:
                random_tree_height = [125, 150, 100, 250]
                trees = tree_img.get_rect(midtop = (525, random.choice(random_tree_height)))
                list_of_trees.append(trees)

            if event.type == BADTIMER:
                badguys = badguy_img.get_rect(center = (525, random.randrange(40,230)))
                list_of_badguys.append(badguys)
            
            if event.type == DRAGONFLAP:                
                dragon_index = (dragon_index + 1) %2
                dragon_img = dragon_frames[dragon_index]
                dragon_img = pygame.transform.scale(dragon_img, (int(dragon_img.get_width() * 0.15), int(dragon_img.get_height() * 0.15)))

            if event.type == POINTS:
                game_points = game_points + 1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if 80 < event.pos[0] < 218 and 167 < event.pos[1] < 223:            
                    print("restart")
                    var_x, dragon_rect, dragon_new_pos, game_points, list_of_trees, list_of_badguys, list_of_fireballs, clock, running, collided = reset(dragon_img)

                if 299 < event.pos[0] < 403 and 167 < event.pos[1] < 223:            
                    running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    print("add firball to list")
                    fireballs = fireball_img.get_rect(midtop = (152, dragon_rect.centery))
                    list_of_fireballs.append(fireballs)
                    print(list_of_fireballs)

            if event.type == GRAVITYTIMER:
                g_force = -g_force
                pygame.time.set_timer(GRAVITYTIMER, 0)
                     

        # end screen loop
        


        #game logic
        if collided:
            end_screen(window, game_points, POINTS)
        else:
            window.blit(bkg_img, (0,0))
            var_x -= 1
            dragon_y_delta += g_force
            dragon_new_pos += dragon_y_delta
            dragon_new_pos = max(dragon_new_pos,10)
            # rotated_dragon = rotate_dragon(dragon_img, dragon_y_delta)
            dragon_rect.centery = dragon_new_pos
            dragon_movement(window, dragon_img, dragon_rect)
            tree_movement(window, list_of_trees, tree_img)
            base_movement(window, base_img, var_x)
            badguy_movement(window,list_of_badguys,badguy_img)
            fireball_movement(window, list_of_fireballs, fireball_img)
            points_text = pygame.font.Font('freesansbold.ttf',25)
            points_text, points_text_rect = text_objects(str(game_points), points_text)
            points_text_rect.center = (150,15)
            window.blit(points_text, points_text_rect)
            high_text = pygame.font.Font('freesansbold.ttf',25)
            high_text, high_text_rect = text_objects(str(high_score), high_text)
            high_text_rect.center = (350,15)
            window.blit(high_text, high_text_rect)            
            high_score = new_high_score(game_points, high_score)
            if var_x <= -200:
                var_x = 0
            collided = collision(list_of_trees, list_of_badguys, dragon_rect)
            game_points = collision2(list_of_fireballs, list_of_badguys, game_points)
        clock.tick(60)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    game_build()