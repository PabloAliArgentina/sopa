import random
from copy import deepcopy

with open('lemario.txt', 'r') as f:
    words = f.readlines()

aligns = ('vertical', 'horizontal', 'diagonal')
directions = ('forwards', 'backwards')
letters = ('aábcdeéfghiíjklmnñoópqrstuúvwxyz').upper()

matrix_size = 20
matrix = [[' ' for _ in range(matrix_size)] for _ in range(matrix_size)]
chosen_words = []

words_number = 5
while len(chosen_words) < words_number:
    align = random.choice(aligns)
    direction = random.choice(directions)
    original_word = random.choice(words).replace('\n', '').upper()
    word = original_word

    if direction == 'backwards':
        word = word[::-1]

    if len(word) > matrix_size: continue
    if any( [(word in chw) for chw in chosen_words]): continue

    failed = False
    if align == 'vertical':
        column = random.randint(0, matrix_size - 1)
        row = random.randint(0, (matrix_size - len(word)))
        _matrix = deepcopy(matrix)
        for l in word:
            field = _matrix[row][column]
            if field == ' ' or field == l:
                _matrix[row][column] = l
            else:
                failed = True
                break
            row += 1
        if not failed:
            matrix = deepcopy(_matrix)       

    elif align == 'horizontal':
        column = random.randint(0, matrix_size - len(word))
        row = random.randint(0, matrix_size - 1)
        _matrix = deepcopy(matrix)
        for l in word:
            field = _matrix[row][column]
            if field == ' ' or field == l:
                _matrix[row][column] = l
            else:
                failed = True
                break
            column += 1
        if failed == False:
            matrix = deepcopy(_matrix) 

    elif align == 'diagonal':
        column = random.randint(0, matrix_size - len(word))
        row = random.randint(0, matrix_size - len(word))
        _matrix = deepcopy(matrix)
        for l in word:
            field = _matrix[row][column]
            if field == ' ' or field == l:
                _matrix[row][column] = l
            else:
                failed = True
                break
            column += 1
            row += 1
        if not failed:
            matrix = deepcopy(_matrix) 
    else:
        failed = True

    if not failed:
        chosen_words.append(original_word)

for row in range(len(matrix)):
    for column in range(len(matrix)):
        char = random.choice(letters)
        if matrix[row][column] == ' ':
            matrix[row][column] = char
    print(matrix[row])
    
print (chosen_words)
    

    

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def crear_pdf(matriz, palabras, nombre_archivo):
    c = canvas.Canvas(nombre_archivo, pagesize=letter)
    width, height = letter

    # Definir dimensiones y estilos para la tabla
    cell_width = 20
    cell_height = 20
    matriz_width = len(matriz[0]) * cell_width
    matriz_height = len(matriz) * cell_height

    # Calcular coordenadas para centrar la matriz horizontalmente
    matriz_x_offset = (width - matriz_width) / 2
    matriz_y_offset = (height - matriz_height)

    # Dibujar la matriz en el PDF
    for i, fila in enumerate(matriz):
        for j, elemento in enumerate(fila):
            c.drawString(matriz_x_offset + j * cell_width, matriz_y_offset + (len(matriz) - i - 1) * cell_height, str(elemento))

    # Calcular el espacio disponible para las palabras
    espacio_palabras = matriz_width
    # Calcular el ancho total de las palabras
    palabras_width_total = len(palabras) * cell_width
    # Calcular el ancho que cada palabra debería ocupar
    ancho_palabra = palabras_width_total / len(palabras)

    # Calcular coordenadas para centrar las palabras horizontalmente
    palabras_x_offset = matriz_x_offset + (matriz_width - palabras_width_total) / 2
    palabra_y_offset = matriz_y_offset - 100

    # Escribir las palabras debajo de la matriz
    for i, palabra in enumerate(palabras):
        c.drawString(palabras_x_offset, palabra_y_offset + i * 15, palabra)

    c.save()


crear_pdf(matrix, chosen_words, 'sopa.pdf')