#!/usr/bin/env python3
"""Safety helpers for WordPress API Pro scripts.

These helpers intentionally avoid third-party dependencies so the skill remains
portable inside OpenClaw agent environments.
"""

from __future__ import annotations

import http.client
import ipaddress
import os
import socket
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Iterable

DEFAULT_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
# Ceiling on any request that does not set its own. Not a performance knob -
# it exists so a hung or black-holed connection cannot stall an agent for
# ever. Generous enough for a 10 MB media upload on a slow link.
DEFAULT_REQUEST_TIMEOUT = 300  # seconds
TEXT_MAX_BYTES = 2 * 1024 * 1024  # 2 MB


class SafetyError(ValueError):
    """Raised when an input crosses the skill's safety boundaries."""


class HostResolutionError(SafetyError):
    """A hostname could not be resolved at all.

    Unreachable, not unsafe - a typo'd domain is not an attempt to reach
    internal infrastructure, and the site audit has to keep reporting it as a
    site that did not respond. Subclasses SafetyError so callers that only
    care about "this was refused" (the media and file paths) are unchanged.
    """


def _split_roots(raw: str | None) -> list[Path]:
    if not raw:
        return [Path.cwd().resolve()]
    roots: list[Path] = []
    for item in raw.split(os.pathsep):
        item = item.strip()
        if item:
            roots.append(Path(item).expanduser().resolve())
    return roots or [Path.cwd().resolve()]


def allowed_roots() -> list[Path]:
    """Return local filesystem roots this skill may read from.

    Defaults to the current working directory. Override with
    WP_ALLOWED_FILE_ROOTS using os.pathsep-separated paths.
    """

    return _split_roots(os.getenv("WP_ALLOWED_FILE_ROOTS"))


def validate_local_file(path_value: str, *, purpose: str = "file", max_bytes: int = DEFAULT_MAX_BYTES) -> Path:
    """Validate and resolve a local file path before reading it."""

    if not path_value:
        raise SafetyError(f"Missing {purpose} path")

    path = Path(path_value).expanduser().resolve()
    roots = allowed_roots()

    if not path.exists():
        raise SafetyError(f"{purpose} not found: {path}")
    if not path.is_file():
        raise SafetyError(f"{purpose} is not a regular file: {path}")
    if not any(path == root or root in path.parents for root in roots):
        roots_text = ", ".join(str(root) for root in roots)
        raise SafetyError(
            f"Refusing to read {path}. Allowed roots: {roots_text}. "
            "Set WP_ALLOWED_FILE_ROOTS to opt in to another directory."
        )
    size = path.stat().st_size
    if size > max_bytes:
        raise SafetyError(f"{purpose} is too large: {size} bytes > {max_bytes} bytes")
    return path


def _hostname_addresses(hostname: str) -> Iterable[ipaddress._BaseAddress]:
    for family, _, _, _, sockaddr in socket.getaddrinfo(hostname, None):
        if family in (socket.AF_INET, socket.AF_INET6):
            yield ipaddress.ip_address(sockaddr[0])


def validate_remote_url(url: str) -> str:
    """Validate a remote URL before fetching it.

    Only HTTPS URLs are allowed. Hostnames resolving to private, loopback,
    link-local, multicast, unspecified, or reserved addresses are blocked to
    reduce SSRF/exfiltration risk in agentic contexts.
    """

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise SafetyError("Remote media URLs must use https://")
    if not parsed.hostname:
        raise SafetyError("Remote URL must include a hostname")

    _assert_public_host(parsed.hostname)
    return url


def _assert_public_host(hostname: str) -> list[str]:
    """Raise SafetyError unless every address the hostname resolves to is public.

    Shared by validate_remote_url (media downloads, HTTPS only) and
    validate_probe_url (the site audit, which must also reach http://).
    Returns the validated addresses so a caller can CONNECT to one of them
    rather than resolving the name a second time. Resolving twice is a
    time-of-check/time-of-use gap: an attacker controlling the name can answer
    a public address for the check and a private one microseconds later, when
    urlopen resolves it again. The pinned handlers below close that window.
    """

    try:
        addresses = list(_hostname_addresses(hostname))
    except socket.gaierror as exc:
        raise HostResolutionError(f"Could not resolve host {hostname!r}: {exc}") from exc

    if not addresses:
        raise SafetyError(f"Host {hostname!r} resolved to no addresses")

    for address in addresses:
        # is_global is the allowlist half and carries the rule: enumerating
        # non-public categories misses whatever the enumeration forgot, and it
        # forgot RFC 6598 shared address space (100.64.0.0/10) - a CGNAT
        # address is none of private/loopback/link-local/multicast/reserved/
        # unspecified to Python, and is routable on the networks that use it.
        # The named flags stay as the deny half: 64:ff9b::/96 is is_global and
        # still not somewhere this skill should be pointed.
        if not address.is_global or any(
            [
                address.is_private,
                address.is_loopback,
                address.is_link_local,
                address.is_multicast,
                address.is_reserved,
                address.is_unspecified,
            ]
        ):
            raise SafetyError(f"Refusing host {hostname!r}; resolved to unsafe address {address}")
    return [str(address) for address in addresses]


def validate_probe_url(url: str) -> str:
    """Validate a URL the unauthenticated site audit is about to probe.

    Unlike validate_remote_url this permits http://, because detecting whether
    a site redirects to HTTPS is one of the audit's own checks. It still
    refuses any host that resolves to a private, loopback, link-local,
    multicast, reserved or unspecified address, so the audit cannot be pointed
    at internal infrastructure.
    """

    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise SafetyError("Audit URLs must use http:// or https://")
    if not parsed.hostname:
        raise SafetyError("Audit URL must include a hostname")
    _assert_public_host(parsed.hostname)
    return url


def validate_probe_host(hostname: str) -> str:
    """Validate a bare hostname the audit is about to connect to directly.

    The TLS expiry check opens a socket to the host rather than fetching a
    URL, so it has no scheme to validate - only the address rule applies.
    """

    if not hostname:
        raise SafetyError("Audit host must not be empty")
    _assert_public_host(hostname)
    return hostname


class _ValidatingRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Re-validate the target of every redirect, with the caller's own rule.

    Validating only the URL the caller supplied is not enough: a public host is
    free to answer a redirect to an internal address, and urlopen would follow
    it. The rule differs by caller - the audit may follow http://, a media
    download may not - so the validator is a parameter rather than a fixed
    policy.
    """

    def __init__(self, validator):
        super().__init__()
        self._validator = validator

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is None:
            return None
        self._validator(new.full_url)
        return new


def _public_addresses(hostname: str) -> list[str]:
    """Validated addresses for a hostname, in order, without duplicates."""

    seen: set[str] = set()
    unique: list[str] = []
    for address in _assert_public_host(hostname):
        if address not in seen:
            seen.add(address)
            unique.append(address)
    return unique


def _connect_to_public_host(host, port, timeout, source_address=None):
    """Open a socket to an address this module just validated.

    Everything that enforces the address rule connects through here, so the
    address that was checked is the address that is used. Resolving the name
    again at connect time is the DNS-rebinding hole: the check and the use
    would be two different lookups, and an attacker who controls the name
    decides what the second one returns.
    """

    last_error = None
    for address in _public_addresses(host):
        try:
            return socket.create_connection((address, port), timeout, source_address)
        except OSError as exc:      # try the next address, as getaddrinfo order intends
            last_error = exc
    raise last_error if last_error else SafetyError(f"Host {host!r} resolved to no usable address")


class _PinnedHTTPConnection(http.client.HTTPConnection):
    """HTTPConnection that dials a validated address instead of re-resolving."""

    def connect(self):
        self.sock = _connect_to_public_host(self.host, self.port, self.timeout, self.source_address)
        if self._tunnel_host:
            self._tunnel()


class _PinnedHTTPSConnection(http.client.HTTPSConnection):
    """As above, with TLS still verified against the NAME, not the address.

    The certificate and SNI use self.host, so pinning the address changes only
    which endpoint is dialled - it never weakens certificate validation.
    """

    def connect(self):
        sock = _connect_to_public_host(self.host, self.port, self.timeout, self.source_address)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
            sock = self.sock
        self.sock = self._context.wrap_socket(sock, server_hostname=self._tunnel_host or self.host)


class _PinnedHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return self.do_open(_PinnedHTTPConnection, req)


class _PinnedHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(_PinnedHTTPSConnection, req, context=self._context)


PROXY_ENV_VARS = ("http_proxy", "https_proxy", "all_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY")


def _address_enforcing_opener(validator, env=None):
    """An opener that holds every hop AND every connection to `validator`.

    Proxies are disabled here, and that is load-bearing rather than tidiness.
    urllib's default ProxyHandler rewrites the connection host to the proxy
    before these handlers run, so the pinned connection would validate and dial
    the PROXY while the real target travelled on in the absolute request URI
    (http) or in CONNECT (https) - and the proxy would resolve that target
    itself, with none of these rules applied. The pin would be enforcing the
    address of the wrong host. A private enterprise proxy would also be refused
    outright as an unsafe address, which is a confusing way to fail.

    WP_ALLOW_PROXY=1 restores proxy use for an environment where the proxy is
    the only egress, at the cost of end-to-end address enforcement: from there
    the proxy decides what it connects to. That mode also drops the pinned
    connection classes, because they would refuse the proxy itself - an
    enterprise proxy is normally on a private address, which is exactly the
    kind of address they exist to reject. Pinning a connection whose host has
    been rewritten to the proxy enforces nothing anyway: it would check the
    address of the proxy while the real target rides along in the request.
    URL-level validation stays in both modes, for the initial URL and every
    redirect target.
    """

    env = env if env is not None else os.environ
    if env.get("WP_ALLOW_PROXY") == "1":
        return urllib.request.build_opener(_ValidatingRedirectHandler(validator))
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        _PinnedHTTPHandler(),
        _PinnedHTTPSHandler(),
        _ValidatingRedirectHandler(validator),
    )


_proxy_warning_emitted = False


def _warn_proxy_in_use(env=None) -> None:
    """Warn once, when a fetch that claims address enforcement actually runs.

    Warning at import time instead would fire twice (one opener each) in every
    CLI that imports this module - including create_post and the rest, which
    never touch these openers and whose address rules are unaffected.
    """

    global _proxy_warning_emitted
    env = env if env is not None else os.environ
    if _proxy_warning_emitted or env.get("WP_ALLOW_PROXY") != "1":
        return
    if not any(env.get(name) for name in PROXY_ENV_VARS):
        return
    _proxy_warning_emitted = True
    print(
        "SECURITY WARNING: WP_ALLOW_PROXY=1 and a proxy is configured - "
        "the proxy resolves and connects to the target, so this skill's "
        "address rules are not enforced end to end.",
        file=sys.stderr,
    )


_PROBE_OPENER = _address_enforcing_opener(validate_probe_url)
_MEDIA_OPENER = _address_enforcing_opener(validate_remote_url)


def connect_public_tls(host, port=443, timeout=10):
    """TLS-connect to a validated address for `host`, for certificate inspection.

    The site audit's expiry check opens its own socket rather than fetching a
    URL, so it needs the same pinning the openers above apply.
    """

    context = ssl.create_default_context()
    sock = _connect_to_public_host(host, port, timeout)
    try:
        return context.wrap_socket(sock, server_hostname=host)
    except Exception:
        sock.close()
        raise


def urlopen_probe(req, timeout=None):
    """urlopen for the unauthenticated site audit.

    Validates the requested URL and the target of every redirect against the
    public-address rule. Carries no credentials, so unlike
    urlopen_authenticated it has no Authorization header to strip.
    """

    url = req.full_url if isinstance(req, urllib.request.Request) else req
    validate_probe_url(url)
    _warn_proxy_in_use()
    return _PROBE_OPENER.open(
        req, timeout=DEFAULT_REQUEST_TIMEOUT if timeout is None else timeout)


def read_limited_response(response, *, max_bytes: int = DEFAULT_MAX_BYTES) -> bytes:
    """Read a response body with a strict size limit."""

    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(65536, max_bytes + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > max_bytes:
            raise SafetyError(f"Remote response is too large: > {max_bytes} bytes")
    return b"".join(chunks)


def fetch_https_media(url: str, *, timeout: int = 20, max_bytes: int = DEFAULT_MAX_BYTES):
    """Fetch a validated HTTPS URL and return (response, body)."""

    validate_remote_url(url)
    _warn_proxy_in_use()
    request = urllib.request.Request(url, headers={"User-Agent": "wordpress-api-pro/3.4.0"})
    # Through the media opener, so a redirect is held to the same rule as the
    # URL the caller supplied: HTTPS only, and a globally reachable address.
    # Without it a public HTTPS host could redirect to http://127.0.0.1/ and
    # urlopen would follow, which is the SSRF this validator exists to prevent.
    response = _MEDIA_OPENER.open(request, timeout=timeout)
    body = read_limited_response(response, max_bytes=max_bytes)
    return response, body


class _AuthStrippingRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Drop the Authorization header when a redirect leaves the origin.

    CPython's HTTPRedirectHandler copies every header except content-length
    and content-type onto the redirected request, so a WordPress site (or
    anything in front of it) answering 30x with a Location on another host
    receives the Basic-Auth application password verbatim. requests strips it;
    urllib does not. Same-origin redirects keep the header so ordinary
    WordPress behaviour (trailing slashes, canonical URLs) still works.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is None:
            return None
        if not same_origin(req.full_url, new.full_url):
            for name in list(new.headers):
                if name.lower() == "authorization":
                    del new.headers[name]
            # Request stores headers capitalized; unredirected_hdrs too.
            for name in list(getattr(new, "unredirected_hdrs", {})):
                if name.lower() == "authorization":
                    del new.unredirected_hdrs[name]
        return new


def same_origin(first: str, second: str) -> bool:
    """True when two URLs share scheme, host and effective port."""

    a, b = urllib.parse.urlparse(first), urllib.parse.urlparse(second)
    default = {"http": 80, "https": 443}
    return (
        a.scheme == b.scheme
        and (a.hostname or "").lower() == (b.hostname or "").lower()
        and (a.port or default.get(a.scheme)) == (b.port or default.get(b.scheme))
    )


_AUTH_SAFE_OPENER = urllib.request.build_opener(_AuthStrippingRedirectHandler)


def urlopen_authenticated(req, timeout=None):
    """urlopen for requests that carry credentials.

    Identical to urllib.request.urlopen except that a redirect crossing the
    origin loses the Authorization header, and an unset timeout is bounded
    rather than infinite. Every authenticated call in this
    skill goes through here; a bare urlopen with an Authorization header is a
    credential-forwarding bug.
    """

    return _AUTH_SAFE_OPENER.open(
        req, timeout=DEFAULT_REQUEST_TIMEOUT if timeout is None else timeout)


def check_wp_url_scheme(url, env=None):
    """Refuse a WordPress API URL that is plaintext http:// on a non-local host.

    Basic-Auth credentials would travel unencrypted, and an app password read
    off the wire is the whole site. Localhost and .local/.test/.localhost dev
    hosts are exempt and never warn.

    Refusing is the default as of 3.9.0. The escape hatch is a HOST LIST, not a
    switch: WP_ALLOW_HTTP=staging.example.com (comma-separated for several)
    permits plaintext for exactly those hosts. WP_ALLOW_HTTP=1 is refused as of
    3.9.5 - it used to mean "any host", so one variable set for one staging box
    silently covered every site the agent touched afterwards, including
    production. WP_REQUIRE_HTTPS=1 still refuses everything and wins over the
    list.

    Returns the url unchanged (never mutates it); raises SafetyError to refuse.
    """

    env = env if env is not None else os.environ
    parsed = urllib.parse.urlparse(url if "://" in str(url) else "https://" + str(url))
    host = (parsed.hostname or "").lower()
    is_local = (
        host in ("localhost", "127.0.0.1", "0.0.0.0", "::1")
        or host.endswith(".local")
        or host.endswith(".test")
        or host.endswith(".localhost")
    )
    if parsed.scheme == "http" and not is_local:
        msg = (
            "WordPress URL '%s' uses plaintext http:// - "
            "Basic-Auth credentials would be sent unencrypted. Use https:// in production." % url
        )
        # Strictness is checked FIRST: when WP_REQUIRE_HTTPS=1 is also set, every
        # other message here would propose a change that cannot work, because it
        # overrides the allowlist either way.
        if env.get("WP_REQUIRE_HTTPS") == "1":
            raise SafetyError(msg + " (WP_REQUIRE_HTTPS=1 is set - refusing.)")
        raw = env.get("WP_ALLOW_HTTP") or ""
        allowed = {item.strip().lower() for item in raw.split(",") if item.strip()}
        if allowed & {"1", "true", "yes", "all", "*"}:
            raise SafetyError(
                msg + " WP_ALLOW_HTTP no longer takes a blanket value: name the host(s) "
                "instead, e.g. WP_ALLOW_HTTP=%s" % (host or "staging.example.com")
            )
        if host not in allowed:
            hint = (" (Set WP_ALLOW_HTTP=%s to send them to THIS host anyway.)" % host) if host else ""
            raise SafetyError(msg + hint)
        print("SECURITY WARNING: " + msg
              + " (WP_ALLOW_HTTP names %s - continuing.)" % host, file=sys.stderr)
    return url


def require_secure_wp_url(url, env=None):
    """check_wp_url_scheme at the CLI boundary: exit 2 instead of raising.

    Every script calls this one line before it authenticates, so a refusal has
    to read as a safety error rather than as an uncaught traceback.
    """

    try:
        return check_wp_url_scheme(url, env=env)
    except SafetyError as error:
        die_safety(error)


def check_wp_url_schemes(targets, env=None):
    """Check a whole batch of targets up front. Returns a list of (label, message).

    `targets` is an iterable of (label, url) pairs. A multi-site run must know
    about every insecure URL BEFORE it writes to the first site: refusing in the
    middle of the loop leaves the earlier sites modified, the later ones
    untouched and no summary printed.
    """

    problems = []
    for label, url in targets:
        try:
            check_wp_url_scheme(url, env=env)
        except SafetyError as error:
            problems.append((label, str(error)))
    return problems


def require_secure_wp_urls(targets, env=None):
    """check_wp_url_schemes at the CLI boundary: exit 2 naming every offender."""

    problems = check_wp_url_schemes(targets, env=env)
    if problems:
        for label, message in problems:
            print(f"Safety error: {label}: {message}", file=sys.stderr)
        sys.exit(2)


def should_confirm_publish(status, assume_yes, is_tty):
    """True only when we should interactively prompt before a live publish:
    going to 'publish', not pre-approved with --yes, and attached to a TTY.
    Non-interactive (agent/CI) contexts return False -> behavior unchanged."""
    return status == "publish" and not assume_yes and bool(is_tty)


class ErrorResult(dict):
    """A helper's failure envelope.

    Still a dict - it serialises identically and callers can index it - but a
    distinct TYPE, because key presence cannot identify a failure here. The ACF
    and JetEngine getters return the SITE's own field dictionary, so a custom
    field named "error" (or an explicit --field error lookup) is ordinary data
    that must not be mistaken for a failed call.
    """


def error_result(message, **extra) -> ErrorResult:
    """Build the failure envelope every helper returns instead of raising."""

    return ErrorResult({"error": message, **extra})


def exit_on_error_result(result) -> None:
    """Exit 1 when a helper returned an ErrorResult instead of raising.

    Several scripts report failure by returning rather than raising, so without
    this the CLI printed the error and still exited 0 - which CI and an agent
    both read as success. Call it after printing the result, so the JSON is
    still on stdout for whoever wants to parse it.
    """

    if isinstance(result, ErrorResult):
        sys.exit(1)


def die_safety(error: Exception) -> None:
    print(f"Safety error: {error}", file=sys.stderr)
    sys.exit(2)
