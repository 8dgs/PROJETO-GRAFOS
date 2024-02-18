import csv
from geopy.distance import geodesic

def ler_csv(nome_arquivo):
    # Função para ler o arquivo CSV e extrair os dados relevantes
    dados = []
    with open(nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo:
        leitor_csv = csv.DictReader(arquivo, delimiter=';')
        for linha in leitor_csv:
            # Verifica se os valores de latitude e longitude não estão vazios
            if linha['latitude'] and linha['longitude']:
                # Armazena apenas as colunas 'escola', 'longitude' e 'latitude'
                dados.append({'escola': linha['escola'], 'longitude': linha['longitude'], 'latitude': linha['latitude']})
                # Mensagens de depuração
                print(f"Escola: {linha['escola']}, Latitude: {linha['latitude']}, Longitude: {linha['longitude']}")
    return dados

class Grafo:
    def __init__(self):
        # Inicializa o grafo com um dicionário vazio para armazenar os vértices e suas adjacências
        self.vertices = {}

    def adicionar_aresta(self, vertice1, vertice2, distancia_metros):
        # Adiciona uma aresta entre dois vértices ao grafo
        if vertice1 not in self.vertices:
            self.vertices[vertice1] = {}
        if vertice2 not in self.vertices:
            self.vertices[vertice2] = {}

        # Adiciona a distância como peso da aresta
        self.vertices[vertice1][vertice2] = distancia_metros
        self.vertices[vertice2][vertice1] = distancia_metros

    def prim_mst(self, vertice_inicio, dados):
        # Implementação do algoritmo de Prim para encontrar a árvore geradora mínima
        print("Iniciando algoritmo de Prim a partir do vértice:", vertice_inicio)
        if vertice_inicio not in self.vertices:
            print(f"A escola de início '{vertice_inicio}' não está no banco de dados.")
            return []

        visitados = set()
        arvore = []

        # Adiciona o vértice inicial ao conjunto de visitados
        visitados.add(vertice_inicio)

        while len(visitados) < len(self.vertices):
            menor_valor = float('inf')
            menor_aresta = None

            for vertice in visitados:
                for vizinho, valor in self.vertices[vertice].items():
                    # Encontra a menor aresta conectando um vértice visitado a um vértice não visitado
                    if vizinho not in visitados and float(valor) < menor_valor:
                        menor_valor = float(valor)
                        menor_aresta = (vertice, vizinho, valor)

            if menor_aresta:
                # Adiciona a menor aresta à árvore geradora mínima e marca o vértice vizinho como visitado
                arvore.append(menor_aresta)
                visitados.add(menor_aresta[1])
                print(f"Aresta adicionada: {menor_aresta}")
            else:
                # Conclui a construção da árvore geradora mínima
                print("Construção da árvore geradora mínima concluída.")
                break

        # Verifica se a árvore foi construída corretamente
        if len(arvore) != len(self.vertices) - 1 or not self.is_tree(arvore):
            print("Erro: A árvore geradora mínima não foi construída corretamente.")

        return arvore

    def is_tree(self, arvore):
        # Verifica se a árvore geradora mínima é uma árvore válida
        visitados = set()
        visitados.add(arvore[0][0])

        for aresta in arvore:
            vertice1, vertice2, valor = aresta
            if vertice2 in visitados:
                return False
            visitados.add(vertice2)

        return len(visitados) == len(self.vertices)

# Exemplo de uso:
dados = ler_csv('info_escolas_2023_27122023.csv')

# Criar o grafo e adicionar as arestas
grafo = Grafo()
for i, dado1 in enumerate(dados):
    for j, dado2 in enumerate(dados):
        if i < j:  # Adicionar cada aresta apenas uma vez
            coord1 = (float(dado1['latitude']), float(dado1['longitude']))
            coord2 = (float(dado2['latitude']), float(dado2['longitude']))
            distancia_metros = geodesic(coord1, coord2).meters
            grafo.adicionar_aresta(i, j, round(distancia_metros))  # Arredondar para o metro mais próximo

# Nome da escola de início
vertice_inicio = input("Digite o nome da escola de início: ")

# Obter o índice da escola de início nos dados
indice_inicio = None
for i, dado in enumerate(dados):
    if dado['escola'] == vertice_inicio:
        indice_inicio = i
        break

# Construir a árvore geradora mínima a partir da escola de início
arvore_geradora_minima = grafo.prim_mst(indice_inicio, dados)

# Calcular a distância total percorrida pela árvore geradora mínima
distancia_total_metros = sum(aresta[2] for aresta in arvore_geradora_minima)

# Converter a distância total para quilômetros
distancia_total_km = distancia_total_metros / 1000

# Imprimir as arestas da árvore geradora mínima
print("Arestas da Árvore Geradora Mínima:")
for aresta in arvore_geradora_minima:
    vertice1, vertice2, valor = aresta
    escola1 = dados[vertice1]['escola']
    escola2 = dados[vertice2]['escola']
    print(f"{escola1} - {escola2}, Distância: {valor} m")

print(f"Distância total percorrida pela árvore geradora mínima: {distancia_total_km:.3f} km")