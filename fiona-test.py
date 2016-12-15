# import fiona
# import os
# import pprint
import geopandas as gpd
import matplotlib.pyplot as plt

gdb_path = os.path.expanduser('~/work/test-data/test.gdb')

# l = [0,1,2,3]  # Building, Door, Room, Reference
# for i in l:
#     print(i)
#     source = fiona.open(gdb_path, 'r', layer=i)
#     print(len(source))
#     print(source.meta["schema"]["properties"].keys())
#     rec = next(source)
#     pprint.pprint(rec['properties'])

room = gpd.read_file(gdb_path, layer=2)
print(room.head())

room.plot(linewidth=0.7, column='Shape_Area', cmap='viridis')
fig = plt.gcf()
fig.set_size_inches(12, 8)
cur_axes = plt.gca()
cur_axes.axison = False
plt.show()


reference = gpd.read_file(gdb_path, layer=3)
print(reference.head())


reference.plot(linewidth=0.7, color='k')
fig = plt.gcf()
fig.set_size_inches(12, 8)
cur_axes = plt.gca()
cur_axes.axison = False
plt.show()

fig, ax = plt.subplots()
fig.set_size_inches(12, 8)
ax.set_aspect('equal')
ax.axison = False
room.plot(ax=ax, linewidth=0, column='Shape_Area', cmap='viridis')
reference.plot(ax=ax, linewidth=0.7, color='k')
plt.show()
