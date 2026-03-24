# Pong em Python com Pygame

## Descrição

Este projeto consiste em uma implementação simples do jogo Pong utilizando a biblioteca Pygame em Python. O jogo possui dois jogadores:

* Player 1 controlado pelo teclado
* Player 2 controlado por uma inteligência simples que segue a bola

A partida termina quando um dos jogadores alcança 10 pontos.

---

## Tecnologias utilizadas

* Python
* Pygame

Para instalar o Pygame:

```
pip install pygame
```

---

## Como executar

1. Clone ou baixe o repositório.
2. Instale a biblioteca pygame.
3. Execute o arquivo principal.

```
python main.py
```

Ao iniciar o programa, um menu será exibido. Pressione a tecla **Espaço** para começar o jogo.

---

## Controles

Player 1:

* Seta para cima: mover a raquete para cima
* Seta para baixo: mover a raquete para baixo

Player 2:

* Controlado automaticamente pelo jogo.

---

# Estrutura do Código

O projeto foi organizado em classes, cada uma responsável por uma parte específica do jogo.

## Classe Menu

Responsável por exibir o menu inicial e aguardar o jogador iniciar a partida.

Trecho principal:

```
class Menu:
    def executar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        return True
```

Neste trecho o programa verifica se a tecla **Espaço** foi pressionada. Quando isso ocorre, o jogo principal é iniciado.

---

## Classe Paddle

Representa as raquetes dos jogadores.

Trecho responsável pela criação da raquete:

```
class Paddle:
    def __init__(self, x, y, largura_r, altura_r):
        self.x = x
        self.y = y
        self.largura = largura_r
        self.altura = altura_r
```

Esses valores definem a posição inicial e o tamanho da raquete dentro da tela.

Movimentação do jogador:

```
def mover_player(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and self.y > 0:
        self.y -= 5

    if keys[pygame.K_DOWN] and self.y < altura - self.altura:
        self.y += 5
```

O método verifica se as teclas direcionais estão pressionadas e altera a posição da raquete.

---

## Classe Ball

Responsável pela bola do jogo, incluindo movimento e colisões.

Movimento da bola:

```
def atualizar(self):
    self.x += self.vel_x
    self.y += self.vel_y
```

A cada frame a posição da bola é atualizada de acordo com sua velocidade.

Colisão com as raquetes:

```
def colidir(self, p1, p2):
    if self.rect().colliderect(p1.rect()) or self.rect().colliderect(p2.rect()):
        self.vel_x = -self.vel_x
```

Quando a bola colide com uma das raquetes, a direção horizontal é invertida.

---

## Classe Score

Controla a pontuação da partida.

Trecho responsável por adicionar ponto ao jogador:

```
def ponto_p1(self):
    self.player1 += 1
```

Sempre que a bola ultrapassa o lado direito da tela, o Player 1 recebe um ponto.

Quando um jogador atinge 10 pontos, o jogo termina.

---

## Classe Game

Responsável pelo loop principal do jogo.

Trecho do loop:

```
while True:
    self.bola.atualizar()
    self.bola.colidir(self.player1, self.player2)
```

Neste trecho a bola é movimentada e as colisões são verificadas a cada frame do jogo.

Também são atualizados:

* movimentação das raquetes
* pontuação
* renderização dos objetos na tela

---

## Classe App

Responsável por iniciar o programa e controlar a execução geral.

Trecho principal:

```
if __name__ == "__main__":
    App().executar()
```

Esse bloco garante que o jogo será iniciado apenas quando o arquivo for executado diretamente.