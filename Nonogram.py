import numpy as np 
import string # Biblioteca para gerar o alfabeto
import time 
import os 
import csv

historico = []

def criar_jogo(lin, col):
    #gera o nonogram e o nonogram resolvido
    nonogram = np.zeros((lin, col)).astype(int)
    nonogram_resolvido = np.ones((lin, col)).astype(int)
    if (lin == 5 and col == 5):
        max_zeros = np.random.randint(5, 11)
    elif (lin == 9 and col == 9):
        max_zeros = np.random.randint(16, 36)
    #resolve o problema de gerar mais zeros do que o permitido
    indices = np.random.choice(lin * col, max_zeros, replace=False)
    for idx in indices:
        i = idx // col
        j = idx % col
        nonogram_resolvido[i, j] = 0
    return nonogram, nonogram_resolvido


def exibit_tabuleiro(nonogram, dicas_linhas, dicas_colunas):
    alfabeto = list(string.ascii_uppercase) # Gera o alfabeto
    numeros = list(range(1, len(nonogram)+1))
    #Gera a interface para o usuário ver o nonogram
    print()
    print("",end="    ")
    print(" ".join([str(x) for x in numeros]))
    print("  ╔" + "═"*(len(nonogram)*2+1) + "╗")
    for x in range(len(nonogram)):
        print(f'{alfabeto[x]} ║ {str(nonogram[x]).replace("[", "").replace("]", "").replace("1", "█").replace("0",".")} ║', end="")
        print(f'{dicas_linhas[x]}')
    print("  ╚" + "═"*(len(nonogram)*2+1) + "╝")
    print("   ", end="")
    for i in range(len(dicas_colunas)): 
        for x in dicas_colunas:
            try:
                print(x[i], end =' ') 
            except:
                print(" ", end =' ')
        print("\n", end="   ")
    return None
        
    
def alterar_nonogram(nonogram, op): #altera a seleção do usuário no nonogram
    linha = (int(op[0])-1)
    coluna = int(list(string.ascii_uppercase).index(op[1]))
    if nonogram[coluna, linha] == 1:
        nonogram[coluna, linha] = 0
    else:
        nonogram[coluna, linha] = 1
    return nonogram

def dicas_nonogram(nonogram_resolvido): #gera as dicas para o nonogram
    altura, largura = nonogram_resolvido.shape
    dicas_linhas = []
    dicas_colunas = []

    # Gerar dicas para as linhas
    for i in range(altura):
        dica_linha = []
        sequencia_atual = 0
        for j in range(largura):
            if nonogram_resolvido[i, j] == 1:
                sequencia_atual += 1
            elif sequencia_atual > 0:
                dica_linha.append(sequencia_atual)
                sequencia_atual = 0
        if sequencia_atual > 0:
            dica_linha.append(sequencia_atual)
        dicas_linhas.append(dica_linha)

    # Gerar dicas para as colunas
    for j in range(largura):
        dica_coluna = []
        sequencia_atual = 0
        for i in range(altura):
            if nonogram_resolvido[i, j] == 1:
                sequencia_atual += 1
            elif sequencia_atual > 0:
                dica_coluna.append(sequencia_atual)
                sequencia_atual = 0
        if sequencia_atual > 0:
            dica_coluna.append(sequencia_atual)
        dicas_colunas.append(dica_coluna)
    return dicas_linhas, dicas_colunas

def preencher_dicas(nonogram, nonogram_resolvido): #Dar dicas para o usuário
    altura, largura = nonogram_resolvido.shape
    for i in range(altura):
        for j in range(largura):
            if (nonogram[i, j] == 1 and nonogram_resolvido[i, j] == 0):
                return f"O espaço {j+1}{string.ascii_uppercase[i]} foi preenchido incorretamente!" 
    for i in range(altura):
        for j in range(largura):
            if (nonogram[i, j] != nonogram_resolvido[i, j]):
                return f"O espaço {j+1}{string.ascii_uppercase[i]} precisa ser preenchido!" 


def verificar_vitoria(nonogram, nonogram_resolvido): #Verifica se o usuário venceu
    if np.array_equal(nonogram, nonogram_resolvido):
        return True
    else:
        return False


def salvar_jogo(nonogram, nonogram_resolvido): #Salva o jogo na pasta saves
    nome_save = input("Digite o nome do save:")
    nome_save = (nome_save+"--"+str(time.strftime("%d-%m-%Y_%H-%M-%S"))+".npy")
    try:
        os.mkdir("saves")
    except:
        pass
    with open(f'saves/{nome_save}', 'wb') as f:
        np.save(f, nonogram)
        np.save(f, nonogram_resolvido)
    return None


def salvar_historico(nome_usuario, nivel_jogo, tempo_partida): #Salva o histórico dos usuários que jogaram 
    dados = [nome_usuario, nivel_jogo, tempo_partida]
    with open("historico.csv", 'a', newline='') as arquivo_csv:
        writer = csv.writer(arquivo_csv)
        writer.writerow(dados)

def carregar_jogo(): #Carrega o jogo salvo
    try:
        saves = os.listdir("saves")
        print("Saves disponíveis:")
        for i in range(len(saves)):
            print(f"{i+1} - {saves[i]}")
        op = int(input("Digite o número do save que deseja carregar: "))
        with open(f'saves/{saves[op-1]}', 'rb') as f:
            nonogram = np.load(f)
            nonogram_resolvido = np.load(f)
        return nonogram, nonogram_resolvido, saves[op-1]
    except:
        return None, None, None

def rodar_jogo(nonogram, nonogram_resolvido, dicas_linhas, dicas_colunas, nome_save=""): #Roda o jogo
     inicio = time.time()
     penalizacao = 0
     contador_dicas = 1
     print("\n")
     print("Iniciando jogo, divirta-se!")
     print("\n")
     print("\tComandos: 'sair' para sair, 'dica' para dica")
     print("Como escolher? Digite o número da coluna e a letra da linha (ex: 1A, 2B, 3C, etc.)")
     print("\n")
     while True:
        exibit_tabuleiro(nonogram, dicas_linhas, dicas_colunas)
        op = input("Digite a sua escolha: ").upper()
        if(op == "DICA"):
            print(preencher_dicas(nonogram, nonogram_resolvido))
            penalizacao += 10*contador_dicas
            contador_dicas += 1
            print()
        elif(op == "SAIR"):
            nome = input("Digite o seu nome: ")
            nivel_jogo = 0
            if(nonogram.shape == (5,5)):
                nivel_jogo = "5x5"
            else:
                nivel_jogo = "9x9"
            tempo_jogo = time.time() - inicio
            historico.append([nome, nivel_jogo, tempo_jogo+penalizacao]) #salvar historico
            print("Você saiu do jogo\n")
            print(f"Você jogou por {tempo_jogo:.2f} segundos")
            print(f"Você foi penalizado em {penalizacao} segundos")
            print(f"Seu tempo final foi de {tempo_jogo+penalizacao:.2f} segundos\n")
            print("Deseja salvar o jogo?")
            print("1 - Sim")
            print("2 - Não")
            op = input("Digite a sua escolha: ")
            if(op == "1"):
                if(nome_save != ""):
                    os.remove(f"saves/{nome_save}")
                salvar_jogo(nonogram, nonogram_resolvido)
                print("Jogo salvo!")
                print("Voltando para o menu inicial...")
                iniciar()
            else:
                print("Voltando para o menu inicial...")
                iniciar()
        else:
            try:
                if(op[0].isdigit() == False or op[1].isalpha() == False):
                    print("Escolha inválida")
                    continue
                if(ord(op[1])-65 >= nonogram.shape[0] or int(op[0])-1 >= nonogram.shape[1]):               
                    print("Escolha inválida")
                    continue
            except:
                print("Escolha inválida")
                continue
            nonogram = alterar_nonogram(nonogram, op)
            #print()
            #exibit_tabuleiro(nonogram_resolvido, dicas_linhas, dicas_colunas)
            if(verificar_vitoria(nonogram, nonogram_resolvido) == True):
                tempo_jogo = time.time() - inicio
                print("Parabéns, você venceu!")
                print(f"Você jogou por {tempo_jogo:.2f} segundos")
                print(f"Você foi penalizado em {penalizacao} segundos")
                print(f"Seu tempo final foi de {tempo_jogo+penalizacao:.2f} segundos\n")
                nome = input("Digite o seu nome: ")
                nivel_jogo = 0
                if(nonogram.shape == (5,5)):
                    nivel_jogo = "5x5"
                else:
                    nivel_jogo = "9x9"
                tempo_jogo = time.time() - inicio
                historico.append([nome, nivel_jogo, tempo_jogo+penalizacao]) #salvar historico
                print("Voltando para o menu inicial...")
                iniciar()



def iniciar(): #inicia o jogo
    print("Bem vindo a página inicial do Nonogrammm!")    
    print("Escolha uma opcao: ")
    print("1 - novo jogo")
    print("2 - Carregar jogo salvo")
    print("3 - Historico de jogos")
    print("4 - Sair")
    op = input("Digite a sua escolha: ")
    if(op == "1"):
        print("Escolha o tamanho do tabuleiro: ")
        print("1 - 5x5")
        print("2 - 9x9")
        print("3 - voltar")
        op = input("Digite a sua escolha: ")
        if(op == "1"):
            nonogram, nonogram_resolvido = criar_jogo(5,5)
            dicas_linhas, dicas_colunas = dicas_nonogram(nonogram_resolvido)
            rodar_jogo(nonogram, nonogram_resolvido, dicas_linhas, dicas_colunas)
        elif(op == "2"):
            nonogram, nonogram_resolvido = criar_jogo(9,9)
            dicas_linhas, dicas_colunas = dicas_nonogram(nonogram_resolvido)
            rodar_jogo(nonogram, nonogram_resolvido, dicas_linhas, dicas_colunas)
        elif(op == "3"):
            iniciar()
        else:
            print("Opção inválida!")
            iniciar()
    elif(op == "2"):
        nonogram, nonogram_resolvido, nome_save = carregar_jogo()
        if(str(nonogram) == "None"):
            print("Não há nenhum save disponível!")
            input("Pressione enter para voltar ao menu inicial...")
            iniciar()
        dicas_linhas, dicas_colunas = dicas_nonogram(nonogram_resolvido)
        rodar_jogo(nonogram, nonogram_resolvido, dicas_linhas, dicas_colunas, nome_save)
    elif(op == "3"):
        try:
            print("Historico de jogos: ") #salva o histório de usuários quando sai do programa
            with open("historico.csv", 'r') as arquivo_csv:
                reader = csv.reader(arquivo_csv)
                for row in reader:
                    print(f"Nome: {row[0]} | Nivel: {row[1]} | Tempo: {float(row[2]):.2f} segundos")
            input("Pressione enter para voltar ao menu inicial...")
            iniciar()
        except:
            print("Nenhum histórico foi salvo ainda!")
            input("Pressione enter para voltar ao menu inicial...")
            iniciar()
    elif(op == "4"):
        for i in range(len(historico)):
            salvar_historico(historico[i][0], historico[i][1], historico[i][2])
        print("Obrigado por jogar!")    
        exit()
    else:
        print("Opcao invalida!")
        iniciar()

    
    """nonogram, nonogram_resolvido = criar_jogo(5,5)
    dicas_linhas, dicas_colunas = dicas_nonogram(nonogram_resolvido)
    
    exibit_tabuleiro(nonogram, dicas_linhas, dicas_colunas)"""
   

        


iniciar()


