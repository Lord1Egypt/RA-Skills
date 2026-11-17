#!/usr/bin/env python3
"""
scholar-proxy.py — Local HTTPS CONNECT proxy that routes blocked foreign domains
through the Scholar (scholar.edu.cn / scholar.work) reverse-proxy farm.

Why this exists:
    `scholartools` installs a system-wide local DNS (127.0.0.1:53) + a root CA so
    that git / docker / curl transparently reach github.com & friends. That needs
    root. This script provides the same routing as a *user-space* CONNECT proxy,
    so tools can reach proxied domains without touching /etc/hosts or /etc/resolv.conf.

Mechanism:
    1. A client (git, curl, docker, pip, ...) sends `CONNECT github.com:443`.
    2. We resolve github.com through the DoH endpoint https://doh.scholar.work/dns-query.
       - If it maps to a 205.164.50.x proxy IP, we dial that IP (SNI stays github.com).
       - Otherwise we dial the real host directly.
    3. We reply "200 Connection Established" and pipe bytes both ways.

Usage:
    scholar-proxy.py [--listen 127.0.0.1:1080]
Then point tools at it, e.g.:
    export https_proxy=http://127.0.0.1:1080 http_proxy=http://127.0.0.1:1080
    GIT_SSL_NO_VERIFY=1 git clone https://github.com/octocat/Hello-World.git
    HTTPS_PROXY=http://127.0.0.1:1080 curl https://github.com/ -k
"""
import argparse
import base64
import select
import socket
import socketserver
import struct
import threading
import urllib.request

DOH_URL = "https://doh.scholar.work/dns-query"
PROXY_NET = "205.164.50."  # scholar reverse-proxy farm


def doh_resolve(host: str) -> str | None:
    """Return an IPv4 address for `host` via the scholar DoH endpoint, else None."""
    tid = 0x7E11
    header = struct.pack(">HHHHHH", tid, 0x0100, 1, 0, 0, 0)
    qname = b"".join(bytes([len(p)]) + p.encode() for p in host.rstrip(".").split(".")) + b"\x00"
    msg = header + qname + struct.pack(">HH", 1, 1)
    b64 = base64.urlsafe_b64encode(msg).decode().rstrip("=")
    req = urllib.request.Request(f"{DOH_URL}?dns={b64}", headers={"Accept": "application/dns-message"})
    try:
        raw = urllib.request.urlopen(req, timeout=10).read()
    except Exception:
        return None
    if struct.unpack(">H", raw[6:8])[0] == 0:
        return None
    off = 12
    while raw[off] != 0:
        off += 1 + raw[off]
    off += 1 + 4
    ancount = struct.unpack(">H", raw[6:8])[0]
    for _ in range(ancount):
        if raw[off] & 0xC0 == 0xC0:
            off += 2
        else:
            while raw[off] != 0:
                off += 1 + raw[off]
            off += 1
        rtype, _rclass, _ttl, rdlen = struct.unpack(">HHIH", raw[off:off + 10])
        off += 10
        rdata = raw[off:off + rdlen]
        off += rdlen
        if rtype == 1 and rdlen == 4:
            return socket.inet_ntoa(rdata)
    return None


def dial_target(host: str, port: int) -> socket.socket:
    """Connect to `host:port`, preferring the scholar proxy IP when applicable."""
    ip = doh_resolve(host)
    if ip:
        return socket.create_connection((ip, port), timeout=20)
    # fall back to the OS resolver (works for non-blocked / non-proxied hosts)
    infos = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
    for fam, _, proto, _, addr in infos:
        s = socket.socket(fam, socket.SOCK_STREAM)
        s.settimeout(20)
        try:
            s.connect(addr)
            return s
        except OSError:
            s.close()
    raise OSError(f"cannot connect to {host}:{port}")


class ConnectHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client = self.request
        client.settimeout(30)
        try:
            data = client.recv(65536)
            if not data or not data.startswith(b"CONNECT"):
                return
            line = data.split(b"\r\n", 1)[0].decode(errors="replace")
            _, target, _ = line.split(" ", 2)
            host, port = target.rsplit(":", 1)
            port = int(port)
        except Exception:
            client.close()
            return
        try:
            upstream = dial_target(host, port)
        except Exception:
            client.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
            client.close()
            return
        client.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        upstream.settimeout(None)
        client.settimeout(None)
        try:
            self._pipe(client, upstream)
        finally:
            for s in (client, upstream):
                try:
                    s.close()
                except OSError:
                    pass

    @staticmethod
    def _pipe(a, b):
        while True:
            r, _, _ = select.select([a, b], [], [], 60)
            if not r:
                return
            for src in r:
                dst = b if src is a else a
                try:
                    chunk = src.recv(65536)
                except OSError:
                    return
                if not chunk:
                    return
                try:
                    dst.sendall(chunk)
                except OSError:
                    return


class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    ap = argparse.ArgumentParser(description="Scholar CONNECT proxy")
    ap.add_argument("--listen", default="127.0.0.1:1080", help="bind address:port (default 127.0.0.1:1080)")
    args = ap.parse_args()
    host, port = args.listen.rsplit(":", 1)
    with ThreadedServer((host, int(port)), ConnectHandler) as server:
        print(f"scholar-proxy listening on {host}:{port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
