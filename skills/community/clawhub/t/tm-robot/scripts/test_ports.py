import socket

for port in [5890, 5891, 5892]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('192.168.1.13', port))
    sock.close()
    print(f'Port {port}: {"OPEN" if result == 0 else "CLOSED (" + str(result) + ")" }')
