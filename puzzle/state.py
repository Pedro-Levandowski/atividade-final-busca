from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        filhos = []
        vazio = self.blank_index
        linha = vazio // 3
        coluna = vazio % 3

        movimentos = [
            ("UP", linha - 1, coluna),
            ("DOWN", linha + 1, coluna),
            ("LEFT", linha, coluna - 1),
            ("RIGHT", linha, coluna + 1),
        ]

        for acao, nova_linha, nova_coluna in movimentos:
            if nova_linha < 0 or nova_linha > 2 or nova_coluna < 0 or nova_coluna > 2:
                continue

            novo_indice = nova_linha * 3 + nova_coluna
            pecas = list(self.tiles)
            pecas[vazio], pecas[novo_indice] = pecas[novo_indice], pecas[vazio]
            filhos.append(State(tuple(pecas), parent=self, action=acao, cost=self.cost + 1))

        return filhos

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        caminho = []
        atual = self
        while atual is not None:
            caminho.append(atual)
            atual = atual.parent
        caminho.reverse()
        return caminho

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        acoes = []
        for estado in self.path():
            if estado.action is not None:
                acoes.append(estado.action)
        return acoes

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
