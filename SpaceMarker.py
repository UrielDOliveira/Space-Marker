import pygame
from tkinter import simpledialog
import pickle
from arquivo import carregar_imagem


pygame.init()

largura = 1280
altura = 720
janela = pygame.display.set_mode((largura, altura))
icone = pygame.image.load('space.png')
fundo = None
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
musica = pygame.mixer.music.load("Musica.mp3")
fonte = pygame.font.Font(None, 24)
estrelas = []

pygame.display.set_caption("Marcador de Estrelas")
pygame.mixer.init()
pygame.mixer.music.play(-1)
pygame.display.set_icon(icone)

def desenhar_linhas():
    for i in range(len(estrelas) - 1):
        ponto1 = estrelas[i]['pos']
        ponto2 = estrelas[i + 1]['pos']
        pygame.draw.line(janela, BRANCO, ponto1, ponto2, 2)

def salvar_marcacoes():
    with open("marcacoes.pkl", "wb") as arquivo:
        pickle.dump(estrelas, arquivo)
    print("Marcações salvas com sucesso!")

def carregar_marcacoes():
    try:
        with open("marcacoes.pkl", "rb") as arquivo:
            estrelas.extend(pickle.load(arquivo))
        print("Marcações carregadas com sucesso!")
    except FileNotFoundError:
        print("Não há marcações salvas.")

def excluir_marcacoes():
    estrelas.clear()
    print("Todas as marcações foram excluídas.")

try:
    fundo = carregar_imagem("fundo.jpg")
except FileNotFoundError:
    print("Erro ao carregar a imagem de fundo.")

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif evento.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            nome = simpledialog.askstring("Space", "Nome da Estrela") or "desconhecido"
            estrela = {'nome': nome, 'pos': pos}
            estrelas.append(estrela)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif evento.key == pygame.K_F10:
                salvar_marcacoes()
            elif evento.key == pygame.K_F11:
                carregar_marcacoes()
            elif evento.key == pygame.K_F12:
                excluir_marcacoes()

    janela.fill(PRETO)

    if fundo:
        janela.blit(fundo, (0, 0))  # Desenha a imagem de fundo

    desenhar_linhas()

    for estrela in estrelas:
        pygame.draw.circle(janela, BRANCO, estrela['pos'], 10)
        texto = f"{estrela['nome']} ({estrela['pos'][0]}, {estrela['pos'][1]})"
        texto_surface = fonte.render(texto, True, BRANCO)
        posicao_texto = texto_surface.get_rect(center=(estrela['pos'][0], estrela['pos'][1] - 20))
        janela.blit(texto_surface, posicao_texto)  # Desenha o nome da estrela

    texto_salvar = fonte.render("F10 - Salvar marcações", True, BRANCO)
    texto_carregar = fonte.render("F11 - Carregar marcações", True, BRANCO)
    texto_excluir = fonte.render("F12 - Excluir marcações", True, BRANCO)

    janela.blit(texto_salvar, (10, 10))
    janela.blit(texto_carregar, (10, 40))
    janela.blit(texto_excluir, (10, 70))

    pygame.display.update()
