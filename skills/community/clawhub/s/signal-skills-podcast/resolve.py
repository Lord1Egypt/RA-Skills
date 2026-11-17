#!/usr/bin/env python3
"""Resolve any podcast URL -> RSS feed + episode list + transcript URLs.

Works for ANY show, not one hardcoded feed.

  python3 resolve.py "<url-or-show-name>" [--name SHOW] [--limit N] [--download DIR] [--use-proxy]

Fetches connect directly and refuse non-public addresses at connect time.
HTTP(S)_PROXY is ignored unless --use-proxy is passed, for a machine with no
direct route out; the proxy then connects, so DNS rebinding is not prevented.

Handles:
  podcasts.apple.com/<cc>/podcast/<slug>/id<SHOW>?i=<EPISODE>
  a direct RSS url (any other http(s) URL is treated as one)
  a bare show name, or --name SHOW (searched via iTunes; the first hit is used)
  open.spotify.com/show/... only together with --name: Spotify has no open
    API, so the link itself cannot be resolved
  youtube.com/watch?v=... or youtu.be/... (single video)
  youtube.com/@handle, /channel/UC..., /playlist?list=... (multiple videos, needs --limit)

YouTube requires yt-dlp on PATH (`brew install yt-dlp` / `pipx install yt-dlp`).
There is no RSS feed for YouTube — each video is fetched directly via yt-dlp:
metadata via `-J --skip-download`, transcript via auto-captions (falls back to
manual subs if present). No podcast:transcript tag equivalent exists, so
`have` transcript count reflects whichever videos actually have an en/en-orig
caption track — some videos (esp. very new ones) may have none yet.
"""
import http.client
import ipaddress
import json
import os
import re
import socket
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

PNS = {"podcast": "https://podcastindex.org/namespace/1.0"}
UA = {"User-Agent": "Mozilla/5.0 (compatible; podcast-skill/1.0)"}


class BlockedURL(Exception):
    """A URL or address this script refuses to contact."""


# Explicit lists rather than ipaddress.is_global, whose answers have shifted
# between Python releases. Same lists as cited's safe_fetch.py.
_BLOCKED_V4 = tuple(ipaddress.ip_network(n) for n in (
    "0.0.0.0/8", "10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8", "169.254.0.0/16",
    "172.16.0.0/12", "192.0.0.0/24", "192.0.2.0/24", "192.88.99.0/24", "192.168.0.0/16",
    "198.18.0.0/15", "198.51.100.0/24", "203.0.113.0/24", "224.0.0.0/4", "240.0.0.0/4",
))
_BLOCKED_V6 = tuple(ipaddress.ip_network(n) for n in (
    "::/96", "64:ff9b:1::/48", "100::/64", "2001::/23", "2001:db8::/32", "2002::/16",
    "3fff::/20", "5f00::/16", "fc00::/7", "fe80::/10", "fec0::/10", "ff00::/8",
))
_NAT64 = ipaddress.ip_network("64:ff9b::/96")


def is_blocked_ip(ip):
    """True if `ip` is not a public unicast address."""
    if ip.version == 6:
        if ip.ipv4_mapped is not None:
            return is_blocked_ip(ip.ipv4_mapped)
        if ip in _NAT64:  # DNS64 synthesizes these for public IPv4 sites; judge the embedded v4
            return is_blocked_ip(ipaddress.IPv4Address(int(ip) & 0xFFFFFFFF))
        return any(ip in net for net in _BLOCKED_V6)
    return any(ip in net for net in _BLOCKED_V4)


def _is_noncanonical_numeric_host(host):
    """2130706433, 0x7f000001, 0177.0.0.1, 127.1: inet_aton accepts these, a dotted quad aside."""
    if not re.fullmatch(r"[0-9a-fx.]+", host) or not re.search(r"\d", host):
        return False
    try:
        ipaddress.ip_address(host)
        return False
    except ValueError:
        pass
    try:
        socket.inet_aton(host)
    except OSError:
        return False
    return True


def check_url(url):
    """Raise BlockedURL unless `url` is http(s) on a host with only public addresses.

    Feed URLs come from the user or iTunes and transcript URLs from the feed, so
    a hostile feed could otherwise read local files or internal services into
    --download."""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme.lower() not in ("http", "https"):
        raise BlockedURL(f"URL scheme {parts.scheme or '(none)'} is not allowed: {url}")
    if not parts.hostname:
        raise BlockedURL(f"URL has no host: {url}")
    # Resolvers disagree on these (0177.0.0.1 is loopback on Linux, not on macOS), so don't ask one.
    if _is_noncanonical_numeric_host(parts.hostname):
        raise BlockedURL(f"host {parts.hostname} is a non-canonical numeric address")
    try:
        _checked_addresses(parts.hostname, parts.port or 443)
    except socket.gaierror:
        return  # the fetch reports it, or with --use-proxy the proxy resolves it


def _checked_addresses(host, port):
    infos = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
    for info in infos:
        if is_blocked_ip(ipaddress.ip_address(str(info[4][0]).split("%", 1)[0])):
            raise BlockedURL(f"{host} resolves to non-public address {info[4][0]}")
    return infos


def _guarded_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
    """socket.create_connection that connects only to the addresses it just checked,
    so a DNS answer that changes after check_url (rebinding) cannot reach a local service."""
    host, port = address
    error = None
    for family, socktype, proto, _, sockaddr in _checked_addresses(host, port):
        sock = socket.socket(family, socktype, proto)
        try:
            if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                sock.settimeout(timeout)
            if source_address:
                sock.bind(source_address)
            sock.connect(sockaddr)
            return sock
        except OSError as ex:
            error = ex
            sock.close()
    raise error or OSError(f"no addresses for {host}")


class _Guarded:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_connection = _guarded_connection  # http.client opens every socket through this


class _GuardedHTTPConnection(_Guarded, http.client.HTTPConnection):
    pass


class _GuardedHTTPSConnection(_Guarded, http.client.HTTPSConnection):
    pass


class _GuardedHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return self.do_open(_GuardedHTTPConnection, req)


class _GuardedHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(_GuardedHTTPSConnection, req, context=self._context)


class _CheckedRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _opener(use_proxy=False):
    if use_proxy:  # the proxy connects, so only check_url's earlier lookup applies
        return urllib.request.build_opener(_CheckedRedirects)
    # ProxyHandler({}) ignores HTTP(S)_PROXY: a proxy would connect past the guard.
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({}), _GuardedHTTPHandler, _GuardedHTTPSHandler, _CheckedRedirects)


_OPENER = _opener()


def get(url, timeout=60):
    check_url(url)
    return _OPENER.open(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def itunes(params):
    return json.loads(get("https://itunes.apple.com/" + params).decode("utf-8", "replace"))


class NotAFeed(Exception):
    """The fetched document is not an RSS feed."""


def _host(src):
    """Hostname of a URL, with or without its scheme; "" for a bare show name."""
    if "://" not in src and re.match(r"[\w.-]+\.[a-z]{2,}(/|$)", src, re.IGNORECASE):
        src = "https://" + src
    try:
        return (urllib.parse.urlsplit(src).hostname or "").lower() if "://" in src else ""
    except ValueError:
        return ""


def _on(host, domain):
    return host == domain or host.endswith("." + domain)


def is_youtube(src):
    host = _host(src)
    return _on(host, "youtube.com") or _on(host, "youtu.be")


def yt_dlp_json(url, extra=()):
    cmd = ["yt-dlp", "--skip-download", "--no-warnings", "-J", *extra, url]
    try:
        raw = subprocess.run(cmd, capture_output=True, check=True, timeout=60).stdout
    except FileNotFoundError:
        sys.exit("yt-dlp not found on PATH. Install with `brew install yt-dlp`.")
    except subprocess.CalledProcessError as ex:
        sys.exit(f"yt-dlp failed for {url}: {ex.stderr.decode('utf-8', 'replace')[:400]}")
    return json.loads(raw)


def yt_list_videos(src, limit):
    """Single video URL -> [that video]. Channel/@handle/playlist -> up to `limit`
    videos, newest first, via yt-dlp's flat-playlist mode (fast, no per-video fetch)."""
    if re.search(r"[?&]v=|youtu\.be/", src):
        d = yt_dlp_json(src)
        return [{"id": d["id"], "title": d.get("title", ""),
                  "date": _yt_date(d.get("upload_date"))}]
    d = yt_dlp_json(src, extra=["--flat-playlist", "--playlist-end", str(limit)])
    entries = d.get("entries") or [d]
    out = []
    for e in entries[:limit]:
        if not e or not e.get("id"):
            continue
        out.append({"id": e["id"], "title": e.get("title", ""),
                     "date": _yt_date(e.get("upload_date"))})
    return out


def _yt_date(upload_date):
    if not upload_date or len(upload_date) != 8:
        return ""
    return f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"


def yt_transcript(video_id, workdir):
    """Auto-captions preferred (near-universal); falls back to manual subs.
    Returns flattened text, or None if neither track exists."""
    url = f"https://www.youtube.com/watch?v={video_id}"
    base = os.path.join(workdir, video_id)
    for sub_flag in ("--write-auto-sub", "--write-sub"):
        cmd = ["yt-dlp", "--skip-download", "--no-warnings", sub_flag,
               "--sub-lang", "en.*", "--sub-format", "vtt",
               "-o", base + ".%(ext)s", url]
        subprocess.run(cmd, capture_output=True, timeout=120)
        for fname in os.listdir(workdir):
            if fname.startswith(os.path.basename(base)) and fname.endswith(".vtt"):
                path = os.path.join(workdir, fname)
                text = flatten_transcript_file(path)
                os.remove(path)
                return text
    return None


def flatten_transcript_file(path):
    with open(path, "rb") as f:
        raw = f.read()
    txt = raw.decode("utf-8", "replace")
    lines = [l for l in txt.splitlines()
             if l.strip() and "-->" not in l and not l.strip().isdigit()
             and not l.startswith(("WEBVTT", "NOTE", "Kind:", "Language:"))]
    lines = [re.sub(r"<[^>]+>", "", l) for l in lines]
    return "\n".join(dict.fromkeys(lines))


def run_youtube(src, limit, dl):
    videos = yt_list_videos(src, limit)
    print(f"show: (YouTube) {src}")
    print(f"episodes: {len(videos)} shown\n")

    if not dl:
        for i, v in enumerate(videos):
            print(f"{i:2d} {v['date']} | {v['title'][:64]}")
        print("\n! Pass --download DIR to fetch auto-caption transcripts via yt-dlp.")
        return

    os.makedirs(dl, exist_ok=True)
    man = []
    for i, v in enumerate(videos):
        slug = re.sub(r"[^a-z0-9]+", "-", v["title"].lower()).strip("-")[:40]
        p = os.path.join(dl, f"{i:02d}-{slug}.txt")
        text = yt_transcript(v["id"], dl)
        if text is None:
            print(f"  {i:2d} FAIL no en captions -> {v['title'][:40]}")
            continue
        open(p, "w").write(text)
        man.append({"title": v["title"], "date": v["date"], "path": os.path.abspath(p),
                     "words": len(text.split()), "target": i == 0, "video_id": v["id"]})
        print(f"  {len(text.split()):6d}w -> {p}")
    json.dump(man, open(os.path.join(dl, "manifest.json"), "w"), indent=1)
    print(f"\nmanifest: {os.path.join(dl, 'manifest.json')}  ({len(man)} files)")


def resolve_source(src, name=None):
    """-> (feed_url, show_id|None, episode_id|None, show_name)

    Routed on the hostname, never on a substring: a feed URL that merely
    contains "apple" or "spotify" is still a feed."""
    host = _host(src)
    is_apple, is_spotify = _on(host, "apple.com"), _on(host, "spotify.com")
    if host and not (is_apple or is_spotify):
        return (src if "://" in src else "https://" + src), None, None, "(direct feed)"

    show_id = ep_id = None
    if is_apple:
        m = re.search(r"/id(\d+)", src)
        if m:
            show_id = m.group(1)
        m = re.search(r"[?&]i=(\d+)", src)
        if m:
            ep_id = m.group(1)

    if not show_id:
        if host and not name:
            what = "Spotify has no open API, so a Spotify link" if is_spotify else "This Apple link has no show id, so it"
            sys.exit(f'{what} cannot be resolved to a feed. Run again with the show\'s name: '
                     f'resolve.py "{src}" --name "<show name>", or pass its RSS or Apple Podcasts URL.')
        name = name or src
        q = urllib.parse.urlencode({"term": name, "entity": "podcast", "limit": 5})
        res = itunes("search?" + q).get("results", [])
        if not res:
            sys.exit(f"No podcast found for: {name}")
        show_id = str(res[0]["collectionId"])
        print(f"! Matched show: {res[0]['collectionName']}", file=sys.stderr)

    look = itunes(f"lookup?id={show_id}&entity=podcast").get("results", [])
    if not look:
        sys.exit(f"iTunes lookup failed for show id {show_id}")
    feed = look[0].get("feedUrl")
    name = look[0].get("collectionName", "?")
    if not feed:
        sys.exit(f"Show '{name}' exposes no feedUrl (Apple-exclusive?).")
    return feed, show_id, ep_id, name


def episode_title_for_id(show_id, ep_id):
    """Apple ?i= ids resolve via the SHOW lookup with entity=podcastEpisode."""
    if not (show_id and ep_id):
        return None
    for e in itunes(f"lookup?id={show_id}&entity=podcastEpisode&limit=200").get("results", []):
        if str(e.get("trackId")) == str(ep_id):
            return e.get("trackName")
    return None


def parse_feed(xml_bytes, limit):
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as ex:
        raise NotAFeed(f"not XML: {ex}") from ex
    ch = root.find("channel")
    if ch is None:
        raise NotAFeed(f"root element is <{root.tag.rsplit('}', 1)[-1]}>, not an RSS <rss><channel>")
    out = []
    for it in ch.findall("item")[:limit]:
        tr = it.find("podcast:transcript", PNS)
        out.append({
            "title": (it.findtext("title") or "").strip(),
            "date": (it.findtext("pubDate") or "")[:16],
            "transcript": tr.get("url") if tr is not None else None,
        })
    return out


def flatten_transcript(url):
    raw = get(url)
    if url.endswith(".json") or raw[:1] in (b"{", b"["):
        d = json.loads(raw)
        segs = d.get("segments") or d.get("results") or []
        if segs:
            return "\n".join(s.get("body") or s.get("text", "") for s in segs)
        return json.dumps(d)
    txt = raw.decode("utf-8", "replace")
    if "WEBVTT" in txt[:64] or "-->" in txt[:400]:  # vtt/srt
        lines = [l for l in txt.splitlines()
                 if l.strip() and "-->" not in l and not l.strip().isdigit()
                 and not l.startswith(("WEBVTT", "NOTE", "Kind:", "Language:"))]
        return "\n".join(dict.fromkeys(lines))
    return txt


def main():
    a = sys.argv[1:]
    if "--use-proxy" in a:
        a.remove("--use-proxy")
        global _OPENER
        _OPENER = _opener(use_proxy=True)
    elif any(urllib.request.getproxies().get(s) for s in ("http", "https")):
        print("note: HTTP(S)_PROXY is set but not used. If fetches fail to resolve hosts, re-run with "
              "--use-proxy (the address check is weaker through a proxy).", file=sys.stderr)
    if not a:
        sys.exit(__doc__)
    name = a[a.index("--name") + 1] if "--name" in a else None
    src = name if a[0].startswith("--") else a[0]
    limit = int(a[a.index("--limit") + 1]) if "--limit" in a else 12
    dl = a[a.index("--download") + 1] if "--download" in a else None

    if is_youtube(src):
        run_youtube(src, limit, dl)
        return

    feed, show_id, ep_id, name = resolve_source(src, name)
    print(f"show: {name}\nfeed: {feed}")

    target = episode_title_for_id(show_id, ep_id)
    if ep_id:
        print(f"episode i={ep_id} -> {target or 'UNRESOLVED (falling back to newest)'}")

    try:
        eps = parse_feed(get(feed), limit)
    except BlockedURL as ex:
        sys.exit(f"Refused to fetch the feed: {ex}")
    except NotAFeed as ex:
        sys.exit(f"{feed} is not an RSS podcast feed ({ex}). Pass the show's RSS URL, its Apple Podcasts URL, or its name.")
    have = sum(1 for e in eps if e["transcript"])
    print(f"episodes: {len(eps)} shown, {have} with embedded transcripts\n")
    for i, e in enumerate(eps):
        mark = "<<< TARGET" if target and e["title"] == target else ""
        print(f"{i:2} {'OK ' if e['transcript'] else '-- '} {e['date']} | {e['title'][:64]} {mark}")

    if not have:
        print("\n! No podcast:transcript tags. Fall back, in order:"
              "\n  1. show's own site (google '<title> transcript')"
              "\n  2. yt-dlp --write-auto-sub --skip-download --sub-lang en --sub-format vtt <yt-url>"
              "\n  3. uv run --with openai-whisper whisper ep.mp3 --model small --output_format txt")
        return

    if dl:
        os.makedirs(dl, exist_ok=True)
        man = []
        for i, e in enumerate(eps):
            if not e["transcript"]:
                continue
            slug = re.sub(r"[^a-z0-9]+", "-", e["title"].lower()).strip("-")[:40]
            p = os.path.join(dl, f"{i:02d}-{slug}.txt")
            try:
                t = flatten_transcript(e["transcript"])
                open(p, "w").write(t)
                man.append({"title": e["title"], "date": e["date"],
                            "path": os.path.abspath(p), "words": len(t.split()),
                            "target": bool(target and e["title"] == target)})
                print(f"  {len(t.split()):6d}w -> {p}")
            except Exception as ex:
                print(f"  FAIL {e['title'][:40]}: {ex}")
        json.dump(man, open(os.path.join(dl, "manifest.json"), "w"), indent=1)
        print(f"\nmanifest: {os.path.join(dl, 'manifest.json')}  ({len(man)} files)")


if __name__ == "__main__":
    main()
