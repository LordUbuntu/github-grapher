# Jacobus Burger (2025-02-09)
# A web crawler to explore and graph social connections on GitHub from
#   a given user page for a specified graph depth, run in parallel
#   for faster performance.
# The start of a larger project that will get it's own repo once I figure
#   out a better name for it and have more time.

# This version will be just a CLI tool to scan and visualize connections rapidly,
#   but in the future I'll do an interactive version with jupyter notebooks
#   and / or some framework like Dash
# (2025-06-30) I need to come back to this project and figure out how to
#   scrape followers and following from github foreach user page...


# Features:
# - command line utility with flags to specify exploration depth, output, and more
# - generate graphs as graphviz (.gz) files
# - record and store network links as .csv and other data formats
# - seperate jupyter notebook for interactive visualization demo using pyvis and ipysigma
# - multiprocessing queue for fast performance
import argparse                 # CLI
import multiprocessing as mp    # multiprocessing for faster execution
# should I use plotly? Maybe for the web interface using DASH?
import graphviz as gv           # generate .gv and .svg files to render graph
import re
import requests as req          # getting requests from site
import bs4                      # parsing site


def get_neighbours(url: str) -> list[str]:
    """returns a list of adjacent URL"""
    # get contents of URL request (GitHub API?)
    res = req.request("GET", url)
    if res.ok:
        html = res.content
    # parse with bs4 for href tags
    soup = bs4.BeautifulSoup(markup=res.content, features="html5lib")
    # extract URL strings into list
    raw_urls = soup.find_all('a', href=True)
    # TODO: how to get the links to other user pages from this info?

    # return list of URL strings
    return urls


# some properties are known about the graph G of GitHub user relations:
# 1. it is a digraph
# 2. it may be cyclical on some subgraphs
# 3. each vertex may be isolated or in some subgraph

# graphviz
# G = gz.DiGraph()
# recursively:
#   G.node(root)
#   G.node(neighbour1)
#   G.edge(root, neighbour1)
#   ...
#   G.node(neighbourN)
#   G.edge(root, neighbourN)
# at the end:
#   G.render(filename=output_name_arg, format=format_arg)

# algorithm:
# - start at current node URL (top of multiprocessing pool queue) (a queue is used to avoid a runaway process)
# - wait for 50ms or so
# - scrape its page for current node username, add this node to graphviz with that name
# - scrape its page for followers / following URLs
# - test connection to that URL and ignore if it fails, otherwise add to queue
# - also add each connected neighbour name to graphviz, and add an edge from current node towards those neighbours
# - explore breadth first search, keeping below a limit defined by the depth argument (or not if an argument of -1 is given)
