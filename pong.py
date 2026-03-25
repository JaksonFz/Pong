import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

largura = 800
altura = 600


class Audio:
    def __init__(self):
        self.hit_paddle = pygame.mixer.Sound("assets/Paddle.wav")
        self.hit_wall = pygame.mixer.Sound("assets/Hall.wav")
        self.score = pygame.mixer.Sound("assets/Score.wav")
        pygame.mixer.music.load("assets/Soundtrack.wav")
        pygame.mixer.music.set_volume(0.5)

    def play_music(self):
        pygame.mixer.music.play(-1)

    def play_hit_paddle(self):
        self.hit_paddle.play()

    def play_hit_wall(self):
        self.hit_wall.play()

    def play_score(self):
        self.score.play()


class Menu:
    def __init__(self, tela):
        self.tela = tela

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        return True

            self.tela.fill(PRETO)

            font = pygame.font.SysFont(None, 50)
            text = font.render("Pong", True, BRANCO)
            text_rect = text.get_rect(center=(largura // 2, altura // 4 + 50))
            self.tela.blit(text, text_rect)

            font_blynk = pygame.font.SysFont(None, 26)
            tempo = pygame.time.get_ticks()

            if tempo % 2000 < 1000:
                text_blynk = font_blynk.render("Pressione Espaço para Jogar", True, BRANCO)
                text_blynk_rect = text_blynk.get_rect(center=(largura // 2, altura // 2 + 60))
                self.tela.blit(text_blynk, text_blynk_rect)

            pygame.display.flip()


class Paddle:
    def __init__(self, x, y, largura_r, altura_r):
        self.x = x
        self.y = y
        self.largura = largura_r
        self.altura = altura_r

    def rect(self):
        return pygame.Rect(self.x, self.y, self.largura, self.altura)

    def mover_player(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.y > 0:
            self.y -= 5

        if keys[pygame.K_DOWN] and self.y < altura - self.altura:
            self.y += 5

    def mover_cpu(self, bola_y):
        if self.y + self.altura // 2 < bola_y:
            self.y += 5
        elif self.y + self.altura // 2 > bola_y:
            self.y -= 5

        if self.y < 0:
            self.y = 0
        elif self.y > altura - self.altura:
            self.y = altura - self.altura

    def desenhar(self, tela):
        pygame.draw.rect(tela, BRANCO, (self.x, self.y, self.largura, self.altura))


class Ball:
    def __init__(self, tamanho, verdadeira=True):
        self.tamanho = tamanho
        self.verdadeira = verdadeira
        self.cor = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )
        self.reset()

    def velocidade_inicial(self):
        vx = random.randint(-1, 1)
        vy = random.randint(-1, 1)
        while vx == 0 and vy == 0:
            vx = random.randint(-1, 1)
            vy = random.randint(-1, 1)
        return vx * 5, vy * 5

    def rect(self):
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)

    def atualizar(self, audio):
        self.x += self.vel_x
        self.y += self.vel_y

        if self.y <= 0:
            self.vel_x = random.choice([-1, 1]) * 5
            self.vel_y = random.randint(0, 1) * 5
            audio.play_hit_wall()

        if self.y >= altura - self.tamanho:
            self.vel_x = random.choice([-1, 1]) * 5
            self.vel_y = random.randint(-1, 0) * 5
            audio.play_hit_wall()

    def colidir(self, p1, p2, audio):
        if self.rect().colliderect(p1.rect()):
            self.vel_x = random.randint(1, 1) * 5
            self.vel_y = random.randint(-1, 1) * 5
            audio.play_hit_paddle()
            return True

        if self.rect().colliderect(p2.rect()):
            self.vel_x = random.randint(-1, -1) * 5
            self.vel_y = random.randint(-1, 1) * 5
            audio.play_hit_paddle()
            return True

        return False

    def reset(self):
        self.x = largura // 2 - self.tamanho // 2
        self.y = altura // 2 - self.tamanho // 2
        self.vel_x, self.vel_y = self.velocidade_inicial()

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.tamanho)


class Score:
    def __init__(self):
        self.player1 = 0
        self.player2 = 0

    def ponto_p1(self):
        self.player1 += 1
        if self.player1 >= 10:
            return True
        return False

    def ponto_p2(self):
        self.player2 += 1
        if self.player2 >= 10:
            return True
        return False

    def desenhar(self, tela):
        font_score = pygame.font.SysFont(None, 36)
        score_text = font_score.render(f"{self.player1}  -  {self.player2}", True, BRANCO)
        tela.blit(score_text, score_text.get_rect(center=(largura // 2, 30)))


class Game:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock()

        self.audio = Audio()
        self.audio.play_music()

        raquete_largura = 10
        raquete_altura = 60
        tamanho_bola = 7

        self.player1 = Paddle(15, altura / 2 - raquete_altura // 2, raquete_largura, raquete_altura)
        self.player2 = Paddle(largura - 15 - raquete_largura, altura / 2 - raquete_altura // 2, raquete_largura, raquete_altura)

        self.bolas = [Ball(tamanho_bola, verdadeira=True)]
        self.tempo_ultimo_spawn = pygame.time.get_ticks()
        self.score = Score()

    def reset_bolas(self):
        self.bolas = [Ball(7, verdadeira=True)]
        self.tempo_ultimo_spawn = pygame.time.get_ticks()

    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return True

            self.tela.fill(PRETO)

            tempo_atual = pygame.time.get_ticks()
            novas_bolas = []

            for bola in self.bolas:
                bola.atualizar(self.audio)
                colidiu = bola.colidir(self.player1, self.player2, self.audio)

                if colidiu and tempo_atual - self.tempo_ultimo_spawn >= 5000:
                    self.tempo_ultimo_spawn = tempo_atual
                    for _ in range(3):
                        nova = Ball(bola.tamanho, verdadeira=False)
                        nova.x = bola.x
                        nova.y = bola.y
                        novas_bolas.append(nova)

                if bola.verdadeira:
                    if bola.x <= 0:
                        self.audio.play_score()
                        if self.score.ponto_p2():
                            return True
                        self.reset_bolas()

                    if bola.x >= largura - bola.tamanho:
                        self.audio.play_score()
                        if self.score.ponto_p1():
                            return True
                        self.reset_bolas()

            self.bolas.extend(novas_bolas)

            self.player1.mover_player()

            if self.bolas:
                self.player2.mover_cpu(self.bolas[0].y)

            self.player1.desenhar(self.tela)
            self.player2.desenhar(self.tela)

            for bola in self.bolas:
                bola.desenhar(self.tela)

            self.score.desenhar(self.tela)

            pygame.display.flip()
            self.clock.tick(60)


class App:
    def __init__(self):
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Pong")

    def executar(self):
        menu = Menu(self.tela)

        while True:
            if not menu.executar():
                break

            game = Game(self.tela)
            if not game.executar():
                break

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    App().executar()