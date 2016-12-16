import geopandas as gpd
import networkx as nx
import pandas as pd
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
rooms.plot(ax=ax, linewidth=0.3, color='#DDDDDD')
reference = gpd.read_file(gdb_path, layer=3)
reference.plot(ax=ax, linewidth=0.7, color='k')
ax.set_aspect('equal')
plt.show()


# create room's centroids
fig, ax = plt.subplots()
fig.set_size_inches(12, 12)
ax.axison = False
rooms.plot(ax=ax, linewidth=0.3, color='#DDDDDD')
rooms.geometry.centroid.plot(ax=ax, markersize=6, color='#6677AA')
ax.set_aspect('equal')
plt.show()

# create edges if two room polygons touch each other
from shapely.geometry import LineString
lines = {'geometry':[], 'from':[], 'to':[]}
buffer_size = 0.02
for index1, room1 in rooms.iterrows():
    for index2, room2 in rooms.iterrows():
        if room1.geometry.buffer(buffer_size).intersects(room2.geometry.buffer(buffer_size)) \
            and index1 > index2:
            lines["from"].append(index1)
            lines["to"].append(index2)
            lines["geometry"].append(LineString([room1.geometry.centroid, room2.geometry.centroid]))

edges = gpd.GeoDataFrame(lines)



# let's create network, not just displaying..
room_network = nx.Graph()
for i, edge in edges.iterrows():
    room_network.add_edge(edge["from"], edge["to"])

# calculate closeness and add the values to rooms
closeness = nx.closeness_centrality(room_network)
rooms['closeness'] = pd.Series(closeness)

# color rooms by closeness
fig, ax = plt.subplots()
fig.set_size_inches(12, 12)
ax.axison = False
rooms.plot(ax=ax, linewidth=0.3, column='closeness', cmap='coolwarm')
edges.plot(ax=ax, linewidth=0.3, color='#888888')
rooms.geometry.centroid.plot(ax=ax, markersize=6, color='#DDDDDD')
ax.set_aspect('equal')
plt.show()


comm = nx.girvan_newman(room_network)
print(comm)
