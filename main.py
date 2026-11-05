# main.py
import pygame
import sys
import os
from configuracoes import *

try:
    from scripts.jogador import Aprendiz 
    from scripts.inimigo import AnalistaRH, JustaCausa, CaixaInterativa, Cogumelo
except ImportError:
    from jogador import Aprendiz 
    from inimigo import AnalistaRH, JustaCausa, CaixaInterativa, Cogumelo

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)
clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 36)
fonte_titulo = pygame.font.SysFont(None, 48)

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

img_fundo = carregar_imagem("mapa_rh.png")
if img_fundo:
    proporcao = ALTURA / img_fundo.get_height()
    nova_largura = int(img_fundo.get_width() * proporcao)
    img_fundo = pygame.transform.scale(img_fundo, (nova_largura, ALTURA))

img_piso = carregar_imagem("piso.png")
img_plat = carregar_imagem("plataforma.png")

img_moeda = carregar_imagem("dinheiro.png")
if not img_moeda:
    img_moeda = carregar_imagem("moedas_jogo.png")

if img_moeda:
    img_moeda = pygame.transform.scale(img_moeda, (30, 30))

jogador = Aprendiz(LARGURA // 2, ALTURA - 100)

porta_rh = pygame.Rect(150, 150, 100, 150)
porta_manutencao = pygame.Rect(350, 150, 100, 150)
porta_qualidade = pygame.Rect(550, 150, 100, 150)

def carregar_mapa(area):
    plataformas = []
    pecas = []
    analistas = []
    plantas = []
    caixas = []
    cogumelos = []
    
    if area == "RH":
        tamanho = 6000
        
        plataformas.append(pygame.Rect(0, ALTURA - 40, 800, 40))
        
        caixa1 = CaixaInterativa(500, ALTURA - 180)
        caixas.append(caixa1)
        plataformas.append(caixa1.rect)
        
        plataformas.append(pygame.Rect(950, 450, 100, 20))  
        plataformas.append(pygame.Rect(1200, 380, 100, 20)) 
        plataformas.append(pygame.Rect(1450, 450, 100, 20)) 
        
        plataformas.append(pygame.Rect(1700, ALTURA - 40, 1000, 40)) 
        
        analistas = [
            AnalistaRH(1800, ALTURA - 80, 1750, 2100),
            AnalistaRH(2300, ALTURA - 80, 2150, 2600)
        ]
        pecas = [pygame.Rect(1240, 340, 30, 30)]

        posicoes_canos = [2800, 3100, 3400, 3700]
        for i, x in enumerate(posicoes_canos):
            alt_cano = 80 if i % 2 == 0 else 120 
            cano = pygame.Rect(x, ALTURA - 40 - alt_cano, 50, alt_cano)
            plataformas.append(cano)
            
            if i < len(posicoes_canos) - 1:
                plataformas.append(pygame.Rect(x + 50, ALTURA - 40, posicoes_canos[i+1] - (x + 50), 40))
            
            y_topo_planta = ALTURA - 40 - alt_cano - 40
            y_fundo_planta = ALTURA - 40 - alt_cano + 10 
            plantas.append(JustaCausa(x, y_topo_planta, y_fundo_planta))
            
        plataformas.append(pygame.Rect(3750, ALTURA - 40, 600, 40)) 

        caixa2 = CaixaInterativa(4000, ALTURA - 180)
        caixas.append(caixa2)
        plataformas.append(caixa2.rect)

        parede = pygame.Rect(4500, ALTURA - 200, 50, 200)
        plataformas.append(parede)
        plataformas.append(pygame.Rect(4350, ALTURA - 40, 150, 40)) 
        
        plataformas.append(pygame.Rect(4250, ALTURA - 90, 50, 20))
        plataformas.append(pygame.Rect(4380, ALTURA - 150, 50, 20))
        
        analistas.append(AnalistaRH(4100, ALTURA - 80, 4000, 4300))

        plataformas.append(pygame.Rect(4550, ALTURA - 40, 1500, 40)) 
        analistas.append(AnalistaRH(5000, ALTURA - 80, 4800, 5400))
        analistas.append(AnalistaRH(5300, ALTURA - 80, 5100, 5600))
        
        pecas.append(pygame.Rect(4400, ALTURA - 190, 30, 30))
        pecas.append(pygame.Rect(5200, 350, 30, 30))

    else:
        tamanho = LARGURA

    porta_saida = pygame.Rect(tamanho - 400, 150, 20, ALTURA - 190)
    return tamanho, plataformas, pecas, analistas, plantas, porta_saida, caixas, cogumelos

estado_atual = "MENU"
area_escolhida = ""
camera_x = 0 
pontos_trabalho = 0 
animacao_etapa = 0 

rodando = True
while rodando:
    clock.tick(FPS)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if estado_atual == "MENU":
        if teclas[pygame.K_RETURN]: 
            estado_atual = "ESCOLHA_PORTAS"
            jogador.rect.x, jogador.rect.y = LARGURA // 2, ALTURA - 100
            jogador.adulto = False
            jogador.vel = jogador.vel_base
            jogador.rect.height = 60
            jogador.cor = AZUL_VW
            jogador.tempo_invencivel = 0

    elif estado_atual == "ESCOLHA_PORTAS":
        jogador.mover_livre(teclas) 
        
        if jogador.rect.colliderect(porta_rh):
            area_escolhida = "RH"
            estado_atual = "FABRICA"

        if estado_atual == "FABRICA":
            tamanho_fase, plataformas, pecas, analistas_rh, plantas_rh, porta_saida, caixas_mapa, cogumelos_mapa = carregar_mapa(area_escolhida)
            jogador.tamanho_mapa = tamanho_fase
            jogador.rect.x, jogador.rect.y = 50, 50 

    elif estado_atual == "FABRICA":
        jogador.mover_plataforma(teclas, plataformas)
        
        if jogador.bateu_cabeca:
            zona_cabeca = pygame.Rect(jogador.rect.left, jogador.rect.top - 8, jogador.rect.width, 10)
            for caixa in caixas_mapa:
                if caixa.ativa and zona_cabeca.colliderect(caixa.rect):
                    caixa.ativa = False
                    cogumelos_mapa.append(Cogumelo(caixa.rect.x + 5, caixa.rect.top - 32))
        
        for cogumelo in cogumelos_mapa[:]:
            cogumelo.mover(plataformas)
            if jogador.rect.colliderect(cogumelo.rect):
                jogador.crescer()
                cogumelos_mapa.remove(cogumelo)
                pontos_trabalho += 50
        
        for peca in pecas[:]: 
            if jogador.rect.colliderect(peca):
                pecas.remove(peca)
                pontos_trabalho += 10 
                
        for analista in analistas_rh[:]:
            analista.mover()
            if jogador.rect.colliderect(analista.rect):
                if jogador.vel_y > 0 and jogador.rect.bottom <= analista.rect.centery + 15:
                    analistas_rh.remove(analista)
                    jogador.vel_y = -18       
                    pontos_trabalho += 20
                else:
                    if not jogador.tomar_dano():
                        estado_atual = "GAME_OVER"
                            
        for planta in plantas_rh:
            planta.mover()
            if jogador.rect.colliderect(planta.rect):
                if not jogador.tomar_dano():
                    estado_atual = "GAME_OVER"
                        
        if jogador.rect.top > ALTURA:
            estado_atual = "GAME_OVER"

        if jogador.rect.colliderect(porta_saida):
            estado_atual = "ANIMACAO_FINAL"
            animacao_etapa = 1
            jogador.rect.right = porta_saida.left
            jogador.vel_y = 0

        camera_x = jogador.rect.x - (LARGURA // 2)
        if camera_x < 0: camera_x = 0
        if camera_x > jogador.tamanho_mapa - LARGURA: camera_x = jogador.tamanho_mapa - LARGURA

    elif estado_atual == "ANIMACAO_FINAL":
        if animacao_etapa == 1:
            jogador.rect.y += 4 
            if jogador.rect.bottom >= ALTURA - 40:
                jogador.rect.bottom = ALTURA - 40
                animacao_etapa = 2
        elif animacao_etapa == 2:
            jogador.rect.x += 3 
            if jogador.rect.left > porta_saida.right + 150:
                estado_atual = "VITORIA"
        camera_x = jogador.rect.x - (LARGURA // 2)
        if camera_x < 0: camera_x = 0
        if camera_x > jogador.tamanho_mapa - LARGURA: camera_x = jogador.tamanho_mapa - LARGURA

    elif estado_atual == "VITORIA":
        if teclas[pygame.K_m]:
            estado_atual = "ESCOLHA_PORTAS"
            jogador.rect.x, jogador.rect.y = LARGURA // 2, ALTURA - 100
            pontos_trabalho = 0
            jogador.adulto = False
            jogador.vel = jogador.vel_base
            jogador.rect.height = 60
            jogador.cor = AZUL_VW
            jogador.tempo_invencivel = 0

    elif estado_atual == "GAME_OVER":
        if teclas[pygame.K_RETURN]:
            estado_atual = "FABRICA"
            jogador.rect.x, jogador.rect.y = 50, 50
            jogador.adulto = False
            jogador.vel = jogador.vel_base
            jogador.rect.height = 60
            jogador.cor = AZUL_VW
            jogador.tempo_invencivel = 0
            tamanho_fase, plataformas, pecas, analistas_rh, plantas_rh, porta_saida, caixas_mapa, cogumelos_mapa = carregar_mapa(area_escolhida)
            jogador.tamanho_mapa = tamanho_fase
            pontos_trabalho = 0
        elif teclas[pygame.K_m]:
            estado_atual = "ESCOLHA_PORTAS"
            jogador.rect.x, jogador.rect.y = LARGURA // 2, ALTURA - 100
            jogador.adulto = False
            jogador.vel = jogador.vel_base
            jogador.rect.height = 60
            jogador.cor = AZUL_VW
            jogador.tempo_invencivel = 0
            pontos_trabalho = 0

    # --- DESENHO NA TELA ---
    if estado_atual == "MENU":
        tela.fill((20, 30, 40)) 
        titulo = fonte_titulo.render(TITULO, True, (255, 255, 255))
        subtitulo = fonte.render("Projeto Integrador - SENAI / VW", True, (0, 180, 250))
        instrucao_menu = fonte.render("Pressione ENTER para Iniciar", True, (255, 215, 0))
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 180))
        tela.blit(subtitulo, (LARGURA // 2 - subtitulo.get_width() // 2, 250))
        tela.blit(instrucao_menu, (LARGURA // 2 - instrucao_menu.get_width() // 2, 400))

    elif estado_atual == "ESCOLHA_PORTAS":
        tela.fill(CINZA)
        portas = [
            (porta_rh, (150, 50, 200), "RH"),
            (porta_manutencao, (100, 100, 100), "Manutenção"),
            (porta_qualidade, (100, 100, 100), "Qualidade")
        ]
        
        for porta, cor, nome in portas:
            pygame.draw.rect(tela, cor, porta)
            pygame.draw.rect(tela, PRETO, porta, 3)
            pygame.draw.circle(tela, PRETO, (porta.right - 15, porta.centery), 8)
            
            if porta != porta_rh:
                for y in range(porta.top + 10, porta.bottom - 20, 20):
                    pygame.draw.ellipse(tela, (60, 60, 60), (porta.centerx - 10, y, 20, 25), 4)
                pygame.draw.rect(tela, (218, 165, 32), (porta.centerx - 15, porta.centery - 10, 30, 25))
                pygame.draw.arc(tela, (192, 192, 192), (porta.centerx - 10, porta.centery - 25, 20, 25), 0, 3.14, 4)
            
            texto_render = fonte.render(nome, True, BRANCO)
            pos_x_texto = porta.centerx - (texto_render.get_width() // 2)
            tela.blit(texto_render, (pos_x_texto, 110))
            
        tela.blit(fonte.render("Ande até a porta do departamento:", True, BRANCO), (180, 40))
        
        if jogador.rect.colliderect(porta_manutencao) or jogador.rect.colliderect(porta_qualidade):
            aviso_breve = fonte_titulo.render("EM BREVE!", True, (255, 50, 50)) 
            tela.blit(aviso_breve, (LARGURA // 2 - aviso_breve.get_width() // 2, 340))
            
        jogador.desenhar(tela)

    elif estado_atual in ["FABRICA", "ANIMACAO_FINAL"]: 
        tela.fill((135, 206, 235)) 
        
        if img_fundo:
            fundo_largura = img_fundo.get_width()
            rel_x = camera_x % fundo_largura
            tela.blit(img_fundo, (-rel_x, 0))
            if rel_x > 0:
                tela.blit(img_fundo, (fundo_largura - rel_x, 0))

        pygame.draw.rect(tela, (15, 15, 25), (0, ALTURA - 40, LARGURA, 40))
            
        for planta in plantas_rh:
            planta.desenhar(tela, camera_x)

        for plat in plataformas:
            if plat in [c.rect for c in caixas_mapa]: continue
            
            plat_tela = plat.copy()
            plat_tela.x -= camera_x
            
            if plat.width == 50 and plat.height in [80, 120, 200]: 
                pygame.draw.rect(tela, (0, 180, 0), plat_tela) 
                pygame.draw.rect(tela, (0, 100, 0), plat_tela, 3)
            elif img_piso and plat.height == 40:
                tela.blit(pygame.transform.scale(img_piso, (plat.width, plat.height)), plat_tela)
                pygame.draw.line(tela, (30, 180, 30), (plat_tela.left, plat_tela.top), (plat_tela.right, plat_tela.top), 4)
            elif img_plat and plat.height == 20:
                tela.blit(pygame.transform.scale(img_plat, (plat.width, plat.height)), plat_tela)
                pygame.draw.rect(tela, (255, 255, 255), plat_tela, 1)
            else:
                pygame.draw.rect(tela, (120, 60, 20), plat_tela)
                pygame.draw.rect(tela, (50, 200, 50), (plat_tela.left, plat_tela.top, plat_tela.width, 6))
                pygame.draw.rect(tela, (0, 0, 0), plat_tela, 2)

        for caixa in caixas_mapa:
            caixa.desenhar(tela, camera_x)
            
        for cogumelo in cogumelos_mapa:
            cogumelo.desenhar(tela, camera_x)

        for peca in pecas:
            peca_tela = peca.copy()
            peca_tela.x -= camera_x
            if img_moeda:
                tela.blit(img_moeda, peca_tela)
            else:
                pygame.draw.rect(tela, (255, 215, 0), peca_tela) 
            
        for analista in analistas_rh:
            analista.desenhar(tela, camera_x)

        mastro_tela = porta_saida.copy()
        mastro_tela.x -= camera_x
        pygame.draw.rect(tela, (180, 180, 180), mastro_tela) 
        pygame.draw.circle(tela, (255, 0, 0), (mastro_tela.centerx, mastro_tela.top), 15) 
            
        predio_tela = pygame.Rect(porta_saida.x + 100, ALTURA - 140, 140, 100)
        predio_tela.x -= camera_x
        pygame.draw.rect(tela, (50, 50, 150), predio_tela) 
        tela.blit(fonte.render("Diretoria", True, BRANCO), (predio_tela.x + 25, predio_tela.y + 35))

        tela.blit(fonte.render(f"Área: {area_escolhida}", True, PRETO), (20, 20))
        tela.blit(fonte.render(f"Desempenho: {pontos_trabalho} pts", True, PRETO), (20, 50))
        
        if estado_atual == "FABRICA" or (estado_atual == "ANIMACAO_FINAL" and animacao_etapa <= 2):
            jogador.desenhar(tela, camera_x)
        
    elif estado_atual == "VITORIA":
        tela.fill((50, 150, 50))
        titulo_vitoria = fonte_titulo.render("PARABÉNS! PROMOVIDO!", True, BRANCO)
        texto_pontos = fonte.render(f"Desempenho Total: {pontos_trabalho} pts", True, BRANCO)
        instrucao_vitoria = fonte.render("Pressione [ M ] para escolher outro departamento", True, (255, 215, 0))
        tela.blit(titulo_vitoria, (LARGURA // 2 - titulo_vitoria.get_width() // 2, 200))
        tela.blit(texto_pontos, (LARGURA // 2 - texto_pontos.get_width() // 2, 270))
        tela.blit(instrucao_vitoria, (LARGURA // 2 - instrucao_vitoria.get_width() // 2, 350))

    elif estado_atual == "GAME_OVER":
        tela.fill((150, 50, 50))
        titulo_go = fonte_titulo.render("DEMITIDO!", True, BRANCO)
        texto_motivo = fonte.render("Você caiu ou levou Justa Causa.", True, BRANCO)
        instrucao_go1 = fonte.render("Pressione [ ENTER ] para tentar esta fase novamente", True, BRANCO)
        instrucao_go2 = fonte.render("Pressione [ M ] para voltar à escolha de portas", True, (255, 215, 0))
        tela.blit(titulo_go, (LARGURA // 2 - titulo_go.get_width() // 2, 180))
        tela.blit(texto_motivo, (LARGURA // 2 - texto_motivo.get_width() // 2, 240))
        tela.blit(instrucao_go1, (LARGURA // 2 - instrucao_go1.get_width() // 2, 320))
        tela.blit(instrucao_go2, (LARGURA // 2 - instrucao_go2.get_width() // 2, 370))

    pygame.display.flip()

pygame.quit()
sys.exit()