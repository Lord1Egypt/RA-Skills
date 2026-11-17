#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yotta-recon（元析）—— 零依赖自研网络侦察引擎
====================================================

跨智能体的网络侦察能力：端口 / 服务 / 版本指纹探测。纯 Python 3.8+ 标准库实现，
不依赖 nmap 等任何外部工具，Windows / Linux / macOS 通用。

特性
----
- TCP connect 端口扫描（并发、可限速、自定义端口集 / CIDR / 主机名）
- 服务指纹：banner grab + 按端口协议探测（HTTP / SSH / FTP / SMTP / POP3 / IMAP /
  Redis / MySQL / PostgreSQL / TLS / MongoDB 等）
- 版本提取与已知风险提示（只提示存在公开已知漏洞，不提供利用细节）
- Scope Guard 授权纪律：未授权目标默认拒绝，授权声明 + 双保险校验
- 输出：文本 / JSON / Markdown 报告；扫描留痕（报告头含时间与授权来源）

用法
----
  python3 scripts/yotta_recon.py scan --targets 127.0.0.1 --top 100
  python3 scripts/yotta_recon.py scan --targets 192.168.1.0/30 --scope scope.txt --yes
  python3 scripts/yotta_recon.py fingerprint --host 127.0.0.1 --port 80
  python3 scripts/yotta_recon.py check-scope --targets 8.8.8.8 --scope scope.txt
  python3 scripts/yotta_recon.py local
  python3 scripts/yotta_recon.py list-ports
  python3 scripts/yotta_recon.py --version

Windows 下用 python 代替 python3。
"""

import argparse
import concurrent.futures as cf
import ipaddress
import json
import os
import random
import re
import socket
import string
import sys
import time
from datetime import datetime, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

VERSION = "0.1.10"
TOOL = "yotta-recon"
TOOL_CN = "元析"

# ---------------------------------------------------------------------------
# 常用端口表：端口 -> 服务名（首版内置，够日常资产盘点用）
# ---------------------------------------------------------------------------
TOP_PORTS = {
    20: "ftp-data", 21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp",
    53: "dns", 67: "dhcp", 68: "dhcp", 69: "tftp", 80: "http",
    110: "pop3", 111: "rpcbind", 123: "ntp", 135: "msrpc", 137: "netbios-ns",
    138: "netbios-dgm", 139: "netbios-ssn", 143: "imap", 161: "snmp",
    162: "snmptrap", 179: "bgp", 194: "irc", 389: "ldap", 443: "https",
    445: "microsoft-ds", 465: "smtps", 514: "syslog", 515: "printer",
    548: "afp", 554: "rtsp", 587: "smtp", 631: "ipp", 636: "ldaps",
    873: "rsync", 993: "imaps", 995: "pop3s", 1025: "msrpc",
    1080: "socks-proxy", 1099: "rmi", 1194: "openvpn", 1433: "mssql",
    1434: "ms-sql-m", 1521: "oracle", 1723: "pptp", 2049: "nfs",
    2082: "cpanel", 2083: "cpanel-ssl", 2181: "zookeeper", 2222: "ssh-alt",
    2375: "docker", 2376: "docker-tls", 3000: "http-alt", 3128: "squid",
    3306: "mysql", 3389: "rdp", 3690: "svn", 4369: "epmd",
    5000: "http-alt", 5001: "http-alt", 5432: "postgresql", 5555: "adb",
    5601: "kibana", 5672: "amqp", 5900: "vnc", 5984: "couchdb",
    6000: "x11", 6379: "redis", 6443: "kubernetes", 7001: "weblogic",
    7002: "weblogic-ssl", 7070: "http-alt", 8000: "http-alt",
    8008: "http-alt", 8009: "ajp", 8080: "http-alt", 8081: "http-alt",
    8082: "http-alt", 8083: "http-alt", 8088: "http-alt", 8090: "http-alt",
    8161: "activemq", 8443: "https-alt", 8500: "consul", 8888: "http-alt",
    9000: "http-alt", 9001: "http-alt", 9042: "cassandra", 9090: "prometheus",
    9092: "kafka", 9200: "elasticsearch", 9300: "elasticsearch",
    9418: "git", 9999: "http-alt", 10000: "webmin", 11211: "memcached",
    15672: "rabbitmq", 16379: "redis-alt", 27017: "mongodb", 28017: "mongodb",
    50000: "sap", 50070: "hadoop-namenode",
}

# 视为 HTTP 服务并发送 HTTP 探测的端口
HTTP_PORTS = {
    80, 443, 3000, 5000, 5001, 5601, 6443, 7001, 7002, 7070, 8000, 8008,
    8080, 8081, 8082, 8083, 8088, 8090, 8161, 8443, 8500, 8888, 9000, 9001,
    9090, 9200, 9300, 9999, 10000, 15672, 28017, 50000, 50070,
}

# 已知风险映射：(product 小写, 版本前缀) -> (severity, 提示)
# 仅用于提示「该版本存在公开已知漏洞，请人工核实」，不提供利用细节。
KNOWN_RISKS = [
    (("proftpd", "1.3.5"), 3, "ProFTPD 1.3.5 存在公开已知漏洞（CVE-2015-3306），请人工核实补丁状态。"),
    (("vsftpd", "2.3.4"), 3, "vsftpd 2.3.4 存在公开已知漏洞（CVE-2011-2523），请人工核实。"),
    (("openssh", "5."), 2, "OpenSSH 5.x 已停止维护，存在多项公开已知漏洞，建议升级并人工核实。"),
    (("openssh", "6."), 2, "OpenSSH 6.x 已停止维护，存在多项公开已知漏洞，建议升级并人工核实。"),
    (("openssh", "7."), 1, "OpenSSH 7.x 较旧，建议人工核实补丁状态并考虑升级。"),
    (("apache", "2.4.7"), 1, "Apache 2.4.7 较旧，存在多项公开已知漏洞，建议人工核实并升级。"),
    (("apache", "2.2."), 1, "Apache 2.2.x 已停止维护，建议升级并人工核实。"),
    (("nginx", "1.0."), 1, "nginx 1.0.x 已停止维护，建议升级并人工核实。"),
    (("php", "5."), 2, "PHP 5.x 已停止维护，存在多项公开已知漏洞，建议升级并人工核实。"),
    (("mysql", "5.5"), 1, "MySQL 5.5 已停止维护，建议人工核实并升级。"),
    (("mysql", "5.6"), 1, "MySQL 5.6 已停止维护，建议人工核实并升级。"),
    (("proftpd", "1.3.3"), 2, "ProFTPD 1.3.3 较旧，存在公开已知漏洞，建议人工核实。"),
    (("vsftpd", "2.3.2"), 2, "vsftpd 2.3.2 存在公开已知漏洞（CVE-2011-0993 等），建议人工核实。"),
]

SEVERITY_LABEL = {0: "none", 1: "low", 2: "medium", 3: "high"}

# ---------------------------------------------------------------------------
# 目标与端口解析
# ---------------------------------------------------------------------------

def parse_ports(spec, default_top=100):
    """解析端口说明 -> 有序去重列表。

    支持：'22,80,443' / '1-1024' / 'top' / 'top:50'（默认 'top:100'）。
    """
    spec = (spec or "").strip().lower()
    if not spec:
        spec = "top"
    if spec.startswith("top"):
        n = default_top
        if ":" in spec:
            try:
                n = int(spec.split(":", 1)[1])
            except ValueError:
                raise ValueError("top 端口数量必须为整数: %s" % spec)
        if n < 1:
            raise ValueError("top 端口数量必须 >= 1")
        return sorted(TOP_PORTS.keys())[:n]
    ports = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, _, hi = part.partition("-")
            try:
                lo_i, hi_i = int(lo), int(hi)
            except ValueError:
                raise ValueError("非法端口范围: %s" % part)
            if lo_i < 1 or hi_i > 65535 or lo_i > hi_i:
                raise ValueError("非法端口范围: %s" % part)
            ports.extend(range(lo_i, hi_i + 1))
        else:
            try:
                p = int(part)
            except ValueError:
                raise ValueError("非法端口: %s" % part)
            if p < 1 or p > 65535:
                raise ValueError("非法端口: %s" % part)
            ports.append(p)
    return sorted(set(ports))


def expand_target(item):
    """单个目标字符串 -> host 列表（CIDR 自动展开，保留顺序）。"""
    item = item.strip()
    if "/" in item:
        try:
            net = ipaddress.ip_network(item, strict=False)
        except ValueError:
            raise ValueError("非法 CIDR: %s" % item)
        return [str(h) for h in net.hosts()]
    return [item]


def parse_targets(spec, target_file=None):
    """解析目标 -> (hosts, source_desc)。

    支持 IP / CIDR / 主机名，逗号分隔；--target-list 文件每行一个，# 为注释。
    """
    hosts = []
    sources = []
    if target_file:
        if not os.path.isfile(target_file):
            raise ValueError("目标文件不存在: %s" % target_file)
        with open(target_file, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                hosts.extend(expand_target(line))
        sources.append("file:%s" % target_file)
    if spec:
        for item in spec.split(","):
            item = item.strip()
            if item:
                hosts.extend(expand_target(item))
        sources.append("cli")
    if not hosts:
        raise ValueError("未指定目标（--targets 或 --target-list 至少其一）")
    seen, out = set(), []
    for h in hosts:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out, ";".join(sources) or "cli"


# ---------------------------------------------------------------------------
# Scope Guard：授权纪律（未授权目标默认拒绝）
# ---------------------------------------------------------------------------

def is_ip_literal(host):
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def classify_ip(ip_str):
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return "unknown"
    if ip.is_loopback:
        return "loopback"
    if ip.is_link_local:
        return "link_local"
    if ip.is_private:
        return "private"
    if ip.is_multicast:
        return "multicast"
    if ip.is_reserved:
        return "reserved"
    if ip.is_unspecified:
        return "unspecified"
    return "public"


def resolve_host(host):
    """主机名 -> IP 列表；IP 字面量原样返回。失败抛 ValueError。"""
    if is_ip_literal(host):
        return [host]
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        raise ValueError("无法解析主机名: %s" % host)
    ips = []
    for info in infos:
        ip = info[4][0]
        if ip not in ips:
            ips.append(ip)
    return ips


class ScopeGuard(object):
    """授权范围判定（Scope Guard 硬机制）。

    放行规则（满足其一）：
      1. 目标是回环地址（127.0.0.0/8、::1）—— 本机自测默认放行；
      2. 目标在 --scope 授权文件声明的 IP / CIDR / 主机名范围内；
      3. 用户显式 --assume-authorized（声明已获授权）且通过确认
         （--yes 或交互确认）。

    未授权目标默认拒绝，绝不静默放行；拒绝时退出码 3。
    """

    def __init__(self, scope_file=None, assume_authorized=False, yes=False):
        self.scope_file = scope_file
        self.assume_authorized = assume_authorized
        self.yes = yes
        self.scope_networks = []
        self.scope_hosts = set()
        if scope_file:
            self._load_scope(scope_file)

    def _load_scope(self, path):
        if not os.path.isfile(path):
            raise ValueError("授权范围文件不存在: %s" % path)
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "/" in line:
                    try:
                        self.scope_networks.append(ipaddress.ip_network(line, strict=False))
                    except ValueError:
                        raise ValueError("授权范围文件含非法 CIDR: %s" % line)
                else:
                    self.scope_hosts.add(line)

    def in_scope_ip(self, ip_str):
        """单个 IP 是否在授权范围（loopback 恒放行）。"""
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            return False
        if ip.is_loopback:
            return True
        if ip_str in self.scope_hosts or str(ip) in self.scope_hosts:
            return True
        for net in self.scope_networks:
            if ip in net:
                return True
        return False

    def check_host(self, host):
        """单个目标是否放行。返回 (allowed, reason)。

        主机名：域名本身在 scope_hosts 直接放行；否则要求解析出的全部 IP
        都在授权范围（保守）。
        """
        if self.assume_authorized:
            return True, "assume-authorized"
        if host in self.scope_hosts:
            return True, "scope-host:%s" % host
        try:
            ips = resolve_host(host)
        except ValueError as exc:
            return False, str(exc)
        for ip in ips:
            if not self.in_scope_ip(ip):
                return False, "目标 %s(%s) 不在授权范围" % (host, ip)
        return True, "ok"

    def partition(self, hosts):
        """目标列表 -> (allowed, [(host, reason)])。无交互确认。"""
        allowed, denied = [], []
        for h in hosts:
            ok, reason = self.check_host(h)
            if ok:
                allowed.append(h)
            else:
                denied.append((h, reason))
        return allowed, denied

    def confirm_or_partition(self, hosts, interactive=True):
        """带确认的授权判定。

        非回环且无授权声明的目标：交互场景提示用户确认；非交互场景直接拒绝。
        返回 (allowed, [(host, reason)])。
        """
        allowed, denied = [], []
        pending = []
        pending_reasons = {}
        for h in hosts:
            ok, reason = self.check_host(h)
            if ok:
                allowed.append(h)
            else:
                pending.append(h)
                pending_reasons[h] = reason
        if pending and interactive and not self.yes:
            if self._confirm(pending):
                allowed.extend(pending)
            else:
                denied.extend((h, pending_reasons[h]) for h in pending)
        else:
            denied.extend((h, pending_reasons[h]) for h in pending)
        return allowed, denied

    def _confirm(self, hosts):
        print("=" * 68, file=sys.stderr)
        print("Scope Guard 授权确认", file=sys.stderr)
        print("以下目标不在已声明授权范围内：", file=sys.stderr)
        for h in hosts[:10]:
            print("  - %s" % h, file=sys.stderr)
        if len(hosts) > 10:
            print("  ... 等共 %d 个" % len(hosts), file=sys.stderr)
        print("仅对已获明确授权的目标进行侦察；未经授权扫描他人系统", file=sys.stderr)
        print("违反《网络安全法》与《刑法》第 285/286 条，后果自负。", file=sys.stderr)
        print("确认已获授权？输入 y 继续，其它任意键拒绝：", file=sys.stderr)
        try:
            ans = input("")
        except EOFError:
            return False
        return ans.strip().lower() in ("y", "yes")


# ---------------------------------------------------------------------------
# TCP 探测与扫描
# ---------------------------------------------------------------------------

def tcp_connect(host, port, timeout):
    """TCP connect 探测，返回 (open, err)。"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, None
    except socket.timeout:
        return False, "timeout"
    except OSError as exc:
        return False, str(exc)


def _recv(sock, size=2048, timeout=1.2):
    try:
        sock.settimeout(timeout)
        return sock.recv(size)
    except Exception:
        return b""


def _send(sock, payload):
    try:
        sock.sendall(payload)
    except Exception:
        pass


def _http_probe(sock):
    """发 HTTP/1.0 GET，返回响应文本（截断）。"""
    _send(sock, b"GET / HTTP/1.0\r\nHost: recon\r\nUser-Agent: yotta-recon/0.1\r\n\r\n")
    chunks = []
    try:
        sock.settimeout(1.2)
        while True:
            data = sock.recv(4096)
            if not data:
                break
            chunks.append(data)
            if len(b"".join(chunks)) > 8192:
                break
    except Exception:
        pass
    return b"".join(chunks)


def _redis_probe(sock):
    _send(sock, b"PING\r\n")
    return _recv(sock)


def _smtp_probe(sock):
    data = _recv(sock)
    _send(sock, b"EHLO recon\r\n")
    data2 = _recv(sock)
    return data + data2


def probe_service(host, port, timeout):
    """对单个开放端口做指纹探测。

    返回 dict: product / version / service / banner（banner 为截断文本）。
    """
    result = {"product": None, "version": None, "service": None, "banner": None}
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            s.settimeout(timeout)
            banner = _recv(s)
            raw = banner
            if port in HTTP_PORTS or looks_like_http(banner):
                resp = _http_probe(s)
                if resp:
                    raw = resp
            elif port == 6379:
                resp = _redis_probe(s)
                if resp:
                    raw = resp
            elif port in (25, 587) or looks_like_smtp(banner):
                resp = _smtp_probe(s)
                if resp:
                    raw = resp
            elif not raw:
                # 无主动 banner：试探 HTTP（非标准端口上的 Web 服务常见）
                resp = _http_probe(s)
                if resp and looks_like_http(resp):
                    raw = resp
            text = decode_banner(raw)
            product, version = identify_service(port, text)
            result["product"] = product
            result["version"] = version
            result["service"] = port_service(port)
            result["banner"] = text[:500] or None
    except Exception:
        pass
    return result


def looks_like_http(banner):
    low = banner[:64].lower()
    return low.startswith(b"http/") or b"<!doctype" in low or b"<html" in low


def looks_like_smtp(banner):
    low = banner[:64].lower()
    return low.startswith(b"220") and (b"esmtp" in low or b"smtp" in low)


def decode_banner(raw):
    if not raw:
        return ""
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode("utf-8", errors="replace")


def port_service(port):
    return TOP_PORTS.get(port, "unknown")


def identify_service(port, text):
    """从 banner 文本 + 端口推断 (product, version)。"""
    low = text.lower()

    # TLS 握手：首字节 0x16 = SSLv3/TLS handshake
    if text[:1] == "\x16":
        return "tls", None

    # MySQL 握手：首字节 0x0a，随后协议版本与版本串
    if text[:1] == "\x0a":
        body = text[1:]
        parts = body.split("\x00")
        if parts and parts[0].strip():
            ver = parts[0].strip()
            return "mysql", ver

    # Redis
    if low.startswith("+pong"):
        return "redis", None

    # HTTP（取最后一个 Server 头，自定义值通常在后）
    headers = re.findall(r"server:\s*([^\r\n]+)", low)
    if headers:
        return parse_server_header(headers[-1].strip())

    # SSH
    m = re.search(r"ssh-\d\.\d[-\s]*([^\r\n]+)", low)
    if m:
        ident = m.group(1)
        m2 = re.search(r"openssh[_-]?([\d.]+)", ident)
        if m2:
            return "openssh", m2.group(1)
        m3 = re.search(r"dropbear[_-]?([\d.]+)", ident)
        if m3:
            return "dropbear", m3.group(1)
        return "ssh", None

    # FTP
    if (low.startswith("220") or low.startswith("220-")) and "ftp" in low:
        m = re.search(r"proftpd[ /]?([\d.]+)", low)
        if m:
            return "proftpd", m.group(1)
        m = re.search(r"vsftpd[ /]?([\d.]+)", low)
        if m:
            return "vsftpd", m.group(1)
        m = re.search(r"pure-ftpd[ /]?([\d.]+)", low)
        if m:
            return "pure-ftpd", m.group(1)
        m = re.search(r"filezilla[ /]?([\d.]+)", low)
        if m:
            return "filezilla", m.group(1)
        return "ftp", None

    # SMTP
    if low.startswith("220") and ("esmtp" in low or "smtp" in low or "mail" in low):
        for prod in ("postfix", "exim", "sendmail", "qmail", "microsoft ews", "hMailServer"):
            if prod in low:
                m = re.search(prod.replace(" ", r"\s") + r"[ /]?([\d.]+)", low)
                return prod.replace(" ", "-"), (m.group(1) if m else None)
        return "smtp", None

    # POP3 / IMAP
    if low.startswith("+ok"):
        m = re.search(r"dovecot", low)
        if m:
            return "dovecot-pop3", None
        return "pop3", None
    if low.startswith("* ok"):
        m = re.search(r"dovecot", low)
        if m:
            return "dovecot-imap", None
        return "imap", None

    # PostgreSQL
    if "postgresql" in low or "postgres" in low:
        m = re.search(r"postgres(ql)?[ /_]?([\d.]+)", low)
        return "postgresql", (m.group(2) if m else None)

    # MongoDB
    if "mongodb" in low:
        return "mongodb", None

    # 通用版本模式：product/version 或 product version
    m = re.search(r"([a-z][a-z0-9_.+-]{1,30})[/\s][v]?(\d+(?:\.\d+){1,4})", low)
    if m:
        return m.group(1).lower(), m.group(2)

    return None, None


def parse_server_header(server):
    """解析 Server 头，如 'Apache/2.4.7 (Ubuntu)' / 'nginx/1.18.0'。"""
    low = server.lower()
    m = re.search(r"([a-z][a-z0-9_.-]*)/([\d.]+)", low)
    if m:
        return m.group(1), m.group(2)
    m = re.search(r"([a-z][a-z0-9_.-]*)", low)
    if m:
        return m.group(1), None
    return "http", None


def assess_risk(product, version):
    """按已知风险映射评估。返回 (severity, note)。"""
    if not product or not version:
        return 0, None
    p = product.lower()
    for (prod, prefix), sev, note in KNOWN_RISKS:
        if p == prod and version.startswith(prefix):
            return sev, note
    return 0, None


def scan_target(host, ports, timeout, concurrency, rate=None, probe=True):
    """扫描单个主机的端口列表。返回 {host, ports: [...]}。"""
    opened = []
    start = time.time()

    def work(port):
        if rate:
            time.sleep(rate)
        ok, err = tcp_connect(host, port, timeout)
        if not ok:
            return None
        entry = {"port": port, "state": "open", "service": port_service(port)}
        if probe:
            fp = probe_service(host, port, min(timeout + 0.8, 3.0))
            entry["product"] = fp["product"]
            entry["version"] = fp["version"]
            entry["banner"] = fp["banner"]
            sev, note = assess_risk(fp["product"], fp["version"])
            entry["risk"] = sev
            entry["risk_label"] = SEVERITY_LABEL[sev]
            entry["note"] = note
        else:
            entry["risk"] = 0
            entry["risk_label"] = "none"
            entry["note"] = None
        return entry

    with cf.ThreadPoolExecutor(max_workers=concurrency) as ex:
        for res in ex.map(work, ports):
            if res is not None:
                opened.append(res)
    opened.sort(key=lambda e: e["port"])
    return {
        "host": host,
        "ports": opened,
        "duration_ms": int((time.time() - start) * 1000),
        "port_count": len(opened),
    }


def scan_targets(hosts, ports, timeout, concurrency, rate=None, probe=True):
    results = []
    for h in hosts:
        results.append(scan_target(h, ports, timeout, concurrency, rate, probe))
    return results


# ---------------------------------------------------------------------------
# 本机监听端口（local）—— 读取本机状态，不主动扫描
# ---------------------------------------------------------------------------

def local_listen_ports():
    """返回本机监听端口列表 [{proto, local, port, state, pid}]。

    Linux/macOS 读 /proc/net/tcp、/proc/net/tcp6（零外部依赖）；
    Windows 用系统自带 netstat（只读查询）。
    """
    entries = []
    if os.path.exists("/proc/net/tcp") or os.path.exists("/proc/net/tcp6"):
        for path in ("/proc/net/tcp", "/proc/net/tcp6"):
            if os.path.exists(path):
                entries.extend(_parse_proc_tcp(path))
        return entries
    entries.extend(_netstat_ports())
    return entries


def _parse_proc_tcp(path):
    out = []
    proto = "tcp6" if path.endswith("tcp6") else "tcp"
    try:
        with open(path, "r", encoding="ascii", errors="ignore") as fh:
            lines = fh.readlines()[1:]
    except Exception:
        return out
    for line in lines:
        parts = line.split()
        if len(parts) < 4:
            continue
        local = parts[1]
        st = parts[3]
        if st != "0A":  # LISTEN
            continue
        ip_hex, _, port_hex = local.partition(":")
        try:
            port = int(port_hex, 16)
        except ValueError:
            continue
        ip = _hex_ip_to_str(ip_hex, proto)
        out.append({
            "proto": proto, "local": ip, "port": port,
            "state": "LISTEN", "pid": None,
        })
    return out


def _hex_ip_to_str(ip_hex, proto):
    try:
        if proto == "tcp":
            b = bytes.fromhex(ip_hex)
            return "%d.%d.%d.%d" % (b[3], b[2], b[1], b[0])
        b = bytes.fromhex(ip_hex)
        words = ["%x%04x" % (b[i + 2], b[i]) for i in (0, 4, 8, 12)]
        return ":".join(words)
    except Exception:
        return ip_hex


def _netstat_ports():
    import subprocess
    out = []
    for cmd in (["netstat", "-ano"], ["ss", "-tln"]):
        try:
            proc = subprocess.run(cmd, capture_output=True, timeout=8,
                                  creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            if proc.returncode != 0:
                continue
            text = proc.stdout.decode("utf-8", errors="ignore")
            for line in text.splitlines():
                low = line.lower().strip()
                if not (low.startswith("tcp") or low.startswith("udp")):
                    continue
                if "listen" not in low and "listening" not in low:
                    continue
                parts = line.split()
                if len(parts) < 4:
                    continue
                proto = parts[0].lower()
                local = parts[1]
                if ":" in local and local.count(":") >= 2:
                    port = local.rsplit(":", 1)[1]
                elif "." in local:
                    port = local.rsplit(".", 1)[1]
                else:
                    continue
                try:
                    port_i = int(port)
                except ValueError:
                    continue
                pid = parts[-1] if parts[-1].isdigit() else None
                out.append({
                    "proto": proto, "local": local, "port": port_i,
                    "state": "LISTEN", "pid": pid,
                })
            if out:
                break
        except Exception:
            continue
    # 去重
    seen, uniq = set(), []
    for e in out:
        key = (e["proto"], e["local"], e["port"])
        if key in seen:
            continue
        seen.add(key)
        uniq.append(e)
    return uniq


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------

def build_json(meta, results, denied):
    return {
        "tool": TOOL,
        "version": VERSION,
        "generated_at": meta["generated_at"],
        "scan_id": meta["scan_id"],
        "authorization": meta["authorization"],
        "summary": {
            "hosts": len(results),
            "open_ports": sum(r["port_count"] for r in results),
            "denied_targets": len(denied),
        },
        "denied": [{"host": h, "reason": r} for h, r in denied],
        "results": results,
    }


def format_text(results, denied):
    lines = []
    if denied:
        lines.append("## Scope Guard 拒绝的目标")
        for h, r in denied:
            lines.append("  - %s : %s" % (h, r))
        lines.append("")
    for r in results:
        lines.append("## %s" % r["host"])
        if not r["ports"]:
            lines.append("  （无开放端口 / 无响应）")
            continue
        lines.append("  PORT   STATE SERVICE     VERSION")
        for e in r["ports"]:
            ver = e.get("version") or "-"
            prod = e.get("product") or e.get("service") or "-"
            lines.append("  %-6d open  %-11s %s" % (e["port"], prod, ver))
        lines.append("")
    return "\n".join(lines)


def write_report(path, meta, results, denied):
    lines = []
    lines.append("# %s 侦察报告" % TOOL_CN)
    lines.append("")
    lines.append("- 工具：%s v%s" % (TOOL, VERSION))
    lines.append("- 生成时间：%s" % meta["generated_at"])
    lines.append("- 扫描 ID：%s" % meta["scan_id"])
    lines.append("- 授权来源：%s" % meta["authorization"])
    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    lines.append("| 项 | 值 |")
    lines.append("|---|---|")
    lines.append("| 目标主机数 | %d |" % len(results))
    lines.append("| 开放端口总数 | %d |" % sum(r["port_count"] for r in results))
    lines.append("| 被 Scope Guard 拒绝 | %d |" % len(denied))
    lines.append("")
    if denied:
        lines.append("## Scope Guard 拒绝的目标")
        lines.append("")
        for h, r in denied:
            lines.append("- %s : %s" % (h, r))
        lines.append("")
    for r in results:
        lines.append("## %s" % r["host"])
        lines.append("")
        if not r["ports"]:
            lines.append("（无开放端口 / 无响应）")
            lines.append("")
            continue
        lines.append("| 端口 | 协议 | 状态 | 服务 | 版本 | 风险 | 说明 |")
        lines.append("|---|---|---|---|---|---|---|")
        for e in r["ports"]:
            ver = e.get("version") or "-"
            prod = e.get("product") or e.get("service") or "-"
            risk = e.get("risk_label") or "none"
            note = e.get("note") or "-"
            lines.append("| %d | tcp | open | %s | %s | %s | %s |"
                         % (e["port"], prod, ver, risk, note))
        lines.append("")
    lines.append("---")
    lines.append("> 本报告由 %s 生成，仅用于已授权目标的安全测试 / 资产盘点。" % TOOL_CN)
    lines.append("> 未经授权扫描他人系统违反《网络安全法》与《刑法》第 285/286 条，后果自负。")
    lines.append("> 报告中出现的已知风险提示仅为版本指纹匹配，需人工核实后确认。")
    lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return path


# ---------------------------------------------------------------------------
# 子命令
# ---------------------------------------------------------------------------

def cmd_scan(args):
    hosts, src = parse_targets(args.targets, args.target_list)
    guard = ScopeGuard(args.scope, args.assume_authorized, args.yes)
    allowed, denied = guard.confirm_or_partition(hosts, interactive=args.interactive)
    if denied:
        for h, r in denied:
            print("Scope Guard 拒绝：%s（%s）" % (h, r), file=sys.stderr)
    if not allowed:
        print("错误：所有目标均被 Scope Guard 拒绝，未执行任何扫描。", file=sys.stderr)
        print("请使用 --scope <授权文件> 声明范围，或 --assume-authorized --yes 确认授权。",
              file=sys.stderr)
        return 3
    ports = parse_ports(args.ports, args.top)
    meta = {
        "generated_at": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "scan_id": "%s-%s" % (time.strftime("%Y%m%d-%H%M%S"),
                              "".join(random.choice(string.ascii_lowercase) for _ in range(6))),
        "authorization": ("scope:%s" % args.scope) if args.scope
                         else ("assume-authorized" if args.assume_authorized else "loopback"),
        "targets": allowed,
    }
    if not args.json:
        print("扫描目标 %d 个、端口 %d 个（并发 %d、超时 %dms）..."
              % (len(allowed), len(ports), args.concurrency, args.timeout))
    results = scan_targets(allowed, ports, args.timeout / 1000.0,
                           args.concurrency, rate=args.rate, probe=not args.no_probe)
    if args.json:
        print(json.dumps(build_json(meta, results, denied), ensure_ascii=False, indent=2))
    elif args.report:
        write_report(args.report, meta, results, denied)
        print("报告已写入：%s" % args.report)
        print(format_text(results, denied))
    else:
        print(format_text(results, denied))
    if not args.json:
        total = sum(r["port_count"] for r in results)
        print("")
        print("摘要：%d 台主机，共 %d 个开放端口；扫描 ID %s"
              % (len(results), total, meta["scan_id"]))
    return 0


def cmd_fingerprint(args):
    if not args.host or not args.port:
        print("错误：fingerprint 需要 --host 与 --port", file=sys.stderr)
        return 2
    guard = ScopeGuard(args.scope, args.assume_authorized, args.yes)
    allowed, denied = guard.confirm_or_partition([args.host], interactive=args.interactive)
    if not allowed:
        print("Scope Guard 拒绝：%s 不在授权范围。" % args.host, file=sys.stderr)
        return 3
    ok, err = tcp_connect(args.host, args.port, args.timeout / 1000.0)
    if not ok:
        print("端口 %s:%d 不可达（%s）" % (args.host, args.port, err))
        return 0
    fp = probe_service(args.host, args.port, min(args.timeout / 1000.0 + 0.8, 3.0))
    sev, note = assess_risk(fp["product"], fp["version"])
    print("host: %s" % args.host)
    print("port: %d" % args.port)
    print("service: %s" % (fp["product"] or fp["service"] or "unknown"))
    print("version: %s" % (fp["version"] or "-"))
    print("risk: %s" % SEVERITY_LABEL[sev])
    if note:
        print("note: %s" % note)
    if fp["banner"]:
        print("banner: %r" % fp["banner"][:200])
    if args.json:
        print(json.dumps({"host": args.host, "port": args.port,
                          "service": fp["product"] or fp["service"],
                          "version": fp["version"],
                          "risk": SEVERITY_LABEL[sev],
                          "note": note, "banner": fp["banner"]},
                         ensure_ascii=False, indent=2))
    return 0


def cmd_check_scope(args):
    hosts, _ = parse_targets(args.targets, args.target_list)
    guard = ScopeGuard(args.scope, args.assume_authorized, False)
    allowed, denied = guard.partition(hosts)
    for h in allowed:
        print("ALLOW  %s" % h)
    for h, r in denied:
        print("DENY   %s (%s)" % (h, r))
    if denied:
        print("共 %d 个目标被拒绝；请补充 --scope 或 --assume-authorized。" % len(denied),
              file=sys.stderr)
        return 3
    return 0


def cmd_local(_args):
    entries = local_listen_ports()
    if not entries:
        print("未检测到监听端口，或当前平台不支持本机枚举（可尝试系统 netstat -tln）。")
        return 0
    print("本地监听端口：")
    print("  PROTO  PORT  LOCAL            PID")
    for e in entries:
        pid = e.get("pid") or "-"
        print("  %-6s %-6d %-16s %s" % (e["proto"], e["port"], e["local"], pid))
    return 0


def cmd_list_ports(_args):
    print("内置常用端口表（%d 个，--ports top 使用）" % len(TOP_PORTS))
    for port, svc in sorted(TOP_PORTS.items()):
        print("  %-6d %s" % (port, svc))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog=TOOL,
        description="%s（%s）零依赖自研网络侦察引擎（端口 / 服务 / 版本指纹 + Scope Guard）"
                    % (TOOL, TOOL_CN),
    )
    ap.add_argument("--version", action="version", version="%s %s" % (TOOL, VERSION))
    sub = ap.add_subparsers(dest="cmd", metavar="<command>")

    p_scan = sub.add_parser("scan", help="端口/服务/版本指纹扫描")
    p_scan.add_argument("--targets", default="", help="目标：IP/CIDR/主机名，逗号分隔")
    p_scan.add_argument("--target-list", default=None, help="目标文件（每行一个，# 注释）")
    p_scan.add_argument("--ports", default="", help="端口：'22,80,443' / '1-1024' / 'top[:N]'")
    p_scan.add_argument("--top", type=int, default=100, help="--ports top 时取前 N 个（默认 100）")
    p_scan.add_argument("--scope", default=None, help="授权范围文件（Scope Guard）")
    p_scan.add_argument("--assume-authorized", action="store_true",
                        help="声明目标已获授权（配合 --yes 使用）")
    p_scan.add_argument("--yes", action="store_true", help="跳过交互确认（仅与授权声明搭配）")
    p_scan.add_argument("--no-interactive", action="store_true", help="非交互模式（拒绝未授权）")
    p_scan.add_argument("--timeout", type=int, default=1200, help="连接超时 ms（默认 1200）")
    p_scan.add_argument("--concurrency", type=int, default=64, help="并发连接数（默认 64）")
    p_scan.add_argument("--rate", type=float, default=None, help="每次连接间隔秒（限速）")
    p_scan.add_argument("--no-probe", action="store_true", help="只探端口，不做服务指纹")
    p_scan.add_argument("--json", action="store_true", help="输出 JSON")
    p_scan.add_argument("--report", default=None, help="Markdown 报告输出路径")
    p_scan.set_defaults(func=cmd_scan)

    p_fp = sub.add_parser("fingerprint", help="单端口深度指纹")
    p_fp.add_argument("--host", required=True)
    p_fp.add_argument("--port", type=int, required=True)
    p_fp.add_argument("--scope", default=None)
    p_fp.add_argument("--assume-authorized", action="store_true")
    p_fp.add_argument("--yes", action="store_true")
    p_fp.add_argument("--no-interactive", action="store_true")
    p_fp.add_argument("--timeout", type=int, default=1200)
    p_fp.add_argument("--json", action="store_true")
    p_fp.set_defaults(func=cmd_fingerprint)

    p_cs = sub.add_parser("check-scope", help="Scope Guard 授权预检")
    p_cs.add_argument("--targets", default="")
    p_cs.add_argument("--target-list", default=None)
    p_cs.add_argument("--scope", default=None)
    p_cs.add_argument("--assume-authorized", action="store_true")
    p_cs.set_defaults(func=cmd_check_scope)

    p_local = sub.add_parser("local", help="本机监听端口清单（只读）")
    p_local.set_defaults(func=cmd_local)

    p_lp = sub.add_parser("list-ports", help="列出内置端口表")
    p_lp.set_defaults(func=cmd_list_ports)

    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 2
    try:
        args.interactive = not getattr(args, "no_interactive", False)
        return args.func(args)
    except ValueError as exc:
        print("错误：%s" % exc, file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("已中断。", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
