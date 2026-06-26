import requests
import socket
import os

host = os.environ.get("TUNNEL_HOST", "127.0.0.1")
http_port = os.environ.get("TUNNEL_HTTP_PORT", "8080")
token = os.environ.get("TUNNEL_AGENT_TOKEN")

# 1. 获取临时端口
resp = requests.post(f"http://{host}:{http_port}/api/session", json={"token": token})
port = resp.json()["port"]

# 2. 立即连接
s = socket.socket()
s.connect((host, port))
s.send(b"ls -la\n")
print(s.recv(4096).decode())
s.close()