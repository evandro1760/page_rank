from bs4 import BeautifulSoup
from os import listdir as la
import networkx as nx
import matplotlib.pyplot as plt
from sys import argv

def show_grafo(G, pos, pages_ranks, error, conv = False):
    if(conv):
        plt.figure('[CONVERGIU] MAX ERROR='+str(error)[:5])
        cmap = plt.cm.summer
        tcol = 'black'
        op = options2
    else:
        cmap = plt.cm.winter
        plt.figure('MAX ERROR='+str(error)[:5])
        tcol = 'red'
        op = options1
    
    nx.draw(G, **op, pos=pos,
        edge_color=range(G.number_of_edges()),
        edge_cmap=cmap)
    for page in pages_ranks:
        x,y = pos[page]
        plt.text(x-int(x < 0)*0.1,y+(0.1*(2*int(y >= 0)-1)),
			s=str(pages_ranks[page])[:5], color=tcol)
    plt.show()

options1 = {
    'node_color': '#757bff',
    'node_size': 5000,
    'width': 3,
    'arrowstyle': '-|>',
    'arrowsize': 12,
    'with_labels': True,
}

options2 = {
    'node_color': '#ff7575',
    'node_size': 5000,
    'width': 3,
    'arrowstyle': '-|>',
    'arrowsize': 12,
    'with_labels': True,
}

G = nx.DiGraph()

pages = la('pages/')
G.add_nodes_from(pages, type = 'machine')

plt.show()

pages_ranks = {}
#alfa (probabilidade do teleporte) e epsilon (erro aceitável para convergência). 
alfa = float(argv[1])
eg = float(argv[2])

parents = {x:[] for x in pages}
children = {x:[] for x in pages}

for page in pages:
    pages_ranks[page] = 1/len(pages)
    
    html_doc = '\n'.join(open('pages/' + page, 'r').readlines())
    soup = BeautifulSoup(html_doc, 'html.parser')

    for link in soup.find_all('a'):
        link_page = link.get('href')
        G.add_edge(page, link_page)
        
        #Tem que criar duplicatas
        parents[link_page].append(page)
        children[page].append(link_page)

pos = nx.circular_layout(G)
show_grafo(G, pos, pages_ranks, error = 0)

algum_acima_erro = True #pra entrar no loop
while(algum_acima_erro):
    algum_acima_erro = False #assumindo que todos estao abaixo do erro
    error = []
    for page in pages:
        new_pr = 0        
		#pegando os que apontam para ela
        for parent in parents[page]:
            new_pr += (pages_ranks[parent] / len(children[parent]))
        new_pr = (alfa / len(pages)) + new_pr * (1 - alfa)
        error.append(abs(new_pr - pages_ranks[page]))
        if(error[-1] >= eg):
            algum_acima_erro = True #se algum ficar acima do erro, seta pra True, para continuar loop
        pages_ranks[page] = new_pr
    show_grafo(G, pos, pages_ranks, error = max(error))
show_grafo(G, pos, pages_ranks, error = max(error), conv = True)
    