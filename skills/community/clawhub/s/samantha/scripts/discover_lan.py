#!/usr/bin/env python3
"""局域网设备发现"""
import socket
import time

SSDP_ADDR = '239.255.255.250'
SSDP_PORT = 1900

msg = '''M-SEARCH * HTTP/1.1
HOST: 239.255.255.250:1900
MAN: "ssdp:discover"
MX: 3
ST: ssdp:all

'''

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)
sock.sendto(msg.encode(), (SSDP_ADDR, SSDP_PORT))

print('局域网搜索中...')
found = []
try:
    while True:
        data, addr = sock.recvfrom(4096)
        msg = data.decode('utf-8', errors='ignore')
        if 'xiaomi' in msg.lower() or 'mi-' in msg.lower() or '小爱' in msg:
            print(f'找到: {addr[0]}')
            print(msg[:300])
            print('---')
            found.append(addr[0])
except socket.timeout:
    print('搜索完成')

sock.close()

if not found:
    print('\n未发现小米设备，尝试 ping 扫描常用网段...')
    # 尝试常见的本地 IP 段
    import subprocess
    for i in range(1, 20):
        ip = f'192.168.31.{i}'
        result = subprocess.run(['ping', '-n', '1', '-w', '200', ip], 
                               capture_output=True, text=True)
        if 'TTL' in result.stdout or 'ttl' in result.stdout.lower():
            print(f'活跃设备: {ip}')
