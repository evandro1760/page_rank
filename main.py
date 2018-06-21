from bs4 import BeautifulSoup
from os import listdir as la
import networkx as nx
import matplotlib.pyplot as plt

#def show_grafo(Grafo, pos, nodo )

options = {
    'node_color': '#e8e9ff',
    'node_size': 5000,
    'width': 3,
    'arrowstyle': '-|>',
    'arrowsize': 12,
    'with_labels': True,
}

G = nx.DiGraph()

pages = la('pages/')
#pages_name = [x.replace('.html','') for x in pages]
G.add_nodes_from(pages, type = 'machine')

#nx.draw(G, **options, pos=nx.circular_layout(G))

plt.show()

pages_ranks = {}
#alfa (probabilidade do teleporte) e epsilon (erro aceitável para convergência). 
eg = 1e-2
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
pos = nx.circular_layout(G)
#nx.draw(G, **options, pos=pos,
#    edge_color=range(G.number_of_edges()),
#    edge_cmap=plt.cm.Blues)

#plt.show()


algum_acima_erro = True #pra entrar no loop
while(algum_acima_erro):
    algum_acima_erro = False #assumindo que todos estao abaixo do erro

    nx.draw(G, **options, pos=pos,
    edge_color=range(G.number_of_edges()),
    edge_cmap=plt.cm.Blues)
    
    for page in pages:
        new_pr = 0
        #pegando os que apontam para ela
        for parent in parents[page]:
            new_pr += (pages_ranks[parent] / len(children[parent]))
        new_pr = (alfa / len(pages)) + new_pr * (1 - alfa)
        if(abs(new_pr - pages_ranks[page]) >= eg):
            algum_acima_erro = True #se algum ficar acima do erro, seta pra True, para continuar loop
        pages_ranks[page] = new_pr
        x,y = pos[page]
        plt.text(x,y,s='',bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
        plt.text(x,y+(0.1*(2*int(y >= 0)-1)),s=str(pages_ranks[page])[:5])
        #    bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')
    plt.show()