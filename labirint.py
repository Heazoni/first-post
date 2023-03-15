from pygame import *

# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # вызываем конструктор класса Sprite
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - картинку
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # метод, отрисовывающий героя в окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        if pacman.rect.x <= win_width-80 and pacman.x_speed > 0 or pacman.rect.x >= 0 and  pacman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if pacman.rect.y <= win_height-80 and pacman.y_speed > 0 or pacman.rect.y >= 0 and  pacman.y_speed < 0:
            self.rect.y += self.y_speed
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.top, p.rect.bottom)
# создаем окно
win_width = 700
win_height = 500
display.set_caption('Лабиринт')
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)

# создаем стены-картинки
w1 = GameSprite('wall.png', win_width/2 - win_width/3, win_height/2, 300, 50)
w2 = GameSprite('wall.png', 370, 100, 50, 400)
# создаем спрайты
pacman = Player('player.png', 5, win_height-80, 80, 80, 0, 0)
# игровой цикл
run = True

barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)

monster = GameSprite('enemy.png', win_width -80, 100, 80, 80)
final_sprite = GameSprite('win.png', win_width -85, win_height - 100, 80, 80)
finish = False
while run:
    # цикл срабатывает каждую 0.05 секунду
    time.delay(20)
    
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                pacman.x_speed = -5
            elif e.key == K_RIGHT:
                pacman.x_speed = 5
            elif e.key == K_UP:
                pacman.y_speed = -5
            elif e.key == K_DOWN:
                pacman.y_speed = 5
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                pacman.x_speed = 0
            elif e.key == K_RIGHT:
                pacman.x_speed = 0
            elif e.key == K_UP:
                pacman.y_speed = 0
            elif e.key == K_DOWN:
                pacman.y_speed = 0
    if not finish:
        window.fill(back)
        barriers.draw(window)
        monster.reset()
        final_sprite.reset()
        
        pacman.reset()
        pacman.update()
        
        if sprite.collide_rect(pacman, monster):
            finish = True
            img = image.load('2.png')
            window.fill((0,0,0))
            window.blit(transform.scale(img, (win_width, win_height)), (90, 0))
            
            time.delay(100)
            
        if sprite.collide_rect(pacman, final_sprite):
            finish = True
            img = image.load('4.png')
            window.fill((0,0,0))
            window.blit(transform.scale(img, (win_width, win_height)), (90, 0))
            
            time.delay(100)

        if sprite.spritecollide(pacman, barriers, False):
            finish = True 
            img = image.load('2.png')
            window.fill((0,0,0))
            window.blit(transform.scale(img, (win_width, win_height)), (90, 0))
    
    display.update() 
display.update()
