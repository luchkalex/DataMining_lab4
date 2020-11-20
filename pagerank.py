import networkx as nx
import urllib as ul
import numpy
from bs4 import BeautifulSoup


def page_rank(G: nx.Graph, alpha=0.5):
    nodes_quantity = len(list(G.nodes))

    answers = numpy.array([-alpha] * nodes_quantity)

    matrix = numpy.array([[0.0] * nodes_quantity] * nodes_quantity)

    index_queue = {}

    j = 0

    for node in list(G.nodes):
        index_queue[node] = j
        j += 1

    i = 0
    j = 0
    for node in list(G.nodes):
        matrix[i][index_queue[node]] = -1
        for predecessors in G.predecessors(node):
            for _ in G.neighbors(predecessors):
                j += 1
            if node != predecessors:
                matrix[i][index_queue[predecessors]] = 1 / j * alpha
            j = 0
        i += 1
    pageranks = numpy.linalg.solve(matrix, answers)

    pagerank_dictionary = {}

    i = 0
    for node in list(G.nodes):
        pagerank_dictionary[node] = pageranks[i]
        i += 1

    return pagerank_dictionary


def getSetOfLinks(url, root):
    try:
        fp = ul.request.urlopen(url)
    except ul.error.HTTPError:
        return None

    bytes = fp.read()
    htmlString = bytes.decode("utf8")
    soup = BeautifulSoup(htmlString, 'html.parser')
    set_of_links = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        if type(href) == str:
            a = "" + href
            if a.startswith("/"):
                set_of_links.add(root + a)
            elif a.startswith(site):
                set_of_links.add(a)
    fp.close()
    return set_of_links


# -------------- Page rank calculation ------------------
# Site for test "https://bpa.com.ua/"
site = input("Enter web site: ")

main_set_of_links = getSetOfLinks(site, site)

unresolved_links = main_set_of_links.copy()

pages_links = {site: unresolved_links}

broken_links = set()

while len(unresolved_links) > 0:
    link = unresolved_links.pop()
    set_for_check = getSetOfLinks(link, site)

    if set_for_check is not None:
        difference = set_for_check.difference(main_set_of_links)
        main_set_of_links = main_set_of_links.union(difference)
        unresolved_links = unresolved_links.union(difference)

        pages_links[link] = set_for_check.copy()
    else:
        broken_links.add(link)

for br_link in broken_links:
    main_set_of_links.remove(br_link)
    for title in pages_links:
        if pages_links[title].__contains__(br_link):
            pages_links[title].remove(br_link)

# Create graph
G = nx.DiGraph()

# Add nodes
for title in pages_links:
    G.add_node(title)

# Add edges
for title in pages_links:
    for link in pages_links[title]:
        G.add_edge(title, link)
        print("\nFrom: " + title + " to: " + link)

# for node in G.nodes:
#     print("\n\n--Site--    " + node)
#     for suc in G.successors(node):
#         print("Out " + suc)
#     for ne in G.predecessors(node):
#         print("In " + ne)

pr = page_rank(G, 0.5)

pr = sorted(pr.items(), key=lambda x: x[1], reverse=True)

i = 0
for key, value in pr:
    print(str(value) + "\tPagerank for Site: \t" + key)
    i += 1
    if i > len(pr) - 1:
        break
