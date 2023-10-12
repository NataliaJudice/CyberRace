import pygame 
from pygame.locals import * 
from sys import exit 
import os 
from random import randrange,choice

pygame.init()

#acesso a pasta
diretorio_principal = os.path.dirname(__file__)
diretorio_Imagens = os.path.join(diretorio_principal, 'css')


#variaveis globais
largura = 640
altura = 480
branco = 0,0,0
velocidade = 1
OBescolha = choice([1,2,3])
movimento = 0 
fonte = pygame.font.SysFont('arial',20, True, True)
score = 0
a = False
matou = False
kills= 0
meta = 1
win = False
cena = "menu"
colidiu1=False
colidiu2=False
gameover = False
tutorial = False

#título
tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Cyber Race')

#spritesheets
Personagem = pygame.image.load(os.path.join(diretorio_Imagens, 'ssperson.png')).convert_alpha()
Obstaculo = pygame.image.load(os.path.join(diretorio_Imagens, 'ssobsaculos.png')).convert_alpha()

#funções

def reiniciar_jogo():
   global score, meta, kills, velocidade,colidiu1,colidiu2,OBescolha,gameover
   OBescolha = choice([1,2,3])
   score = 0
   kills = 0
   meta = 1
   velocidade = 1
   gameover = False 
   colidiu1 = False
   colidiu2 = False 
   personagem.rect.y= altura - 100 - 96//2
   personagem.pulo = False
   voador.rect.x = largura
   passaro.rect.x=largura
   nave.rect.x=largura

def exibir_mensagem(msg,tamanho,cor):
   fonte = pygame.font.SysFont('comicsans', tamanho, True, False)
   mensagem = f'{msg}'
   textoF = fonte.render(mensagem,True,cor)
   return textoF

#classes 
class Persona(pygame.sprite.Sprite):
  def __init__(self):
     pygame.sprite.Sprite.__init__(self)
     self.sprites = []
     self.img1 = Personagem.subsurface((6*96,0), (96,96))
     self.img1 = pygame.transform.scale(self.img1, (128,128))
     self.img2 = Personagem.subsurface((7*96,0), (96,96))
     self.img2 = pygame.transform.scale(self.img2, (128,128))
     for i in range(6):
        img = Personagem.subsurface((i*96,0), (96,96))
        img = pygame.transform.scale(img, (128,128))
        self.sprites.append(img)

     self.atual = 0
     self.image = self.sprites[self.atual]
     self.rect = self.image.get_rect()
     self.rect1 = self.img1.get_rect()
     self.rect.center = (60, altura-70)
     self.mask = pygame.mask.from_surface(self.image)
     self.recty = altura-70 - 96//2
     self.abaixo = False
     self.pulo = False

  def update(self):
     #animação
     self.atual = self.atual + 0.025
     if self.atual > 6:
        self.atual = 0
     self.image = self.sprites[int(self.atual)]
     
     #pular
     if self.pulo == True: 
       if self.rect.y <= 150:
           self.pulo = False
       self.rect.y -= 1

     else: 
        if self.rect.y < self.recty:
           self.rect.y += 1
        else: 
           self.rect.y == self.recty 

     #abaixar
     if self.abaixo == True:
        self.image = self.img1
        self.mask = pygame.mask.from_surface(self.img1)
        self.rect.center = (60,altura-60)
     else:
        self.image = self.sprites[int(self.atual)] 
        self.mask = pygame.mask.from_surface(self.image)

  def abaixar(self):
     self.abaixo = True

  def levantar(self):
     self.abaixo = False

  def pular(self):
      self.pulo = True

class Voador(pygame.sprite.Sprite): 
   def __init__(self):
     pygame.sprite.Sprite.__init__(self) 
     self.sprites = []    

     for i in range(4):
        img = Obstaculo.subsurface((i*96,0), (96,96))
        img = pygame.transform.scale(img, (96,96))
        self.sprites.append(img)

     self.atual = 0
     self.image = self.sprites[self.atual]
     self.rect = self.image.get_rect()
     self.rect.center = (largura, altura-125)
     self.mask = pygame.mask.from_surface(self.image)
     self.Identificador = OBescolha
     self.rect.x = largura
         
   def update(self):
     if self.Identificador == 1:
      self.atual = self.atual + 0.05
      if self.atual > 4:
         self.atual = 0
      self.image = self.sprites[int(self.atual)]

      if self.rect.topright[0] < 0:
         self.rect.x = largura
      self.rect.x -= velocidade  

class Nave(pygame.sprite.Sprite):
    def __init__(self):
     pygame.sprite.Sprite.__init__(self)
     self.sprites = []    

     for i in range(4,7):
        img = Obstaculo.subsurface((i*96,0), (96,96))
        img = pygame.transform.scale(img, (128,128))
        self.sprites.append(img)

     self.atual = 0
     self.image = self.sprites[self.atual]
     self.rect = self.image.get_rect()
     self.rect.center = (largura, altura-60)
     self.mask = pygame.mask.from_surface(self.image)
     self.Identificador = OBescolha
     self.rect.x = largura
         
    def update(self):
     if self.Identificador == 2:
      self.atual = self.atual + 0.01
      if self.atual > 3:
         self.atual = 0
      self.image = self.sprites[int(self.atual)]

      if self.rect.topright[0] < 0:
         self.rect.x = largura
      self.rect.x -= velocidade  

class Lua(pygame.sprite.Sprite):
  def __init__(self):
     pygame.sprite.Sprite.__init__(self) 
     self.image = pygame.image.load('css/luaa.png')
     self.image = pygame.transform.scale(self.image, (32,32)) 
     self.rect = self.image.get_rect()
     self.rect.center = (largura-50, altura-400)
 
class Char(pygame.sprite.Sprite):
  def __init__(self):
     pygame.sprite.Sprite.__init__(self) 
     self.image = Obstaculo.subsurface((7*96,0), (96,96))
     self.image = pygame.transform.scale(self.image, (64,64)) 
     self.rect = self.image.get_rect()
     self.rect.center = (100, 50)

class Passaro(pygame.sprite.Sprite):
  def __init__(self):
     pygame.sprite.Sprite.__init__(self)
     self.sprites = []    

     for i in range(7,10):
        img = Obstaculo.subsurface((i*96,0), (96,96))
        img = pygame.transform.scale(img, (96,96))
        self.sprites.append(img)

     self.atual = 0
     self.image = self.sprites[self.atual]
     self.rect = self.image.get_rect()
     self.rect.center = (largura, altura-50)
     self.mask = pygame.mask.from_surface(self.image)
     self.rect.x = largura
     self.Identificador = OBescolha
     self.vazio = pygame.image.load('css/vazio.png')
     self.morreu = False

     

  def update(self):
   if self.Identificador == 3:
      self.atual = self.atual + 0.05
      if self.atual > 3:
         self.atual = 0
      self.image = self.sprites[int(self.atual)]

      if self.rect.topright[0] < 0:
         self.rect.x = largura
      self.rect.x -= velocidade  

      if self.morreu == True:
         self.image = self.vazio
         self.mask = pygame.mask.from_surface(self.vazio)
      else:
         self.image = self.sprites[int(self.atual)]  
         self.mask = pygame.mask.from_surface(self.image)  

class Tiro(pygame.sprite.Sprite):
    def __init__(self):
     pygame.sprite.Sprite.__init__(self)
     self.image = pygame.image.load('css/pewpew.png')
     self.rect = self.image.get_rect()
     self.rect.center = (60, altura-50)
     self.mask = pygame.mask.from_surface(self.image)
     self.Identificador = OBescolha
     self.rect.x = 60
     self.imgx = 60
     self.atiro = False
     self.vazio = pygame.image.load('css/vazio.png')

    def update(self):
     
        
     if self.atiro==True:
        self.rect.x += 10
        self.image = pygame.image.load('css/pewpew.png')
        self.mask = pygame.mask.from_surface(self.image)
        

     else:
        self.image = self.vazio
        self.mask = pygame.mask.from_surface(self.vazio)
        self.rect.x = self.imgx

       
    def atirar(self):
       self.atiro = True

    def naoatirar(self):
       self.atiro = False   

class Chao(pygame.sprite.Sprite):
  def __init__(self, pos_x):
     pygame.sprite.Sprite.__init__(self) 
     self.image = pygame.image.load('css/chaoo.png')
     self.image = pygame.transform.scale(self.image, (32*2,32*2)) 
     self.rect = self.image.get_rect()
     self.rect.y = altura - 55
     self.rect.x = pos_x * 64
     


  def update(self): 
     if self.rect.topright[0] < 0:
        self.rect.x = largura
     self.rect.x -=1

bg = pygame.image.load('css/backgrounddd.png').convert_alpha()
bgW= bg.get_width()

p = int(largura/bgW) + 2

#listas 
obstaculos = pygame.sprite.Group() 
mataveis = pygame.sprite.Group()
todasS = pygame.sprite.Group() 


#instanciação de objetos

char = Char()
todasS.add(char) 

passaro = Passaro()
todasS.add(passaro)
mataveis.add(passaro) 

for i in range(15):
  chao = Chao(i)
  todasS.add(chao) 

luaa = Lua()
todasS.add(luaa)  

nave = Nave()
todasS.add(nave)
obstaculos.add(nave)

voador = Voador()
todasS.add(voador)
obstaculos.add(voador)

tiro = Tiro()
todasS.add(tiro)

personagem = Persona()
todasS.add(personagem)  

imagemFundo = pygame.image.load('css/fundo.png').convert()
imagemFundo = pygame.transform.scale(imagemFundo,(largura, altura))
imagemMenu = pygame.image.load('css/MenuCR.png').convert()
imagemMenu = pygame.transform.scale(imagemMenu,(largura, altura))
tut = pygame.image.load('css/tutorialCR.png').convert_alpha()
tut = pygame.transform.scale(tut,(largura, altura))

       
#loop do jogo
while True:
   if cena == "jogo":
    mensagem = f"{int(score)}"
    mensagem2 = f"{int(kills)}/{int(10*meta)}"
    textoF = fonte.render(mensagem, True, (255,255,255))
    textoF2 = fonte.render(mensagem2, True, (255,255,255))
    
    teclas = pygame.key.get_pressed()

    #personagem abaixa
    if teclas[pygame.K_DOWN]:
       if personagem.rect.y != personagem.recty:
           pass
       else:
          personagem.abaixar()
    else:
       personagem.levantar()

    #não deixa as imagens se repetirem ocupando a tela toda   
    tela.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
           
        #personagem pula 
        if event.type == KEYDOWN:
           if event.key == pygame.K_UP:
              if personagem.rect.y != personagem.recty or personagem.abaixo == True:
                 pass
              else:
                personagem.pular() 

           if event.key == pygame.K_r and colidiu1==True or colidiu2==True:
              reiniciar_jogo()       
           if event.key == pygame.K_m and colidiu1==True or colidiu2==True:
              cena = "menu"       

        if event.type == KEYDOWN:
           if event.key == pygame.K_RIGHT:
              tiro.atirar()
           else:
              tiro.naoatirar()
        else:
           if event.type == KEYUP:
              tiro.naoatirar()

    if personagem.rect.y < personagem.recty and personagem.abaixo == False and gameover == False:    
           tiro.atiro = False
           personagem.image = personagem.img2 
           personagem.mask = pygame.mask.from_surface(personagem.image)
           
                            

    #colisões usando masks    
    colisao = pygame.sprite.spritecollide(personagem,obstaculos,False,pygame.sprite.collide_mask)               
    colisao2 = pygame.sprite.spritecollide(personagem,mataveis,False,pygame.sprite.collide_mask)               
    matar = pygame.sprite.spritecollide(tiro,mataveis,False,pygame.sprite.collide_mask)               

   #mostra a cor de fundo na tela  
    tela.blit(imagemFundo,(0,0))
            
    for i in range(p):
      tela.blit(bg,(i*bgW + movimento - bgW,0))

      
    tela.blit(textoF, (580,40))
    tela.blit(textoF2, (110,40))

    #desenha todos os objetos inseridos na lista 
    todasS.draw(tela)   


    #condição que faz com que toda vez que um objeto sair da tela outro seja sorteado

    if colisao:
       colidiu1 = True
    else:
       colidiu1 = False

    if colisao2:
       colidiu2 = True
    else:
       colidiu2 = False

    if matar:
       matou = True
       kills +=1
    
    if kills == (10*meta):
       meta += 2
    if kills == 100:
       win = True   

    if a == False:
     if nave.rect.topright[0] <=0 or voador.rect.topright[0]<=0 or passaro.rect.topright[0]<=0:
         OBescolha = choice([1,2])
         matou = False
         nave.rect.x = largura
         passaro.rect.x = largura
         voador.rect.x = largura
         nave.Identificador = OBescolha
         passaro.Identificador = OBescolha
         voador.Identificador = OBescolha
    else: 
     if nave.rect.topright[0] <=0 or voador.rect.topright[0]<=0 or passaro.rect.topright[0]<=0:
            OBescolha = choice([1,2,3])
            matou = False
            nave.rect.x = largura
            passaro.rect.x = largura
            voador.rect.x = largura
            nave.Identificador = OBescolha
            passaro.Identificador = OBescolha
            voador.Identificador = OBescolha
        

    if matou == True: 
      passaro.morreu = True
        
    else:
       passaro.morreu = False

    
    
    #caso ocora uma colisao todas as animações param
    if colidiu1 or colidiu2:
       gameover = True
       gameo = pygame.image.load('css/gameover.png').convert_alpha()
       gameo = pygame.transform.scale(gameo,(550,550))
       tela.blit(gameo,(100,100))   
       pass 
    else:
      score += 0.05
      if score >= 200:
       a = True
      else: 
       a = False 
      
      if score > 300.00000000003394:
         velocidade = 1.5

      movimento -= 1
      if abs(movimento) > bgW:
         movimento = 0

     
      todasS.update()

   elif cena =="menu":
       for event in pygame.event.get():
         if event.type == QUIT:
            pygame.quit()
            exit()
         if event.type == KEYDOWN:
           if event.key == pygame.K_j:
              reiniciar_jogo() 
              cena = 'jogo'
           if event.key == pygame.K_t:
              tutorial=True
           if event.key == pygame.K_s and tutorial == True:
              tutorial=False  

         tela.blit(imagemMenu,(0,0)) 
         instrucoes = pygame.image.load('css/menuins.png').convert_alpha()
         instrucoes = pygame.transform.scale(instrucoes,(350,350))
         tela.blit(instrucoes,(300,150))
         if tutorial==True:
            tela.blit(tut,(0,0))
         else:
            pass    

   

         
      

   pygame.display.flip()     