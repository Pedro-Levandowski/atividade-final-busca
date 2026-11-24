import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distancia = 0
        for indice, peca in enumerate(state.tiles):
            if peca == 0:
                continue
            indice_objetivo = GOAL_STATE.index(peca)
            linha, coluna = indice // 3, indice % 3
            linha_obj, coluna_obj = indice_objetivo // 3, indice_objetivo % 3
            distancia += abs(linha - linha_obj) + abs(coluna - coluna_obj)
        return distancia

    def search(self, initial: State) -> SearchResult:
        fronteira = [(self.heuristic(initial), initial)]
        explorados = set()

        expandidos = 0
        gerados = 1
        max_fronteira = 1

        while fronteira:
            f, atual = heapq.heappop(fronteira)

            if atual.tiles in explorados:
                continue
            explorados.add(atual.tiles)

            if atual.is_goal:
                return SearchResult(atual, expandidos, gerados, max_fronteira, atual.cost)

            expandidos += 1
            for filho in atual.neighbors():
                if filho.tiles not in explorados:
                    f_filho = filho.cost + self.heuristic(filho)
                    heapq.heappush(fronteira, (f_filho, filho))
                    gerados += 1

            max_fronteira = max(max_fronteira, len(fronteira))

        return SearchResult(None, expandidos, gerados, max_fronteira)
