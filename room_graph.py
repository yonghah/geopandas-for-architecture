import geopandas as gpd
import matplotlib.pyplot as plt
import os

# read room polygons in esri gdb
gdb_path = os.path.expanduser('~/work/test-data/test.gdb')
rooms = gpd.read_file(gdb_path, layer=2)
print(rooms.head())

# See how rooms look like
fig, ax = plt.subplots()
fig.set_size_inches(12, 12)
ax.axison = False
rooms.plot(ax=ax, linewidth=0.3, column='Shape_Area', cmap='viridis')

# create room's centroids
rooms.geometry.centroid.plot(ax=ax, markersize=8, color='k')
ax.set_aspect('equal')
plt.show()


from shapely.geometry import LineString
lines = {'geometry':[], 'from':[], 'to':[]}
buffer_size = 0.02
for index1, room1 in rooms.iterrows():
    for index2, room2 in rooms.iterrows():
        if room1.geometry.buffer(buffer_size).intersects(room2.geometry.buffer(buffer_size)) \
            and index1 > index2:
            lines["from"].append(room1)
            lines["to"].append(room2)
            lines["geometry"].append(LineString([room1.geometry.centroid, room2.geometry.centroid]))

edges = gpd.GeoDataFrame(lines)

fig, ax = plt.subplots()
fig.set_size_inches(12, 12)
ax.axison = False
rooms.plot(ax=ax, linewidth=0.3, column='Shape_Area', cmap='viridis')
edges.plot(ax=ax, linewidth=0.7, color='r')
rooms.geometry.centroid.plot(ax=ax, markersize=8, color='k')
ax.set_aspect('equal')
plt.show()

# let's create network, not just displaying..
import networkx as nx
