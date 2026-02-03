from geopy import distance
from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.list_stati = []
        self.dict_stati = {}
        self.graph = nx.Graph()
        self.lista_connessioni = []
        self.dict_pesi = {}
        self.path = []
        self.path_edge = []
        self.sol_best = 0

    def get_years(self):
        return DAO.get_years()

    def get_shape(self, anno):
        return DAO.get_shape(anno)

    def crea_grafo(self,anno,forma):
        self.list_stati = DAO.get_state()
        for state in self.list_stati:
            self.dict_stati[state.id] = state
            if state not in self.graph:
                self.graph.add_node(state)
        self.lista_connessioni = DAO.get_connessioni()
        pesi = DAO.get_peso(anno,forma)
        for state in self.list_stati:
            if state.id not in pesi:
                self.dict_pesi[state.id] = 0
            else:
                self.dict_pesi[state.id] = pesi[state.id]

        for z in self.lista_connessioni:
            peso = self.dict_pesi[z[0]] + self.dict_pesi[z[1]]
            self.graph.add_edge(self.dict_stati[z[0]], self.dict_stati[z[1]], weight=peso)
        print(self.graph)
        return self.graph


    def get_peso_tot(self,stato):

        pass

    def compute_path(self):
        self.path = []
        self.path_edge = []
        self.sol_best = 0

        partial = []
        for n in self.graph.nodes():
            partial.clear()
            partial.append(n)
            self._ricorsione(partial,[])


    def _ricorsione(self, partial, partial_edge):
        n_last = partial[-1]

        neighbors = self.get_admissible_neighbs(n_last, partial_edge)
        if len(neighbors) == 0:
            weigh_path = self.compute_weight_path(partial_edge)
            if weigh_path > self.sol_best:
                self.sol_best = weigh_path + 0.0
                self.path = partial[:]
                self.path_edge = partial_edge[:]
            return

        for n in neighbors:
            partial_edge.append((n_last,n,self.graph.get_edge_data(n_last,n)['weight']))
            partial.append(n)

            self._ricorsione(partial,partial_edge)
            partial_edge.pop()
            partial.pop()



    def get_admissible_neighbs(self, n_last, partial_edges):
        all_neigh = self.graph.edges(n_last,data=True)
        result = []

        for e in all_neigh:
            if len(partial_edges) != 0:
                if e[2]["weight"] > partial_edges[-1][2]:
                    result.append(e[1])
            else:
                result.append(e[1])
        return result


    def compute_weight_path(self, mylist):
        weight = 0
        for e in mylist:
            weight += distance.geodesic((e[0].lat, e[0].lng),
                                        (e[1].lat, e[1].lng)).km
        return weight

    def get_sum_weight_per_node(self):
        pp = []
        for n in self.graph.nodes():
            sum_w = 0
            for e in self.graph.edges(n, data=True):
                sum_w += e[2]['weight']
            pp.append((n.id, sum_w))
        return pp

    def get_edges(self):
        return list(self.graph.edges(data=True))

    def get_distance_weight(self,e):
        return distance.geodesic((e[0].lat, e[0].lng),
                                    (e[1].lat, e[1].lng)).km