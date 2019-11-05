from bs4 import BeautifulSoup, Tag
import requests
import itertools
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt


def find_all_li(start):
    """
    Function finding all <li> tags in html code between start and first found <h2>
    :param start: starting Tag
    :return: list of <li> tags
    """
    li = []
    next_node = start
    while True:
        next_node = next_node.nextSibling
        if isinstance(next_node, Tag):
            if next_node.name == "h2":  # if we get to the next <h2> tag then end loop
                break
            li.extend(next_node.find_all('li'))  # find all <li> tags in next_node and add them to list
    return li


def clear_text(text):
    """
    Function deleting not necessary space in text and diacritics
    :param text: text to clear
    :return:
    """
    pl = 'ąĄćĆęĘłŁńŃóÓśŚżŻźŹ'
    eng = 'aAcCeElLnNoOsSzZzZ'
    translator = str.maketrans(pl, eng)

    return text.replace(" ", "").translate(translator)


def draw_graph(G):
    """
    Function plotting a network
    :param G: graph to plot
    :return:
    """
    graph_pos = nx.spring_layout(G, k=0.6, weight=None)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    node_size = nx.get_node_attributes(G, 'size')

    nx.draw_networkx_nodes(G, graph_pos, nodelist=node_size.keys(), node_size=[v * 10 for v in node_size.values()],
                           alpha=0.8)
    nx.draw_networkx_labels(G, graph_pos, font_size=10)
    nx.draw_networkx_edges(G, graph_pos, width=0.8, alpha=0.8)
    nx.draw_networkx_edge_labels(G, graph_pos, label_pos=0.3, edge_labels=edge_labels, font_size=8)

    plt.show()


if __name__ == '__main__':
    index_url = "http://prac.im.pwr.wroc.pl/~hugo/HSC/Publications.html"

    r = requests.get(index_url)

    soup = BeautifulSoup(r.content, 'html.parser')
    h2 = soup.find_all('h2')  # find all <h2> tags

    li = find_all_li(h2[3])  # find all <li> tags starting from 3rd <h2> tag which is start of research papers

    connections = []
    vertices = []

    for i in li:
        # get all authors of publications from <b> tag and clear their names
        authors = [clear_text(link.string) for link in i.find_all('b')]
        vertices.extend(authors)

        # set connection between every pair of authors
        connections.extend([i for i in itertools.combinations(authors, 2)])

    c_vertices = Counter(vertices)
    c_connections = Counter(connections)

    G = nx.Graph()

    for i in c_vertices:
        G.add_node(i, size=c_vertices[i])

    for j in c_connections:
        G.add_edge(j[0], j[1], weight=c_connections[j])

    draw_graph(G)
