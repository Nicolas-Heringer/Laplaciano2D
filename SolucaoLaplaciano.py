import pygame
import sys
import numpy as np
import math

# Inicializa o Pygame
pygame.init()

# Configurações iniciais
largura_tela = 800
altura_tela = 800
L = 8  # Tamanho do lado dos retângulos

# Mapeamento de temperatura para cor (degradê de azul a vermelho)
def temperatura_para_cor(temperatura):
    # Use max e min para garantir que a temperatura esteja no intervalo [0, 255]
    temperatura = max(0, min(255, temperatura))
    # Mapeia a temperatura para uma cor de azul (0, 0, 255) a vermelho (255, 0, 0)
    return (255-temperatura, 255-temperatura, 255-temperatura)

def temperatura_para_cor_curva(temperatura, expoente=1):
    # Normaliza a temperatura para o intervalo [0, 1]
    temperatura_normalizada = max(0, min(1, temperatura / 1000))
    
    # Mapeia a temperatura usando uma função exponencial
    componente_vermelha = int(255 * math.exp(-expoente * temperatura_normalizada))
    
    # Componentes verde e azul são inversamente proporcionais à componente vermelha
    componente_verde = 255 - componente_vermelha
    componente_azul = 255 - componente_vermelha
    
    return (componente_vermelha, componente_verde, componente_azul)

# Função de diferenças finitas modificada para atualizar diretamente os valores de temperatura
temperatura_fixa_borda = 0
def avancar(temperaturas, temperaturas_n, temperaturas_n_m1, f, c, dx, dy, dt):
    # Calcula os coeficientes Cx e Cy
    Cx2 = (c*dt/dx)**2
    Cy2 = (c*dt/dy)**2
    
    # Percorre os pontos internos da malha
    for i in range(1, len(temperaturas)-1):
        for j in range(1, len(temperaturas[0])-1):
            # Verifica se o ponto está na borda
            if i == 0 or i == len(temperaturas) - 1 or j == 0 or j == len(temperaturas[0]) - 1:
                # Mantém a temperatura fixa na borda (você pode ajustar o valor conforme necessário)
                temperaturas[i][j] = temperatura_fixa_borda
            else:
                # Calcula as segundas derivadas parciais em x e y
                u_xx = temperaturas_n[i-1][j] - 2*temperaturas_n[i][j] + temperaturas_n[i+1][j]
                u_yy = temperaturas_n[i][j-1] - 2*temperaturas_n[i][j] + temperaturas_n[i][j+1]
                
                # Aplica a fórmula de diferenças finitas
                temperaturas[i][j] = -temperaturas_n_m1[i][j] + 2*temperaturas_n[i][j] + Cx2*u_xx + Cy2*u_yy + dt**2*f(i,j)

# Encontrar o lado menor da tela
lado_menor = min(largura_tela, altura_tela)

# Calcular o número de linhas e colunas com base no lado menor
num_linhas = lado_menor // L
num_colunas = lado_menor // L

# Centralizar o grid na tela
margem_x = (largura_tela - num_colunas * L) // 2
margem_y = (altura_tela - num_linhas * L) // 2

# Inicializa as temperaturas das células como 0
temperaturas_n_m1 = [[0] * num_colunas for _ in range(num_linhas)]
temperaturas_n = [[0] * num_colunas for _ in range(num_linhas)]
temperaturas_n_p1 = [[0] * num_colunas for _ in range(num_linhas)]

# Configurações da janela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Grid 2D')

# Loop principal
while True:
    for evento in pygame.event.get():
    
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Obtém as coordenadas do mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Calcula a célula correspondente às coordenadas do mouse
            celula_x = (mouse_x - margem_x) // L
            celula_y = (mouse_y - margem_y) // L

            # Incrementa a temperatura da célula clicada
            temperaturas_n[celula_y][celula_x] = 100

    # Aplica o algoritmo de diferenças finitas para avançar no tempo
    avancar(temperaturas_n_p1, temperaturas_n, temperaturas_n_m1, 
            lambda i, j: 0,  # Função de fonte (por enquanto, zero)
            c=1, dx=1, dy=1, dt=0.1)

    # Atualiza os arrays temporais
    temperaturas_n_m1, temperaturas_n, temperaturas_n_p1 = temperaturas_n, temperaturas_n_p1, temperaturas_n_m1

    # Preenche a tela com uma cor de fundo
    tela.fill((20, 20, 20))

    # Desenha o grid 2D
    for linha in range(num_linhas):
        for coluna in range(num_colunas):
            x = margem_x + coluna * L
            y = margem_y + linha * L

            # Obtém a cor com base na temperatura da célula
            cor_celula = temperatura_para_cor(temperaturas_n[linha][coluna])

            pygame.draw.rect(tela, cor_celula, (x, y, L, L), 0)

    pygame.display.flip()
