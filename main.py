from bs4 import BeautifulSoup
from os import listdir as la
import networkx as nx
import matplotlib.pyplot as plt

options = {
    'node_color': 'white',
    'node_size': 5000,
    'width': 3,
    'arrowstyle': '-|>',
    'arrowsize': 12,
    'with_labels': True,
}

G = nx.DiGraph()

pages = la('pages/')
#pages_name = [x.replace('.html','') for x in pages]
G.add_nodes_from(pages, weight=0.4)

#nx.draw(G, **options, pos=nx.circular_layout(G))

plt.show()

pages_ranks = {}
eg = 0.01
alfa = 0.1

parents = {x:[] for x in pages}
children = {x:[] for x in pages}

for page in pages:
    #print(page)
    pages_ranks[page] = 1/len(pages)
    
    html_doc = '\n'.join(open('pages/' + page, 'r').readlines())
    soup = BeautifulSoup(html_doc, 'html.parser')

    for link in soup.find_all('a'):
        link_page = link.get('href')
        G.add_edge(page, link_page)
        
        #Tem que criar duplicatas
        parents[link_page].append(page)
        children[page].append(link_page)

#nx.draw_networkx_labels(G)
#labels = nx.draw_networkx_labels(G, pos=pos)
nx.draw(G, **options, pos=nx.circular_layout(G),
    edge_color=range(G.number_of_edges()),
    edge_cmap=plt.cm.Blues)

plt.show()


todos_abaixo_erro = False
while(not todos_abaixo_erro):
    for page in pages:
        new_pr = 0
        #pegando os que apontam para ela
        for parent in parents[page]:
            new_pr += (pages_ranks[parent] / len(children[parent]))
        new_pr = (alfa / len(pages)) + new_pr * (1 - alfa)
        if(abs(new_pr - pages_ranks[page]) <= eg):
            todos_abaixo_erro = True
        pages_ranks[page] = new_pr
        
