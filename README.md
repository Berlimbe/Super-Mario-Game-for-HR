# Jogo de Plataforma Corporativo (Estilo Mario)

## Sobre o Projeto#
Jogo de plataforma 2D estilo Super Mario desenvolvido para a disciplina de Rotinas de Pessoal II. Com artes originais feitas inteiramente à mão, o jogo leva o colaborador por uma jornada através dos diferentes setores da empresa, desviando de perigos corporativos e obstáculos clássicos em busca da maior pontuação possível.

## Áreas e Desafios#
O jogador percorre quatro grandes setores da organização:
Qualidade
Manutenção
Site

## RH (Recursos Humanos)#
Inimigos e Obstáculos pelo Caminho:
Inimigo "Careca Barrigudo": Ronda os setores e exige saltos precisos para ser evitado.
Buracos: Exigem atenção no tempo de pulo para não cair.
Canos e Flores: Obstáculos clássicos de plataforma adaptados ao cenário artesanal do jogo.

## Tecnologias e Estrutura#
O projeto foi construído em Python com arquitetura modular:
pygame: Motor principal responsável pela física de plataforma, colisões, renderização de sprites, áudio e controle de pontuação.
sys e os: Gerenciamento de caminhos de diretórios (carregamento seguro de assets/artes manuais em diferentes sistemas operacionais) e encerramento limpo do sistema.
configuracoes.py: Módulo dedicado (from configuracoes import *) contendo as constantes do jogo, como resolução de tela, taxa de quadros (FPS), física de gravidade e parâmetros das fases.

## Pré-requisitos e Instalação#
Para rodar o jogo, é necessário instalar a biblioteca pygame via pip:
Clone o repositório ou extraia os arquivos em uma pasta local:
```
git clone <url-do-repositorio>
cd <pasta-do-projeto>
```
Instale a dependência necessária no terminal:
```
pip install pygame
```
Inicie o jogo executando o script principal:
```
python main.py
```

Controles
```
Movimentação: A / D ou Setas Esquerda / Direita
Pular: Espaço / W / Seta para Cima
```
