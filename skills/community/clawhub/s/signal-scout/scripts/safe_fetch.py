"""Guarded HTTP(S) fetching for verify_sources.py. Standard library only.
Copied from cited's safe_fetch.py, without its result type, retries and body
handling, which verify_sources.py has its own versions of.

analysis.json is untrusted input: an agent wrote it, and a source_url can point
anywhere. Every request and every redirect hop is checked:

- Scheme: only http and https. No file:, ftp:, data:, or anything else.
- Address: the hostname is resolved, and the connection is refused if ANY
  resolved address is loopback, private, link-local (cloud metadata),
  carrier-grade NAT, multicast, reserved, or otherwise not public. The check
  runs inside the connection itself, on the exact addresses being connected
  to, so a DNS answer that changes between check and connect (rebinding)
  cannot slip through. Numeric hosts in non-canonical spellings
  (2130706433, 0x7f000001, 0177.0.0.1, 127.1) are refused outright.
- Redirects: each hop is re-checked against the same rules; at most
  `max_redirects` hops are followed.

With `use_env_proxy` the proxy makes the connection, so the target is resolved
and checked first, and a rebinding DNS answer can still differ.
"""

from __future__ import annotations

import functools
import http.client
import ipaddress
import re
import socket
import ssl
import unicodedata
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

ALLOWED_SCHEMES = ("http", "https")


class BlockedURL(Exception):
    """A URL or address the fetch policy refuses to contact."""


class RedirectLimit(Exception):
    """More redirects than the policy allows."""


@dataclass(frozen=True)
class FetchPolicy:
    allow_private: bool = False                    # disables the address check entirely
    allow_hosts: frozenset[str] = frozenset()      # hostnames exempt from the address check
    max_redirects: int = 5
    use_env_proxy: bool = False                    # honor HTTP(S)_PROXY; weakens the address check


# Explicit lists rather than ipaddress.is_global, whose answers have shifted
# between Python releases. Sources: IANA IPv4/IPv6 Special-Purpose Address
# Registries (anything not globally reachable), plus multicast.

_BLOCKED_V4 = tuple(ipaddress.ip_network(n) for n in (
    "0.0.0.0/8", "10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8", "169.254.0.0/16",
    "172.16.0.0/12", "192.0.0.0/24", "192.0.2.0/24", "192.88.99.0/24", "192.168.0.0/16",
    "198.18.0.0/15", "198.51.100.0/24", "203.0.113.0/24", "224.0.0.0/4", "240.0.0.0/4",
))
_BLOCKED_V6 = tuple(ipaddress.ip_network(n) for n in (
    "::/96",            # unspecified, loopback, deprecated IPv4-compatible
    "64:ff9b:1::/48",   # local-use NAT64
    "100::/64",         # discard-only
    "2001::/23",        # IETF protocol assignments, incl. Teredo (2001::/32)
    "2001:db8::/32",    # documentation
    "2002::/16",        # 6to4 (can embed any IPv4, including private)
    "3fff::/20",        # documentation
    "5f00::/16",        # SRv6 SIDs
    "fc00::/7",         # unique local (incl. AWS IMDS fd00:ec2::254)
    "fe80::/10",        # link-local
    "fec0::/10",        # deprecated site-local
    "ff00::/8",         # multicast
))
_NAT64 = ipaddress.ip_network("64:ff9b::/96")
_BLOCKED_NAMES = ("localhost",)
_BLOCKED_SUFFIXES = (".localhost", ".local", ".internal", ".home.arpa")


def is_blocked_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """True if `ip` is not a public unicast address."""
    if isinstance(ip, ipaddress.IPv6Address):
        if ip.ipv4_mapped is not None:
            return is_blocked_ip(ip.ipv4_mapped)
        if ip in _NAT64:  # DNS64 synthesizes these for public IPv4 sites; judge the embedded v4
            return is_blocked_ip(ipaddress.IPv4Address(int(ip) & 0xFFFFFFFF))
        return any(ip in net for net in _BLOCKED_V6)
    return any(ip in net for net in _BLOCKED_V4)


def _parse_ip(text: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address | None:
    try:
        return ipaddress.ip_address(text.split("%", 1)[0])
    except ValueError:
        return None


def _is_noncanonical_numeric_host(host: str) -> bool:
    """2130706433, 0x7f000001, 0177.0.0.1, 127.1: inet_aton accepts these and
    many resolvers turn them into an address. There is no reason for a
    citation to use one, so they are refused rather than interpreted."""
    if _parse_ip(host) is not None:
        return False
    if not re.fullmatch(r"[0-9a-fx.]+", host) or not re.search(r"\d", host):
        return False
    try:
        socket.inet_aton(host)
    except OSError:
        return False
    return True


def _host_exempt(host: str, policy: FetchPolicy) -> bool:
    return policy.allow_private or host.rstrip(".").lower() in policy.allow_hosts


def url_problem(url: str, policy: FetchPolicy) -> str | None:
    """Why `url` must not be fetched under `policy`, or None if it may be.
    Checks scheme, host presence and literal addresses. Hostnames are
    resolved and checked at connect time, not here."""
    try:
        parsed = urllib.parse.urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        return f"malformed URL ({exc})"
    scheme = parsed.scheme.lower()
    if scheme not in ALLOWED_SCHEMES:
        return f"URL scheme {scheme + ':' if scheme else '(none)'} is not allowed; only http and https are fetched"
    # Fullwidth and circled digits resolve to the ASCII address they normalize to.
    host = unicodedata.normalize("NFKC", parsed.hostname or "").rstrip(".")
    if not host:
        return "URL has no host"
    if port == 0:
        return "URL has an invalid port"
    if _host_exempt(host, policy):
        return None
    if host in _BLOCKED_NAMES or host.endswith(_BLOCKED_SUFFIXES):
        return f"host {host} is a local name"
    ip = _parse_ip(host)
    if ip is not None and is_blocked_ip(ip):
        return f"address {ip} is not a public address"
    if _is_noncanonical_numeric_host(host):
        return f"host {host} is a non-canonical numeric address"
    return None


def _resolve_checked(host: str, port: int, policy: FetchPolicy) -> list[tuple]:
    infos = socket.getaddrinfo(host, port, 0, socket.SOCK_STREAM)
    if not _host_exempt(host, policy):
        for info in infos:
            ip = _parse_ip(str(info[4][0]))
            if ip is None or is_blocked_ip(ip):
                raise BlockedURL(f"host {host} resolves to non-public address {info[4][0]}")
    return infos


def _guarded_create_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                               source_address=None, *, policy: FetchPolicy) -> socket.socket:
    """Drop-in for socket.create_connection that refuses non-public
    addresses and connects only to the addresses it checked."""
    host, port = address
    last_error: OSError | None = None
    for family, socktype, proto, _, sockaddr in _resolve_checked(host, port, policy):
        sock = socket.socket(family, socktype, proto)
        try:
            if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                sock.settimeout(timeout)
            if source_address:
                sock.bind(source_address)
            sock.connect(sockaddr)
            return sock
        except OSError as exc:
            last_error = exc
            sock.close()
    raise last_error or OSError(f"no addresses for {host}")


def _guarded(base: type, policy: FetchPolicy) -> type:
    class Guarded(base):  # type: ignore[misc, valid-type]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            # http.client opens every socket through this attribute (3.10-3.13).
            self._create_connection = functools.partial(_guarded_create_connection, policy=policy)

    return Guarded


class _GuardedHTTPHandler(urllib.request.HTTPHandler):
    def __init__(self, policy: FetchPolicy) -> None:
        super().__init__()
        self._conn_class = _guarded(http.client.HTTPConnection, policy)

    def http_open(self, req):
        return self.do_open(self._conn_class, req)


class _GuardedHTTPSHandler(urllib.request.HTTPSHandler):
    def __init__(self, policy: FetchPolicy) -> None:
        super().__init__(context=ssl.create_default_context())
        self._conn_class = _guarded(http.client.HTTPSConnection, policy)

    def https_open(self, req):
        return self.do_open(self._conn_class, req, context=self._context)


def _keep_alive(base: type) -> type:
    """urllib always sends `Connection: close`. Some proxies (Claude Code's
    sandbox proxy among them) then drop the tail of the response when the
    server closes, and the body comes back short. Asking for keep-alive lets
    the response end by its own framing instead."""
    class KeepAlive(base):  # type: ignore[misc, valid-type]
        def putheader(self, header: str, *values: Any) -> None:
            if header.lower() == "connection":
                values = ("keep-alive",)
            super().putheader(header, *values)

    return KeepAlive


class _ProxyHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return self.do_open(_keep_alive(http.client.HTTPConnection), req)


class _ProxyHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(_keep_alive(http.client.HTTPSConnection), req, context=self._context)


class _GuardedRedirectHandler(urllib.request.HTTPRedirectHandler):
    max_redirections = 1_000  # our own hop count below is the real limit

    def __init__(self, policy: FetchPolicy) -> None:
        super().__init__()
        self._policy = policy

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        hops = getattr(req, "_hops", 0) + 1
        if hops > self._policy.max_redirects:
            raise RedirectLimit(f"more than {self._policy.max_redirects} redirects")
        problem = url_problem(newurl, self._policy)
        if problem is None and self._policy.use_env_proxy:
            problem = _resolution_problem(newurl, self._policy)
        if problem:
            raise BlockedURL(f"redirect to {newurl} refused: {problem}")
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None:
            new._hops = hops
        return new


def _resolution_problem(url: str, policy: FetchPolicy) -> str | None:
    """Proxy mode only: the proxy connects, so the best we can do is resolve
    the target ourselves first. A rebinding DNS answer can still differ."""
    parsed = urllib.parse.urlsplit(url)
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
    try:
        _resolve_checked(host, port, policy)
    except BlockedURL as exc:
        return str(exc)
    except OSError:
        return None  # let the proxy report resolution failures
    return None


def _build_opener(policy: FetchPolicy) -> urllib.request.OpenerDirector:
    # Built by hand: build_opener() always adds FileHandler, FTPHandler and
    # DataHandler, which is exactly the surface this module exists to remove.
    opener = urllib.request.OpenerDirector()
    if policy.use_env_proxy:
        handlers: list[urllib.request.BaseHandler] = [
            urllib.request.ProxyHandler(),
            _ProxyHTTPHandler(),
            _ProxyHTTPSHandler(context=ssl.create_default_context()),
        ]
    else:
        handlers = [_GuardedHTTPHandler(policy), _GuardedHTTPSHandler(policy)]
    handlers += [
        urllib.request.UnknownHandler(),
        urllib.request.HTTPDefaultErrorHandler(),
        _GuardedRedirectHandler(policy),
        urllib.request.HTTPErrorProcessor(),
    ]
    for handler in handlers:
        opener.add_handler(handler)
    return opener


def open_url(request: urllib.request.Request, timeout: float, policy: FetchPolicy):
    """urlopen under `policy`. Raises BlockedURL if the URL, a redirect or a
    resolved address is refused."""
    problem = url_problem(request.full_url, policy)
    if problem is None and policy.use_env_proxy:
        problem = _resolution_problem(request.full_url, policy)
    if problem:
        raise BlockedURL(problem)
    return _build_opener(policy).open(request, timeout=timeout)
