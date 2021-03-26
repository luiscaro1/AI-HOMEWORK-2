import graph as gr
import vgraph as vg
import matplotlib.pyplot as plt

polys = [[gr.Point(0.0, 1.0), gr.Point(3.0, 1.0), gr.Point(1.5, 4.0)],
         [gr.Point(4.0, 4.0), gr.Point(7.0, 4.0), gr.Point(5.5, 8.0)]]

g = vg.VisGraph()
g.build(polys)

# This assignment explores the dijkstra's shortest path algorithm
shortest = g.shortest_path(gr.Point(1.5, 0.0), gr.Point(4.0, 6.0))
print(shortest)

plt.figure()
p1x = [0.0, 3.0, 1.5, 0.0]
p1y = [1.0, 1.0, 4.0, 1.0]

plt.plot(p1x, p1y)

p2x = [4.0, 7.0, 5.5, 4.0]
p2y = [4.0, 4.0, 8.0, 4.0]

plt.plot(p2x, p2y)

# origin
plt.plot(1.5, 0, 'ro')

# goal
plt.plot(4.0, 6.0, 'ro')

path_x = []
path_y = []
for p in shortest:
    path_x.append(p.x)
    path_y.append(p.y)

plt.plot(path_x, path_y)
plt.grid(True)

plt.show()
