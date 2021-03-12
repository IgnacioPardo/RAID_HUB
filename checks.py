import sched, time, requests
from nodes import node_list

#Threading
from threading import Thread

s = sched.scheduler(time.time, time.sleep)
def check_all(sc): 
	for n in node_list():
		while (stat := 'class="RAID_NODE"' not in (resp := requests.get(n).text)):
			continue
	s.enter(60*5, 1, check_all, (sc,))

def loop():
	s.enter(60*5, 1, check_all, (s,))
	s.run()

def keep_alive():
	t = Thread(target=loop)
	t.start()

keep_alive()