from collections import Counter

import networkx as nx
from matplotlib import pyplot as plt

from hybit_graph.classes import Node
from hybit_graph.functions import load_data

# Die Nummer des letzten Modellierungsvorhabens
MAX_MODELING_PROPOSAL_NO = 22


def build_simple_figure(edges):
    G = nx.MultiDiGraph(directed=True)

    for edge in edges:
        G.add_edge(edge.node_in, edge.node_out)

    # see https://stackoverflow.com/a/20133763
    pos = nx.spring_layout(G, k=1, iterations=20)
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color='lightblue')
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True)
    plt.savefig("simple_network.pdf")
    plt.show()


# Check if a given value is the one of a "Modellierungsvorhaben"
def is_mv(value):
    if isinstance(value, Node):
        value = value.id

    return str(value).isnumeric() and 1 <= int(value) <= MAX_MODELING_PROPOSAL_NO


def build_figure(edges, only_modelling=False, show=False):
    # to avoid lines getting to big, we apply a factor to the width of the edges
    # if edges become too thick, increase this factor
    WIDTH_SCALING_FACTOR = 3

    G = nx.MultiDiGraph(directed=True)

    for edge in edges:
        if not only_modelling or (only_modelling and is_mv(edge.node_in) and is_mv(edge.node_out)):
            G.add_edge(edge.node_in, edge.node_out)

    # see https://stackoverflow.com/a/58259281
    width_dict = Counter(G.edges())
    edge_width = [(u, v, {'width': value}) for ((u, v), value) in width_dict.items()]

    G_new = nx.DiGraph()
    G_new.add_edges_from(edge_width)

    pos = nx.circular_layout(G_new)
    # pos = nx.spring_layout(G_new, k=1, iterations=10, seed=1)
    # nx.draw(G_new, pos)

    width = [max(1, G_new[u][v]['width'] / WIDTH_SCALING_FACTOR) for u, v in G_new.edges()]
    nx.draw_networkx_edges(G_new, pos, width=width)

    edge_labels = dict([((u, v,), d['width']) for u, v, d in G_new.edges(data=True)])
    nx.draw_networkx_edge_labels(G_new, pos, edge_labels=edge_labels, label_pos=0.5, font_size=10)

    nx.draw_networkx_labels(G_new, pos, font_size=8)
    node_colors = ['lightgreen' if is_mv(lbl) else 'lightblue' for lbl, _ in G_new.nodes.items()]
    nx.draw_networkx_nodes(G_new, pos, node_size=200, node_color=node_colors)

    filename = "network%s.pdf" % ('_only_modelling' if only_modelling else '')
    plt.savefig(filename)

    print("Created %s; you might open it using e.g. evince %s" % (filename, filename))
    if show:
        plt.show()


if __name__ == '__main__':
    _, edges, _ = load_data("Schnittstellen.xlsx")
    build_figure(edges, show=True)
    build_figure(edges, show=True, only_modelling=True)
