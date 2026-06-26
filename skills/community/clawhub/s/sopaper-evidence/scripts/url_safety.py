#!/usr/bin/env python3

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse


BLOCKED_HOSTS = {"localhost", "localhost.localdomain"}


def is_public_ip(address: str) -> bool:
    ip = ipaddress.ip_address(address)
    return not (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def assert_public_http_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("only http and https URLs are allowed")
    if not parsed.hostname:
        raise ValueError("URL must include a hostname")
    if parsed.username or parsed.password:
        raise ValueError("URLs with embedded credentials are not allowed")

    host = parsed.hostname.strip().lower().rstrip(".")
    if host in BLOCKED_HOSTS or host.endswith(".localhost") or host.endswith(".local"):
        raise ValueError(f"local host is not allowed: {host}")

    try:
        if not is_public_ip(host):
            raise ValueError(f"non-public IP address is not allowed: {host}")
        return
    except ValueError as exc:
        if "does not appear to be an IPv4 or IPv6 address" not in str(exc):
            raise

    try:
        infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError(f"hostname could not be resolved safely: {host}") from exc

    addresses = {item[4][0] for item in infos}
    if not addresses:
        raise ValueError(f"hostname has no resolved addresses: {host}")
    blocked = [address for address in addresses if not is_public_ip(address)]
    if blocked:
        raise ValueError(f"hostname resolves to non-public address: {host}")


def is_safe_public_http_url(url: str) -> bool:
    try:
        assert_public_http_url(url)
        return True
    except ValueError:
        return False
