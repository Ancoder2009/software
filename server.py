import socket
import json
import os
import sys
from time import sleep as wait

def get_files(root):
	di, fi = [], []
	for root, dirs, files in os.walk(root):
		for d in dirs:
			di.append(os.path.join(root, d))    
		for f in files:
			fi.append(os.path.join(root, f))
	return di, fi

port = 5000
host = ''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((host, port))

	s.listen(1)
	conn, addr = s.accept()
	with conn as con:
		print(str(addr[0]) + " has connected to the server!")
		while True:
			msg = con.recv(1248010)
			try:
				parsedmsg = json.loads(msg)
			except:
				con.close()
			try:
				if parsedmsg["method"] == "init":
					if os.path.isdir(parsedmsg["dir"]):
						dirs, files = get_files(parsedmsg["dir"])
						con.send(json.dumps({"method": "file_preflight", "count": len(files), "files": files, "dirs": dirs}).encode())
						wait(.5)
						for i in files:
							with open(i, 'rb') as f:
								file = f.read()
								con.send(file)
								f.close()
							wait(.5)
					else:
						con.send(json.dumps({}).encode())
				elif parsedmsg["method"] == "push":
						if parsedmsg["method"] == "push":
							for i in parsedmsg["dirs"]:
								try:
									os.makedirs(i)
								except:
									pass
							for i in parsedmsg["files"]:
								file = con.recv(12480100)
								with open(i, 'wb') as f:
									print(f"Downloading file {i}.")
									f.write(file)
									print("Downloaded!")
									f.close()
								print("Client Push Complete!")
			except ValueError:
				con.close()