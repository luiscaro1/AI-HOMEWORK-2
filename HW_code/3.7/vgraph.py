from timeit import default_timer
from sys import stdout, version_info
from multiprocessing import Pool
from tqdm import tqdm
from warnings import warn

from graph import Graph, Edge
from shortest_path import shortest_path
from vv import visible_vertices, point_in_polygon
from vv import closest_point

PYTHON3 = version_info[0] == 3
if PYTHON3:
    xrange = range
    import pickle
else:
    import cPickle as pickle


class VisGraph(object):

    def __init__(self):
        self.graph = None
        self.visgraph = None

    def load(self, filename):

        with open(filename, 'rb') as load:
            self.graph, self.visgraph = pickle.load(load)

    def save(self, filename):

        with open(filename, 'wb') as output:
            pickle.dump((self.graph, self.visgraph), output, -1)

    def build(self, input, workers=1, status=True):

        self.graph = Graph(input)
        self.visgraph = Graph([])

        points = self.graph.get_points()
        batch_size = 10

        if workers == 1:
            for batch in tqdm([points[i:i + batch_size]
                               for i in xrange(0, len(points), batch_size)],
                              disable=not status):
                for edge in _vis_graph(self.graph, batch):
                    self.visgraph.add_edge(edge)
        else:
            pool = Pool(workers)
            batches = [(self.graph, points[i:i + batch_size])
                       for i in xrange(0, len(points), batch_size)]

            results = list(tqdm(pool.imap(_vis_graph_wrapper, batches), total=len(batches),
                                disable=not status))
            for result in results:
                for edge in result:
                    self.visgraph.add_edge(edge)

    def find_visible(self, point):


        return visible_vertices(point, self.graph)

    def update(self, points, origin=None, destination=None):


        for p in points:
            for v in visible_vertices(p, self.graph, origin=origin,
                                      destination=destination):
                self.visgraph.add_edge(Edge(p, v))

    def shortest_path(self, origin, destination):


        origin_exists = origin in self.visgraph
        dest_exists = destination in self.visgraph
        if origin_exists and dest_exists:
            return shortest_path(self.visgraph, origin, destination)
        orgn = None if origin_exists else origin
        dest = None if dest_exists else destination
        add_to_visg = Graph([])
        if not origin_exists:
            for v in visible_vertices(origin, self.graph, destination=dest):
                add_to_visg.add_edge(Edge(origin, v))
        if not dest_exists:
            for v in visible_vertices(destination, self.graph, origin=orgn):
                add_to_visg.add_edge(Edge(destination, v))
        return shortest_path(self.visgraph, origin, destination, add_to_visg)

    def point_in_polygon(self, point):


        return point_in_polygon(point, self.graph)

    def closest_point(self, point, polygon_id, length=0.001):


        return closest_point(point, self.graph, polygon_id, length)


def _vis_graph_wrapper(args):
    try:
        return _vis_graph(*args)
    except KeyboardInterrupt:
        pass


def _vis_graph(graph, points):
    visible_edges = []
    for p1 in points:
        for p2 in visible_vertices(p1, graph, scan='half'):
            visible_edges.append(Edge(p1, p2))
    return visible_edges
