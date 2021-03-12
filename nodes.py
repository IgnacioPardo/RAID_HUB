import os, pickle, json, requests, ast
nodes_loc = os.getenv("nodes_loc")

def clear():
	if os.path.isfile(nodes_loc):
		os.system("rm "+ nodes_loc)
	f = open(nodes_loc, "w")
	f.close()
	pickle.dump({"registered": {}, "relations":{}}, open(nodes_loc, 'wb'))
	return {}

if not os.path.isfile(nodes_loc):
	clear()

def to_str():
	return str(os.stat(nodes_loc).st_size / 1024) + ' KB | ' + str(len(l_nodes())) + ' keys'

def nodes_size():
	return os.stat(nodes_loc).st_size / 1024

def keys_size():
	return len(l_nodes())

def l_nodes():
	nodes = pickle.load(open(nodes_loc, 'rb'))
	return nodes

def u_nodes(nodes):
	pickle.dump(nodes, open(nodes_loc, 'wb'))

def add_node(url):
	nodes = l_nodes()
	if url in node_list():
		for n in nodes["registered"].keys():
			if url == nodes["registered"][n]:
				return n
	if len(nodes["registered"].keys()) == 0:
		index = 0
	else:
		index = max(list(nodes["registered"].keys()))+1 
	nodes["registered"][index] = url
	u_nodes(nodes)
	return index

def node_status(url):
	resp = requests.get(url+"/usage").text
	_node = json.loads(resp)
	return _node["ram"] < 0.9 and _node["disk"] < 0.9

def set_relation(_id):
	nodes = l_nodes()
	for i in nodes["registered"].keys():
		n = nodes["registered"][i]
		if node_status(n):
			if _id:
				nodes["relations"][_id] = n
				u_nodes(nodes)
			return n
	u_nodes(nodes)
	return "no available nodes"

def set_node_data(url, data, _id):
	_id = str(_id)
	#CHECK STATUS OF NODE
	x = requests.post(url+'/set'+(("/"+_id) if _id else ""), data = {'request': json.dumps(data)})
	return json.loads(x.text) 

def rel_node(_id=None):
	nodes = l_nodes()
	if _id in nodes["relations"].keys():
		return nodes["relations"][_id]
	else:
		return set_relation(_id)
	
def _set(data, _id=None):
	node = rel_node(_id)
	resp = set_node_data(node, data, _id)
	print(resp)
	if resp["success"]:
		_id = int(resp["id_set"])
		rel_node(_id)
		return resp
	else:
		resp["error"] = "NODE Error, url: " + node
		return resp

def _get_node(_id):
	nodes = l_nodes()
	return nodes["relations"][int(_id)]

def _get(_id=None):
	if _id:
		node = _get_node(_id)
		#CHECK STATUS OF NODE
		resp = requests.get(node + '/get/'+str(_id)).text
		return resp
	else:
		db = {}
		nodes = node_list()
		for n in nodes:
			#CHECK STATUS OF NODE
			db.update(ast.literal_eval(requests.get(n + '/getAll').text))
		print(db)
		return str(db)

def node_list():
	return l_nodes()["registered"].values()