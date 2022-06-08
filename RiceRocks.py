# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
angle_vel = 0
angular_vel = 0.1
rock_group = set([])
missile_group = set([])
explosion_group = set([])
remove_explosion = set([])
num = 0
started  = False


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0]+self.image_size[0],self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)        

    def update(self):
        self.pos[0] = self.vel[0] + self.pos[0]
        self.pos[1] = self.vel[1] + self.pos[1]
        self.angle += self.angle_vel
        if self.thrust:
            change = angle_to_vector(self.angle)
            self.vel[0] = (change[0] * 1.2)
            self.vel[1] = (change[1] * 1.2)
        else:
            self.vel[0] = 0
            self.vel[1] = 0
            
        self.pos[0] = self.pos[0] + self.vel[0]
        self.pos[1] = self.pos[1] + self.vel[1]

        if self.pos[0] < 0:
            self.pos[0] = WIDTH
        elif self.pos[0] > WIDTH:
            self.pos[0] = 0
            
        if self.pos[1] < 0:
            self.pos[1] = HEIGHT
        elif self.pos[1] > HEIGHT:
            self.pos[1] = 0
            
    def shoot(self):
        global a_missile, missile_group
        shooting = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * shooting[0], self.pos[1] + self.radius * shooting[1]]
        missile_vel = [self.vel[0] + 6 * shooting[0], self.vel[1] + 6 * shooting[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)        
        
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None,):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.animated = info.get_animated()
        self.lifespan = 500
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_size[0] * self.age + self.image_center[1],self.image_center[1]],self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = self.vel[0] + self.pos[0]
        self.pos[1] = self.vel[1] + self.pos[1]
        
        self.age += 10
        if self.age >= self.lifespan:
            return True
        else:
            return False
        
    def reflection(self, group):
        for element in group:
            if element.pos[0] < 0:
                element.pos[0] = WIDTH
            elif element.pos[0] > WIDTH:
                element.pos[0] = 0

            if element.pos[1] < 0:
                element.pos[1] = HEIGHT
            elif element.pos[1] > HEIGHT:
                element.pos[1] = 0
        
    def get_position(self):
        return self.pos
    
    def get_velocity(self):
        return self.vel
    
    def get_radius(self):
        return self.radius
    
    def get_age(self):
        return self.age
    
    def get_lifespan(self):
        return self.lifespan

    def collide(self,other_sprite):
        if dist(self.get_position(), other_sprite.get_position()) <= self.get_radius() + other_sprite.get_radius():
            return True
        return False

def process_sprite_group(group, canvas):
    global missile_group
    remove = set([])
    
    for element in group:
        should_delete = element.update()
        element.draw(canvas)
        element.reflection(group)

        if should_delete:
            remove.add(element)
    for element1 in remove:
         group.remove(element1)
   
    
def group_collide(group, other_object):
    global lives, num, explosion_group
    copy_of_group = set([])
    num = 0 
    for element in group:
        if element.collide(other_object):
            copy_of_group.add(element)
    for element1 in copy_of_group:
        group.remove(element1)
        num += 1
        explosion = Sprite(element1.get_position(),[0, 0], 0 , 0 , explosion_image, explosion_info, explosion_sound)
        explosion_group.add(explosion)
    if num > 0:
        return True    
    else:
        return False
    
def group_group_collide(group1,group2):
    global lives, score
    remove_rock_group = set([])
    num = 0
    for element in group1:
        if group_collide(group2,element):
            remove_rock_group.add(element)
    for element1 in remove_rock_group:
        group1.remove(element1)
        num += 1
        score += 1*10
 
def click(pos):
    global lives, started , my_ship, rock_group, score
    centre = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
        
    if not started:
        started = True
        timer.start()

    
#key handlers to control the rotation of the ship
def keydown(key):
    global angle_vel, angular_vel
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel -= angular_vel
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel += angular_vel
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrust = True
        ship_thrust_sound.play()
    elif simplegui.KEY_MAP["space"] == key:
        my_ship.shoot()
        missile_sound.play()        
          
def keyup(key):
    global angle_vel, angular_vel
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel = 0
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel = 0
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrust = False
        ship_thrust_sound.rewind()
                
def draw(canvas):
    global time, score, missile_group, explosion_group, rock_group, num, lives , started, my_ship
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text('Lives' + " " + str(lives), (20, 40), 25, 'white')
    canvas.draw_text('Score' + "    " + str(score), (600, 40), 25, 'white')
           
    
    # draw ship and sprites
    my_ship.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    for rock in rock_group:
        rock.reflection(rock_group)
        rock.draw(canvas)
        rock.update()
        
    ship_collide = group_collide(rock_group, my_ship) 
    if ship_collide:
        if lives >= 0:
            lives -= 1
    
    group_group_collide(rock_group,missile_group)
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
        soundtrack.play()
        
    if lives == 0:
        soundtrack.pause()
        started = False
        timer.stop()
        remove_all_rock = set([])
        for rock in rock_group:
            remove_all_rock.add(rock)
        for all_rock in remove_all_rock:
            rock_group.remove(all_rock)
        lives = 3
        score = 0
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0 , 0],0,ship_image, ship_info)
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock , rock_group    
    if len(rock_group) < 12:
        a_rock = Sprite([random.random()*WIDTH, random.random()*HEIGHT], [random.random(), random.random()],random.random(),random.random() * 0.1, asteroid_image, asteroid_info)    
        rock_group.add(a_rock)
        
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([400, 300], [0.3, 0.4], 0, 0.1, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

frame.start()