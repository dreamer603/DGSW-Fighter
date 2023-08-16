import pygame
import sys
from pygame import mixer
from fighter import Fighter
from pyvidplayer import Video

pygame.init()

# 게임 창 만들기
Screen_Width = 1000
Screen_Height = 600

Screen = pygame.display.set_mode((Screen_Width,Screen_Height))
pygame.display.set_caption("DGSW Fighter")

# 프레임 세팅
clock = pygame.time.Clock()
Fps = 100

# 색상 정의
Red = (255 , 0, 0)
Yellow = (255, 255, 0)
Gray = (220, 220, 220)

# 인 게임 내 값 설정
Intro_Count = 3
Last_Count_Update = pygame.time.get_ticks()
Score = [0, 0] 
Round_Over = False
Round_Over_CoolDown = 2000

# 플레이어블 캐릭터 설정
MinHo_Size = 162
MinHo_Scale = 4
MinHo_Offset = [72, 56]
MinHo_Data = [MinHo_Size, MinHo_Scale, MinHo_Offset]
JuHwan_Size = 250
JuHwan_Scale = 3
JuHwan_Offset = [112, 107]
JuHwan_Data = [JuHwan_Size, JuHwan_Scale, JuHwan_Offset]
GunWo_Size = 250
GunWo_Scale = 500
GunWo_Offset = [72, 56]
GunWo_Data = [GunWo_Size, GunWo_Scale, GunWo_Offset]

# 효과음 로드
MinHo_sd = pygame.mixer.Sound("assets/sounds/MinHo_sd.wav")
MinHo_sd.set_volume(0.1)
JuHwan_sd = pygame.mixer.Sound("assets/sounds/JuHwan_sd.wav")
JuHwan_sd.set_volume(0.1)
GunWo_sd = pygame.mixer.Sound("assets/sounds/GunWo_sd.mp3")
GunWo_sd.set_volume(0.4)

# 배경 이미지 로드
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
scaled_bg = pygame.transform.scale(bg_image, (Screen_Width, Screen_Height))
MinHo_HP_bg = pygame.image.load("assets/images/background/Health_Bar.png").convert_alpha()
JuHwan_HP_bg = pygame.transform.flip(MinHo_HP_bg, True, False)

# 승리 이미지 로드
victory_img = pygame.image.load("assets/icons/victory.png").convert_alpha()
p1_Win_img = pygame.image.load("assets/icons/HoWin.png").convert_alpha()
p2_Win_img = pygame.image.load("assets/icons/HwanWin.png").convert_alpha()

# 스프라이트 시트 로드
MinHo_Sheet = pygame.image.load("assets/images/MinHo/Sprites/MinHo.png").convert_alpha()
JuHwan_Sheet = pygame.image.load("assets/images/JuHwan/Sprites/JuHwan.png").convert_alpha()
GunWo_Sheet = pygame.image.load("assets/images/hidden/Sprites/GunWo.png").convert_alpha()

# 애니메이션 지정
MinHo_Animation_Steps = [10, 8, 1, 7, 7, 3, 7]
JuHwan_Animation_Steps = [8, 8, 1, 8, 8, 3, 7]
GunWo_Animation_Steps = 6
current_scene = 0
animation_speed = 10

GunWo_Anis = []
for i in range(7):
    x = i * GunWo_Size
    y = 0
    rect = pygame.Rect(x, y, GunWo_Size, GunWo_Size)
    GunWo_Ani = GunWo_Sheet.subsurface(rect)
    GunWo_Ani = pygame.transform.scale(GunWo_Ani, (800, 800))
    GunWo_Anis.append(GunWo_Ani)

# 폰트
Count_Font = pygame.font.Font("assets/fonts/turok.ttf", 80)
Score_Font = pygame.font.Font("assets/fonts/turok.ttf", 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    Screen.blit(img, (x, y))

# 배경 이미지 구현
def draw_bg():
    Screen.blit(scaled_bg, (0,0))

# 인트로 로드
intro_vid = Video("assets/videos/intro_main.mp4")
intro_vid.set_size((1000, 600))

def intro():
    while True:
        intro_vid.set_volume(0.3)
        intro_vid.vid_draw(Screen, (0, 0))
        pygame.display.update()
        if intro_vid._video.get_pts() > 24:
            intro_vid.close()
            return
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                intro_vid.close()
                return
            if event.type == pygame.QUIT:
                 pygame.quit()

# 플레이어블 캐릭터 체력 구현
def draw_health_bar(health, x, y):
    bar = health / 100
    pygame.draw.rect(Screen, Gray, (x-2, y-2, 405, 35))
    pygame.draw.rect(Screen, Red, (x, y, 400, 30))
    pygame.draw.rect(Screen, Yellow, (x, y, 400 * bar, 30))

# 플레이어블 캐릭터 인스턴스 만들기
MinHo = Fighter(1, 200, 310, False, MinHo_Data, MinHo_Sheet, MinHo_Animation_Steps, MinHo_sd)
JuHwan = Fighter(2, 700, 310, True, JuHwan_Data, JuHwan_Sheet, JuHwan_Animation_Steps, JuHwan_sd)

# 히든 커맨드
def hidden(target, tx, ty):
    if i == 2:
        GunWo_sd.play()
    if i >= 5:
        target.health = 0
        draw_health_bar(target.health, tx, ty)
        pygame.display.flip()
        current_scene = 0
        target.alive = False
        Round_Over = True
        pygame.time.wait(2000)
        pygame.quit()
    pygame.display.flip()
    clock.tick(animation_speed)

def draw_all():
    # 배경 초기화
    Screen.fill((0, 0, 0))
    draw_bg()

    # 체력 바 그리기
    Screen.blit(MinHo_HP_bg, (10, 8))
    Screen.blit(JuHwan_HP_bg, (557, 8))
    draw_health_bar(MinHo.health, 22, 18)
    draw_health_bar(JuHwan.health, 573, 18)
    

    # 점수 표기
    draw_text("MinHo: " + str(Score[0]), Score_Font, Red, 20, 70)
    draw_text("JuHwan: " + str(Score[1]), Score_Font, Red, 580, 70)

    # 라운드 표기
    draw_text("Round", Score_Font, Red, 462, 5)
    if Score[0] + Score[1] == 0:
        draw_text("1", Count_Font, Red, 490, 20)
    else:
        draw_text(str(Score[0] + Score[1]+1), Count_Font, Red, 480, 20)

    # 애니메이션 업데이트
    MinHo.update()
    JuHwan.update()

    # 플레이어블 캐릭터 그리기
    MinHo.draw(Screen)
    JuHwan.draw(Screen)

# 인트로 실행
intro()

# BGM 로드
pygame.mixer.music.load("assets/sounds/BGM.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000)

# 게임 루프
run = True
while run:

    clock.tick(Fps)

    # 화면 구성
    draw_all()

    # 승패 확인
    if Round_Over == False:
        if MinHo.alive  == False:
                Score[1] += 1
                Round_Over = True
                Round_Over_Time = pygame.time.get_ticks()
        elif JuHwan.alive == False:
                Score[0] += 1
                Round_Over = True
                Round_Over_Time = pygame.time.get_ticks()
    else:
            if max(Score) < 3:
                Screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - Round_Over_Time > Round_Over_CoolDown:
                Round_Over = False
                if Score[0] == 3:
                    MinHo.win(Screen, p1_Win_img)
                elif Score[1] == 3:
                    JuHwan.win(Screen, p2_Win_img)
                else:
                    Intro_Count = 3 

    if Intro_Count <= 0:
        #플레이어블 캐릭터 움직이기
        MinHo.move(Screen_Width, Screen_Height, Screen, JuHwan, Round_Over, "JuHwan")
        JuHwan.move(Screen_Width, Screen_Height, Screen, MinHo, Round_Over, "MinHo")
    else:
            # 화면 카운트
        if Score[0] == 3:
            MinHo.win(Screen, p1_Win_img)
        elif Score[1] == 3:
            JuHwan.win(Screen, p2_Win_img)
        else:
            draw_text(str(Intro_Count), Count_Font, Red, Screen_Width / 2, Screen_Height / 3)
            if (pygame.time.get_ticks() - Last_Count_Update) >= 1000:
                Intro_Count -= 1
                Last_Count_Update = pygame.time.get_ticks()
                MinHo = Fighter(1, 200, 310, False, MinHo_Data, MinHo_Sheet, MinHo_Animation_Steps, MinHo_sd)
                JuHwan = Fighter(2, 700, 310, True, JuHwan_Data, JuHwan_Sheet, JuHwan_Animation_Steps, JuHwan_sd)

    key = pygame.key.get_pressed()

    if key[pygame.K_4] and key[pygame.K_q]:
        for i in range(GunWo_Animation_Steps):
            draw_all()
            Screen.blit(GunWo_Anis[i], (30, -20))
            hidden(JuHwan, 573, 18)

    elif key[pygame.K_0] and key[pygame.K_MINUS]:
        for i in range(GunWo_Animation_Steps):
            draw_all()
            Flip_GunWo = pygame.transform.flip(GunWo_Anis[i], True, False)
            Screen.blit(Flip_GunWo, (250, -20))
            hidden(MinHo, 22, 18)

    # 게임 꺼짐 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

#나가기
pygame.quit()