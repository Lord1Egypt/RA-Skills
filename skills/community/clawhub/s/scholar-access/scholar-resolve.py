#!/usr/bin/env python3
"""
scholar-resolve.py — Resolve a hostname through the Scholar (scholar.edu.cn / scholar.work)
DNS-over-HTTPS endpoint.

The education-network "学术资源" service runs a smart-DNS at
https://doh.scholar.work/dns-query that maps blocked foreign domains
(github.com, huggingface.co, hub.docker.com, ...) onto a reverse-proxy farm
(205.164.50.x). Connecting to that IP with the real SNI/Host reaches the real
site through the education network's international channel.

Usage:
    scholar-resolve.py <hostname> [qtype]
Examples:
    scholar-resolve.py github.com
    scholar-resolve.py huggingface.co
Output:
    One resolved IP per line (A records). Proxy IPs are in 205.164.50.0/24.
Exit codes:
    0  resolved at least one address
    1  usage error
    2  DoH query failed / no A records
"""
import base64
import socket
import struct
import sys
import urllib.request

DOH_URL = "https://doh.scholar.work/dns-query"
QTYPES = {"A": 1, "AAAA": 28, "CNAME": 5}


def build_query(name: str, qtype: int) -> bytes:
    tid = 0x5A17
    flags = 0x0100  # RD
    header = struct.pack(">HHHHHH", tid, flags, 1, 0, 0, 0)
    qname = b"".join(bytes([len(part)]) + part.encode() for part in name.rstrip(".").split(".")) + b"\x00"
    question = qname + struct.pack(">HH", qtype, 1)
    return header + question


def doh_query(name: str, qtype: int) -> bytes:
    msg = build_query(name, qtype)
    b64 = base64.urlsafe_b64encode(msg).decode().rstrip("=")
    url = f"{DOH_URL}?dns={b64}"
    req = urllib.request.Request(url, headers={"Accept": "application/dns-message"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def decode_name(raw: bytes, offset: int):
    """Decode a (possibly compressed) DNS name starting at offset; returns (name, next_offset)."""
    labels = []
    jumped = False
    next_off = offset
    while True:
        length = raw[next_off]
        if length & 0xC0 == 0xC0:
            pointer = struct.unpack(">H", raw[next_off:next_off + 2])[0] & 0x3FFF
            if not jumped:
                offset = next_off + 2
            next_off = pointer
            jumped = True
        elif length == 0:
            next_off += 1
            break
        else:
            labels.append(raw[next_off + 1:next_off + 1 + length].decode(errors="replace"))
            next_off += 1 + length
    return ".".join(labels), (offset if jumped else next_off)


def parse_answers(raw: bytes, qtype: int):
    ancount = struct.unpack(">H", raw[6:8])[0]
    offset = 12
    # skip question section
    while raw[offset] != 0:
        offset += 1 + raw[offset]
    offset += 1 + 4  # null byte + QTYPE(2) + QCLASS(2)

    results = []
    for _ in range(ancount):
        name, offset = decode_name(raw, offset)
        rtype, rclass, ttl, rdlen = struct.unpack(">HHIH", raw[offset:offset + 10])
        offset += 10
        rdata = raw[offset:offset + rdlen]
        offset += rdlen
        if rtype == 1 and rdlen == 4:
            results.append(("A", socket.inet_ntoa(rdata)))
        elif rtype == 28 and rdlen == 16:
            results.append(("AAAA", socket.inet_ntop(socket.AF_INET6, rdata)))
        elif rtype == 5:
            cname, _ = decode_name(raw, offset - rdlen)
            results.append(("CNAME", cname))
        else:
            results.append((str(rtype), rdlen))
    return results


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    host = sys.argv[1]
    qtype = QTYPES.get((sys.argv[2] if len(sys.argv) > 2 else "A").upper(), 1)
    try:
        raw = doh_query(host, qtype)
    except Exception as e:
        print(f"ERROR: DoH query failed: {e}", file=sys.stderr)
        return 2
    answers = parse_answers(raw, qtype)
    ips = [ip for typ, ip in answers if typ == "A"]
    if not ips:
        print(f"ERROR: no A records for {host}", file=sys.stderr)
        return 2
    for ip in ips:
        print(ip)
    return 0


if __name__ == "__main__":
    sys.exit(main())
