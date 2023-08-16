import pygame
import time
import random

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0
        # 0: 정자세; 1: 달리기; 2:점프; 3: 공격1; 4: 공격2; 5: 맞음; 6: 죽음;
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_sound = sound
        self.attack_cooldown = 0
        self.active_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True
        self.actvie = 0
        self.active_hit = False
        self.JuHwan_Actibe_sd = pygame.mixer.Sound("assets/sounds/JuHwan_Active.wav")
        self.JuHwan_Actibe_sd.set_volume(0.4)
        self.critical = 0
        self.down = False
        self.up = False

    def load_images(self, sprite_sheet, animation_steps):
        # 스프라이트 시트에서 이미지 추출
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, Screen_Width, Screen_Height, surface, target, round_over, attack_target):
        Speed = 10
        Gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = False

        # 키 가져오기
        key = pygame.key.get_pressed()

        if (self.attacking == False) and (self.alive == True) and (round_over == False):
            # 민호 컨트롤
            if self.player == 1:
                # 움직이기
                if key[pygame.K_a]:
                    dx = -Speed
                    self.running = True
                if key[pygame.K_d]:
                    dx = Speed
                    self.running = True

                # 점프
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                
                # 액티브 스킬
                if key[pygame.K_d] and key[pygame.K_r] and (self.active_cooldown == 0):
                    dx = 400
                    self.attack(surface, target, attack_target)
                    self.attack_type = 2
                    target.health -= 25
                    self.active_cooldown = 500

                # 평타
                elif key[pygame.K_r] or key[pygame.K_e]:
                    self.attack(surface, target, attack_target)
                    # 공격 유형 확인
                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[pygame.K_r]:
                        self.attack_type = 2

                # 상대 스킬 피격 효과
                if self.active_hit == True:
                    dx = -1000
                    self.health -= 20
                    self.active_hit = False

                if self.up == True:
                    dy = -150
                    dx = -10
                    self.up = False

                if self.down == True:
                    dy = 100
                    dx = 10
                    self.down = False
                    
            
            # 주환 컨트롤
            if self.player == 2:
                # 움직이기
                if key[pygame.K_j]:
                    dx = -Speed
                    self.running = True
                if key[pygame.K_l]:
                    dx = Speed
                    self.running = True

                # 점프
                if key[pygame.K_i] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                
                # 액티브 스킬
                if key[pygame.K_l] and [pygame.K_p] and (self.active_cooldown == 0):
                    self.JuHwan_Actibe_sd.play()
                    self.attack(surface, target, attack_target)
                    self.attack_type = 2
                    target.active_hit = True
                    self.health += 20
                    self.active_cooldown = 500

                # 평타
                elif key[pygame.K_o] or key[pygame.K_p]:
                    self.attack(surface, target, attack_target)
                    # 공격 유형 확인
                    if key[pygame.K_o]:
                        self.attack_type = 1
                        if target.hit == True:
                            target.up = True
                    if key[pygame.K_p]:
                        self.attack_type = 2
                        if target.hit == True:
                            target.down = True

                # 상대 스킬 피격 효과
                if (self.hit == True) and (self.active_hit == True):
                    self.critical = random.randrange(1, 10)
                    if self.critical <= 4:
                        self.health -= 10
                    
                    

        # 중력
        self.vel_y += Gravity
        dy += self.vel_y

        # 플레이어블 캐릭터 위치 확인
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > Screen_Width:
            dx = Screen_Width - self.rect.right
        if self.rect.bottom + dy > Screen_Height - 110:
            self.vel_y = 0
            self.jump = False
            dy = Screen_Height - 110 - self.rect.bottom

        # 플레이어블 캐릭터가 서로 마주보도록 하기
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # 공격 쿨타임
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.active_cooldown > 0:
            self.active_cooldown -= 1
                
        # 플레이어블 캐릭터 위치 업데이트
        self.rect.x += dx
        self.rect.y += dy

    # 애니메이션 업데이트
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        # 플레이어의 행동 확인
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else: 
            self.update_action(0)

        animation_cooldown = 20
        self.image = self.animation_list[self.action][self.frame_index]   

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.attacking == True:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.hit == True:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 20

    def attack(self, surface, target, attack_target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_sound.play()
            p1_attacking_rect = pygame.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flip), self.rect.y, 2.5 * self.rect.width, self.rect.height)
            p2_attacking_rect = pygame.Rect(self.rect.centerx - (4 * self.rect.width * self.flip), self.rect.y, 4 * self.rect.width, self.rect.height * 100)
            if attack_target == "JuHwan":
                if p1_attacking_rect.colliderect(target.rect):
                    target.health -= 10
                    target.hit = True
            elif attack_target == "MinHo":
                if p2_attacking_rect.colliderect(target.rect):
                    target.health -= 10
                    target.hit = True


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def win(self, Screen, Win_img):
        Screen.blit(Win_img, (360, 150))
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()
        