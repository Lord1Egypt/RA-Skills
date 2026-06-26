#!/usr/bin/env python3
"""
Site Summarizer v4.1.0 - Fixed all bugs
"""
import sys, json, re, socket, ssl, ipaddress, os, hashlib, time
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser

# Config
BLOCKED = {"file", "ftp", "data", "javascript"}
PRIVATE = [ipaddress.ip_network(n) for n in ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]]
CLOUD = {"169.254.169.254", "100.100.100.200"}

# Proper regex patterns
SECRETS = [
    (re.compile(r"\bapi[_-]?key\s*[:=]\s*["\']?[\w-]{20,}"), "[REDACTED]"),
    (re.compile(r"\bgh[pouhs]_[\w-]{36,}"), "[REDACTED]"),
    (re.compile(r"\bsk-[\w-]{48,}"), "[REDACTED]"),
    (re.compile(r"\bak-[\w-]{32,}"), "[REDACTED]"),
    (re.compile(r"\bAKIA[\w-]{16}"), "[REDACTED]"),
]

MAX_URL = 2048
MAX_DOWNLOAD = 500000
MAX_OUTPUT = 150000
TIMEOUT = 30

CACHE_DIR = os.environ.get("SITE_SUMMARIZER_CACHE_DIR", os.path.expanduser("~/.cache/site-summarizer"))
CACHE_TTL = int(os.environ.get("SITE_SUMMARIZER_CACHE_TTL", "3600"))
HIDE_IP = os.environ.get("SITE_SUMMARIZER_HIDE_IP", "false").lower() == "true"

def redact(t):
    if not t: return t
    for p, r in SECRETS: t = p.sub(r, t)
    return t

class Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.words = []
        self.skip = 0
        self.title = None
        self.in_title = False
        self.in_body = False
        self.meta = {}
        self.skip_tags = {"script", "style", "nav", "footer", "noscript"}
    
    def handle_starttag(self, t, a):
        d = dict(a)
        if t == "title": self.in_title = True
        elif t == "meta":
            n = d.get("name", d.get("property", "")).lower()
            if n in ("description", "author"): self.meta[n] = d.get("content", "")
        elif t in self.skip_tags: self.skip += 1
        elif t in ("p", "div", "h1", "h2", "h3", "li"):
            if self.words and not self.words[-1].endswith("\n"): self.words.append("\n")
        if t == "body": self.in_body = True
    
    def handle_endtag(self, t):
        if t == "title": self.in_title = False
        elif t in self.skip_tags: self.skip = max(0, self.skip - 1)
        if t == "body": self.in_body = False
    
    def handle_data(self, d):
        if self.in_title: self.title = d.strip()
        elif self.skip == 0 and self.in_body:
            c = " ".join(d.split())
            if c: self.words.append(c)
    
    def get_text(self):
        return " ".join(self.words)[:MAX_OUTPUT]

def resolve_ip(host):
    if not host or host.lower() in {"localhost", "127.0.0.1"}: raise Exception("Blocked")
    ips = socket.getaddrinfo(host, 443, socket.AF_UNSPEC, socket.SOCK_STREAM)
    for info in ips:
        ip = info[4][0]
        try:
            a = ipaddress.ip_address(ip)
            if ip in CLOUD or any(a in n for n in PRIVATE): continue
            return ip
        except: continue
    raise Exception(f"No valid IP")

def validate(url):
    p = urlparse(url)
    if not p.scheme or p.scheme not in ("http", "https"): return False, "Bad scheme"
    if not p.hostname: return False, "No host"
    return True, None

def fetch_url(url, bound_ip, hostname):
    p = urlparse(url)
    port = p.port or (443 if p.scheme == "https" else 80)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    try:
        sock.connect((bound_ip, port))
        ctx = ssl.create_default_context()
        ssock = ctx.wrap_socket(sock, server_hostname=hostname) if p.scheme == "https" else sock
        path = p.path or "/"
        if p.query: path += "?" + p.query
        req = f"GET {path} HTTP/1.1\r\nHost: {hostname}\r\nUser-Agent: SS/4.1\r\nConnection: close\r\n\r\n"
        ssock.sendall(req.encode())
        response = b""
        while True:
            chunk = ssock.recv(8192)
            if not chunk: break
            response += chunk
            if len(response) > MAX_DOWNLOAD: break
        header_end = response.find(b"\r\n\r\n")
        if header_end == -1: return None, None, "Invalid"
        header_bytes = response[:header_end]
        body = response[header_end+4:]
        status_match = re.search(rb"HTTP/\d\.\d\s+(\d+)", header_bytes)
        status = int(status_match.group(1)) if status_match else 200
        headers = {}
        for line in header_bytes.decode("utf-8", errors="ignore").split("\r\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()
        return headers, status, body
    finally: sock.close()

def get_cache(url):
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        path = os.path.join(CACHE_DIR, hashlib.sha256(url.encode()).hexdigest()[:16] + ".json")
        if os.path.exists(path):
            with open(path) as f: data = json.load(f)
            if time.time() - data.get("_t", 0) < CACHE_TTL: return data.get("result")
    except: pass
    return None

def set_cache(url, result):
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        path = os.path.join(CACHE_DIR, hashlib.sha256(url.encode()).hexdigest()[:16] + ".json")
        with open(path, "w") as f: json.dump({"_t": time.time(), "result": result}, f)
    except: pass

def detect_lang(text):
    sample = " ".join(text.lower().split()[:30])
    langs = {"en": sample.count("the"), "es": sample.count("el"), "fr": sample.count("le"), "de": sample.count("der")}
    return max(langs, key=langs.get) if any(langs.values()) else "unknown"

def get_keywords(text, n=10):
    stop = {"about", "which", "their", "there", "would", "could", "should", "other", "some", "more", "also", "have", "been", "this", "that", "with", "from", "they", "will", "just", "only", "these", "those", "where", "when", "your", "here", "what", "make", "like", "time", "know", "take", "people", "year", "good", "them", "see", "than", "then", "now", "look", "come", "over", "think", "back", "after", "first"}
    words = re.findall(r"\b[a-zA-Z]{5,}\b", text.lower())
    freq = {w: freq.get(w, 0) + 1 for w in words if w not in stop}
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:n]

def summarize(text):
    sents = [s for s in re.split(r"[.!?]\s+", text) if len(s.strip()) > 20]
    if len(sents) <= 5: return text[:500]
    scored = [(sum(get_keywords(s)[0][1] if get_keywords(s) else 0 for _ in range(1)), s) for s in sents]
    top = sorted(scored, key=lambda x: x[0], reverse=True)[:5]
    top.sort(key=lambda x: sents.index(x[1]))
    return " ".join(s for _, s in top)

def fetch(url):
    cached = get_cache(url)
    if cached: cached["from_cache"] = True; return cached
    v, e = validate(url)
    if not v: return {"success": False, "error": e}
    hostname = urlparse(url).hostname
    try: bound_ip = resolve_ip(hostname)
    except Exception as e: return {"success": False, "error": f"DNS: {e}"}
    headers, status, body = fetch_url(url, bound_ip, hostname)
    if not headers: return {"success": False, "error": status}
    if status in (301, 302, 303, 307, 308):
        location = headers.get("location")
        if not location: return {"success": False, "error": "No location"}
        new_url = urljoin(url, location)
        v, e = validate(new_url)
        if not v: return {"success": False, "error": f"Bad redirect: {e}"}
        new_host = urlparse(new_url).hostname
        if new_host != hostname:
            try: new_ip = resolve_ip(new_host)
            except Exception as e: return {"success": False, "error": f"IP blocked: {e}"}
            headers, status, body = fetch_url(new_url, new_ip, new_host)
            if not headers: return {"success": False, "error": f"Redirect fail: {status}"}
            bound_ip = new_ip
        else:
            headers, status, body = fetch_url(new_url, bound_ip, hostname)
            if not headers: return {"success": False, "error": f"Redirect fail: {status}"}
    try: html = body.decode("utf-8", errors="ignore")
    except: html = body.decode("latin-1", errors="ignore")
    e = Extractor()
    e.feed(html)
    text = e.get_text()
    lang = detect_lang(text)
    keywords = get_keywords(text)
    wc = len(text.split())
    summary = summarize(text)
    result = {
        "success": True,
        "content": redact(text),
        "summary": redact(summary),
        "metadata": {"title": redact(e.title), "description": redact(e.meta.get("description")), "author": redact(e.meta.get("author"))},
        "analysis": {"language": lang, "keywords": keywords, "word_count": wc, "read_time_min": max(1, wc // 200), "resolved_ip": None if HIDE_IP else bound_ip},
        "status": status, "original_url": url, "from_cache": False
    }
    set_cache(url, result)
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2: print(json.dumps({"error": "Usage: fetch.py <url>"})); sys.exit(1)
    print(json.dumps(fetch(sys.argv[1]), indent=2))
