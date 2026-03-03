import pygame
import sys
import random

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Janela')

PRETO = (0, 0, 0)

def cor_aleatoria():
    return (
        random.randint(1, 255),
        random.randint(1, 255),
        random.randint(1, 255)
    )

def velocidade_inicial():
    vx = random.randint(-1, 1)
    vy = random.randint(-1, 1)
    while vx == 0 and vy == 0:
        vx = random.randint(-1, 1)
        vy = random.randint(-1, 1)
    return vx, vy

def mover(rect, velocidade_x, velocidade_y, cor):
    rect.x += velocidade_x
    rect.y += velocidade_y

    if rect.right >= largura:
        velocidade_x = random.randint(-1, 0)
        velocidade_y = random.randint(-1, 1)
        cor = cor_aleatoria()

    if rect.left <= 0:
        velocidade_x = random.randint(0, 1)
        velocidade_y = random.randint(-1, 1)
        cor = cor_aleatoria()

    if rect.bottom >= altura:
        velocidade_x = random.randint(-1, 1)
        velocidade_y = random.randint(-1, 0)
        cor = cor_aleatoria()

    if rect.top <= 0:
        velocidade_x = random.randint(-1, 1)
        velocidade_y = random.randint(0, 1)
        cor = cor_aleatoria()

    return velocidade_x, velocidade_y, cor

tamanho_fonte = 50
fonte = pygame.font.SysFont(None, tamanho_fonte)

cor1 = cor_aleatoria()
cor2 = cor_aleatoria()

texto1 = fonte.render("Objeto01", True, cor1)
texto2 = fonte.render("Objeto02", True, cor2)

texto_rect1 = texto1.get_rect(center=(largura / 3, altura / 2))
texto_rect2 = texto2.get_rect(center=(largura / 1.5, altura / 2))

velocidade_x1, velocidade_y1 = velocidade_inicial()
velocidade_x2, velocidade_y2 = velocidade_inicial()

clock = pygame.time.Clock()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill(PRETO)

    velocidade_x1, velocidade_y1, cor1 = mover(
        texto_rect1, velocidade_x1, velocidade_y1, cor1
    )

    velocidade_x2, velocidade_y2, cor2 = mover(
        texto_rect2, velocidade_x2, velocidade_y2, cor2
    )

    if texto_rect1.colliderect(texto_rect2):

        if texto_rect1.centerx < texto_rect2.centerx:
            texto_rect1.x -= 5
            texto_rect2.x += 5
        else:
            texto_rect1.x += 5
            texto_rect2.x -= 5

        if texto_rect1.centery < texto_rect2.centery:
            texto_rect1.y -= 5
            texto_rect2.y += 5
        else:
            texto_rect1.y += 5
            texto_rect2.y -= 5

        velocidade_x1, velocidade_y1 = velocidade_inicial()
        velocidade_x2, velocidade_y2 = velocidade_inicial()

        cor1 = cor_aleatoria()
        cor2 = cor_aleatoria()

    texto1 = fonte.render("Objeto01", True, cor1)
    texto2 = fonte.render("Objeto02", True, cor2)

    tela.blit(texto1, texto_rect1)
    tela.blit(texto2, texto_rect2)

    clock.tick(240)
    pygame.display.flip()

pygame.quit()
sys.exit()