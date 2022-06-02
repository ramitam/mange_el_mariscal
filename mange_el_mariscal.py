import pygame
import random
import math
from pygame import mixer

# inicializar pygame
pygame.init()

#crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

#título e ícono
pygame.display.set_caption('LA NAVE DE MANGE XD')
icono = pygame.image.load('jugador-de-futbol-americano (2).png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('fondo.jpg')

#agregar musica
mixer.music.load('musica_fondo.flac')
mixer.music.set_volume(0.05)
mixer.music.play(-1)

#variables del mangesito
img_jugador = pygame.image.load('american-football.png')
jugador_x = 368
jugador_y = 525
jugador_x_cambio = 0

#variables de los otros jugadores
img_companiero = []
companiero_x = []
companiero_y = []
companiero_x_cambio = []
companiero_y_cambio = []
cantidad_companieros = 8

for e in range(cantidad_companieros):
    img_companiero.append(pygame.image.load('el-jugador-de-rugby.png'))
    companiero_x.append(random.randint(0, 736))
    companiero_y.append(random.randint(50, 200))
    companiero_x_cambio.append(0.3)
    companiero_y_cambio.append(50)

#variables de la pelota
img_pelota = pygame.image.load('pelota-de-rugby.png')
pelota_x = 0
pelota_y = 525
pelota_x_cambio = 0
pelota_y_cambio = 1
pelota_visible = False

#puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

#texto fin del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_fuente_final = fuente_final.render('PERDISTE GUACHIN \# GAMEDAYBRO', True, (0, 0, 0))
    pantalla.blit(mi_fuente_final,(14,200))

#funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Pases completados: {puntaje}', True, (0, 0, 0))
    pantalla.blit(texto, (x, y))

#funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

#funcion companiero
def companiero(x, y, ene):
    pantalla.blit(img_companiero[ene], (x, y))

#funcion pasar la pelota
def pasar_pelota(x, y):
    global pelota_visible
    pelota_visible = True
    pantalla.blit(img_pelota, (x + 32, y + 20))
    #revisar valores!!

#funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    d = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if d < 30:
        return True
    else:
        return False


#loop del juego
se_ejecuta = True
while se_ejecuta:
    #imagen de fondo:
    pantalla.blit(fondo, (0,0))

    #acá se van iterando todos los eventos
    for evento in pygame.event.get():
        #evento para cerrar el juego
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        #evento cuando se presiona una tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                jugador_x_cambio = -0.3
            if evento.key == pygame.K_d:
                jugador_x_cambio = 0.3
            if evento.key == pygame.K_SPACE:
                jugador_x_cambio = 0
            if evento.key == pygame.K_p:
                sonido_pase = mixer.Sound('tiro.mp3')
                sonido_pase.play()
                if not pelota_visible:
                    pelota_x = jugador_x
                    pasar_pelota(pelota_x, pelota_y)

    #modificar la ubicación de mange
    jugador_x += jugador_x_cambio

    #mantener a mange dentro de los bordes
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # modificar la ubicación de los compañeros
    for e in range(cantidad_companieros):

        #fin del juego
        if companiero_y[e] > 450:
            for k in range(cantidad_companieros):
                companiero_y[k] = 1000
            texto_final()
            break

        companiero_x[e] += companiero_x_cambio[e]

        # mantener a los compañeros dentro de los bordes
        if companiero_x[e] <= 0:
            companiero_x_cambio[e] = 0.3
            companiero_y[e] += companiero_y_cambio[e]
        elif companiero_x[e] >= 736:
            companiero_x_cambio[e] = -0.3
            companiero_y[e] += companiero_y_cambio[e]
        # colision
        colision = hay_colision(companiero_x[e], companiero_y[e], pelota_x, pelota_y)
        if colision:
            sonido_colision = mixer.Sound('atrapo.mp3')
            sonido_colision.play()
            pelota_y = 525
            pelota_visible = False
            puntaje += 1
            companiero_x[e] = random.randint(0, 736)
            companiero_y[e] = random.randint(50, 200)

        companiero(companiero_x[e], companiero_y[e], e)
    #movimiento de la pelota
    if pelota_y <= -64:
        pelota_y = 500
        pelota_visible = False
    if pelota_visible:
        pasar_pelota(pelota_x, pelota_y)
        pelota_y -= pelota_y_cambio

    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)

    #esto va actualizando mi programa, por cada vuelta de loop va cambiando las cosas. ideal ponerlo al final.
    pygame.display.update()
