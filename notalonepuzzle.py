from ortools.linear_solver import pywraplp
import itertools as it
import copy


def solve_NotAlone(grid, solsProibidas):

    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return

    n = len(grid)

    x = {}
    for i in range(n):
        for j in range(n):
            x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')

    for i in range(n):
        solver.Add( solver.Sum([x[i, j] for j in range(n)]) == (n//2))

    for j in range(n):
        solver.Add( solver.Sum([x[i, j] for i in range(n)]) == (n//2))

    for i in range(n):
        for j in range(1,n-1):
            solver.Add(x[i, j] >= x[i, j-1] + x[i, j+1] - 1)
            solver.Add(x[i, j] <= x[i, j-1] + x[i, j+1])

    for j in range(n):
        for i in range(1,n-1):
            solver.Add(x[i, j] >= x[i-1, j] + x[i+1, j] - 1)
            solver.Add(x[i, j] <= x[i-1, j] + x[i+1, j])

    for i in range(n):
        for j in range(n):
            if grid[i][j] != ' ':
                solver.Add(x[i,j] == (1 if grid[i][j] == 'A' else 0))

    for s in solsProibidas:
        uns = sum( [sum([x[i,j] for j in range(n)]) for i in range(n)] )
        solver.Add(solver.Sum([(-x[i,j] if s[i][j] == 1 else x[i,j])  for i in range(n) for j in range(n)]) >= 1 - uns)

    objective = solver.Objective()
    for i in range(n):
        for j in range(n):
            objective.SetCoefficient(x[i,i], 1.0)
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        T = []
        for i in range(n):
            linha = ''
            for j in range(n):
                if x[i, j].solution_value() > 0.5:
                    linha = ''.join([linha, 'A'])
                else:
                    linha = ''.join([linha, 'Z'])
            T.append(linha)
        return tuple(T)
    else:
        return None


def filtrar(dominio, posicao, valor):
    return [d for d in dominio if d[posicao] == valor]
    
def resolver(tabuleiro):
    
    n = len(tabuleiro)
    assert n % 2 == 0, print(f'Dimensão do tabuleiro deve ser par.')
    
    grid = {(i,j):tabuleiro[i][j] for i in range(n) for j in range(n)}
    
    dom = set()
    base = ['A' for _ in range(n//2)]
    base.extend(['Z' for _ in range(n//2)])
    base = ''.join(base)
   
    for p in it.permutations(base):
        sequencia = ''.join(p)
        if 'AZA' not in sequencia and 'ZAZ' not in sequencia:
            dom.add(sequencia)
    dom = list(dom)
    

    linhas = {i : list(dom) for i in range(n)}
    colunas = {i : list(dom) for i in range(n)}

    fila = set()
    
    for i in range(n):
        for j in range(n):
            if grid[i,j] != ' ':
                fila.add( (i,j) )

    while len(fila) > 0:
        i,j = fila.pop()
        
        antigaLinhai = linhas[i]
        antigaColunaj = colunas[j]
        linhas[i] = filtrar(linhas[i], j, grid[i,j])
        colunas[j] = filtrar(colunas[j], i, grid[i,j])

        if linhas[i] != antigaLinhai:
            for outroj in range(n):
                if outroj != j:
                    antes = set([d[i] for d in colunas[outroj]])
                    depois = set([d[outroj] for d in linhas[i]])
                    if len(depois) == 0:
                        return set()
                    if len(depois) < len(antes):
                        valor = depois.pop()
                        grid[i,outroj] = valor
                        fila.add( (i,outroj) )

        if colunas[j] != antigaColunaj:
            for outroi in range(n):
                if outroi != i:
                    antes = set([d[j] for d in linhas[outroi]])
                    depois = set([d[outroi] for d in colunas[j]])
                    if len(depois) == 0:
                        return set()
                    if len(depois) < len(antes):
                        valor = depois.pop()
                        grid[outroi,j] = valor
                        fila.add( (outroi,j) )

            
    solucaoUnica = True
    for i in range(n):
        if len(linhas[i]) > 1:
            solucaoUnica = False
    
    if solucaoUnica:
        solucao = set()
        T = []
        for i in range(n):
            linha = ''.join([grid[i,j] for j in range(n)])
            T.append(linha)
        solucao.add(tuple(T))
        return solucao
    else:
        solucoes = set()
        for i in range(n):
            if len(linhas[i]) > 1:
                for sequencia in linhas[i]:
                    tab = copy.deepcopy(tabuleiro)
                    tab[i] = sequencia
                    for T in resolver(tab):
                        solucoes.add(T)
                break
        return solucoes


if __name__ == '__main__':

    tabuleiro1 = [
        '      ',
        '      ',
        '   A A',
        '      ',
        '   A  ',
        '    A '
    ]

    tabuleiro10 = [
        '      ',
        '      ',
        'A  A  ',
        '      ',
        '  Z   ',
        ' Z    '
    ]
    
    tabuleiro30 = [
        ' A A  ',
        '  Z   ',
        '      ',
        '      ',
        '     A',
        '  Z  A'
    ]

    tabuleiro8_1 = [
        '        ',
        'A AAZ   ',
        'ZZA     ',
        '  AAAAZZ',
        '     ZZ ',
        ' AZ  Z  ',
        'A Z ZA  ',
        '  Z  AA '
    ]

    tabuleiro8_1_vazio = [
        '        ',
        'A AAZ   ',
        'ZZA     ',
        '        ',
        '        ',
        '        ',
        '        ',
        '        '
    ]

    tabuleiro = tabuleiro10
    print(tabuleiro)

    print('\nENCONTRANDO SOLUCOES VIA PROPAGACAO:')

    conjuntoSolucoesPR = resolver(tabuleiro)
    for s in conjuntoSolucoesPR:
        print('Solução encontrada:')
        for linha in s:
            print(linha)
        print('')
    print(f'Número de soluções via propagação: {len(conjuntoSolucoesPR)}')


    print('\nENCONTRANDO SOLUCOES VIA PROGRAMACAO LINEAR INTEIRA:')
    
    conjuntoSolucoesPLI = set()
    solucoes01Conhecidas = []

    while True:
        solucao = solve_NotAlone(tabuleiro, solucoes01Conhecidas)
        if not solucao:
            break
        conjuntoSolucoesPLI.add(solucao)
        solucao01 = []
        for i in range(len(solucao)):
            solucao01.append([])
            for j in range(len(solucao)):
                solucao01[-1].append(1 if solucao[i][j] == 'A' else 0)
        solucoes01Conhecidas.append(solucao01)

    for s in conjuntoSolucoesPLI:
        print('Solução encontrada:')
        for linha in s:
            print(linha)
        print('')
    print(f'Número de solucoes via PLI: {len(conjuntoSolucoesPLI)}')

    if conjuntoSolucoesPR == conjuntoSolucoesPLI:
        print('\nConjuntos idênticos de soluções.')
    else:
        print('Algo errado: diferentes conjunções de soluções obtidos.')
