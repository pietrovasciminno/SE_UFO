import flet as ft
from UI.view import View
from modell.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        self._view.dd_shape.options.clear()
        self._view.dd_year.options.clear()
        anni = self._model.get_years()
        for y in anni:
            self._view.dd_year.options.append(ft.dropdown.Option(f"{y}"))
        self._view.update()


    def handler_dd_shape(self, e):
        anno = int(self._view.dd_year.value)
        self._view.dd_shape.options.clear()
        forme = self._model.get_shape(anno)
        for y in forme:
            self._view.dd_shape.options.append(ft.dropdown.Option(f"{y}"))
        self._view.update()





    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        anno = int(self._view.dd_year.value)
        forma  = self._view.dd_shape.value
        self._model.crea_grafo(anno,forma)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di vertici: {self._model.graph.number_of_nodes()} | Numero archi: {self._model.graph.number_of_edges()}"))
        info = self._model.get_sum_weight_per_node()
        for i in info:
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Nodo: {i[0]}, somma pesi su archi = {i[1]}"))
        self._view.update()





    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        self._model.compute_path()

        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Peso cammino massimo: {self._model.sol_best}"))

        for edge in self._model.path_edge:
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f"{edge[0].id} --> {edge[1].id}: weight {edge[2]} distance {self._model.get_distance_weight(edge)}"))

        self._view.update()
