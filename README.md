# Not Alone Puzzle

Este repositório contém uma implementação acadêmica para resolução do problema
**Not Alone Puzzle**, desenvolvida no contexto de uma monografia na Universidade
Federal do Ceará.

O projeto tem finalidade totalmente acadêmica. Os commits no GitHub serão
utilizados para divulgação do trabalho e para versionamento do código durante o
desenvolvimento da pesquisa.

## Autoria

**Autor:** Prof. Dr. Tibérius de Oliveira e Bonates, da Universidade Federal do
Ceará.

**Coautor:** João Paulo Venancio Silva

## Resumo

O puzzle **Not Alone** insere-se na classe de problemas de satisfação de
restrições, exigindo métodos eficientes para explorar o seu espaço de busca.
Esta monografia propõe e avalia duas abordagens computacionais exatas e
complementares para a resolução do problema a partir de subconjuntos
arbitrários de dicas iniciais.

A primeira abordagem formula o puzzle como um modelo de Programação Linear
Inteira (PLI), capaz de identificar uma solução factível e, por meio da adição
de cortes para soluções já encontradas, enumerar todas as configurações válidas
para uma dada instância.

A segunda abordagem consiste em um algoritmo dedicado baseado em propagação de
restrições. Diferentemente da formulação PLI, esse método não depende de
solvers de otimização genéricos: ele utiliza inferência lógica, filtragem de
domínios e poda do espaço de busca para encontrar uma ou todas as soluções
possíveis.

As metodologias são comparadas experimentalmente em instâncias de referência
nas dimensões `6 x 6` e `8 x 8`, incluindo casos conhecidos por admitirem
solução única. O objetivo é contrastar o custo computacional de uma formulação
algébrica genérica com o desempenho de um algoritmo especializado em dedução
baseada no domínio do problema.

## O Problema

O Not Alone Puzzle é tratado neste projeto como um problema de preenchimento de
um tabuleiro quadrado de dimensão par. Cada célula deve receber um dos dois
símbolos possíveis:

- `A`
- `Z`

Algumas células podem vir previamente preenchidas, funcionando como dicas da
instância. As demais células aparecem como espaços em branco.

As soluções consideradas válidas seguem as seguintes regras:

- Cada linha deve conter a mesma quantidade de símbolos `A` e `Z`.
- Cada coluna deve conter a mesma quantidade de símbolos `A` e `Z`.
- Não podem ocorrer os padrões `AZA` ou `ZAZ` em linhas.
- Não podem ocorrer os padrões `AZA` ou `ZAZ` em colunas.
- As dicas já presentes no tabuleiro devem ser preservadas.

Assim, para um tabuleiro `6 x 6`, por exemplo, cada linha e cada coluna deve
conter exatamente três símbolos `A` e três símbolos `Z`.

## Abordagens Utilizadas

O arquivo `notalonepuzzle.py` implementa as duas abordagens descritas no
resumo: uma por propagação de restrições e outra por Programação Linear
Inteira. Ambas foram concebidas para encontrar uma ou todas as soluções válidas
para um tabuleiro parcialmente preenchido.

### 1. Propagação de Restrições

A função `resolver(tabuleiro)` utiliza uma estratégia baseada em domínios e
propagação de restrições.

Primeiro, o algoritmo gera todas as sequências possíveis para uma linha ou
coluna, respeitando a quantidade igual de `A` e `Z` e proibindo os padrões
`AZA` e `ZAZ`.

Depois, cada linha e cada coluna recebe inicialmente esse conjunto de
sequências possíveis. A partir das dicas do tabuleiro, o algoritmo filtra os
domínios das linhas e colunas afetadas. Quando uma célula passa a ter apenas um
valor possível, essa informação é propagada para outras linhas e colunas.

Se a propagação não for suficiente para determinar todo o tabuleiro, o
algoritmo escolhe uma linha ainda ambígua e testa recursivamente cada sequência
possível para ela. Dessa forma, a busca combina:

- filtragem de domínios;
- propagação de valores fixados;
- recursão para explorar alternativas restantes.

O resultado é um conjunto contendo todas as soluções encontradas.

### 2. Programação Linear Inteira

A função `solve_NotAlone(grid, solsProibidas)` formula o puzzle como um problema
de Programação Linear Inteira usando o pacote OR-Tools.

Cada célula `(i, j)` do tabuleiro é representada por uma variável binária:

- `x[i, j] = 1`, se a célula contém `A`;
- `x[i, j] = 0`, se a célula contém `Z`.

As regras do puzzle são modeladas como restrições lineares:

- soma igual a `n/2` em cada linha;
- soma igual a `n/2` em cada coluna;
- restrições que impedem os padrões `AZA` e `ZAZ`;
- restrições que fixam as dicas fornecidas na instância.

Para obter todas as soluções, o programa chama o resolvedor repetidamente. A
cada solução encontrada, uma nova restrição de corte é adicionada para proibir
que a mesma solução seja retornada novamente.

Ao final, o código compara o conjunto de soluções obtido por propagação com o
conjunto de soluções obtido por Programação Linear Inteira. Essa comparação
serve como uma validação experimental entre as duas abordagens.

## Como Executar

Instale a dependência principal:

```bash
pip install ortools
```

Execute o script:

```bash
python notalonepuzzle.py
```

## Uso das Instâncias

As instâncias obtidas a partir do site de referência estão organizadas em:

```text
instances/site/6x6/
instances/site/8x8/
```

Cada arquivo representa uma única instância do puzzle. O padrão adotado é:

- `A` para uma célula preenchida com `A`;
- `Z` para uma célula preenchida com `Z`;
- `.` para uma célula vazia.

Exemplo de instância `6 x 6`:

```text
......
......
...A.A
......
...A..
....A.
```

O código converte automaticamente os pontos (`.`) para espaços em branco antes
de resolver o puzzle, preservando o formato interno usado pelos algoritmos.

Para escolher qual instância será resolvida, altere manualmente a variável
`instancia` no bloco principal do arquivo `notalonepuzzle.py`:

```python
instancia = 'instances/site/6x6/p01.txt'
```

Por exemplo, para resolver a vigésima instância `8 x 8`, use:

```python
instancia = 'instances/site/8x8/p20.txt'
```

Ao executar o programa, as duas abordagens implementadas são aplicadas sobre a
instância selecionada, e os conjuntos de soluções encontrados são comparados ao
final.
