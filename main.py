import sys
import math

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image


# Variaveis globais
global angulo, fAspect, rotX, rotY, rotZ, obsX, obsY, obsZ, solAtivo
global rotX_ini, rotY_ini, obsX_ini, obsY_ini, obsZ_ini, x_ini, y_ini, botao
global sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune

solAtivo = 1
orbita = 1
eixoX, eixoY, eixoZ = 0, 0, 0

SENS_ROT = 5.0

# Desenha planetas simples
cache = {}

texture_cache = {}
def load_texture(texture_path):
    if texture_path in texture_cache:
        return texture_cache[texture_path]

    # Abre a imagem usando PIL
    image = Image.open(texture_path)

    # Redimensiona a imagem apenas se não estiver no cache
    image.thumbnail((200, 200))  # Redimensiona a imagem para um tamanho máximo de 512x512
    image = image.convert("RGBA")

    # Obtém os dados da imagem
    image_data = image.tobytes("raw", "RGBA", 0, -1)

    # Gera uma textura OpenGL
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Define os parâmetros de textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Carrega os dados da imagem para a textura OpenGL
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    # Armazena a textura em cache
    texture_cache[texture_path] = texture_id

    return texture_id


def calcular_posicoes(a, raio):
    if (a, raio) in cache:
        return cache[(a, raio)]

    cos_a = math.cos(2.0 * math.pi * a * raio / 100)
    sin_a = math.sin(2.0 * math.pi * a * raio / 100)

    cache[(a, raio)] = (cos_a, sin_a)
    return cos_a, sin_a

def Desenha_planeta(pos_y, pos_x, escala, diametro, raio, texture_path):
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    a = t * 2

    cos_a, sin_a = calcular_posicoes(a, raio)

    glPushMatrix()
    glRasterPos2f(0, -pos_y)
    glTranslated(0, -pos_y, 0)
    glTranslatef((pos_x * cos_a), (pos_y + pos_y * sin_a), 0)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, load_texture(texture_path))  # Carrega a textura
    obj = gluNewQuadric()

    glScalef(escala, escala, escala)
    glRotated(a * 20, 0, 0, 1)

    # Defina coordenadas de textura (pode precisar ajustar)
    gluQuadricTexture(obj, GL_TRUE)

    gluSphere(obj, diametro, 25, 25)

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()


# Desenha planetas com satélites e aneis, como é o caso de Jupter


def Desenha_planetas_com_Satelites_e_Aneis(pos_y, pos_x, escala, diametro1, diametro2, raio, raio_lua, texture_path_planeta=None, texture_path_satelite=None, corAnel=[1.0, 1.0, 1.0]):
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    a = t * 2

    cos_raio, sin_raio = calcular_posicoes(a, raio)
    cos_raio_lua, sin_raio_lua = calcular_posicoes(a, raio_lua)

    glPushMatrix()
    glRasterPos2f(0, -pos_y)
    glTranslated(0, -pos_y, 0)
    glTranslatef(pos_x * cos_raio, pos_y + pos_y * sin_raio, 0)
    obj = gluNewQuadric()

    # Desenha o planeta
    if texture_path_planeta:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, load_texture(texture_path_planeta))
        glScalef(escala, escala, escala)
        glRotated(a * 20, 0, 0, 1)
        gluQuadricTexture(obj, GL_TRUE)
        gluSphere(obj, diametro1, 25, 25)
        glDisable(GL_TEXTURE_2D)
    else:
        glColor3f(1.0, 1.0, 1.0)
        glScalef(escala, escala, escala)
        glRotated(a * 20, 0, 0, 1)
        gluSphere(obj, diametro1, 25, 25)

    # Desenha o anel
    glColor3f(corAnel[0], corAnel[1], corAnel[2])
    desenhaAnel(pos_x / 60, pos_y / 60)

    # Desenha o satélite
    if texture_path_satelite:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, load_texture(texture_path_satelite))
        glTranslatef(pos_x / 10 * cos_raio_lua, pos_y / 10 * sin_raio_lua, 0)
        glColor3f(1.0, 1.0, 1.0)
        glScalef(escala, escala, escala)
        glRotated(a * 5, 1, 0, 1)
        gluQuadricTexture(obj, GL_TRUE)
        gluSphere(obj, diametro2, 50, 50)
        glDisable(GL_TEXTURE_2D)
    else:
        glTranslatef(pos_x / 10 * cos_raio_lua, pos_y / 10 * sin_raio_lua, 0)
        glColor3f(1.0, 1.0, 1.0)
        glScalef(escala, escala, escala)
        glRotated(a * 5, 1, 0, 1)
        gluSphere(obj, diametro2, 50, 50)

    glPopMatrix()


# Desenha planetas capenas com satélite, que é o caso da Terra

def desenha_planetas_com_Satelites(pos_y, pos_x, escala, diametro1, diametro2, raio, raio_lua, texture_path, textura_satelite):
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    a = t * 2

    cos_raio, sin_raio = calcular_posicoes(a, raio)
    cos_raio_lua, sin_raio_lua = calcular_posicoes(a, raio_lua)

    glPushMatrix()
    glRasterPos2f(0, -pos_y)
    glTranslated(0, -pos_y, 0)
    glTranslatef(pos_x * cos_raio, pos_y + pos_y * sin_raio, 0)

    # Desenha o planeta se o caminho da textura for fornecido
    if texture_path:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, load_texture(texture_path))
        obj = gluNewQuadric()
        glScalef(escala, escala, escala)
        glRotated(a * 20, 0, 0, 1)
        gluQuadricTexture(obj, GL_TRUE)
        gluSphere(obj, diametro1, 25, 25)
        glDisable(GL_TEXTURE_2D)

    # Desenha o satélite se o caminho da textura for fornecido
    if textura_satelite:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, load_texture(textura_satelite))
        glTranslatef(pos_x / 10 * cos_raio_lua, pos_y / 10 * sin_raio_lua, 0)
        glColor3f(1.0, 1.0, 1.0)
        glScalef(escala, escala, escala)
        glRotated(a * 5, 1, 0, 1)
        gluQuadricTexture(obj, GL_TRUE)
        gluSphere(obj, diametro2, 50, 50)
        glDisable(GL_TEXTURE_2D)

    glPopMatrix()




def desenhaAnel(eixoX, eixoY):
    glPushMatrix()
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        rad = i * 3.14 / 180
        glVertex2f(math.cos(rad) * eixoX, math.sin(rad) * eixoY)
    glEnd()
    glPopMatrix()

# Desenha o sistema solar e as orbitas dos planetas
    

"""
def Desenha_planeta_com_nome(pos_y, pos_x, escala, diametro, raio, texture_path, nome_planeta):
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    a = t * 2

    cos_a, sin_a = calcular_posicoes(a, raio)

    glPushMatrix()
    glRasterPos2f(0, -pos_y)
    glTranslated(0, -pos_y, 0)
    glTranslatef((pos_x * cos_a), (pos_y + pos_y * sin_a), 0)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, load_texture(texture_path))  # Carrega a textura
    obj = gluNewQuadric()

    glScalef(escala, escala, escala)
    glRotated(a * 20, 0, 0, 1)

    # Defina coordenadas de textura (pode precisar ajustar)
    gluQuadricTexture(obj, GL_TRUE)

    gluSphere(obj, diametro, 25, 25)

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    # Renderiza o nome do planeta abaixo dele
    planet_x = (pos_x * cos_a)
    planet_y = (pos_y + pos_y * sin_a)
    text_x = planet_x - len(nome_planeta) * 0.015  # Ajuste fino para alinhar o texto
    text_y = planet_y - 0.3  # Distância fixa abaixo do planeta
    glPushMatrix()
    glRasterPos2f(text_x, text_y)
    for char in nome_planeta:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(char))
    glPopMatrix()
    """


def Sistema_Solar():
    global mercury_texture_id, venus_texture_id

    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    a = t
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # SOL



    light_ambient = [0.5, 0.5, 0.5, 1.0]  # Luz ambiente branca
    light_diffuse = [0.7, 0.7, 0.7, 1.0]  # Luz difusa branca
    light_specular = [1.0, 1.0, 1.0, 1.0]  # Luz especular branca
    light_position = [1.0, 0.0, 5.0, 1.0]

    mat_ambient = [0.7, 0.7, 0.7, 1.0]
    mat_diffuse = [0.8, 0.8, 0.8, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    high_shininess = [10.0]

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glPushMatrix()
    glRasterPos2f(0, 1.5)
    qobj = gluNewQuadric()
    glEnable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 0.5)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, high_shininess)
    glRotated(a * 7, 0, 0, 1)
    # glScalef(3, 3, 3)
    gluSphere(qobj, 1, 25, 25)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    glDisable(GL_LIGHTING)
    Desenha_planeta(0, 0, 10, 0.48, 3.7, "sol.jpg")
    glEnable(GL_LIGHTING)
    # MERCURIO - Diametro: 4.879,4 km
    Desenha_planeta(7, 7, 2, 0.48, 3.7, "mercurio.jpg")

    #
    # # # VENUS - Diametro: 12.103,6 km
    Desenha_planeta(17, 17, 1.2, 1.21, 2.5, "venus.jpg")
    #
    # # TERRA E LUA - Diametro Terra: 12.756,2 km
    desenha_planetas_com_Satelites(27, 27, 1.2, 1.27, 0.5, 1.9, 0.8, "terra.jpg", "lua.jpg")
    #
    # # MARTE - Diametro: 6.792,4 km
    Desenha_planeta(41, 41, 1.2, 0.68, 0.5, "marte.jpg")
    #
    # # JUPITER       */ #Diametro: 142.984 km
    Desenha_planetas_com_Satelites_e_Aneis(80, 80, 1.5, 1.43, 0.25, 1.9, 1, "jupiter.jpg", "europa.jpg", [0.41, 0.41, 0.41])
    #
    # # SATURNO     */ #Diametro: 120.536 km
    Desenha_planetas_com_Satelites_e_Aneis(97, 97, 1.5, 1.2, 0.25, 1.5, 1, "saturno.jpg", "titan.jpg", [0.41, 0.41, 0.41])
    #
    # # URANO   */ #Diametro: 51.118 km
    Desenha_planetas_com_Satelites_e_Aneis(107, 107, 1.5, 0.51, 0.25, 1.2, 1.3, "Urano.jpg", "Ariel.jpg", [0.41, 0.41, 0.41])
    #
    # # NETUNO   */  #Diametro: 49.528 km
    Desenha_planetas_com_Satelites_e_Aneis(127, 127, 1.5, 0.495, 0.20, 1, 1, "netuno.jpg", "tritao.jpg", [0.41, 0.41, 0.41])

    glDisable(GL_LIGHTING)  # Desabilita a iluminação
    glDisable(GL_LIGHT0)
    glRasterPos2f(0, -51)

# Cria uma orbita


def Desenha_Orbita(pos_y, pos_x):
    # Insere a matriz de transformacoes corrente na pilha para realizar as transformacoes
    # Serve para restringir o efeito das transformacoes ao escopo que desejamos ou lembrar da sequencia de transformacoes realizadas
    glPushMatrix()
    glTranslated(0, -pos_y, 0)  # Produz uma translacao em (x, y, z)
    # glBegin Inicia uma lista de vertices, e o argumento determina qual objeto sera desenhado
    # GL_LINE_LOOP exibe uma sequencia de linhas conectando os pontos definidos por glVertex e ao final liga o primeiro como ultimo ponto
    glBegin(GL_LINE_LOOP)
    for i in range(100):  # Desenha a linha da orbita, a variavel i vai juntando cada linha em uma circunferencia
        glVertex2f(
            pos_x * math.cos(2.0 * 3.14 * i / 100),
            pos_y + pos_y * math.sin(2.0 * 3.14 * i / 100)
        )  # Especifica um vertice

    glEnd()  # Fim do begin
    glPopMatrix()  # Fim do push

# Chama a funcao para criar as orbitas de cada planeta


def mostraOrbitas():

    # MERCURIO - Diametro: 4.879,4 km
    Desenha_Orbita(7, 7)

    # VENUS - Diametro: 12.103,6 km
    Desenha_Orbita(17, 17)

    # TERRA - Diametro: 12.756,2 km
    Desenha_Orbita(27, 27)

    # MARTE -Diametro: 6.792,4 km
    Desenha_Orbita(41, 41)

    # JUPITER - Diametro: 142.984 km
    Desenha_Orbita(80, 80)

    # SATURNO - Diametro: 120.536 km
    Desenha_Orbita(97, 97)

    # URANO -Diametro: 51.118 km
    Desenha_Orbita(107, 107)

    # NETUNO - Diametro: 49.528 km
    Desenha_Orbita(127, 127)


def DesenhaTexto(texto, x, y):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 600, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for char in texto:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)



def Sistema_Solar_com_orbitas():
    glDrawBuffer(GL_BACK)
    # Limpa a janela de visualização com a cor de fundo especificada
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Desenha todos os objetos do sistema solar e suas órbitas
    Sistema_Solar()
    mostraOrbitas()

    """ NÃO FUNCIONANDO -Desenha os nomes dos planetas
    Desenha_planeta_com_nome(7, 7, 2, 0.48, 3.7, "mercurio.jpg", "Mercurio")
    Desenha_planeta_com_nome(17, 17, 1.2, 1.21, 2.5, "venus.jpg", "Venus")
    Desenha_planeta_com_nome(27, 27, 1.2, 1.27, 1.9, "terra.jpg", "Terra")
    Desenha_planeta_com_nome(41, 41, 1.2, 0.68, 0.5, "marte.jpg", "Marte")
    Desenha_planeta_com_nome(80, 80, 1.5, 1.43, 1.9, "jupiter.jpg", "Jupiter")
    Desenha_planeta_com_nome(97, 97, 1.5, 1.2, 1.5, "saturno.jpg", "Saturno")
    Desenha_planeta_com_nome(107, 107, 1.5, 0.51, 1.2, "Urano.jpg", "Urano")
    Desenha_planeta_com_nome(127, 127, 1.5, 0.495, 1, "netuno.jpg", "Netuno")
    """
   
    DesenhaTexto("Universidade Federal do Agreste de Pernambuco - UFAPE", 10, 20)
    DesenhaTexto("Disciplina: Computação Gráfica 2023.1", 10, 35)
    DesenhaTexto("Docente: Ícaro Lins", 10, 50)
    DesenhaTexto("Discentes: David Lucas, Rian Wilker e Victor Winicius", 10, 65)
    
    glutSwapBuffers()


def atualiza():
    # Marca o plano normal da janela atual como precisando ser reexibido na proxima iteracao do glutMainLoop
    glutPostRedisplay()


def Inicializa():
    global angulo, rotX, rotY, rotZ, obsX, obsY, obsZ
    global sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune

    # Inicializa a variavel que especifica o angulo da projecao
    # perspectiva
    angulo = 30
    # Inicializa as variaveis usadas para alterar a posicao do
    # observador virtual
    rotX = 0
    rotY = 0
    rotZ = 0
    obsX = obsY = 0
    obsZ = 1000
    rotX = -5.6
    rotY = 5.6
    rotZ - 0
    # #Inicializa obj
    # inicializaObj()

    # Especificando que as facetas traseiras serao cortadas
    glEnable(GL_CULL_FACE)  # Habilita recursos do GL -> cortar as facetas
    glCullFace(GL_BACK)  # Nao mostrar faces do lado de dentro

    # Prepara o OpenGL para realizar calculos de iluminacao
    glEnable(GL_LIGHTING)
    # Especifica que a fonte de luz tem cor padrao para luz (branco)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)  # Atualiza o buffer de profundidade

# Passos padrao da biblioteca
# Especifica a posicao do observador e do alvo


def PosicionaObservador():
    # Especifica o sistema de coordenadas do modelo
    glMatrixMode(GL_MODELVIEW)
    # Inicializa sistema de coordenadas do modelo
    glLoadIdentity()

    # Posiciona e orienta o observador - transformacoes geometricas de translacao e rotacao em (eixoX, eixoY, eixoZ)
    glTranslatef(-obsX*0.5, -obsY*0.5, -obsZ*0.5)
    glRotatef(rotX, 1, 0, 0)
    glRotatef(rotY, 0, 1, 0)
    glRotatef(rotZ, 0, 0, 1)

# Funcao padrao da biblioteca para especificar o volume de visualizacao


def EspecificaParametrosVisualizacao():
    global angulo, fAspect
    # Especifica sistema de coordenadas de projecao
    # Aplica operações de matriz subsequentes à pilha da matriz de projeção.
    # prepara a matriz de projeção para receber novas multiplicações
    glMatrixMode(GL_PROJECTION)
    # Inicializa sistema de coordenadas de projecao
    glLoadIdentity()  # faz as multiplicações com base nas npvas modificações
    # Especifica a projecao perspectiva(angulo,aspecto,zMin,zMax)
    # A função gluPerspective especifica um frusto de exibição no sistema de coordenadas do mundo.
    # Em geral, a taxa de proporção em gluPerspective deve corresponder à taxa de proporção do visor associado.
    # Por exemplo, aspect = 2.0 significa que o ângulo de exibição do visualizador é duas vezes maior em x do que em y
    gluPerspective(angulo, fAspect, 0.5, 2000)
    # Especifica a posicao do observador e do alvo
    PosicionaObservador()

# Funcao padrao da biblioteca para alterar o tamanho da tela


def Redimensiona(w, h):
    global fAspect
    # Para previnir uma divisao por zero
    if (h == 0):
        h = 1

    # Especifica as dimensoes da viewport
    # o glViewport especifica a transformação afim de x e y de coordenadas de dispositivos normalizadas para coordenadas de janelas.
    # O OpenGL dimensionará automaticamente a renderização para que ela se encaixe no porta de exibição dada.
    # Faz o mesmo para o resto de seus viewports e no final você tem uma janela com poucas renderizações diferentes,
    # cada uma com seus próprios parâmetros. Desta forma, você pode ter quantas renderizações distintas em uma única janela/destino de renderização o que quiser
    glViewport(0, 0, w, h)
    # Calcula a correção de aspecto
    fAspect = w/h
    # Especifica o volume de visualizacao
    EspecificaParametrosVisualizacao()

# Funcoes para interagir com teclado e mouse


def SpecialKeyboard(tecla, x, y):
    global angulo
    if tecla == GLUT_KEY_RIGHT:
        glRotatef(1, 1, 0, 0)

    elif tecla == GLUT_KEY_LEFT:
        glRotatef(1, 0, 1, 0)

    elif tecla == GLUT_KEY_DOWN:
        if angulo <= 150:
            angulo += 5

    elif tecla == GLUT_KEY_UP:
        if angulo >= 10:
            angulo -= 5

    EspecificaParametrosVisualizacao()
    glutPostRedisplay()


# Gerencia os eventos do mouse, se botao foi pressionado ou nao


def GerenciaMouse(button, state, eixoX, eixoY):
    global obsX, obsY, obsZ, rotX, rotY, obsX_ini, obsY_ini, obsZ_ini, rotX_ini, rotY_ini, x_ini, y_ini, botao

    # Se foi pressionado, salva os parametros atuais
    if (state == GLUT_DOWN):
        x_ini = eixoX
        y_ini = eixoY
        obsX_ini = obsX
        obsY_ini = obsY
        obsZ_ini = obsZ
        rotX_ini = rotX
        rotY_ini = rotY
        botao = button
    else:
        botao = -1


def GerenciaMovimento(eixoX, eixoY):
    global x_ini, y_ini, rotX, rotY, obsX, obsY, obsZ

    # Botao esquerdo do mouse
    if (botao == GLUT_LEFT_BUTTON):
        # Calcula diferenças
        deltax = x_ini - eixoX
        deltay = y_ini - eixoY
        # E modifica angulos
        rotY = rotY_ini - deltax/SENS_ROT
        rotX = rotX_ini - deltay/SENS_ROT

    # Padrao da funcao, ja que altera a visualizacao (angulo ou distancia)
    PosicionaObservador()
    # Marca para exibir novamente o plano da janela atual na proxima iteracao do glutMainLoop
    # Marque o plano normal da janela atual como precisando ser reexibido. Na próxima iteração através do glutMainLoop,
    # o retorno de chamada de exibição da janela será chamado para reexibir o plano normal da janela
    glutPostRedisplay()


def main():
    # Inicializa a lib glut, com um contexto openGL especificando a versao e em modo de compatibilidade
    # Sera utilizada para criar janelas, ler o teclado e o mouse
    glutInit(sys.argv)
    glutInitContextVersion(1, 1)
    glutInitContextProfile(GLUT_COMPATIBILITY_PROFILE)

    # Inicia uma janela, definindo tamanho e posicao
    # Define janela com RGB, profundidade de dois buffers (um exibido e outro renderizando para trocar com o atual)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(500, 100)
    glutCreateWindow("Sistema Solar")

    # imprimeInstrucoes() <-> Metodo comentado

    # Exibe na tela o retorno da funcao chamada
    glutDisplayFunc(Sistema_Solar_com_orbitas)
    glutReshapeFunc(Redimensiona)

    # Define o retorno das teclas direcionais, teclado e mouse para a janela atual (callback gerado por evento)
    glutSpecialFunc(SpecialKeyboard)
    glutMouseFunc(GerenciaMouse)
    # Quando o mouse se move dentro da janela enquanto um ou mais botoes do mouse sao pressionados
    glutMotionFunc(GerenciaMovimento)

    # Inicializa ambiente (variaveis, fonte de luz e atualizacao de profundidade)
    Inicializa()

    # Processamento em segundo plano ou animacao continua. Chama metodo de atualizar a janela atual
    glutIdleFunc(atualiza)
    # Renderiza a janela criada
    glutMainLoop()
    return 0


main()
