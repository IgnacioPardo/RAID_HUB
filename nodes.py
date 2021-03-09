import os, pickle
nodes_loc = os.getenv("nodes_loc")
if not os.path.isfile(nodes_loc):
		f = open(nodes_loc, "w")
		f.close()

def to_str():
	return str(os.stat(nodes_loc).st_size / 1024) + ' KB | ' + str(len(l_nodes())) + ' keys'

def nodes_size():
	return os.stat(nodes_loc).st_size / 1024

def keys_size():
	return len(l_nodes())

def clear():
	os.system("rm "+ nodes_loc)
	f = open(nodes_loc, "w")
	f.close()
	pickle.dump({}, open(nodes_loc, 'wb'))
	return {}

def l_nodes():
	nodes = pickle.load(open(nodes_loc, 'rb'))
	return nodes

def u_nodes(nodes):
	pickle.dump(nodes, open(nodes_loc, 'wb'))

def add_node(url):
	nodes = l_nodes()
	index = max(list(nodes.keys()))+1 if len(nodes) else 0
	nodes[index] = url
	u_nodes(nodes)
	print(index)
	return index