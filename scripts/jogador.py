# jogador.py
import pygame
import os
from configuracoes import *

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

class Aprendiz:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        self.cor = AZUL_VW  
        self.vel_base = 5
        self.vel = self.vel_base
        
        self.vel_y = 0       
        self.gravidade = 0.8 
        self.forca_pulo_base = -15 
        self.forca_pulo = self.forca_pulo_base
        self.no_chao = False 
        self.bateu_cabeca = False
        
        self.adulto = False
        self.tempo_invencivel = 0

        # Sprites João Jovem (Padrão)
        self.img_idle = carregar_imagem("joao_skin_basica.png")
        img_run1 = carregar_imagem("joao_skin_correndo.png")
        img_run2 = carregar_imagem("joao_skin_correndo2.png")
        img_run3 = carregar_imagem("joao_skin_correndo3.png")
        self.img_run = [img for img in [img_run1, img_run2, img_run3] if img is not None]

        # Sprites João Adulto (Cogumelo)
        self.img_idle_adulto = carregar_imagem("joao_adulto.png")
        ad1 = carregar_imagem("joao_adulto1.png")
        ad2 = carregar_imagem("joao_adulto2.png")
        ad3 = carregar_imagem("joao_adulto3.png")
        self.img_run_adulto = [img for img in [ad1, ad2, ad3] if img is not None]

        self.frame_atual = 0
        self.virado_direita = True
        self.andando = False

    def crescer(self):
        if not self.adulto:
            self.adulto = True
            self.vel = 8  # Aumenta a velocidade ao pegar o cogumelo
            self.rect.height = 85
            self.rect.y -= 25

    def encolher(self):
        self.adulto = False
        self.vel = self.vel_base  # Retorna à velocidade normal (5)
        self.rect.height = 60
        self.rect.y += 25
        self.tempo_invencivel = 60

    def tomar_dano(self):
        if self.tempo_invencivel > 0:
            return True
        if self.adulto:
            self.encolher()
            return True
        else:
            return False

    def mover_livre(self, teclas):
        self.andando = False
        if (teclas[pygame.K_w] or teclas[pygame.K_UP]) and self.rect.top > 0:
            self.rect.y -= self.vel
            self.andando = True
        if (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) and self.rect.bottom < ALTURA:
            self.rect.y += self.vel
            self.andando = True
        if (teclas[pygame.K_a] or teclas[pygame.K_LEFT]) and self.rect.left > 0:
            self.rect.x -= self.vel
            self.virado_direita = False
            self.andando = True
        if (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) and self.rect.right < LARGURA:
            self.rect.x += self.vel
            self.virado_direita = True
            self.andando = True

    def mover_plataforma(self, teclas, plataformas):
        if self.tempo_invencivel > 0:
            self.tempo_invencivel -= 1

        self.bateu_cabeca = False

        dx = 0
        self.andando = False
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx = -self.vel
            self.virado_direita = False
            self.andando = True
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx = self.vel
            self.virado_direita = True
            self.andando = True
            
        self.rect.x += dx
        
        for p in plataformas:
            if self.rect.colliderect(p):
                if dx > 0: 
                    self.rect.right = p.left
                elif dx < 0: 
                    self.rect.left = p.right

        if (teclas[pygame.K_w] or teclas[pygame.K_UP] or teclas[pygame.K_SPACE]) and self.no_chao:
            self.vel_y = self.forca_pulo
            self.no_chao = False

        self.vel_y += self.gravidade
        self.rect.y += self.vel_y
        self.no_chao = False

        for p in plataformas:
            if self.rect.colliderect(p):
                if self.vel_y > 0: 
                    self.rect.bottom = p.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0: 
                    self.rect.top = p.bottom
                    self.vel_y = 0
                    self.bateu_cabeca = True

    def desenhar(self, tela, offset_x=0):
        if self.tempo_invencivel > 0 and (self.tempo_invencivel // 5) % 2 == 0:
            return

        rect_tela = self.rect.copy()
        rect_tela.x -= offset_x

        if self.adulto and self.img_idle_adulto:
            idle_atual = self.img_idle_adulto
            run_atual = self.img_run_adulto if len(self.img_run_adulto) > 0 else self.img_run
        else:
            idle_atual = self.img_idle
            run_atual = self.img_run

        if idle_atual:
            if self.andando and self.no_chao and len(run_atual) > 0:
                self.frame_atual += 0.2
                if self.frame_atual >= len(run_atual):
                    self.frame_atual = 0
                img_selecionada = run_atual[int(self.frame_atual)]
            else:
                self.frame_atual = 0
                img_selecionada = idle_atual
                
            if not self.virado_direita:
                img_selecionada = pygame.transform.flip(img_selecionada, True, False)
                
            img_redimensionada = pygame.transform.scale(img_selecionada, (self.rect.width, self.rect.height))
            tela.blit(img_redimensionada, rect_tela)
        else:
            pygame.draw.rect(tela, self.cor, rect_tela)