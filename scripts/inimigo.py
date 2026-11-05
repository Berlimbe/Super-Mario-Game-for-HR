# inimigo.py
import pygame
import os

def carregar_imagem(nome):
    caminhos = [
        nome,
        os.path.join("imagens", nome),
        nome.lower(),
        os.path.join("imagens", nome.lower())
    ]
    for caminho in caminhos:
        if os.path.exists(caminho):
            img = pygame.image.load(caminho).convert_alpha()
            rect_util = img.get_bounding_rect()
            if rect_util.width > 0 and rect_util.height > 0:
                return img.subsurface(rect_util)
            return img
    return None

class AnalistaRH:
    def __init__(self, x, y, limite_esq, limite_dir):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.cor = (200, 50, 50) 
        self.vel = 2
        self.limite_esq = limite_esq
        self.limite_dir = limite_dir
        self.direcao = 1 
        
        img = carregar_imagem("goomba.png")
        if img:
            self.imagem = pygame.transform.scale(img, (self.rect.width, self.rect.height))
            self.tem_img = True
        else:
            self.tem_img = False

    def mover(self):
        self.rect.x += self.vel * self.direcao
        if self.rect.right >= self.limite_dir:
            self.direcao = -1
        elif self.rect.left <= self.limite_esq:
            self.direcao = 1

    def desenhar(self, tela, offset_x=0):
        rect_tela = self.rect.copy()
        rect_tela.x -= offset_x
        if self.tem_img:
            tela.blit(self.imagem, rect_tela)
        else:
            pygame.draw.rect(tela, self.cor, rect_tela)

class JustaCausa: 
    def __init__(self, x, y_topo, y_fundo):
        self.rect = pygame.Rect(x + 10, y_fundo, 30, 40)
        self.cor = (150, 0, 200) 
        self.vel = 1.5
        self.y_topo = y_topo
        self.y_fundo = y_fundo
        self.direcao = -1 

    def mover(self):
        self.rect.y += self.vel * self.direcao
        if self.rect.y <= self.y_topo:
            self.direcao = 1 
        elif self.rect.y >= self.y_fundo:
            self.direcao = -1 

    def desenhar(self, tela, offset_x=0):
        rect_tela = self.rect.copy()
        rect_tela.x -= offset_x
        pygame.draw.rect(tela, self.cor, rect_tela)

class CaixaInterativa:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.ativa = True
        self.cor_ativa = (255, 200, 0) 
        self.cor_vazia = (139, 69, 19) 
    
    def desenhar(self, tela, offset_x=0):
        rect_tela = self.rect.copy()
        rect_tela.x -= offset_x
        cor = self.cor_ativa if self.ativa else self.cor_vazia
        pygame.draw.rect(tela, cor, rect_tela)
        pygame.draw.rect(tela, (0, 0, 0), rect_tela, 2)
        if self.ativa:
            fonte = pygame.font.SysFont(None, 36)
            texto = fonte.render("?", True, (0, 0, 0))
            tela.blit(texto, (rect_tela.x + 12, rect_tela.y + 8))

class Cogumelo:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.cor = (255, 50, 50) 
        self.vel_x = 3
        self.vel_y = 0
        self.gravidade = 0.8
        
        img = carregar_imagem("cogumelo.png")
        if img:
            self.imagem = pygame.transform.scale(img, (self.rect.width, self.rect.height))
            self.tem_img = True
        else:
            self.tem_img = False
    
    def mover(self, plataformas):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y
        for p in plataformas:
            if self.rect.colliderect(p):
                if self.vel_y > 0:
                    self.rect.bottom = p.top
                    self.vel_y = 0
        
        self.rect.x += self.vel_x
        for p in plataformas:
            if self.rect.colliderect(p):
                if self.vel_x > 0:
                    self.rect.right = p.left
                    self.vel_x *= -1
                elif self.vel_x < 0:
                    self.rect.left = p.right
                    self.vel_x *= -1

    def desenhar(self, tela, offset_x=0):
        rect_tela = self.rect.copy()
        rect_tela.x -= offset_x
        if self.tem_img:
            tela.blit(self.imagem, rect_tela)
        else:
            pygame.draw.rect(tela, self.cor, rect_tela)
            pygame.draw.rect(tela, (255, 255, 255), (rect_tela.x + 5, rect_tela.y + 5, 20, 10))
            pygame.draw.rect(tela, (0, 0, 0), rect_tela, 1)