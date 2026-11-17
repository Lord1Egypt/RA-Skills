#!/usr/bin/env python3
"""
ratsinfo.py - a polite command line client for German council information
systems (Ratsinformationssysteme) that speak OParl 1.0 / 1.1.

Standard library only. No installation, no dependencies.

Design rules, in order of importance:

  1. Be polite. One request per second per host, an identifiable
     User-Agent, exponential backoff on 429 and 503, robots.txt honoured
     by default. Many of these systems run on small municipal data
     centres where dozens of towns share one machine.
  2. Never pretend. If an endpoint is dead, disabled or blocked, say so
     and stop. Do not fall back to scraping the HTML frontend.
  3. Bound every crawl. OParl has no full text search, so any search is a
     client side filter over a paginated list. Always give the crawl a
     date floor and a hard page limit.

Specification: https://oparl.org/spezifikation/online-ansicht/
Endpoint registry: https://dev.oparl.org/api/endpoints
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

__version__ = "1.1.0"

USER_AGENT = os.environ.get(
    "RATSINFO_USER_AGENT",
    f"ratsinfo-de/{__version__} (+https://clawhub.ai/skills/ratsinfo-de) python-urllib",
)

REGISTRY_URL = os.environ.get(
    "RATSINFO_REGISTRY", "https://dev.oparl.org/api/endpoints"
)
CACHE_DIR = os.environ.get(
    "RATSINFO_CACHE", os.path.expanduser("~/.cache/ratsinfo-de")
)

MIN_INTERVAL = max(0.0, float(os.environ.get("RATSINFO_MIN_INTERVAL", "1.0")))
TIMEOUT = float(os.environ.get("RATSINFO_TIMEOUT", "30"))
MAX_RETRIES = 3
MAX_BYTES = 32 * 1024 * 1024
MAX_RETRY_AFTER = 300.0

_last_request_at = {}
_robots_cache = {}
_host_delay = {}
_allowed_hosts = set()
_allow_cross_host = False

# Only http and https. Building our own opener removes urllib's file and ftp
# handlers entirely, so a hostile endpoint cannot point links.next at
# file:///home/you/.ssh/id_rsa and have us read it back to the agent.
_OPENER = urllib.request.build_opener(
    urllib.request.HTTPHandler,
    urllib.request.HTTPSHandler,
    urllib.request.HTTPRedirectHandler,
    urllib.request.HTTPErrorProcessor,
)


# --------------------------------------------------------------------------
# polite HTTP
# --------------------------------------------------------------------------

class RatsinfoError(RuntimeError):
    """Anything that should stop the run with a readable message."""


def _host(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    return f"{parts.scheme}://{parts.netloc}".lower()


def allow_host(url: str) -> None:
    """Every command registers the endpoint the user actually named."""
    _allowed_hosts.add(_host(url))


def set_cross_host(allowed: bool) -> None:
    global _allow_cross_host
    _allow_cross_host = allowed


def _check_url(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https"):
        raise RatsinfoError(
            f"refusing {parts.scheme or 'schemeless'} URL: {url[:120]}\n"
            "  Only http and https are allowed. An OParl endpoint that points\n"
            "  anywhere else is either broken or hostile."
        )
    if not parts.netloc:
        raise RatsinfoError(f"not an absolute URL: {url[:120]}")

    host = _host(url)
    if _allowed_hosts and host not in _allowed_hosts and not _allow_cross_host:
        raise RatsinfoError(
            f"{host} is not the endpoint you asked for.\n"
            "  The server sent a link pointing at a different host. That can be\n"
            "  legitimate, for example a shared document server, and it can be an\n"
            "  attempt to make this client fetch something else. Nothing was\n"
            "  requested. Repeat with --allow-cross-host if you want it followed."
        )
    return url


def _throttle(url: str) -> None:
    """One request per second per host, or slower if robots.txt says so.

    Keyed on the host, not on the municipality: several municipal data
    centres serve dozens of towns from one machine.
    """
    host = _host(url)
    interval = max(MIN_INTERVAL, _host_delay.get(host, 0.0))
    last = _last_request_at.get(host)
    if last is not None:
        wait = interval - (time.monotonic() - last)
        if wait > 0:
            time.sleep(wait)
    _last_request_at[host] = time.monotonic()


def _robots_allows(url: str) -> bool:
    host = _host(url)
    if host not in _robots_cache:
        parser = urllib.robotparser.RobotFileParser()
        parts = urllib.parse.urlsplit(url)
        robots_url = urllib.parse.urlunsplit(
            (parts.scheme, parts.netloc, "/robots.txt", "", "")
        )
        try:
            _throttle(robots_url)
            req = urllib.request.Request(
                robots_url, headers={"User-Agent": USER_AGENT}
            )
            with _OPENER.open(req, timeout=TIMEOUT) as resp:
                body = resp.read(1024 * 1024).decode("utf-8", "replace")
            parser.parse(body.splitlines())
        except urllib.error.HTTPError as exc:
            # RFC 9309: 401 and 403 mean the whole site is off limits,
            # 5xx means off limits for now. Only 404 means "no rules".
            if exc.code in (401, 403):
                parser.disallow_all = True
            elif exc.code >= 500:
                parser.disallow_all = True
            else:
                parser = None
        except Exception:
            parser = None  # no robots.txt reachable, treat as no rules
        _robots_cache[host] = parser
        if parser is not None:
            delay = parser.crawl_delay(USER_AGENT.split("/")[0])
            if delay:
                _host_delay[host] = float(delay)

    parser = _robots_cache[host]
    if parser is None:
        return True
    return parser.can_fetch(USER_AGENT, url)


def _retry_after(exc) -> float | None:
    raw = exc.headers.get("Retry-After") if getattr(exc, "headers", None) else None
    if not raw:
        return None
    try:
        return min(float(raw), MAX_RETRY_AFTER)
    except ValueError:
        return None


def fetch_json(url: str, *, ignore_robots: bool = False) -> dict:
    """GET one JSON document, politely, with backoff. GET only, never POST,
    no credentials, no cookies."""
    url = _check_url(url)
    if not ignore_robots and not _robots_allows(url):
        raise RatsinfoError(
            f"robots.txt on {_host(url)} disallows this path.\n"
            "  Several council systems block their own OParl endpoint with a\n"
            "  blanket rule aimed at search engines. Ask the operator (the\n"
            "  contactEmail in the System object) for permission, then repeat\n"
            "  with --ignore-robots."
        )

    delay = 2.0
    for attempt in range(MAX_RETRIES):
        _throttle(url)
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/json, */*;q=0.5",
                },
                method="GET",
            )
            with _OPENER.open(req, timeout=TIMEOUT) as resp:
                final = resp.geturl()
                if _host(final) != _host(url):
                    _check_url(final)  # a redirect off host needs consent too
                raw = resp.read(MAX_BYTES + 1)
                if len(raw) > MAX_BYTES:
                    raise RatsinfoError(
                        f"{url} returned more than {MAX_BYTES // 1048576} MB. "
                        "Refusing to read further."
                    )
                charset = resp.headers.get_content_charset() or "utf-8"
                ctype = resp.headers.get("Content-Type", "")
                encoding = resp.headers.get("Content-Encoding", "")
        except urllib.error.HTTPError as exc:
            if exc.code in (429, 503) and attempt < MAX_RETRIES - 1:
                time.sleep(_retry_after(exc) or delay)
                delay *= 2
                continue
            raise RatsinfoError(f"HTTP {exc.code} for {url}") from exc
        except RatsinfoError:
            raise
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempt < MAX_RETRIES - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RatsinfoError(f"{type(exc).__name__} for {url}: {exc}") from exc
        except ValueError as exc:  # malformed URL from the server
            raise RatsinfoError(f"cannot request {url[:120]}: {exc}") from exc

        try:
            text = raw.decode(charset, "replace").lstrip("\ufeff")
        except LookupError:
            text = raw.decode("utf-8", "replace").lstrip("\ufeff")

        try:
            doc = json.loads(text)
        except json.JSONDecodeError:
            head = text[:4000]
            snippet = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", head))[:200]
            hint = (
                "  The server sent a compressed body we did not ask for.\n"
                if encoding
                else "  A bot check page here usually means CC e-gov ALLRIS. Those\n"
                "  endpoints need a browser session and are out of scope.\n"
            )
            raise RatsinfoError(
                f"{url} did not return JSON (Content-Type: {ctype or 'unset'}).\n"
                f"  First characters: {snippet.strip()!r}\n" + hint
            )
        if not isinstance(doc, dict):
            raise RatsinfoError(
                f"{url} returned {type(doc).__name__}, not an OParl object."
            )
        return doc

    raise RatsinfoError(f"giving up on {url}")


# --------------------------------------------------------------------------
# OParl helpers
# --------------------------------------------------------------------------

def iter_list(url: str, *, max_pages: int = 20, ignore_robots: bool = False):
    """Walk an OParl external list by following links.next.

    pagination is optional in the specification and totalPages is often
    missing or wrong, so next is the only reliable way forward.
    """
    seen = set()
    page = 0
    while url and page < max_pages:
        if url in seen:  # a few systems link back to themselves
            break
        seen.add(url)
        doc = fetch_json(url, ignore_robots=ignore_robots)
        data = doc.get("data")
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    yield item
                elif isinstance(item, str) and item.startswith("http"):
                    yield _deref(item, ignore_robots=ignore_robots)
        elif data is not None:
            raise RatsinfoError(
                f"{url} returned data as {type(data).__name__}, not a list. "
                "This is not a valid OParl list."
            )
        nxt = (doc.get("links") or {}).get("next") or ""
        url = urllib.parse.urljoin(url, nxt) if nxt else ""
        page += 1


def system_info(endpoint: str, *, ignore_robots: bool = False) -> dict:
    allow_host(endpoint)
    doc = fetch_json(endpoint, ignore_robots=ignore_robots)
    if str(doc.get("type", "")).endswith("Error"):
        raise RatsinfoError(
            f"{endpoint} answers with an OParl error: "
            f"{doc.get('message', 'no message')}. The endpoint exists but is "
            "switched off. This is common in the public registry."
        )
    if "oparlVersion" not in doc:
        raise RatsinfoError(
            f"{endpoint} answered JSON without oparlVersion, so it is not an "
            "OParl System object. Check the URL."
        )
    return doc


def all_bodies(system: dict, *, ignore_robots: bool = False) -> list[dict]:
    body_list = system.get("body")
    if not body_list:
        raise RatsinfoError("System object has no body list.")
    if isinstance(body_list, list):  # some servers inline the bodies
        return [
            b if isinstance(b, dict) else _deref(b, ignore_robots=ignore_robots)
            for b in body_list
        ]
    bodies = list(iter_list(body_list, max_pages=3, ignore_robots=ignore_robots))
    if not bodies:
        raise RatsinfoError("body list is empty.")
    return bodies


def pick_body(system: dict, index: int = 0, *, ignore_robots: bool = False) -> dict:
    """Choose one body. A Kreis or a Verbandsgemeinde often has several, and
    silently taking the first one is how you end up searching the wrong
    council without noticing."""
    bodies = all_bodies(system, ignore_robots=ignore_robots)
    if index < 0 or index >= len(bodies):
        raise RatsinfoError(
            f"body {index} does not exist, this system has {len(bodies)}. "
            "Run the bodies command to see them."
        )
    if len(bodies) > 1 and index == 0:
        print(
            f"note: this system has {len(bodies)} bodies, using "
            f"{bodies[0].get('name', '0')!r}. Use --body N for another one.",
            file=sys.stderr,
        )
    return bodies[index]


def _since_iso(days: int | None, since: str | None) -> str | None:
    if since:
        return since if "T" in since else f"{since}T00:00:00+00:00"
    if days:
        stamp = datetime.now(timezone.utc) - timedelta(days=days)
        return stamp.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    return None


def _with_filter(url: str, **params: str | None) -> str:
    clean = {k: v for k, v in params.items() if v}
    if not clean:
        return url
    parts = urllib.parse.urlsplit(url)
    query = dict(urllib.parse.parse_qsl(parts.query))
    query.update(clean)
    return urllib.parse.urlunsplit(
        parts[:3] + (urllib.parse.urlencode(query), parts[4])
    )


def _matches(item: dict, terms: list[str], fields: tuple[str, ...]) -> bool:
    if not terms:
        return True
    haystack = " ".join(
        str(item.get(f, "")) for f in fields
    ).lower()
    return all(t.lower() in haystack for t in terms)



# --------------------------------------------------------------------------
# the consultation chain: Paper -> Consultation -> AgendaItem -> Meeting
# --------------------------------------------------------------------------

_name_cache: dict[str, str] = {}


def resolve_name(value, *, ignore_robots: bool = False) -> str | None:
    """Turn an organization or person URL into its name, cached.

    A council has a handful of committees, so the cache turns what looks
    like one request per membership into one request per committee.
    """
    if isinstance(value, dict):
        return value.get("name") or value.get("shortName")
    if not isinstance(value, str) or not value.startswith("http"):
        return None
    if value not in _name_cache:
        obj = _deref(value, ignore_robots=ignore_robots)
        _name_cache[value] = obj.get("name") or obj.get("shortName") or value
    return _name_cache[value]


def _deref(value, *, ignore_robots: bool = False):
    """OParl embeds some objects and links others. Accept both."""
    if isinstance(value, dict):
        return value
    if isinstance(value, str) and value.startswith("http"):
        try:
            return fetch_json(value, ignore_robots=ignore_robots)
        except RatsinfoError:
            return {}
    return {}


def _file_info(value):
    """Normalise an OParl File into name, url and size."""
    if isinstance(value, str) and value.startswith("http"):
        return {"name": None, "url": value, "size": None}
    if not isinstance(value, dict):
        return None
    url = value.get("accessUrl") or value.get("downloadUrl")
    if not url:
        return None
    return {
        "name": value.get("name") or value.get("fileName"),
        "url": url,
        "size": value.get("size"),
        "mimeType": value.get("mimeType"),
    }


def _location_name(value):
    if isinstance(value, dict):
        return (
            value.get("description")
            or value.get("streetAddress")
            or value.get("room")
            or value.get("locality")
        )
    return None


def consultation_chain(
    paper_url: str, *, max_steps: int = 50, ignore_robots: bool = False
) -> dict:
    """Resolve what became of a council paper.

    This is the question every user of council records actually has and that
    no council frontend answers: which committee dealt with it, when, in
    what role, with what result, and where it is now. It is answerable
    entirely from OParl metadata, without reading a single PDF.
    """
    paper = fetch_json(paper_url, ignore_robots=ignore_robots)
    if str(paper.get("type", "")).endswith("Error"):
        raise RatsinfoError(f"{paper_url}: {paper.get('message', 'error')}")

    raw_consultations = paper.get("consultation")
    if isinstance(raw_consultations, str):
        raw_consultations = list(
            iter_list(raw_consultations, max_pages=5, ignore_robots=ignore_robots)
        )
    elif isinstance(raw_consultations, dict):
        raw_consultations = [raw_consultations]
    elif raw_consultations is None:
        raw_consultations = []
    elif not isinstance(raw_consultations, list):
        raise RatsinfoError(
            "the consultation field is neither a list, an object nor a URL, "
            "so the route of this paper cannot be resolved. Refusing to guess."
        )

    steps = []
    truncated = len(raw_consultations) > max_steps
    for raw in raw_consultations[:max_steps]:
        consultation = _deref(raw, ignore_robots=ignore_robots)
        if not consultation or consultation.get("deleted"):
            continue
        agenda = _deref(consultation.get("agendaItem"), ignore_robots=ignore_robots)
        meeting = _deref(
            agenda.get("meeting") or consultation.get("meeting"),
            ignore_robots=ignore_robots,
        )
        organization = consultation.get("organization")
        if isinstance(organization, list):
            organization = organization[0] if organization else None
        org_name = resolve_name(organization, ignore_robots=ignore_robots)

        steps.append(
            {
                "date": meeting.get("start"),
                "end": meeting.get("end"),
                "organization": org_name,
                "role": consultation.get("role"),
                "authoritative": bool(consultation.get("authoritative")),
                "public": agenda.get("public"),
                "number": agenda.get("number"),
                "name": agenda.get("name"),
                "result": agenda.get("result"),
                "resolutionText": agenda.get("resolutionText"),
                "resolutionFile": _file_info(agenda.get("resolutionFile")),
                "cancelled": bool(meeting.get("cancelled")),
                "meeting": meeting.get("id"),
                "meeting_name": meeting.get("name"),
                "location": _location_name(meeting.get("location")),
                "invitation": _file_info(meeting.get("invitation")),
                "resultsProtocol": _file_info(meeting.get("resultsProtocol")),
                "verbatimProtocol": _file_info(meeting.get("verbatimProtocol")),
                "participants": len(meeting.get("participant") or []),
                "auxiliaryFiles": [
                    _file_info(f) for f in (meeting.get("auxiliaryFile") or [])[:8]
                ],
            }
        )

    steps.sort(key=lambda s: s.get("date") or "")

    decided = next(
        (s for s in reversed(steps) if s["authoritative"] and s.get("result")), None
    )
    last = steps[-1] if steps else None
    if decided:
        status = f"decided on {(decided['date'] or '')[:10]}: {decided['result']}"
    elif last and last.get("result"):
        status = f"last result {last['result']} on {(last['date'] or '')[:10]}"
    elif last:
        status = f"pending since {(last['date'] or '')[:10]}"
    else:
        status = "no consultation recorded, this paper was never tabled"

    if truncated:
        status = (
            f"{status} (only the first {max_steps} consultations were resolved, "
            "raise --max-steps if you need the rest)"
        )

    files = []
    main = _file_info(paper.get("mainFile"))
    if main:
        main["role"] = "Hauptdokument"
        files.append(main)
    for raw_file in (paper.get("auxiliaryFile") or [])[:20]:
        info = _file_info(raw_file)
        if info:
            info["role"] = "Anlage"
            files.append(info)

    def _names(key):
        out = []
        for item in paper.get(key) or []:
            name = resolve_name(item, ignore_robots=ignore_robots)
            if name:
                out.append(name)
        return out

    return {
        "paper": {
            "reference": paper.get("reference"),
            "name": paper.get("name"),
            "date": paper.get("date"),
            "paperType": paper.get("paperType"),
            "id": paper.get("id"),
            "files": files,
            "keywords": [k for k in (paper.get("keyword") or []) if isinstance(k, str)],
            "underDirectionOf": _names("underDirectionOf"),
            "originator": _names("originatorPerson") + _names("originatorOrganization"),
            "location": _location_name(paper.get("location"))
            or (_location_name((paper.get("location") or [{}])[0])
                if isinstance(paper.get("location"), list) else None),
            "relatedPaper": [
                r if isinstance(r, str) else (r or {}).get("id")
                for r in (paper.get("relatedPaper") or [])
                if isinstance(r, (str, dict))
            ],
            "superordinatedPaper": paper.get("superordinatedPaper"),
        },
        "status": status,
        "steps": steps,
    }


# --------------------------------------------------------------------------
# incremental monitoring
# --------------------------------------------------------------------------

def _state_path(endpoint: str, kind: str) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", f"{_host(endpoint)}-{kind}".lower()).strip("-")
    return os.path.join(CACHE_DIR, f"watch-{slug}.json")


def load_state(endpoint: str, kind: str) -> dict:
    path = _state_path(endpoint, kind)
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError) as exc:
            print(
                f"note: watch state at {path} is unreadable ({exc}), "
                "starting from scratch.",
                file=sys.stderr,
            )
    return {}


def save_state(endpoint: str, kind: str, state: dict) -> None:
    path = _state_path(endpoint, kind)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(state, handle, ensure_ascii=False, indent=1)
    os.replace(tmp, path)  # never leave a half written state behind


def _ics_escape(value: str) -> str:
    """RFC 5545 escaping. Order matters: backslash first.

    Without this a meeting title containing a line break writes arbitrary
    calendar lines into the user's calendar file.
    """
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
        .replace("\r", "")
    )


def _ics_fold(line: str) -> str:
    """Content lines are limited to 75 octets."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    out, start = [], 0
    limit = 75
    while start < len(raw):
        end = min(start + limit, len(raw))
        while end > start and (raw[end - 1] & 0xC0) == 0x80:
            end -= 1  # never split a UTF-8 sequence
        out.append(raw[start:end].decode("utf-8", "ignore"))
        start = end
        limit = 74
    return "\r\n ".join(out)


def _ics_stamp(value):
    """Return a UTC timestamp, or None when the value cannot be trusted.

    German systems send +01:00 and +02:00. Writing those through unchanged
    produced timestamps that no calendar accepts, which silently shifted or
    dropped every appointment.
    """
    if not value or not isinstance(value, str):
        return None
    text = value.strip().replace("Z", "+00:00")  # fromisoformat pre 3.11
    try:
        moment = datetime.fromisoformat(text)
    except ValueError:
        return None
    if moment.tzinfo is None:
        return moment.strftime("%Y%m%dT%H%M%S")  # floating local time
    return moment.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def to_ics(meetings: list) -> str:
    """Minimal iCalendar output. Every project that survived in this field
    offered a calendar feed, because a council date is only useful before it
    happens."""
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:-//ratsinfo-de//{__version__}//DE",
        "CALSCALE:GREGORIAN",
    ]
    written = 0
    for meeting in meetings:
        start = _ics_stamp(meeting.get("start"))
        if not start:
            continue
        written += 1
        uid = re.sub(r"[^A-Za-z0-9]", "", str(meeting.get("id", "")))[-40:] or str(
            written
        )
        event = [
            "BEGIN:VEVENT",
            f"UID:{uid}@ratsinfo-de",
            f"DTSTART:{start}",
        ]
        end = _ics_stamp(meeting.get("end"))
        if end:
            event.append(f"DTEND:{end}")
        summary = str(meeting.get("name") or "Sitzung")
        if meeting.get("cancelled"):
            summary = "ABGESAGT: " + summary
            event.append("STATUS:CANCELLED")
        event.append(f"SUMMARY:{_ics_escape(summary)}")
        url = meeting.get("id")
        if isinstance(url, str) and url.startswith("http"):
            event.append(f"URL:{_ics_escape(url)}")
        event.append("END:VEVENT")
        lines.extend(event)
    lines.append("END:VCALENDAR")
    return "\r\n".join(_ics_fold(line) for line in lines) + "\r\n"


# --------------------------------------------------------------------------
# registry
# --------------------------------------------------------------------------

def load_registry(*, refresh: bool = False) -> list[dict]:
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, "endpoints.json")
    if not refresh and os.path.exists(cache_file):
        age = time.time() - os.path.getmtime(cache_file)
        if age < 7 * 24 * 3600:
            try:
                with open(cache_file, encoding="utf-8") as handle:
                    return json.load(handle)
            except (json.JSONDecodeError, OSError):
                pass  # damaged cache, fetch again

    entries = []
    allow_host(REGISTRY_URL)
    url = REGISTRY_URL
    for _ in range(20):
        doc = fetch_json(url)
        entries.extend(
            e for e in (doc.get("data") or []) if isinstance(e, dict)
        )
        nxt = (doc.get("links") or {}).get("next") or ""
        url = urllib.parse.urljoin(url, nxt) if nxt else ""
        if not url:
            break
    if entries:
        tmp = cache_file + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(entries, handle, ensure_ascii=False, indent=1)
        os.replace(tmp, cache_file)
    return entries


VENDOR_PATTERNS = [
    (r"/webservice/oparl/v1\.\d/", "STERNBERG SD.NET RIM"),
    (r"\.gremien\.info/", "more! software more! rubin"),
    (r"/oparl/1\.\d/system\.asp|/oi/oparl/|/bi/oparl/", "CC e-gov ALLRIS"),
    (r"sitzung-online\.de|ratsinfo-online\.net", "CC e-gov ALLRIS"),
    (r"/oparl/system|/oparl/1\.1/", "SOMACOS Session (probably)"),
]


def guess_vendor(url: str) -> str:
    for pattern, name in VENDOR_PATTERNS:
        if re.search(pattern, url, re.I):
            return name
    return "unknown"


# --------------------------------------------------------------------------
# output
# --------------------------------------------------------------------------

def emit(args, payload, lines: list[str]) -> None:
    """Print either machine readable JSON or the human table.

    An agent should use --json. A person reading a terminal should not have
    to.
    """
    if getattr(args, "json", False):
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        for line in lines:
            print(line)


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_find(args) -> int:
    entries = load_registry(refresh=args.refresh)
    needle = args.name.lower()
    hits = [
        e
        for e in entries
        if needle in str(e.get("title", "")).lower()
        or needle in str(e.get("url", "")).lower()
    ]
    if not hits:
        message = (
            f"No entry for {args.name!r} in the registry "
            f"({len(entries)} endpoints known).\n"
            "The registry is a lower bound, not a census. Many towns never\n"
            "reported their endpoint. Try the vendor URL patterns in\n"
            "references/vendors.md before concluding there is none."
        )
        emit(args, {"query": args.name, "known": len(entries), "hits": []},
             [message])
        return 1

    payload = [
        {
            "title": e.get("title"),
            "url": e.get("url"),
            "vendor_guess": guess_vendor(str(e.get("url", ""))),
        }
        for e in hits
    ]
    lines = []
    for hit in payload:
        lines.append(f"{hit['title'] or '?'}")
        lines.append(f"  {hit['url']}")
        lines.append(f"  vendor guess: {hit['vendor_guess']}")
    emit(args, {"query": args.name, "known": len(entries), "hits": payload}, lines)
    return 0


def cmd_check(args) -> int:
    system = system_info(args.endpoint, ignore_robots=args.ignore_robots)
    bodies = all_bodies(system, ignore_robots=args.ignore_robots)
    payload = {
        "endpoint": args.endpoint,
        "oparlVersion": system.get("oparlVersion"),
        "name": system.get("name"),
        "product": system.get("product"),
        "vendor": system.get("vendor"),
        "vendor_guess": guess_vendor(args.endpoint),
        "contactEmail": system.get("contactEmail"),
        "license": system.get("license"),
        "bodies": [
            {
                "name": b.get("name"),
                "id": b.get("id"),
                "paper": b.get("paper"),
                "meeting": b.get("meeting"),
                "organization": b.get("organization"),
                "person": b.get("person"),
                "ags": b.get("ags"),
                "rgs": b.get("rgs"),
                "equivalent": b.get("equivalent"),
            }
            for b in bodies
        ],
    }

    lines = [
        f"endpoint      {args.endpoint}",
        f"oparlVersion  {system.get('oparlVersion') or '-'}",
        f"name          {system.get('name') or '-'}",
        f"product       {system.get('product') or '-'}",
        f"vendor        {system.get('vendor') or '-'}",
        f"contactEmail  {system.get('contactEmail') or '-'}",
        f"license       {system.get('license') or '-'}",
    ]
    for i, body in enumerate(bodies):
        keys = " ".join(
            f"{k}={body[k]}" for k in ("ags", "rgs") if body.get(k)
        )
        lines.append(
            f"body [{i}]      {body.get('name') or '-'}"
            + (f"   {keys}" if keys else "")
        )
        for key in ("paper", "meeting", "organization", "person"):
            if body.get(key):
                lines.append(f"  {key:<12} {body[key]}")
    if not system.get("license"):
        lines.append("")
        lines.append(
            "Note: no license stated. The documents may still be reusable,"
        )
        lines.append(
            "but nothing here says so. Ask before you republish them."
        )
    emit(args, payload, lines)
    return 0


def cmd_bodies(args) -> int:
    system = system_info(args.endpoint, ignore_robots=args.ignore_robots)
    bodies = all_bodies(system, ignore_robots=args.ignore_robots)
    payload = [
        {
            "index": i,
            "name": b.get("name"),
            "id": b.get("id"),
            "ags": b.get("ags"),
            "rgs": b.get("rgs"),
        }
        for i, b in enumerate(bodies)
    ]
    lines = [
        f"[{b['index']}] {b['name'] or '-'}"
        + (f"   ags={b['ags']}" if b.get("ags") else "")
        + f"\n    {b['id']}"
        for b in payload
    ]
    emit(args, payload, lines)
    return 0


def _list_url(args, key: str) -> str:
    system = system_info(args.endpoint, ignore_robots=args.ignore_robots)
    body = pick_body(system, args.body, ignore_robots=args.ignore_robots)
    url = body.get(key)
    if not url:
        raise RatsinfoError(f"this body publishes no {key} list.")
    since = _since_iso(args.days, args.since)
    field = "modified_since" if args.modified else "created_since"
    return _with_filter(url, **{field: since, "omit_internal": "true"})


def cmd_papers(args) -> int:
    list_url = _list_url(args, "paper")
    terms = args.term or []

    hits: list[dict] = []
    scanned = 0
    for paper in iter_list(
        list_url, max_pages=args.max_pages, ignore_robots=args.ignore_robots
    ):
        scanned += 1
        if paper.get("deleted"):
            continue
        if not _matches(paper, terms, ("name", "reference", "paperType")):
            continue
        files = []
        main = paper.get("mainFile")
        if isinstance(main, dict) and main.get("accessUrl"):
            files.append({"role": "main", "name": main.get("name"),
                          "url": main["accessUrl"]})
        for f in (paper.get("auxiliaryFile") or [])[: args.max_files]:
            if isinstance(f, dict) and f.get("accessUrl"):
                files.append({"role": "auxiliary", "name": f.get("name"),
                              "url": f["accessUrl"]})
        hits.append(
            {
                "reference": paper.get("reference"),
                "name": paper.get("name"),
                "date": paper.get("date"),
                "paperType": paper.get("paperType"),
                "id": paper.get("id"),
                "license": paper.get("license"),
                "files": files,
            }
        )
        if len(hits) >= args.limit:
            break

    lines = []
    for hit in hits:
        lines.append(f"{hit['reference'] or '-':<20} {hit['name'] or '-'}")
        lines.append(
            f"  date {hit['date'] or '-'}   type {hit['paperType'] or '-'}"
        )
        lines.append(f"  {hit['id']}")
        for f in hit["files"]:
            lines.append(f"  {f['role']} {f['name'] or ''} {f['url']}")
    lines.append("")
    lines.append(
        f"{len(hits)} matching of {scanned} scanned. OParl has no full text"
    )
    lines.append(
        "search, so this is a client side filter over titles and reference"
    )
    lines.append(
        "numbers. A document whose subject only appears inside the PDF will"
    )
    lines.append("not be found here. Narrow with --since, widen with --max-pages.")
    emit(args, {"scanned": scanned, "matching": len(hits), "papers": hits}, lines)
    return 0


def cmd_meetings(args) -> int:
    list_url = _list_url(args, "meeting")
    hits: list[dict] = []
    for meeting in iter_list(
        list_url, max_pages=args.max_pages, ignore_robots=args.ignore_robots
    ):
        if meeting.get("deleted"):
            continue
        if not _matches(meeting, args.term or [], ("name",)):
            continue
        hits.append(
            {
                "start": meeting.get("start"),
                "name": meeting.get("name"),
                "id": meeting.get("id"),
            }
        )
        if len(hits) >= args.limit:
            break

    lines = []
    for hit in hits:
        lines.append(f"{hit['start'] or '-':<26} {hit['name'] or '-'}")
        lines.append(f"  {hit['id']}")
    lines.append("")
    lines.append(f"{len(hits)} meetings listed.")
    emit(args, {"meetings": hits}, lines)
    return 0


def cmd_track(args) -> int:
    allow_host(args.paper)
    chain = consultation_chain(
        args.paper, max_steps=args.max_steps, ignore_robots=args.ignore_robots
    )
    paper = chain["paper"]
    lines = [
        f"{paper['reference'] or '-'}  {paper['name'] or '-'}",
        f"  type {paper['paperType'] or '-'}   tabled {paper['date'] or '-'}",
        f"  status: {chain['status']}",
        "",
    ]
    for step in chain["steps"]:
        mark = "*" if step["authoritative"] else " "
        public = "" if step.get("public") is not False else "  [non public]"
        lines.append(
            f"{mark} {(step['date'] or '')[:10]:<12} "
            f"{step['organization'] or step['meeting_name'] or '-'}"
        )
        detail = []
        if step.get("role"):
            detail.append(str(step["role"]))
        if step.get("result"):
            detail.append(f"result: {step['result']}")
        if step.get("cancelled"):
            detail.append("meeting cancelled")
        if detail:
            lines.append("               " + "   ".join(detail) + public)
        elif public:
            lines.append("               " + public.strip())
    if chain["steps"]:
        lines.append("")
        lines.append("* marks the authoritative consultation, the one that decides.")
    emit(args, chain, lines)
    return 0


def cmd_watch(args) -> int:
    """Ask only for what changed since last time, and say what is new."""
    system = system_info(args.endpoint, ignore_robots=args.ignore_robots)
    body = pick_body(system, args.body, ignore_robots=args.ignore_robots)
    kind = args.kind
    url = body.get(kind)
    if not url:
        raise RatsinfoError(f"this body publishes no {kind} list.")

    state = load_state(args.endpoint, kind)
    since = state.get("last_run") or _since_iso(args.days or 30, args.since)
    url = _with_filter(url, modified_since=since, omit_internal="true")

    terms = args.term or []
    fields = ("name", "reference", "paperType") if kind == "paper" else ("name",)
    seen = set(state.get("seen", []))

    fresh, removed, items = [], [], []
    for item in iter_list(
        url, max_pages=args.max_pages, ignore_robots=args.ignore_robots
    ):
        if item.get("deleted"):
            if item.get("id") in seen:
                removed.append(item.get("id"))
            continue
        if not _matches(item, terms, fields):
            continue
        items.append(item)
        if item.get("id") not in seen:
            fresh.append(item)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    if not args.dry_run:
        save_state(
            args.endpoint,
            kind,
            {
                "last_run": now,
                "seen": sorted(
                    seen | {i.get("id") for i in items if i.get("id")}
                )[-5000:],
                "terms": terms,
            },
        )

    if args.ics:
        if kind != "meeting":
            raise RatsinfoError(
                "--ics only makes sense with --kind meeting. Council papers "
                "have no date to put in a calendar."
            )
        with open(args.ics, "w", encoding="utf-8") as handle:
            handle.write(to_ics(items))

    lines = [f"since {since[:19]}"]
    for item in fresh:
        label = item.get("reference") or (item.get("start") or "")[:16] or "-"
        lines.append(f"NEW  {label:<20} {item.get('name') or '-'}")
        lines.append(f"     {item.get('id')}")
    for gone in removed:
        lines.append(f"GONE {gone}")
    lines.append("")
    lines.append(
        f"{len(fresh)} new, {len(removed)} withdrawn, {len(items)} matching in window."
    )
    if args.ics:
        lines.append(f"calendar written to {args.ics}")
    if args.dry_run:
        lines.append("dry run, the watch state was not advanced.")
    emit(
        args,
        {
            "since": since,
            "new": fresh,
            "withdrawn": removed,
            "matching": len(items),
        },
        lines,
    )
    return 0


def cmd_people(args) -> int:
    system = system_info(args.endpoint, ignore_robots=args.ignore_robots)
    body = pick_body(system, args.body, ignore_robots=args.ignore_robots)
    url = body.get("person")
    if not url:
        raise RatsinfoError("this body publishes no person list.")

    hits = []
    for person in iter_list(
        _with_filter(url, omit_internal="true"),
        max_pages=args.max_pages,
        ignore_robots=args.ignore_robots,
    ):
        if person.get("deleted"):
            continue
        if not _matches(person, args.term or [], ("name", "familyName", "givenName")):
            continue
        memberships = []
        for raw in (person.get("membership") or [])[:20]:
            m = raw if isinstance(raw, dict) else {}
            memberships.append(
                {
                    "organization": resolve_name(
                        m.get("organization"), ignore_robots=args.ignore_robots
                    ),
                    "role": m.get("role"),
                    "votingRight": m.get("votingRight"),
                    "startDate": m.get("startDate"),
                    "endDate": m.get("endDate"),
                }
            )
        hits.append(
            {
                "name": person.get("name"),
                "id": person.get("id"),
                "status": person.get("status"),
                "memberships": memberships,
            }
        )
        if len(hits) >= args.limit:
            break

    lines = []
    for hit in hits:
        lines.append(hit["name"] or "-")
        for m in hit["memberships"]:
            span = f"{(m['startDate'] or '')[:10]} to {(m['endDate'] or '')[:10] or 'now'}"
            lines.append(
                f"  {m['organization'] or '-'}   {m['role'] or ''}   {span}"
            )
    lines.append("")
    lines.append(f"{len(hits)} people listed.")
    emit(args, {"people": hits}, lines)
    return 0


def _scan_endpoint(url: str, args) -> dict:
    """Search one municipality. Never raise: a dead endpoint is a result."""
    record = {"endpoint": url, "status": "ok", "municipality": None,
              "ags": None, "hits": [], "note": None}
    try:
        system = system_info(url, ignore_robots=args.ignore_robots)
        body = pick_body(system, 0, ignore_robots=args.ignore_robots)
        record["municipality"] = body.get("name")
        record["ags"] = body.get("ags")
        record["license"] = system.get("license")
        record["contact"] = system.get("contactEmail")
        paper_list = body.get("paper")
        if not paper_list:
            record["status"] = "keine Vorlagenliste"
            return record
        since = _since_iso(args.days, args.since)
        paper_list = _with_filter(
            paper_list, created_since=since, omit_internal="true"
        )
        for paper in iter_list(
            paper_list, max_pages=args.max_pages,
            ignore_robots=args.ignore_robots,
        ):
            if paper.get("deleted"):
                continue
            if not _matches(paper, args.term or [],
                            ("name", "reference", "paperType")):
                continue
            record["hits"].append(
                {
                    "reference": paper.get("reference"),
                    "name": paper.get("name"),
                    "date": paper.get("date"),
                    "paperType": paper.get("paperType"),
                    "id": paper.get("id"),
                    "underDirectionOf": [
                        resolve_name(o, ignore_robots=args.ignore_robots)
                        for o in (paper.get("underDirectionOf") or [])[:2]
                    ],
                    "files": len(paper.get("auxiliaryFile") or [])
                    + (1 if paper.get("mainFile") else 0),
                }
            )
            if len(record["hits"]) >= args.per_municipality:
                break
    except RatsinfoError as exc:
        first = str(exc).splitlines()[0]
        record["status"] = "nicht erreichbar"
        record["note"] = first[:160]
    return record


def cmd_scan(args) -> int:
    """Search many municipalities at once and write a market report.

    This is the question a business actually has: not what one town decided,
    but where, across a whole region, something is moving that concerns me.
    """
    if args.endpoints:
        with open(args.endpoints, encoding="utf-8") as handle:
            urls = [ln.strip() for ln in handle if ln.strip()
                    and not ln.startswith("#")]
    else:
        entries = load_registry(refresh=args.refresh)
        urls = []
        seen_hosts = set()
        for entry in entries:
            url = str(entry.get("url") or "")
            if not url.startswith("http"):
                continue
            host = _host(url)
            if host in seen_hosts:  # the registry is full of duplicates
                continue
            seen_hosts.add(host)
            if args.region and args.region.lower() not in str(
                entry.get("title", "")
            ).lower():
                continue
            urls.append(url)
    urls = urls[: args.max_endpoints]
    for url in urls:
        allow_host(url)

    records = []
    for i, url in enumerate(urls, start=1):
        if not args.json:
            print(f"[{i}/{len(urls)}] {_host(url)}", file=sys.stderr)
        records.append(_scan_endpoint(url, args))

    reachable = [r for r in records if r["status"] == "ok"]
    with_hits = [r for r in reachable if r["hits"]]
    total = sum(len(r["hits"]) for r in reachable)

    summary = {
        "queried": len(records),
        "reachable": len(reachable),
        "with_hits": len(with_hits),
        "hits": total,
        "terms": args.term or [],
        "since": _since_iso(args.days, args.since),
    }

    if args.pdf:
        _scan_pdf(args, summary, records, with_hits)

    lines = [
        f"{len(records)} Kommunen abgefragt, {len(reachable)} erreichbar, "
        f"{len(with_hits)} mit Treffern, {total} Vorlagen insgesamt.",
        "",
    ]
    for record in with_hits:
        lines.append(f"{record['municipality'] or _host(record['endpoint'])}"
                     + (f"  (AGS {record['ags']})" if record.get("ags") else ""))
        for hit in record["hits"]:
            lines.append(
                f"  {(hit['date'] or '')[:10]:<12}{hit['reference'] or '-':<14}"
                f"{hit['name'] or '-'}"
            )
    unreachable = [r for r in records if r["status"] != "ok"]
    if unreachable:
        lines.append("")
        lines.append(f"{len(unreachable)} Endpunkte nicht auswertbar:")
        for record in unreachable[:10]:
            lines.append(f"  {_host(record['endpoint'])}  {record['note'] or record['status']}")
    if args.pdf:
        lines.append("")
        lines.append(f"Bericht: {args.pdf}")
    emit(args, {"summary": summary, "records": records}, lines)
    return 0


def _scan_pdf(args, summary, records, with_hits) -> None:
    import pdfreport

    report = pdfreport.Report(logo=args.logo)
    terms = " und ".join(args.term or []) or "alle Vorlagen"
    report.header(
        args.org,
        "Marktbericht kommunale Vorhaben",
        f"Suchbegriffe: {terms}. Zeitraum ab "
        f"{(summary['since'] or '')[:10] or 'unbegrenzt'}.",
    )
    report.status(
        f"{summary['hits']} Vorlagen in {summary['with_hits']} von "
        f"{summary['reachable']} erreichbaren Kommunen"
    )
    report.field("Abgefragt", f"{summary['queried']} Endpunkte")
    report.field("Erreichbar", f"{summary['reachable']} Endpunkte")
    report.field("Datenquelle", "OParl-Schnittstellen der Kommunen")

    for record in with_hits:
        title = record["municipality"] or _host(record["endpoint"])
        if record.get("ags"):
            title += f"   AGS {record['ags']}"
        report.section(title)
        for hit in record["hits"]:
            detail = []
            if hit.get("paperType"):
                detail.append(str(hit["paperType"]))
            responsible = [d for d in hit.get("underDirectionOf") or [] if d]
            if responsible:
                detail.append("Federfuehrung: " + ", ".join(responsible))
            if hit.get("files"):
                detail.append(f"{hit['files']} Dokumente")
            report.step(
                (hit.get("date") or "")[:10],
                f"{hit['reference'] or ''} {hit['name'] or '-'}".strip(),
                "  \u00b7  ".join(detail),
            )
            report.link("Quelle", "Vorlage im Ratsinformationssystem",
                        hit["id"] or "")

    unreachable = [r for r in records if r["status"] != "ok"]
    if unreachable:
        report.section("Nicht auswertbare Endpunkte")
        report.note(
            "Diese Kommunen stehen im oeffentlichen Verzeichnis, liefern aber "
            "keine auswertbaren Daten. Das ist eine Aussage ueber die "
            "Schnittstelle, nicht ueber die Bautaetigkeit dort."
        )
        for record in unreachable[:25]:
            report.link(_host(record["endpoint"]),
                        record["note"] or record["status"],
                        record["endpoint"])

    report.section("Was in diesen Daten steht und was nicht")
    report.note(
        "Aus der OParl-Schnittstelle stammen: Titel, Aktenzeichen, Art der "
        "Vorlage, Datum, federfuehrende Stelle, Beratungsverlauf, Ergebnis "
        "und die Links auf die Originaldokumente."
    )
    report.note(
        "NICHT enthalten sind Bausumme, Leistungsphase und Haushaltsstelle. "
        "Diese Angaben stehen, wenn ueberhaupt, nur im Text der Vorlage und "
        "werden hier bewusst nicht geschaetzt."
    )
    report.note(
        "Ebenfalls nicht enthalten sind persoenliche Kontaktdaten von "
        "Mandatstraegern. Die Schnittstelle fuehrt sie, sie sind aber zum "
        "Zweck der Buergerkommunikation veroeffentlicht. Der richtige Weg "
        "ist die Funktionsadresse der federfuehrenden Stelle."
    )

    when = datetime.now(timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M")
    report.save(
        args.pdf,
        footer=(
            f"Erstellt am {when} aus den OParl-Schnittstellen der genannten "
            "Kommunen.\n"
            "Amtliche Dokumente sind nach Paragraph 5 UrhG gemeinfrei, "
            "Anlagen koennen fremde Rechte tragen.\n"
            "Erzeugt mit ratsinfo-de, einem quelloffenen Werkzeug."
        ),
    )


def cmd_report(args) -> int:
    """Produce a PDF dossier of one paper's route through the committees.

    This is the artefact people actually keep: something you can put in a
    project file, mail to a client or hand to a committee. The PDF writer is
    part of this skill and needs nothing installed.
    """
    import pdfreport

    allow_host(args.paper)
    chain = consultation_chain(
        args.paper, max_steps=args.max_steps, ignore_robots=args.ignore_robots
    )
    paper = chain["paper"]

    decided = next(
        (s for s in reversed(chain["steps"])
         if s.get("authoritative") and s.get("result")),
        None,
    )
    last = chain["steps"][-1] if chain["steps"] else None
    if decided:
        status_de = (
            f"Entschieden am {(decided['date'] or '')[:10]}: {decided['result']}"
        )
    elif last and last.get("result"):
        status_de = (
            f"Letztes Ergebnis am {(last['date'] or '')[:10]}: {last['result']}"
        )
    elif last:
        status_de = f"Seit {(last['date'] or '')[:10]} in Beratung"
    else:
        status_de = "Keine Beratung verzeichnet"

    report = pdfreport.Report(logo=args.logo)
    report.header(
        args.org,
        paper["name"] or "Ratsvorlage",
        f"Beratungsverlauf zur Vorlage {paper['reference'] or ''}".strip(),
    )
    report.status(status_de)

    report.field("Aktenzeichen", paper["reference"] or "-")
    report.field("Art der Vorlage", paper["paperType"] or "-")
    report.field("Eingebracht am", (paper["date"] or "-")[:10])
    if paper.get("underDirectionOf"):
        report.field("Federfuehrung", ", ".join(paper["underDirectionOf"]))
    if paper.get("originator"):
        report.field("Eingebracht von", ", ".join(paper["originator"]))
    if paper.get("location"):
        report.field("Ortsbezug", paper["location"])
    if paper.get("keywords"):
        report.field("Schlagworte", ", ".join(paper["keywords"]))
    report.field("Quelle", paper["id"] or args.paper)

    report.section("Weg durch die Gremien")
    if not chain["steps"]:
        report.note(
            "Zu dieser Vorlage ist keine Beratung verzeichnet. Sie wurde "
            "eingebracht, aber nach Aktenlage nie auf eine Tagesordnung "
            "gesetzt."
        )
    for step in chain["steps"]:
        detail = []
        if step.get("number"):
            detail.append(f"TOP {step['number']}")
        if step.get("role"):
            detail.append(str(step["role"]))
        if step.get("public") is False:
            detail.append("nichtoeffentlich")
        if step.get("cancelled"):
            detail.append("Sitzung abgesagt")
        if step.get("authoritative"):
            detail.append("massgebliche Beratung")
        if step.get("location"):
            detail.append(str(step["location"]))
        if step.get("participants"):
            detail.append(f"{step['participants']} Teilnehmende")
        report.step(
            (step.get("date") or "")[:10],
            step.get("organization") or step.get("meeting_name") or "-",
            "  \u00b7  ".join(detail),
            marked=bool(step.get("authoritative")),
        )
        if step.get("result"):
            report.result(f"Ergebnis: {step['result']}")
        if step.get("resolutionText"):
            report.quote(step["resolutionText"])
        protocols = [
            ("Einladung", step.get("invitation")),
            ("Ergebnisprotokoll", step.get("resultsProtocol")),
            ("Wortprotokoll", step.get("verbatimProtocol")),
            ("Beschlussausfertigung", step.get("resolutionFile")),
        ]
        for label, info in protocols:
            if info:
                report.link(label, info.get("name") or label, info["url"])

    if paper.get("files"):
        report.section("Dokumente zur Vorlage")
        for info in paper["files"][:12]:
            size = ""
            if info.get("size"):
                size = f"  ({int(info['size']) // 1024} KB)"
            report.link(
                info.get("role") or "Datei",
                (info.get("name") or "ohne Titel") + size,
                info["url"],
            )

    if paper.get("relatedPaper"):
        report.section("Verwandte Vorlagen")
        for related in paper["relatedPaper"][:10]:
            title = resolve_name(related, ignore_robots=args.ignore_robots)
            reference = None
            if isinstance(related, str):
                obj = _deref(related, ignore_robots=args.ignore_robots)
                reference = obj.get("reference")
                title = obj.get("name") or title
            label = f"Vorlage {reference}" if reference else "Vorlage"
            report.link(label, title or "ohne Titel", str(related))

    when = datetime.now(timezone.utc).astimezone().strftime("%d.%m.%Y %H:%M")
    footer = (
        f"Erstellt am {when} aus dem Ratsinformationssystem der Kommune, "
        f"ueber die OParl-Schnittstelle.\n"
        "Amtliche Dokumente sind nach Paragraph 5 UrhG gemeinfrei, Anlagen "
        "koennen fremde Rechte tragen.\n"
        "Erzeugt mit ratsinfo-de, einem quelloffenen Werkzeug."
    )
    report.save(args.pdf, footer=footer)

    size = os.path.getsize(args.pdf)
    lines = [
        f"{args.pdf}  {size} bytes  {len(chain['steps'])} Beratungen",
        chain["status"],
    ]
    emit(args, {"pdf": args.pdf, "bytes": size, **chain}, lines)
    return 0


def cmd_get(args) -> int:
    allow_host(args.url)
    doc = fetch_json(args.url, ignore_robots=args.ignore_robots)
    json.dump(doc, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ratsinfo",
        description="Polite OParl client for German council information systems.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--ignore-robots",
        action="store_true",
        help="only after the operator has allowed you in writing",
    )
    common.add_argument(
        "--json", action="store_true", help="machine readable output"
    )
    common.add_argument(
        "--allow-cross-host",
        action="store_true",
        help="follow links that point at a different host than the endpoint",
    )

    listing = argparse.ArgumentParser(add_help=False)
    listing.add_argument("--term", action="append", help="filter word, repeatable")
    listing.add_argument("--since", help="ISO date, e.g. 2026-01-01")
    listing.add_argument("--days", type=int, help="last N days instead of --since")
    listing.add_argument(
        "--modified",
        action="store_true",
        help="filter on modified_since instead of created_since",
    )
    listing.add_argument(
        "--body", type=int, default=0, help="which body, see the bodies command"
    )
    listing.add_argument("--limit", type=int, default=25)
    listing.add_argument("--max-pages", type=int, default=20)

    p = sub.add_parser("find", parents=[common],
                       help="look up a town in the OParl registry")
    p.add_argument("name")
    p.add_argument("--refresh", action="store_true", help="re-download the registry")
    p.set_defaults(func=cmd_find)

    p = sub.add_parser("check", parents=[common], help="health check one endpoint")
    p.add_argument("endpoint")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("bodies", parents=[common],
                       help="list the bodies this endpoint serves")
    p.add_argument("endpoint")
    p.set_defaults(func=cmd_bodies)

    p = sub.add_parser("papers", parents=[common, listing],
                       help="list council papers")
    p.add_argument("endpoint")
    p.add_argument("--max-files", type=int, default=3)
    p.set_defaults(func=cmd_papers)

    p = sub.add_parser("meetings", parents=[common, listing], help="list meetings")
    p.add_argument("endpoint")
    p.set_defaults(func=cmd_meetings)

    p = sub.add_parser("track", parents=[common],
                       help="what became of one council paper")
    p.add_argument("paper", help="the OParl Paper URL")
    p.add_argument("--max-steps", type=int, default=50,
                   help="how many consultations to resolve at most")
    p.set_defaults(func=cmd_track)

    p = sub.add_parser("watch", parents=[common, listing],
                       help="report only what changed since the last run")
    p.add_argument("endpoint")
    p.add_argument("--kind", choices=["paper", "meeting"], default="paper")
    p.add_argument("--ics", help="also write an iCalendar file to this path")
    p.add_argument("--dry-run", action="store_true",
                   help="do not advance the stored watch state")
    p.set_defaults(func=cmd_watch)

    p = sub.add_parser("people", parents=[common, listing],
                       help="list people and their committee memberships")
    p.add_argument("endpoint")
    p.set_defaults(func=cmd_people)

    p = sub.add_parser("scan", parents=[common, listing],
                       help="search many municipalities and write a market report")
    p.add_argument("--max-endpoints", type=int, default=20,
                   help="how many municipalities to query at most")
    p.add_argument("--per-municipality", type=int, default=10)
    p.add_argument("--endpoints", help="file with one endpoint URL per line")
    p.add_argument("--region", help="only registry entries whose title matches")
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--pdf", help="write a market report to this path")
    p.add_argument("--logo", help="PNG logo for the header")
    p.add_argument("--org", default="Marktbeobachtung")
    p.set_defaults(func=cmd_scan)

    p = sub.add_parser("report", parents=[common],
                       help="write a PDF dossier of one paper's route")
    p.add_argument("paper", help="the OParl Paper URL")
    p.add_argument("--pdf", default="ratsvorlage.pdf", help="output path")
    p.add_argument("--logo", help="PNG logo for the header, optional")
    p.add_argument("--org", default="Ratsinformation",
                   help="the name in the header")
    p.add_argument("--max-steps", type=int, default=50)
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("get", parents=[common],
                       help="fetch one OParl object as JSON")
    p.add_argument("url")
    p.set_defaults(func=cmd_get)

    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    set_cross_host(getattr(args, "allow_cross_host", False))
    try:
        return args.func(args)
    except RatsinfoError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
