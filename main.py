from bs4 import BeautifulSoup
from os import listdir as la
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
pages = la('pages/')
G.add_nodes_from(pages)

pages_ranks = {}
eg = 0.01

parents = {x:[] for x in pages}

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
    
#nx.draw(G, with_labels=True, font_weight='bold')
#plt.show()


"""
error = 1
while(error >= eg):
"""