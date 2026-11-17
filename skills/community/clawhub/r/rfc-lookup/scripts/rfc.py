#!/usr/bin/env python3
"""Look up IETF RFCs from the command line.

Standard library only, deliberately: this file is vendored verbatim into a
ClawHub skill and into a PyPI package, and both need to run wherever there is a
Python interpreter and nothing else.

Two runtime modes, decided by one predicate — whether a local mirror is
populated. Online mode fetches documents on demand over HTTPS; offline mode
reads them from disk and can search their full text. There is no build-time
flavour and no separate "offline edition"; `rfc sync` moves you from one mode to
the other and everything else behaves the same.

The index-parsing approach here — match entries by a leading RFC number, treat
"Not Issued" as a placeholder — follows mcp-server-ietf (MIT, Copyright (c) 2025
Jeff Chiang), https://github.com/tizee/mcp-server-ietf. See NOTICE. The parser
itself is a rewrite; the original's regexes are documented as counter-examples
in parse_index() below.
"""

from __future__ import annotations

import argparse
import contextlib
import gzip
import hashlib
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import zlib
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from email.utils import formatdate
from pathlib import Path

__version__ = "0.6.1"

INDEX_URL = "https://www.rfc-editor.org/rfc-index.txt"
RFC_URL = "https://www.rfc-editor.org/rfc/rfc{number}.txt"
RSYNC_MODULE = "rsync.rfc-editor.org::rfcs-text-only/"

# How long the index is served without asking the RFC Editor whether it moved.
# Revalidation is a conditional GET the CDN answers 304 to, so a refresh past
# this costs a round trip rather than 2 MB, and a day is as fine-grained as the
# corpus gets: RFCs publish in weekday batches at roughly one a day.
INDEX_TTL_SECONDS = 24 * 60 * 60

# When `status` calls the index stale, which is a different question from when
# to refresh it. Refreshing is cheap and happens on a timer the user never sees;
# this is the age at which an index has plausibly missed something they would
# care about, and reaching it means a week with no working refresh at all.
INDEX_STALE_SECONDS = 7 * 24 * 60 * 60
# Where "just read the whole thing" stops being reasonable. Short RFCs are
# cheap and refusing them would be pedantry; past roughly 20k tokens an
# unscoped read stops being a document and becomes a context window. Both
# surfaces advise reading one section, and advice is the weaker half of a
# guardrail — this is the half that holds when the advice is skipped.
WHOLE_DOCUMENT_LINE_LIMIT = 1500
# Enough documents that full-text search is worth offering. A handful of
# on-demand fetches accumulating in the mirror should not look like a sync.
POPULATED_THRESHOLD = 1000
SYNC_STAMP = ".rfc-sync"
# The largest page a search returns. A page is something a reader reads, and
# every payload carries `total`, so a cap costs nothing but rows nobody would
# have read. It also bounds the work: a full-text page spawns one backend
# process per result to quote its lines, which at a corpus-sized page is
# minutes inside one tool call.
MAX_SEARCH_LIMIT = 200
# How long one backend process may run. The count pass reads the whole mirror,
# so this is generous for a local disk and exists for the slow cases — a
# network filesystem, a pathological --regex pattern — that would otherwise
# hold the caller with nothing to cancel it.
SEARCH_TIMEOUT_SECONDS = 60

USER_AGENT = f"rfc-ai-tooling/{__version__} (+https://github.com/shbernal/rfc-ai-tooling)"


class RFCError(Exception):
    """Anything the user should see as a clean error rather than a traceback."""


# A host that ships its own entry point for this CLI sets this to the command
# that reaches it. Nothing observable from inside the process distinguishes an
# ephemeral environment from an installed one — `uvx` leaves the package
# importable and its bin directory on PATH — so the spelling has to come from
# the surface that knows how it is distributed, not from a guess made here.
CLI_NAME: str | None = None


def invocation() -> str:
    """How to re-run this program, spelled the way the caller actually reached it.

    Error messages here tell the reader to run another command, and the two
    surfaces disagree about what that command is. The PyPI package installs no
    `rfc` console script and the skill ships this file with nothing on PATH, so
    a hardcoded "run `rfc sync`" is advice that fails as typed in the place it
    fires most often — the --fulltext refusal, which is the first wall an agent
    hits on an unsynced machine.

    A host that set CLI_NAME has already answered the question and is believed.
    Otherwise: vendored into a package, this file is reachable as a module
    whether it was run with -m or imported by the MCP server, and the module
    path is right in both cases. Standalone, argv[0] is trusted only when it
    points at this very file; anything else is some other program's entry point.
    """
    if CLI_NAME:
        return CLI_NAME
    if __package__:
        return f"python3 -m {__package__}.{Path(__file__).stem}"
    argv0 = sys.argv[0] if sys.argv else ""
    if not argv0:
        return "rfc"
    if Path(argv0).name in {"rfc", "rfc.exe"}:
        return "rfc"
    try:
        if Path(argv0).resolve() == Path(__file__).resolve():
            return f"python3 {argv0}"
    except OSError:
        pass
    return "rfc"


# --------------------------------------------------------------------------
# Index records
# --------------------------------------------------------------------------


@dataclass
class Record:
    number: int
    title: str = ""
    authors: str = ""
    date: str = ""
    status: str = ""
    doi: str = ""
    obsoletes: list[int] = field(default_factory=list)
    obsoleted_by: list[int] = field(default_factory=list)
    updates: list[int] = field(default_factory=list)
    updated_by: list[int] = field(default_factory=list)
    also: list[str] = field(default_factory=list)
    not_issued: bool = False

    def to_dict(self) -> dict:
        """Every field, plus the two the caller would otherwise derive.

        Built from the dataclass rather than restated field by field: a list
        written out by hand is one a new field is quietly missing from, and it
        would go missing from every JSON caller at once.
        """
        return {
            **asdict(self),
            "obsolete": bool(self.obsoleted_by),
            "header": self.header(),
        }

    def header(self) -> str:
        """The banner shown above every result.

        Obsolescence is the highest-value field in the index and the easiest for
        a model to skip, so it goes on its own line with a marker, never folded
        into a list of attributes.
        """
        if self.not_issued:
            return f"RFC {self.number} — Not Issued"
        status = f"  [{self.status}]" if self.status else ""
        lines = [f"RFC {self.number} — {self.title}{status}"]
        if self.obsoleted_by:
            refs = ", ".join(str(n) for n in self.obsoleted_by)
            lines.append(f"!! OBSOLETED BY: RFC {refs}")
        if self.updated_by:
            refs = ", ".join(str(n) for n in self.updated_by)
            lines.append(f"!! UPDATED BY: RFC {refs}")
        return "\n".join(lines)


# The metadata block that closes every entry. Format/Status/DOI must be followed
# by a colon: RFC 4304's *title* contains a bare "(DOI)" and matching that as
# metadata truncates the title and loses the date.
_META_START = re.compile(
    r"\s*\((?:Format:|Status:|DOI:|Obsoletes\s|Obsoleted by\s|Updates\s|Updated by\s|Also\s)"
)
_MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
_DATE_TAIL = re.compile(rf"\s*(?:(?:{_MONTHS})\s+)?\d{{4}}\.?\s*$")
# Where the author list starts: one to four initials followed by a surname.
# Initials may be hyphenated ("M-K.", "Y.-K.") and surnames may begin lowercase
# ("N. ten Oever"), both of which occur in the real index.
_AUTHOR_ONSET = re.compile(r"^(?:[A-Z](?:[.\-]{1,2}[A-Z])*\.\s*){1,4}[A-Za-z]")
_SENTENCE_BREAK = re.compile(r"\.\s+")
_REFS = re.compile(r"\((Obsoletes|Obsoleted by|Updates|Updated by)\s+([^)]*)\)")
_ALSO = re.compile(r"\(Also\s+([^)]*)\)")
_STATUS = re.compile(r"\(Status:\s*([^)]*)\)")
_DOI = re.compile(r"\(DOI:\s*([^)]*)\)")
_RFC_REF = re.compile(r"RFC0*(\d+)")


def parse_index(text: str) -> dict[int, Record]:
    """Parse rfc-index.txt into records keyed by RFC number.

    The file's shape, which the three rules below all depend on:

        2616 Hypertext Transfer Protocol -- HTTP/1.1. R. Fielding, J. Gettys, J.
             Mogul, H. Frystyk, L. Masinter, P. Leach, T. Berners-Lee. June 1999.
             (Format: TXT, PS, PDF, HTML) (Obsoletes RFC2068) (Obsoleted by
             RFC7230, RFC7231, RFC7232, RFC7233, RFC7234, RFC7235) (Updated by
             RFC2817, RFC5785, RFC6266, RFC6585) (Status: DRAFT STANDARD) (DOI:
             10.17487/RFC2616)

    Three traps, each of which has bitten a previous implementation:

    1. Entries begin at column 0; continuation lines are indented and entries are
       separated by blank lines. Reading line by line therefore sees only the
       first physical line of an entry and loses most of the metadata. Join the
       record before parsing anything.

    2. RFC numbers are *not* zero-padded. A regex expecting four or five digits
       silently drops all 999 RFCs below 1000 — including 768, 791, 793 and 959.

    3. The title cannot be taken as everything before the first period. That
       yields "Hypertext Transfer Protocol -- HTTP/1" above, and corrupts every
       title containing a version number, an abbreviation or a hostname. The
       title ends where the author list begins; find that boundary explicitly.
    """
    records: dict[int, Record] = {}
    for block in re.split(r"\n\s*\n", text):
        lines = block.split("\n")
        if not lines or not re.match(r"^\d+\s", lines[0]):
            continue
        joined = " ".join(line.strip() for line in lines if line.strip())
        record = _parse_record(joined)
        if record is not None:
            records[record.number] = record
    return records


def _parse_record(joined: str) -> Record | None:
    num_text, _, rest = joined.partition(" ")
    try:
        number = int(num_text)
    except ValueError:
        return None

    meta_match = _META_START.search(rest)
    prose = (rest[: meta_match.start()] if meta_match else rest).strip()
    metadata = rest[meta_match.start() :] if meta_match else ""

    if prose.rstrip(".").strip() == "Not Issued":
        return Record(number=number, title="Not Issued", not_issued=True)

    record = Record(number=number)

    date_match = _DATE_TAIL.search(prose)
    if date_match:
        record.date = prose[date_match.start() :].strip().rstrip(".")
        body = prose[: date_match.start()]
    else:
        body = prose
    body = body.strip()

    split_at = None
    for match in _SENTENCE_BREAK.finditer(body):
        if _AUTHOR_ONSET.match(body[match.end() :]):
            split_at = match
            break
    if split_at is None:
        # Corporate authorship ("Sun Microsystems", "International Organization
        # for Standardization") has no initials to key on; the first sentence
        # break is the best available boundary.
        split_at = _SENTENCE_BREAK.search(body)

    if split_at is None:
        record.title = body.rstrip(".")
    else:
        record.title = body[: split_at.start()].strip()
        # The author list keeps its terminating period, so that a trailing
        # "Ed." stays "Ed." rather than becoming "Ed" — at the cost of a doubled
        # period where the last author is already an abbreviation, which the
        # index itself prints as "J. Reschke, Ed..".
        authors = body[split_at.end() :].strip()
        record.authors = authors[:-1] if authors.endswith("..") else authors

    for match in _REFS.finditer(metadata):
        refs = [int(n) for n in _RFC_REF.findall(match.group(2))]
        key = match.group(1).lower().replace(" ", "_")
        getattr(record, key).extend(refs)
    for match in _ALSO.finditer(metadata):
        record.also.append(match.group(1).strip())
    status_match = _STATUS.search(metadata)
    if status_match:
        record.status = status_match.group(1).strip()
    doi_match = _DOI.search(metadata)
    if doi_match:
        record.doi = doi_match.group(1).strip()
    return record


# --------------------------------------------------------------------------
# Mirror and mode
# --------------------------------------------------------------------------


# 512 MB of RFC text is data the user asked for, not a cache a cleaner should be
# free to reclaim, so the corpus belongs in the platform's data directory rather
# than its cache directory. Which directory that *is* is the environment's
# answer to give, not ours: ~/.local/share is the fallback the XDG spec names
# for when $XDG_DATA_HOME is unset, and hardcoding it overrides every user who
# has already said where their data goes — a sandbox, a systemd unit, a home
# directory on a small partition. Windows has no such path at all; there the
# answer is %LOCALAPPDATA%, and specifically the local profile, because half a
# gigabyte in the roaming one syncs to a domain controller at every logon.
#
# Computed on call rather than at import: Path.home() raises when there is no
# passwd entry and no $HOME, which is the normal state of a container running
# under an arbitrary UID. As a module constant it took the import down with it,
# and took --mirror and $RFC_MIRROR with that, though either one would have
# meant this function was never needed.
# mcp/smoke.py restates this rule; it is piped into a bare container and cannot
# import this file. A test in mcp/tests asserts the two still agree.
def default_mirror() -> Path:
    base = os.environ.get("LOCALAPPDATA" if os.name == "nt" else "XDG_DATA_HOME")
    # The spec says to ignore a relative value rather than resolve it.
    if base and os.path.isabs(base):
        return Path(base) / "rfc-ai-tooling"
    return Path.home() / ".local" / "share" / "rfc-ai-tooling"


def resolve_mirror(override: str | None = None) -> Path:
    if override:
        return Path(override).expanduser()
    env = os.environ.get("RFC_MIRROR")
    if env:
        return Path(env).expanduser()
    return default_mirror()


def index_path(mirror: Path) -> Path:
    return mirror / "rfc-index.txt"


def document_path(mirror: Path, number: int) -> Path:
    return mirror / f"rfc{number}.txt"


def count_documents(mirror: Path) -> int:
    if not mirror.is_dir():
        return 0
    return sum(1 for _ in mirror.glob("rfc[0-9]*.txt"))


def is_populated(mirror: Path) -> bool:
    """True when the mirror holds enough of the corpus to search its full text."""
    if not index_path(mirror).exists():
        return False
    if (mirror / SYNC_STAMP).exists():
        return True
    return count_documents(mirror) > POPULATED_THRESHOLD


# --------------------------------------------------------------------------
# Network
# --------------------------------------------------------------------------


def _fetch(
    url: str,
    if_modified_since: float | None = None,
    etag: str | None = None,
) -> tuple[bytes | None, str | None]:
    """GET a URL, returning the body and the response's ETag.

    The body is None when the server answers 304, which only a conditional
    request can draw. One return shape for every caller: this is the seam the
    tests replace to stand in for the network, and a shape that depended on an
    argument made each caller assert by hand which one it had been given.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    if if_modified_since is not None:
        request.add_header("If-Modified-Since", formatdate(if_modified_since, usegmt=True))
    if etag:
        request.add_header("If-None-Match", etag)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read(), response.headers.get("ETag")
    except urllib.error.HTTPError as exc:
        if exc.code == 304:
            return None, etag
        if exc.code == 404:
            raise RFCError(f"not found: {url}") from exc
        raise RFCError(f"HTTP {exc.code} fetching {url}") from exc
    except urllib.error.URLError as exc:
        raise RFCError(f"network error fetching {url}: {exc.reason}") from exc


def _replace(src: Path, dst: Path) -> None:
    """os.replace, retried briefly on Windows.

    Windows will not replace a file while another handle has it open, and that
    includes a second writer's rename landing on the same path. Two worker
    threads refreshing the index at once, which POSIX settles silently, fail
    there with PermissionError. Both handles are short-lived, so waiting a few
    milliseconds and trying again is enough.
    """
    for delay in (0.01, 0.02, 0.05, 0.1, 0.2, 0.5):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            if os.name != "nt":
                raise
            time.sleep(delay)
    os.replace(src, dst)


def _write_atomically(path: Path, data: bytes) -> None:
    """Write through a sibling temporary file and rename it into place.

    A half-written file here is worse than no file at all, and it fails
    silently in both directions: a truncated index carries a fresh mtime, so it
    is served as current for a day and reports real RFCs as missing, while a
    truncated document is only ever checked for existence, so nothing repairs
    it. The temporary file is a sibling because os.replace is atomic within a
    filesystem and not across one.

    The name is unique per thread, not only per process: the MCP server runs
    tool calls on worker threads, and two of them fetching the same RFC under
    one PID would truncate and rename each other's temporary file. Not
    mkstemp, which creates the file 0600 where every other file in the mirror
    follows the umask.
    """
    tmp = path.with_name(f"{path.name}.{os.getpid()}.{threading.get_ident()}.part")
    try:
        tmp.write_bytes(data)
        _replace(tmp, path)
    except BaseException:
        with contextlib.suppress(OSError):
            tmp.unlink()
        raise


def ensure_index(
    mirror: Path, ttl: int = INDEX_TTL_SECONDS, force: bool = False
) -> tuple[Path, bool]:
    """Return the local index and whether this call rewrote it.

    The index is refreshed if it is missing or older than the TTL. The second
    half of the return is for load_index: a revalidation the CDN answers 304 to
    still moves the mtime, and re-parsing 2 MB of text that did not change is
    pure work — every day, for a server that stays up.

    The index must not be a write-once cache. An index fetched in January will
    report an RFC published in March as nonexistent, even though its URL fetches
    perfectly well, and there is no way for the user to tell why.

    Revalidation sends both If-None-Match and If-Modified-Since. Since
    2026-08-03 the RFC Editor's CDN honours the first: handed back its own ETag
    it answers 304, so refreshing an index that has not changed costs a header
    exchange rather than 2 MB. It still sends no Last-Modified, and
    ietf-tools/red#475 was closed on 2026-08-03 with that half explicitly
    skipped, so do not expect If-Modified-Since to produce a 304 on its own. It
    is sent anyway because RFC 9110 gives If-None-Match precedence wherever both
    are present, which makes it free, and it would cover an index whose stored
    ETag was lost if the CDN ever starts emitting one.

    A refresh that cannot reach the network is not a failure when an index is
    already on disk. A day-old copy answers nearly every question a current one
    does, and refusing to search because a revalidation timed out is far worse
    than answering from it. The mtime is deliberately left alone in that case,
    so `status` reports the real age and the next call tries again rather than
    treating the failure as a successful refresh.
    """
    path = index_path(mirror)
    etag_path = mirror / ".rfc-index.etag"
    fresh_enough = False
    if path.exists() and not force:
        age = time.time() - path.stat().st_mtime
        fresh_enough = age < ttl
    if fresh_enough:
        return path, False

    known_etag = None
    if path.exists() and etag_path.exists():
        known_etag = etag_path.read_text(encoding="utf-8").strip() or None

    try:
        data, etag = _fetch(
            INDEX_URL,
            if_modified_since=path.stat().st_mtime if path.exists() else None,
            etag=known_etag,
        )
    except RFCError:
        if not path.exists():
            raise  # Nothing to fall back to; the caller has to hear about it.
        return path, False

    if data is None:
        path.touch()
        return path, False

    mirror.mkdir(parents=True, exist_ok=True)
    _write_atomically(path, data)
    if etag:
        # Losing the ETag only costs a revalidation next time.
        with contextlib.suppress(OSError):
            etag_path.write_text(etag, encoding="utf-8")
    return path, True


# The last parse, kept against the identity of the file it came from. Callers
# never mutate what parse_index returns — every write to a Record happens while
# parse_index is still building it — so one dict can be shared.
#
# Threads race on this without a lock, and that was considered: two of them
# missing at once each parse and the later assignment wins, but both entries
# are correct for their key. The cost is a duplicated parse, not a wrong answer.
_index_cache: tuple[tuple[str, int, int], dict[int, Record]] | None = None


def load_index(mirror: Path, offline_only: bool = False) -> dict[int, Record]:
    """Parse the index, reusing the previous parse while the file on disk is unchanged.

    The key is the file's identity, not the fact that a parse has happened. A
    caller that memoized the records themselves would pin its whole process to
    whatever the first call loaded — it would never see a refresh past the TTL,
    and a first call made during an outage would serve the fallback copy for as
    long as it ran. ensure_index leaves the mtime alone precisely so the next
    call retries; caching the records is what turns "the next call" into never.

    Size is in the key alongside mtime because a filesystem with coarse
    timestamps could otherwise miss a rewrite that lands in the same tick as
    the parse before it. The index only grows, so the pair separates them.
    """
    global _index_cache
    path = index_path(mirror)
    # Nothing has been written on this call unless ensure_index says otherwise.
    rewritten = True
    if not offline_only:
        path, rewritten = ensure_index(mirror)
    if not path.exists():
        raise RFCError(
            f"no RFC index at {path}. Run `{invocation()} status` while online to "
            f"fetch it, or `{invocation()} sync` for the full corpus."
        )
    stat = path.stat()
    key = (str(path), stat.st_mtime_ns, stat.st_size)
    if _index_cache is not None:
        cached_key, cached = _index_cache
        if cached_key == key:
            return cached
        # A revalidation answered 304 leaves the bytes alone and moves the
        # mtime anyway, which is the one case where a changed key means
        # nothing. Adopt the new key rather than re-reading what we have.
        if not rewritten and (cached_key[0], cached_key[2]) == (key[0], key[2]):
            _index_cache = (key, cached)
            return cached
    records = parse_index(path.read_text(encoding="utf-8", errors="replace"))
    _index_cache = (key, records)
    return records


def read_document(mirror: Path, number: int) -> str:
    """Read an RFC from the section index or the mirror, fetching and caching
    it if neither has it.

    The index comes first because it is what a machine without the mirror
    holds, and an RFC's text never changes once published, so the two cannot
    disagree. An index that cannot be opened is skipped here, not reported:
    a read has other places to go, and search is where the problem is named.

    Note that this does not consult the index first. An RFC published since the
    last index refresh still fetches perfectly well, and gating retrieval on a
    cached index is how a stale index turns into "no such RFC".
    """
    with contextlib.suppress(RFCError, sqlite3.Error):
        conn = open_section_index(section_index_path(mirror))
        if conn is not None:
            try:
                text = index_document(conn, number)
            finally:
                conn.close()
            if text is not None:
                return text
    path = document_path(mirror, number)
    if path.exists():
        return path.read_text(encoding="utf-8", errors="replace")
    data, _ = _fetch(RFC_URL.format(number=number))
    if data is None:
        raise RFCError(f"RFC {number} could not be retrieved")
    text = data.decode("utf-8", errors="replace")
    try:
        mirror.mkdir(parents=True, exist_ok=True)
        _write_atomically(path, data)
    except OSError:
        pass  # A read-only mirror is fine; we just do not get to cache.
    return text


# --------------------------------------------------------------------------
# Document structure
# --------------------------------------------------------------------------


def split_lines(text: str) -> list[str]:
    """Split on newlines only.

    Not str.splitlines(): it also breaks on form feeds, which paginated RFCs use
    by the hundred. Line numbers computed that way disagree with the file itself
    and with every other tool the agent might reach for, including the ripgrep
    output from full-text search.
    """
    return text.split("\n")


_HEADING = re.compile(r"^(\d+(?:\.\d+)*)\.?[ \t]+(\S.*)$")
_PAGE_FOOTER = re.compile(r"\[Page \d+\]\s*$")
_RUNNING_HEADER = re.compile(r"^RFC \d+\s+.*\s\d{4}\s*$")


def furniture_mask(lines: list[str]) -> list[bool]:
    """Mark page headers, footers and form feeds.

    Pre-RFC-8650 documents are paginated for print: each page ends with a
    "[Page N]" footer, a form feed, and a running header repeating the RFC
    number and date. None of it is content. Post-8650 documents are generated
    from XML and have none of it, so the mask is simply all False there.

    Returned as a mask rather than a filtered list so that reported line numbers
    always refer to the original file and stay valid across --raw.
    """
    mask = [False] * len(lines)
    for i, line in enumerate(lines):
        if "\f" in line or _PAGE_FOOTER.search(line) or _RUNNING_HEADER.match(line):
            mask[i] = True
    return mask


def find_sections(lines: list[str], mask: list[bool] | None = None) -> list[dict]:
    """Numbered headings with their 1-based line numbers.

    Headings sit at column 0 in every RFC generation; the table of contents is
    usually indented, and where it is not, its lines have neighbours.

    The mask can be passed in by a caller that needs one anyway; building it
    walks the whole document with three regexes per line, and a section read
    would otherwise do that twice.
    """
    if mask is None:
        mask = furniture_mask(lines)
    matches = [
        None if masked else _HEADING.match(line) for line, masked in zip(lines, mask, strict=True)
    ]
    depths = [match.group(1).count(".") + 1 if match else 0 for match in matches]
    sections: list[dict] = []
    expected_top = 1
    for i, match in enumerate(matches):
        if not match:
            continue
        number = match.group(1)
        depth = depths[i]
        # A heading stands alone; a numbered line with a neighbour of the same
        # shape is a row. That is what a table of contents at column 0 looks
        # like, and a registry table of dotted addresses or OIDs — and the
        # contents are the costlier of the two, because their 1, 2, 3 use up
        # the sequence below and the real headings are then rejected for not
        # continuing it.
        if (i > 0 and depths[i - 1] == depth) or (i + 1 < len(depths) and depths[i + 1] == depth):
            continue
        # A bare number at column 0 is not enough. Pre-1990 RFCs put tables
        # there — the assigned-numbers family especially — and every row of one
        # parsed as a heading, so `sections` answered with a list of table rows
        # and `get --section` resolved to a row of data. Requiring the top level
        # to count 1, 2, 3 rejects "1996 was a good year" without rejecting a
        # real "2. Terminology". Deeper numbers carry no sequence rule: RFC
        # 2616 skips 13.1 and goes straight to 13.1.1, so demanding a parent
        # costs real subsections.
        if "." not in number:
            # A leading zero is a code, not a section: 0001 is a flag value.
            if number.startswith("0") or int(number) != expected_top:
                continue
            expected_top += 1
        sections.append(
            {
                "section": number,
                "title": match.group(2).strip(),
                "line": i + 1,
                "depth": depth,
            }
        )
    # How long each section is, so that a caller choosing one can see what it
    # costs before paying for it. Without this the only way to find out a
    # section is 1400 lines is to read 1400 lines.
    for i, section in enumerate(sections):
        section["lines"] = _section_end(sections, i, len(lines)) - section["line"] + 1
    return sections


def _section_end(sections: list[dict], index: int, total_lines: int) -> int:
    """Last line of sections[index]: a section runs until the next heading at
    the same or a shallower depth, so section 6 includes 6.1 but stops at 7."""
    depth = sections[index]["depth"]
    for section in sections[index + 1 :]:
        if section["depth"] <= depth:
            return section["line"] - 1
    return total_lines


def section_range(sections: list[dict], wanted: str, total_lines: int) -> tuple[int, int, dict]:
    """Resolve a section selector to a 1-based inclusive line range.

    A section runs until the next heading at the same or a shallower depth, so
    asking for section 6 includes 6.1 and 6.2 but stops at section 7.
    """
    target = wanted.strip().rstrip(".")
    index = None
    for i, section in enumerate(sections):
        if section["section"] == target:
            index = i
            break
    if index is None:
        lowered = target.lower()
        for i, section in enumerate(sections):
            if lowered in section["title"].lower():
                index = i
                break
    if index is None:
        raise RFCError(f"no section {wanted!r}; run `sections` to list them")

    return sections[index]["line"], _section_end(sections, index, total_lines), sections[index]


def section_at(sections: list[dict], line: int, total_lines: int) -> dict | None:
    """The deepest section holding a 1-based line, or None before the first
    heading. Deepest, because a match in 4.2.1 is also inside 4 and 4.2, and
    the narrowest of the three is the one worth reading."""
    found = None
    for i, section in enumerate(sections):
        if section["line"] > line:
            break
        if line <= _section_end(sections, i, total_lines):
            found = section
    return found


def check_whole_document(
    number: int, total_lines: int, *, list_hint: str, override_hint: str
) -> None:
    """Refuse a read of a whole long RFC, naming the way to scope it.

    A large section asked for by name is not the failure mode this exists to
    catch, so read_payload never calls this for one. A line range that covers
    the document is, however it was spelled.
    """
    if total_lines <= WHOLE_DOCUMENT_LINE_LIMIT:
        return
    raise RFCError(
        f"RFC {number} is {total_lines} lines — reading it whole would spend the "
        f"context on a specification you have one question about. Run "
        f"`{list_hint}` to find the section that answers it, then read that. "
        f"{override_hint} overrides this if you genuinely need the entire text."
    )


def slice_lines(
    lines: list[str], start: int, end: int, raw: bool, mask: list[bool] | None = None
) -> str:
    """Extract 1-based inclusive lines, dropping page furniture unless raw."""
    start = max(1, start)
    end = min(len(lines), end)
    if start > end:
        return ""
    chunk = lines[start - 1 : end]
    if raw:
        return "\n".join(chunk)
    if mask is None:
        mask = furniture_mask(lines)
    window = mask[start - 1 : end]
    kept = [line for line, is_furniture in zip(chunk, window, strict=True) if not is_furniture]
    return _collapse_blank_runs(kept)


def _collapse_blank_runs(lines: list[str]) -> str:
    out: list[str] = []
    blanks = 0
    for line in lines:
        if line.strip():
            blanks = 0
            out.append(line)
        else:
            blanks += 1
            if blanks <= 1:
                out.append("")
    return "\n".join(out).strip("\n")


# --------------------------------------------------------------------------
# Search
# --------------------------------------------------------------------------


def _check_limit(limit: int) -> None:
    """A page of fewer than one result is not a page, nor is the whole corpus.

    `hits[:0]` is an empty page under a non-zero total, which renders as "no
    matches"; `hits[:-1]` silently drops the last row while the total still
    counts it. The MCP surface takes this straight from the model, which is
    where a negative one comes from — and where a limit of 100000 comes from,
    which is 4 MB of titles or ten minutes of full-text quoting.
    """
    if limit < 1:
        raise RFCError(f"limit must be at least 1, got {limit}")
    if limit > MAX_SEARCH_LIMIT:
        raise RFCError(
            f"limit must be at most {MAX_SEARCH_LIMIT}, got {limit}; the total "
            "is reported whatever the limit, so a larger page is not needed to count"
        )


def search_titles(
    records: dict[int, Record], query: str, limit: int, use_regex: bool = False
) -> tuple[list[Record], int]:
    """Return one page of matches and how many matched in total.

    The total is not decoration. A caller that only sees the page reports the
    page size as the answer — "20 RFCs mention stateless" when 795 do — which
    is the same failure as falling back to a title search: a confident answer
    to a question nobody asked.
    """
    _check_limit(limit)
    if use_regex:
        try:
            pattern = re.compile(query, re.IGNORECASE)
        except re.error as exc:
            raise RFCError(f"bad regular expression: {exc}") from exc

        def matches(title: str) -> bool:
            return pattern.search(title) is not None
    else:
        terms = [t.lower() for t in query.split() if t]

        def matches(title: str) -> bool:
            lowered = title.lower()
            return all(term in lowered for term in terms)

    hits = [r for _, r in sorted(records.items()) if not r.not_issued and matches(r.title)]
    # Ascending by number alone fills the page with the oldest matches and cuts
    # the newest, which on this corpus keeps RFC 2616 and drops RFC 9110 — the
    # exact instinct the project exists to correct. Superseded documents still
    # appear, and `total` is unchanged; they just stop crowding out what
    # replaced them.
    hits.sort(key=lambda r: bool(r.obsoleted_by))
    return hits[:limit], len(hits)


def _search_tool() -> tuple[str, bool]:
    """Pick a full-text search backend: ripgrep if present, else grep."""
    if shutil.which("rg"):
        return "rg", True
    if shutil.which("grep"):
        return "grep", False
    raise RFCError("full-text search needs `rg` or `grep` on PATH; neither was found")


def search_fulltext(
    mirror: Path,
    query: str,
    limit: int,
    max_lines_per_doc: int = 3,
    use_regex: bool = False,
) -> tuple[list[dict], str, int]:
    r"""Rank documents by how many of their lines match, then quote a few.

    Two passes so that the ranking reflects the real count: capping matches per
    file in a single pass would flatten every document to the same score.

    Both backends are asked for *matching lines* — `rg --count`, not
    `--count-matches` — because otherwise the number means whichever tool
    happened to be installed, and the ranking the two passes exist to produce
    comes out in a different order on a different machine.

    The query is a literal string unless use_regex. A pattern here is the
    backend's own dialect and the two do not agree: `\d` is a digit class to rg
    and a literal `d` to POSIX ERE, and `C++` matches on one and fails to
    compile on the other. Defaulting to literal means a search for
    `application/json;charset` asks what it looks like it asks.

    Returns the page, the backend that produced it, and the total number of
    matching documents — see search_titles on why the total is not optional.
    """
    _check_limit(limit)
    tool, is_rg = _search_tool()
    if is_rg:
        count_cmd = [
            "rg",
            "--count",
            "--no-messages",
            "-i",
            *([] if use_regex else ["-F"]),
            "-e",
            query,
            "--glob",
            "rfc[0-9]*.txt",
            str(mirror),
        ]
    else:
        count_cmd = [
            "grep",
            f"-rci{'E' if use_regex else 'F'}",
            "--include=rfc[0-9]*.txt",
            "--",
            query,
            str(mirror),
        ]

    counts: list[tuple[int, int]] = []
    for line in _run_search(count_cmd):
        path, _, count = line.rpartition(":")
        number = _number_from_path(path)
        if number is None:
            continue
        try:
            matching_lines = int(count)
        except ValueError:
            continue
        if matching_lines:
            counts.append((matching_lines, number))
    counts.sort(key=lambda pair: (-pair[0], pair[1]))

    results = []
    for matching_lines, number in counts[:limit]:
        document = document_path(mirror, number)
        # --no-filename / -h keep the output shape at "line:text" for both tools.
        if is_rg:
            line_cmd = [
                "rg",
                "--line-number",
                "--no-filename",
                "--no-heading",
                "--no-messages",
                "--color",
                "never",
                "--max-count",
                str(max_lines_per_doc),
                "-i",
                *([] if use_regex else ["-F"]),
                "-e",
                query,
                str(document),
            ]
        else:
            line_cmd = [
                "grep",
                f"-nhi{'E' if use_regex else 'F'}",
                "-m",
                str(max_lines_per_doc),
                "--",
                query,
                str(document),
            ]
        matches = []
        for line in _run_search(line_cmd):
            lineno, _, body = line.partition(":")
            if not lineno.isdigit():
                continue
            matches.append({"line": int(lineno), "text": body.strip()})
        results.append({"number": number, "matching_lines": matching_lines, "matches": matches})
    return results, tool, len(counts)


def _run_search(cmd: list[str]) -> list[str]:
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, check=False, timeout=SEARCH_TIMEOUT_SECONDS
        )
    except subprocess.TimeoutExpired as exc:
        raise RFCError(
            f"search timed out: {cmd[0]} did not finish within {SEARCH_TIMEOUT_SECONDS} "
            "seconds; try a more specific query"
        ) from exc
    except OSError as exc:
        raise RFCError(f"could not run {cmd[0]}: {exc}") from exc
    # Exit status 1 means "no matches" for both rg and grep; only 2+ is an error.
    if proc.returncode >= 2:
        message = proc.stderr.strip() or f"{cmd[0]} exited {proc.returncode}"
        raise RFCError(f"search failed: {message}")
    return [line for line in proc.stdout.splitlines() if line]


def _number_from_path(path: str) -> int | None:
    match = re.search(r"rfc(\d+)\.txt$", path)
    return int(match.group(1)) if match else None


# --------------------------------------------------------------------------
# Section index
# --------------------------------------------------------------------------
#
# One SQLite file holding every document, zlib-compressed, and an FTS5 index
# over its sections. It answers the question ripgrep cannot — which section
# says this — ranked by BM25 rather than by how long a document is, and it
# serves reads without the mirror or the network, so a machine holding only
# this file can search and read the whole corpus.
#
# Segmentation is find_sections, the parser `get --section` uses, so a search
# hit, an eval gold ID and a read always name the same span. Each row indexes
# a section's own text, from its heading to the next heading at any depth: a
# parent indexed with its subsections would repeat their text and outrank them
# on length alone. The text before the first heading is a row too, headed by
# the RFC's title, because that is where the abstract is.
#
# The FTS5 table is contentless. Storing the text in it as well would hold the
# corpus twice, uncompressed; snippets come from the compressed copy instead.

SECTION_INDEX_NAME = "rfc-sections.db"
# Bumped whenever a reader of the old layout would misread the new one. A file
# that does not match is refused by name, never half-read.
SECTION_INDEX_SCHEMA = 1
# Chosen on the eval set's dev split; docs/search-evaluation.md has the numbers.
DEFAULT_TOKENIZER = "porter unicode61"
HEADING_WEIGHT = 8.0
OBSOLETE_WEIGHT = 0.5
# A query is a question, not a document: past this many terms the extra ones
# only make the OR wider and the search slower.
MAX_QUERY_TERMS = 32

# What `sync --index` costs, for messages written before the release listing
# is fetched. Measured on the build this version was released with.
INDEX_DOWNLOAD_SIZE = "about 270 MB"
INDEX_RELEASES_URL = "https://api.github.com/repos/shbernal/rfc-ai-tooling/releases?per_page=50"
INDEX_TAG_PREFIX = "index-"
INDEX_ASSET = f"{SECTION_INDEX_NAME}.gz"

# Words a question is made of and an answer is not. BM25 already discounts
# them, but each one left in an OR query matches most of the corpus, and the
# whole match set is scored before the page is cut.
_STOPWORD_TEXT = (
    "a about after all also an and any are as at be been being but by can could "
    "did do does doing for from had has have having how i if in into is it its "
    "may me might must my no not of on or our should so some such than that the "
    "their them then there these they this those to too under until up us was we "
    "were what when where whether which while who whom why will with would you "
    "your"
)
_STOPWORDS = frozenset(_STOPWORD_TEXT.split())
_TERM = re.compile(r"\w+")


def section_index_path(mirror: Path) -> Path:
    return mirror / SECTION_INDEX_NAME


def query_terms(query: str) -> list[str]:
    """The words of a query worth matching, lowercased, without repeats.

    A stopword joined to another word by a hyphen or slash is part of a name
    and stays: "after" is filler in a question and half of Retry-After. A query
    made only of stopwords keeps them too: "to be or not to be" is a question
    someone can ask, and an empty match is not an answer to it.
    """
    words: list[str] = []
    kept: list[str] = []
    for chunk in query.split():
        parts = [w.lower() for w in _TERM.findall(chunk)]
        compound = len(parts) > 1 and bool(re.search(r"\w[-/]\w", chunk))
        for part in parts:
            words.append(part)
            if compound or part not in _STOPWORDS:
                kept.append(part)
    return list(dict.fromkeys(kept or words))[:MAX_QUERY_TERMS]


def _segments(lines: list[str], sections: list[dict]) -> list[tuple[str | None, int, int]]:
    """Each section's own span, heading line first, plus the front matter.

    Returned as (section, first line, last line); the front matter's section
    is None and its span is empty when a heading sits on line 1.
    """
    starts = [s["line"] for s in sections]
    spans: list[tuple[str | None, int, int]] = [
        (None, 1, (starts[0] - 1) if starts else len(lines))
    ]
    for i, section in enumerate(sections):
        last = starts[i + 1] - 1 if i + 1 < len(starts) else len(lines)
        spans.append((section["section"], section["line"], last))
    return spans


def build_section_index(
    mirror: Path,
    dest: Path,
    *,
    tokenizer: str = DEFAULT_TOKENIZER,
    progress: Callable[[int, int], None] | None = None,
) -> dict:
    """Build the section index from a mirror into dest, replacing it whole.

    Written to a sibling file and renamed into place, for the reason
    _write_atomically gives: a reader must see the old index or the new one,
    never a file still being filled.
    """
    if not is_populated(mirror):
        raise RFCError(f"{mirror} is not a synced mirror; run `{invocation()} sync` first")
    records = load_index(mirror, offline_only=True)
    numbered = sorted(
        (number, path)
        for path in mirror.glob("rfc[0-9]*.txt")
        if (number := _number_from_path(str(path))) is not None
    )
    started = time.time()
    tmp = dest.with_name(f"{dest.name}.{os.getpid()}.part")
    tmp.unlink(missing_ok=True)
    conn = sqlite3.connect(tmp)
    try:
        conn.executescript(
            f"""
            PRAGMA journal_mode = OFF;
            PRAGMA synchronous = OFF;
            CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE docs (
                number INTEGER PRIMARY KEY,
                obsolete INTEGER NOT NULL,
                text BLOB NOT NULL
            );
            CREATE TABLE sections (
                id INTEGER PRIMARY KEY,
                number INTEGER NOT NULL,
                section TEXT,
                heading TEXT NOT NULL,
                line INTEGER NOT NULL,
                own_end INTEGER NOT NULL,
                end_line INTEGER NOT NULL
            );
            CREATE VIRTUAL TABLE sections_fts USING fts5(
                heading, body, content='', tokenize='{tokenizer}'
            );
            """
        )
        rows = 0
        for done, (number, path) in enumerate(numbered, 1):
            raw = path.read_bytes()
            lines = split_lines(raw.decode("utf-8", errors="replace"))
            mask = furniture_mask(lines)
            sections = find_sections(lines, mask)
            record = records.get(number)
            title = record.title if record else ""
            conn.execute(
                "INSERT INTO docs VALUES (?, ?, ?)",
                (number, int(bool(record and record.obsoleted_by)), zlib.compress(raw, 9)),
            )
            for i, (section, first, last) in enumerate(_segments(lines, sections)):
                if section is None:
                    heading, body_from, end = title, first, last
                    if first > last:
                        continue
                else:
                    heading, body_from = sections[i - 1]["title"], first + 1
                    end = _section_end(sections, i - 1, len(lines))
                body = "\n".join(
                    line
                    for line, masked in zip(
                        lines[body_from - 1 : last], mask[body_from - 1 : last], strict=True
                    )
                    if not masked
                )
                cursor = conn.execute(
                    "INSERT INTO sections (number, section, heading, line, own_end, end_line) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (number, section, heading, first, last, end),
                )
                conn.execute(
                    "INSERT INTO sections_fts (rowid, heading, body) VALUES (?, ?, ?)",
                    (cursor.lastrowid, heading, body),
                )
                rows += 1
            if progress:
                progress(done, len(numbered))
        conn.execute("CREATE INDEX sections_by_number ON sections (number)")
        conn.execute("INSERT INTO sections_fts (sections_fts) VALUES ('optimize')")
        index_file = index_path(mirror)
        meta = {
            "schema": str(SECTION_INDEX_SCHEMA),
            "built": formatdate(usegmt=True),
            "rfc_index": formatdate(index_file.stat().st_mtime, usegmt=True),
            "documents": str(len(numbered)),
            "sections": str(rows),
            "highest_rfc": str(numbered[-1][0] if numbered else 0),
            "tokenizer": tokenizer,
            "built_by": __version__,
        }
        conn.executemany("INSERT INTO meta VALUES (?, ?)", meta.items())
        conn.commit()
        conn.execute("VACUUM")
    except BaseException:
        conn.close()
        tmp.unlink(missing_ok=True)
        raise
    conn.close()
    os.replace(tmp, dest)
    return {
        **meta,
        "path": str(dest),
        "bytes": dest.stat().st_size,
        "seconds": round(time.time() - started, 1),
    }


def open_section_index(path: Path) -> sqlite3.Connection | None:
    """Open the index read-only, or return None when there is none.

    A file that is there but unreadable, or written for another schema, is an
    error rather than None: treating it as absent would send the caller to
    ripgrep or the network without ever saying the index it downloaded is the
    wrong one.
    """
    if not path.exists():
        return None
    conn = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True)
    try:
        row = conn.execute("SELECT value FROM meta WHERE key = 'schema'").fetchone()
    except sqlite3.DatabaseError as exc:
        conn.close()
        raise RFCError(f"{path} is not a readable section index ({exc}); delete it") from exc
    if row is None or row[0] != str(SECTION_INDEX_SCHEMA):
        conn.close()
        raise RFCError(
            f"{path} is a section index in format {row[0] if row else '?'}, and this "
            f"version reads format {SECTION_INDEX_SCHEMA}. Run `{invocation()} sync "
            f"--index` for a current one, or `{invocation()} index build` from a mirror."
        )
    return conn


def section_index_info(conn: sqlite3.Connection) -> dict:
    return dict(conn.execute("SELECT key, value FROM meta").fetchall())


def index_document(conn: sqlite3.Connection, number: int) -> str | None:
    row = conn.execute("SELECT text FROM docs WHERE number = ?", (number,)).fetchone()
    return zlib.decompress(row[0]).decode("utf-8", errors="replace") if row else None


def _snippet(lines: list[str], first: int, last: int, terms: list[str]) -> dict | None:
    """The line in a span that holds the most query terms.

    Matched by prefix, because the index stems and this does not: "caching"
    should light up a line that says "cached". A heading-only hit has no body
    line to quote, and gets the heading.
    """
    stems = [t[:5] if len(t) > 5 else t for t in terms]
    best, best_score = None, 0
    for number in range(first, last + 1):
        words = [w.lower() for w in _TERM.findall(lines[number - 1])]
        score = sum(any(w.startswith(stem) for w in words) for stem in stems)
        if score > best_score:
            best, best_score = number, score
    if best is None:
        return None
    return {"line": best, "text": lines[best - 1].strip()}


def search_sections(
    conn: sqlite3.Connection,
    query: str,
    limit: int,
    *,
    heading_weight: float = HEADING_WEIGHT,
    obsolete_weight: float = OBSOLETE_WEIGHT,
) -> tuple[list[dict], int]:
    """Rank sections by BM25 over the query's terms; return a page and the total.

    Terms are ORed, not ANDed: a question's words are evidence, and a section
    that answers it rarely contains all of them. An obsoleted RFC's score is
    scaled by obsolete_weight, which ranks it lower as the weight falls.
    """
    _check_limit(limit)
    terms = query_terms(query)
    if not terms:
        raise RFCError("query has no words to search for")
    # Quoted so that a term is never read as FTS5 syntax, and split on "_" so
    # that each quoted string is one token to the tokenizer: unicode61 splits
    # LOCAL_PREF in two, and two tokens in quotes are a phrase.
    tokens = dict.fromkeys(part for term in terms for part in term.split("_") if part)
    match = " OR ".join(f'"{token}"' for token in tokens)
    try:
        total = conn.execute(
            "SELECT count(*) FROM sections_fts WHERE sections_fts MATCH ?", (match,)
        ).fetchone()[0]
        rows = conn.execute(
            """
            SELECT s.number, s.section, s.heading, s.line, s.own_end, s.end_line,
                   bm25(sections_fts, ?, 1.0) * (CASE WHEN d.obsolete THEN ? ELSE 1.0 END)
                       AS score
            FROM sections_fts
            JOIN sections s ON s.id = sections_fts.rowid
            JOIN docs d ON d.number = s.number
            WHERE sections_fts MATCH ?
            ORDER BY score, s.number, s.line
            LIMIT ?
            """,
            (heading_weight, obsolete_weight, match, limit),
        ).fetchall()
    except sqlite3.OperationalError as exc:
        # Exactly the missing module. Every FTS5 error starts "fts5:", and
        # reporting a bad query as a missing extension sends the reader to
        # rebuild Python over a typo.
        if "no such module: fts5" in str(exc):
            raise RFCError(
                "this Python's SQLite was built without FTS5, so the section index "
                "cannot be searched here"
            ) from exc
        raise
    documents: dict[int, list[str]] = {}
    results = []
    for number, section, heading, line, own_end, end_line, score in rows:
        if number not in documents:
            documents[number] = split_lines(index_document(conn, number) or "")
        results.append(
            {
                "number": number,
                "section": section,
                "heading": heading,
                "line": line,
                "end_line": end_line,
                "lines": end_line - line + 1,
                "snippet": _snippet(documents[number], line, own_end, terms),
                "score": round(-score, 4),
            }
        )
    return results, total


# --------------------------------------------------------------------------
# Payloads
# --------------------------------------------------------------------------
#
# One builder per operation, because there are two surfaces and only one
# answer. The CLI and the MCP server used to assemble these dicts separately
# and had already drifted — one carried the search backend's name, the other
# carried a title string where the first carried a whole record — with nothing
# to catch it: `make check-vendor` holds this file identical across its copies,
# and the adapters sit outside that. What is genuinely per-surface is how the
# result is rendered and how the flags are spelled, and that is all the
# surfaces are left holding.


@dataclass(frozen=True)
class ReadHints:
    """How the calling surface spells the flags a read error has to name.

    A refusal that names `--section` to a model calling `get_rfc(section=...)`
    is telling it to type something that does not exist, so the message is
    written once and the spelling is supplied by whoever is being spoken to.
    """

    list_hint: str  # "rfc sections 9110" / "list_sections(9110)"
    override_hint: str  # "--full" / "full=true"
    section_flag: str  # "--section" / "section"
    range_flag: str  # "--lines" / "start_line"
    cap_flag: str  # "--max-lines" / "max_lines"


def bare_header(number: int) -> str:
    """The banner for an RFC the index cannot describe."""
    return f"RFC {number}"


def fulltext_unavailable_message(*, retry_hint: str, remote: bool = False) -> str:
    """Why an unsynced full-text search is an error rather than a title search.

    The reason is the same on both surfaces and only the way out differs, so the
    reason is written here once. `remote` is for a server answering over HTTP,
    where the machine that would need syncing may not be the reader's and
    telling them to sync it is advice that cannot be followed.
    """
    if remote:
        where = (
            "There is no section index or RFC mirror on the machine running this "
            "server. It is answering over HTTP, so that machine may not be yours: if "
            f"it is, run `{invocation()} sync --index` there; if it is not, full-text "
            "search is unavailable on this instance and there is nothing to install."
        )
    else:
        where = (
            "Full-text search needs the section index or a local RFC mirror, and "
            f"neither is present. Run `{invocation()} sync --index` in any shell on "
            f"this machine ({INDEX_DOWNLOAD_SIZE}) for ranked search by section, or "
            f"`{invocation()} sync` (512 MB, a few minutes) for the corpus as files."
        )
    return (
        f"{where} Searching titles instead would quietly answer a different "
        f"question, so this is an error and not a fallback. {retry_hint} if a "
        "title search is what you want."
    )


def header_for(mirror: Path, number: int) -> str:
    """Best-effort banner.

    Worth fetching the index for if it is missing, because the obsolescence
    warning is the main thing this adds over reading the document directly. But
    a missing index must never block reading: fall back to a bare banner.
    """
    try:
        record = load_index(mirror).get(number)
    except RFCError:
        record = None
    return record.header() if record else bare_header(number)


def search_payload(
    mirror: Path,
    query: str,
    *,
    scope: str,
    limit: int,
    regex: bool = False,
    unavailable_message: str,
) -> dict:
    """One page of search results, with the total that page came out of."""
    if scope not in {"title", "fulltext"}:
        raise RFCError("scope must be 'title' or 'fulltext'")
    # An empty query has no terms, so every title matches all of them: the
    # "result" is the index. Everything is not an answer to a search.
    if not query.strip():
        raise RFCError("query is empty")

    populated = is_populated(mirror)
    if scope == "fulltext":
        results, tool, total, problem = _fulltext(mirror, query, limit, regex, populated)
        if results is None:
            raise RFCError(problem or unavailable_message)
        records = _records_for_results(mirror)
        for result in results:
            record = records.get(result["number"])
            result["header"] = record.header() if record else bare_header(result["number"])
            result["title"] = record.title if record else ""
            result["record"] = record.to_dict() if record else None
        payload = {
            "query": query,
            "scope": "fulltext",
            "tool": tool,
            "count": len(results),
            "total": total,
            "truncated": total > len(results),
            "results": results,
        }
        if problem:
            payload["note"] = f"searched the mirror instead of the section index: {problem}"
        return payload

    hits, total = search_titles(load_index(mirror), query, limit, regex)
    return {
        "query": query,
        "scope": "title",
        "count": len(hits),
        "total": total,
        "truncated": total > len(hits),
        "fulltext_available": populated,
        "results": [r.to_dict() for r in hits],
    }


def _fulltext(
    mirror: Path, query: str, limit: int, regex: bool, populated: bool
) -> tuple[list[dict] | None, str, int, str | None]:
    """Search with the best backend present: the section index, else ripgrep
    or grep over the mirror.

    Returns (results, tool, total, problem). Results are None when nothing
    present can answer, and the problem, if any, says why. Results with a
    problem mean the index could not be used and the mirror answered instead,
    which the caller says out loud: a silent fallback is a different ranking
    nobody asked for. A pattern is ripgrep's business, so --regex skips the
    index rather than reading a regex as words.
    """
    problem = None
    if not regex:
        try:
            conn = open_section_index(section_index_path(mirror))
        except RFCError as exc:
            conn, problem = None, str(exc)
        if conn is not None:
            try:
                results, total = search_sections(conn, query, limit)
                return results, "index", total, None
            except RFCError as exc:
                # FTS5 missing from this interpreter's SQLite. The mirror can
                # still answer; anything else the index raises is a real error.
                if not populated or "FTS5" not in str(exc):
                    raise
                problem = str(exc)
            finally:
                conn.close()
    if populated:
        results, tool, total = search_fulltext(mirror, query, limit, use_regex=regex)
        _attach_sections(mirror, results)
        return results, tool, total, problem
    if regex and section_index_path(mirror).exists():
        problem = (
            "a regex is matched line by line against the text, which needs the "
            f"synced mirror (`{invocation()} sync`); the section index searches words. "
            "Drop the regex to search the index."
        )
    return None, "", 0, problem


def _attach_sections(mirror: Path, results: list[dict]) -> None:
    """Name the section each quoted line falls in, so a ripgrep hit says
    where to read just as an index hit does."""
    for result in results:
        lines = split_lines(read_document(mirror, result["number"]))
        sections = find_sections(lines)
        for match in result["matches"]:
            section = section_at(sections, match["line"], len(lines))
            match["section"] = section["section"] if section else None


def _records_for_results(mirror: Path) -> dict[int, Record]:
    """Banners for search results, from the index on disk if there is one.

    offline_only, as before: a search must not stall on a refresh. A machine
    holding only the section index may have no index text at all yet, and its
    results then carry bare banners rather than failing.
    """
    try:
        return load_index(mirror, offline_only=True)
    except RFCError:
        return {}


def sections_payload(mirror: Path, number: int) -> dict:
    lines = split_lines(read_document(mirror, number))
    return {
        "number": number,
        "header": header_for(mirror, number),
        "total_lines": len(lines),
        "sections": find_sections(lines),
    }


def read_payload(
    mirror: Path,
    number: int,
    *,
    section: str | None = None,
    start: int | None = None,
    end: int | None = None,
    max_lines: int | None = None,
    full: bool = False,
    raw: bool = False,
    hints: ReadHints,
) -> dict:
    """Resolve a read to a line range and return it with its banner.

    A range given as None at either end means "from the beginning" or "to the
    end"; a section supplies both. Passing a section and a range together is
    the caller asking for two starting points, which is refused rather than
    resolved in one of the two directions silently.
    """
    lines = split_lines(read_document(mirror, number))
    total = len(lines)
    scoped = start is not None or end is not None

    # These arrive from a model as often as from a person. Out of range, they
    # used to come back as an empty read or a payload describing lines the
    # content did not come from, which reads as an RFC with nothing there.
    if max_lines is not None and max_lines < 1:
        raise RFCError(f"{hints.cap_flag} must be at least 1, got {max_lines}")
    if start is not None and start < 1:
        raise RFCError(f"{hints.range_flag} must be at least 1, got {start}")
    if start is not None and start > total:
        raise RFCError(
            f"RFC {number} has {total} lines; {hints.range_flag} {start} is past the end"
        )
    if end is not None and start is not None and end < start:
        raise RFCError(f"the range ends at line {end}, before it starts at {start}")

    mask = None
    section_info = None
    if section:
        if scoped:
            raise RFCError(
                f"{hints.section_flag} and {hints.range_flag} both choose where to start "
                f"reading; pass one. Use {hints.cap_flag} to cap how much of a section "
                "comes back."
            )
        mask = furniture_mask(lines)
        first, last, section_info = section_range(find_sections(lines, mask), section, total)
    else:
        first = 1 if start is None else start
        last = total if end is None else min(end, total)

    if max_lines is not None:
        last = min(last, first + max_lines - 1)

    # On the range that was resolved, not on whether one was supplied: a range
    # starting at line 1, or a cap larger than the document, is the whole
    # document with scoping's spelling, and used to walk straight past this.
    span = last - first + 1
    if not (section or full) and span > WHOLE_DOCUMENT_LINE_LIMIT:
        if (first, last) == (1, total):
            check_whole_document(
                number, total, list_hint=hints.list_hint, override_hint=hints.override_hint
            )
        raise RFCError(
            f"That is {span} lines of RFC {number}, past the {WHOLE_DOCUMENT_LINE_LIMIT} "
            f"a read returns at once. Run `{hints.list_hint}` to find the section that "
            f"answers your question, or narrow the range with {hints.cap_flag}. "
            f"{hints.override_hint} lifts the limit if you genuinely need all of it."
        )

    return {
        "number": number,
        "header": header_for(mirror, number),
        "section": section_info,
        "start_line": first,
        "end_line": last,
        "total_lines": total,
        "content": slice_lines(lines, first, last, raw, mask),
    }


# --------------------------------------------------------------------------
# Sync
# --------------------------------------------------------------------------


def sync_command(mirror: Path, bwlimit: str, dry_run: bool = False) -> list[str]:
    """Build the rsync invocation. --delete is not optional.

    Without --delete, documents removed upstream linger while the index no
    longer lists them, and the two views of the corpus drift apart.
    """
    cmd = [
        "rsync",
        "-az",
        "--delete",
        f"--bwlimit={bwlimit}",
        "--include=rfc[0-9]*.txt",
        "--include=rfc-index.txt",
        "--exclude=*",
        RSYNC_MODULE,
        f"{mirror}/",
    ]
    if dry_run:
        cmd.insert(1, "--dry-run")
    return cmd


def run_sync(mirror: Path, bwlimit: str, assume_yes: bool, dry_run: bool) -> int:
    if not shutil.which("rsync"):
        raise RFCError("`rsync` is not on PATH; install it and try again")
    cmd = sync_command(mirror, bwlimit, dry_run)
    print(f"About to sync the RFC text corpus into {mirror}")
    print("  roughly 9,800 documents, 512 MB, a few minutes")
    print(f"  source: {RSYNC_MODULE} (volunteer-operated; bandwidth limited to {bwlimit})")
    print(f"  {' '.join(cmd)}")
    if not assume_yes and not dry_run:
        if not sys.stdin.isatty():
            raise RFCError("refusing to sync non-interactively without --yes")
        answer = input("Proceed? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Cancelled.")
            return 1
    mirror.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(cmd, check=False)
    if result.returncode == 0 and not dry_run:
        (mirror / SYNC_STAMP).write_text(f"synced {formatdate(usegmt=True)}\n", encoding="utf-8")
        print(f"\nDone. {count_documents(mirror)} documents in {mirror}")
    return result.returncode


def latest_index_release() -> dict:
    """The newest published section index: its tag, asset URL, size and checksum URL.

    Index builds are releases of their own, tagged index-YYYY-MM-DD and never
    marked latest, so the release a package installer resolves stays the
    software. The listing is newest first; the first index tag in it wins.
    """
    data, _ = _fetch(INDEX_RELEASES_URL)
    try:
        releases = json.loads(data or b"[]")
    except ValueError as exc:
        raise RFCError(f"unreadable release listing from {INDEX_RELEASES_URL}") from exc
    for release in releases:
        if not str(release.get("tag_name", "")).startswith(INDEX_TAG_PREFIX):
            continue
        assets = {a.get("name"): a for a in release.get("assets", [])}
        asset, checksum = assets.get(INDEX_ASSET), assets.get(f"{INDEX_ASSET}.sha256")
        if asset and checksum:
            return {
                "tag": release["tag_name"],
                "url": asset["browser_download_url"],
                "bytes": int(asset.get("size", 0)),
                "sha256_url": checksum["browser_download_url"],
            }
    raise RFCError(f"no published section index found at {INDEX_RELEASES_URL}")


def _download(url: str, dest: Path) -> str:
    """Stream a URL to a file and return its SHA-256.

    Not _fetch: that holds the body in memory, which is fine for a 2 MB index
    and not for this.
    """
    digest = hashlib.sha256()
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as response, dest.open("wb") as out:
            while chunk := response.read(1 << 20):
                digest.update(chunk)
                out.write(chunk)
    except urllib.error.HTTPError as exc:
        raise RFCError(f"HTTP {exc.code} fetching {url}") from exc
    except urllib.error.URLError as exc:
        raise RFCError(f"network error fetching {url}: {exc.reason}") from exc
    return digest.hexdigest()


def run_index_download(mirror: Path, assume_yes: bool) -> int:
    """Fetch the prebuilt section index, verify it, and swap it into place.

    Checked twice before it replaces anything: the download against the
    published SHA-256, and the decompressed file by opening it, which refuses
    a format this version cannot read. A failure at either step leaves the
    previous index untouched.
    """
    release = latest_index_release()
    size = f"{release['bytes'] / 1e6:.0f} MB" if release["bytes"] else "size unknown"
    dest = section_index_path(mirror)
    print(f"About to download the section index into {dest}")
    print(f"  {release['tag']}, {size} compressed")
    print(f"  source: {release['url']}")
    if not assume_yes:
        if not sys.stdin.isatty():
            raise RFCError("refusing to download non-interactively without --yes")
        answer = input("Proceed? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Cancelled.")
            return 1
    mirror.mkdir(parents=True, exist_ok=True)
    expected, _ = _fetch(release["sha256_url"])
    expected_hex = (expected or b"").decode("ascii", errors="replace").split()[:1]
    packed = dest.with_name(f"{dest.name}.{os.getpid()}.gz.part")
    unpacked = dest.with_name(f"{dest.name}.{os.getpid()}.part")
    try:
        actual = _download(release["url"], packed)
        if not expected_hex or actual != expected_hex[0].lower():
            raise RFCError(
                f"the downloaded index does not match its published SHA-256 "
                f"(expected {expected_hex[0] if expected_hex else 'nothing'}, got {actual})"
            )
        with gzip.open(packed, "rb") as source, unpacked.open("wb") as out:
            shutil.copyfileobj(source, out, 1 << 20)
        conn = open_section_index(unpacked)
        if conn is None:
            raise RFCError("the downloaded index vanished before it could be checked")
        info = section_index_info(conn)
        conn.close()
        os.replace(unpacked, dest)
    finally:
        packed.unlink(missing_ok=True)
        unpacked.unlink(missing_ok=True)
    print(
        f"\nDone. {info.get('documents', '?')} documents, {info.get('sections', '?')} "
        f"sections, built {info.get('built', '?')}, in {dest}"
    )
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def parse_number(value: int | str) -> int:
    """Accept 9110, "9110", "rfc9110" or "RFC 9110"; reject everything else.

    Takes an int as well as a string so that the MCP tools can route through it
    too. They used to pass the model's argument straight to a URL, where 0 and
    negative numbers became a fetch of rfc0.txt and a 404 that reads as though
    a real RFC does not exist.
    """
    match = re.fullmatch(r"(?:rfc\s*)?0*(\d+)", str(value).strip(), re.IGNORECASE)
    number = int(match.group(1)) if match else 0
    if not number:
        raise RFCError(f"not an RFC number: {value!r}")
    return number


def _emit(payload: dict, human: str, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(human)


def _describe_age(seconds: float) -> str:
    if seconds < 86400:
        hours = round(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} old"
    days = round(seconds / 86400)
    return f"{days} day{'s' if days != 1 else ''} old"


def cmd_status(args: argparse.Namespace) -> int:
    mirror = resolve_mirror(args.mirror)
    path = index_path(mirror)
    # is_populated() would glob the mirror a second time to answer the same
    # question this count already answers.
    docs = count_documents(mirror)
    populated = path.exists() and ((mirror / SYNC_STAMP).exists() or docs > POPULATED_THRESHOLD)

    section_index = _section_index_status(section_index_path(mirror))
    searchable = populated or section_index.get("usable", False)

    index_info: dict = {"present": path.exists(), "path": str(path)}
    lines = [
        f"mode: {'offline' if populated else 'online'}"
        f" ({'full-text search available' if searchable else 'title search only'})",
        f"mirror: {mirror} ({docs} document{'s' if docs != 1 else ''})",
    ]
    if path.exists():
        age = time.time() - path.stat().st_mtime
        index_info["age_seconds"] = int(age)
        index_info["stale"] = age > INDEX_STALE_SECONDS
        try:
            # offline_only: reporting on the index must not go and refresh it.
            entries = len(load_index(mirror, offline_only=True))
        except (RFCError, OSError):
            entries = 0
        index_info["entries"] = entries
        lines.append(f"index: {path} ({entries} entries, {_describe_age(age)})")
    else:
        lines.append(f"index: not present (will be fetched on first use) — {path}")
    lines.append(section_index.pop("line"))
    if not searchable:
        lines.append(
            f"run `{invocation()} sync --index` for ranked full-text search, or "
            f"`{invocation()} sync` for the whole corpus (512 MB)"
        )

    payload = {
        "mode": "offline" if populated else "online",
        "fulltext_available": searchable,
        "mirror": str(mirror),
        "documents": docs,
        "index": index_info,
        "section_index": section_index,
    }
    _emit(payload, "\n".join(lines), args.json)
    return 0


def _section_index_status(path: Path) -> dict:
    """What `status` says about the section index, plus the line it prints."""
    info: dict = {"present": path.exists(), "path": str(path)}
    if not path.exists():
        info["line"] = f"section index: not present — {path}"
        return info
    try:
        conn = open_section_index(path)
    except RFCError as exc:
        info["usable"] = False
        info["problem"] = str(exc)
        info["line"] = f"section index: {path} (unusable: {exc})"
        return info
    assert conn is not None
    try:
        meta = section_index_info(conn)
    finally:
        conn.close()
    info.update(usable=True, bytes=path.stat().st_size, **meta)
    info["line"] = (
        f"section index: {path} ({meta.get('documents', '?')} documents, "
        f"{meta.get('sections', '?')} sections, built {meta.get('built', '?')})"
    )
    return info


def cmd_meta(args: argparse.Namespace) -> int:
    mirror = resolve_mirror(args.mirror)
    number = parse_number(args.number)
    records = load_index(mirror)
    record = records.get(number)
    if record is None:
        raise RFCError(
            f"RFC {number} is not in the index. If it was published very recently, "
            f"`{invocation()} get {number}` may still retrieve it."
        )
    lines = [record.header()]
    if record.authors:
        lines.append(f"Authors: {record.authors}")
    if record.date:
        lines.append(f"Date: {record.date}")
    for label, refs in (
        ("Obsoletes", record.obsoletes),
        ("Updates", record.updates),
    ):
        if refs:
            lines.append(f"{label}: RFC " + ", ".join(str(n) for n in refs))
    if record.also:
        lines.append("Also: " + ", ".join(record.also))
    if record.doi:
        lines.append(f"DOI: {record.doi}")
    _emit(record.to_dict(), "\n".join(lines), args.json)
    return 0


def _truncation_note(shown: int, total: int) -> str:
    """Say so when a page is not the whole answer.

    Silence here reads as completeness: `--limit` defaults to 20, and a reader
    who is not told otherwise will report 20 as the count.
    """
    if total <= shown:
        return ""
    if shown >= MAX_SEARCH_LIMIT:
        return f"\n\n(showing {shown} of {total} — narrow the query for the rest)"
    return f"\n\n(showing {shown} of {total} — raise --limit for more)"


def _search_human(payload: dict) -> str:
    rows = payload["results"]
    if not rows:
        return "no matches"
    if payload["scope"] == "fulltext" and payload.get("tool") == "index":
        lines: list[str] = []
        for row in rows:
            where = f"§{row['section']} {row['heading']}" if row["section"] else "front matter"
            lines.append(row["header"])
            lines.append(f"   {where}  (line {row['line']}, {row['lines']} lines)")
            if row["snippet"]:
                lines.append(f"   {row['snippet']['line']}: {row['snippet']['text']}")
            lines.append("")
        human = "\n".join(lines).strip()
    elif payload["scope"] == "fulltext":
        lines = []
        for row in rows:
            lines.append(row["header"])
            lines += [
                f"   {m['line']}: {m['text']}"
                + (f"  (§{m['section']})" if m.get("section") else "")
                for m in row["matches"]
            ]
            lines.append("")
        human = "\n".join(lines).strip()
    else:
        human = "\n".join(row["header"] for row in rows)
    human += _truncation_note(payload["count"], payload["total"])
    if payload["scope"] == "title" and not payload["fulltext_available"]:
        human += f"\n\n(titles only — `{invocation()} sync --index` enables full-text search)"
    if payload.get("note"):
        human += f"\n\n({payload['note']})"
    return human


def cmd_search(args: argparse.Namespace) -> int:
    payload = search_payload(
        resolve_mirror(args.mirror),
        args.query,
        scope="fulltext" if args.fulltext else "title",
        limit=args.limit,
        regex=args.regex,
        unavailable_message=fulltext_unavailable_message(retry_hint="Drop --fulltext"),
    )
    _emit(payload, _search_human(payload), args.json)
    return 0


def _sections_human(payload: dict) -> str:
    lines = [payload["header"]]
    if payload["sections"]:
        lines += [
            f"{'  ' * (s['depth'] - 1)}{s['section']}  {s['title']}  "
            f"(line {s['line']}, {s['lines']} lines)"
            for s in payload["sections"]
        ]
    else:
        lines.append(
            "(no numbered headings found — this RFC is not sectioned in the usual "
            "way; use `get --lines A:B`)"
        )
    return "\n".join(lines)


def cmd_sections(args: argparse.Namespace) -> int:
    payload = sections_payload(resolve_mirror(args.mirror), parse_number(args.number))
    _emit(payload, _sections_human(payload), args.json)
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    number = parse_number(args.number)
    start = end = None
    if args.lines:
        match = re.fullmatch(r"(\d+):(\d+)?", args.lines.strip())
        if not match:
            raise RFCError(f"--lines wants START:END, got {args.lines!r}")
        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else None
    payload = read_payload(
        resolve_mirror(args.mirror),
        number,
        section=args.section,
        start=start,
        end=end,
        max_lines=args.max_lines,
        full=args.full,
        raw=args.raw,
        hints=ReadHints(
            list_hint=f"{invocation()} sections {number}",
            override_hint="--full",
            section_flag="--section",
            range_flag="--lines",
            cap_flag="--max-lines",
        ),
    )
    _emit(payload, f"{payload['header']}\n\n{payload['content']}", args.json)
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    mirror = resolve_mirror(args.mirror)
    if args.index:
        if args.dry_run:
            raise RFCError("--dry-run applies to the corpus sync, not to --index")
        return run_index_download(mirror, args.yes)
    return run_sync(mirror, args.bwlimit, args.yes, args.dry_run)


def cmd_index_build(args: argparse.Namespace) -> int:
    mirror = resolve_mirror(args.mirror)
    dest = Path(args.output).expanduser() if args.output else section_index_path(mirror)

    def progress(done: int, total: int) -> None:
        if done % 500 == 0 or done == total:
            print(f"\r{done}/{total} documents", end="", file=sys.stderr, flush=True)

    stats = build_section_index(mirror, dest, tokenizer=args.tokenizer, progress=progress)
    print(file=sys.stderr)
    human = (
        f"{stats['documents']} documents, {stats['sections']} sections, "
        f"{stats['bytes'] / 1e6:.0f} MB, {stats['seconds']:.0f}s\n{stats['path']}"
    )
    _emit(stats, human, args.json)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=invocation(),
        description=(
            f"Look up IETF RFCs. Works with no setup; `{invocation()} sync` adds full-text search."
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    # Named rather than resolved: resolving here would call default_mirror() on
    # every run just to build the help, which is the one thing it must not do
    # when there is no home directory to find. `status` prints the live path.
    parser.add_argument(
        "--mirror",
        help="corpus directory (default: $RFC_MIRROR, else the platform data directory)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_read_flags(p: argparse.ArgumentParser) -> None:
        p.add_argument("--json", action="store_true", help="machine-readable output")

    p_status = sub.add_parser("status", help="show mode, mirror and index age")
    add_read_flags(p_status)
    p_status.set_defaults(func=cmd_status)

    p_search = sub.add_parser("search", help="search RFC titles, or full text with --fulltext")
    p_search.add_argument("query")
    p_search.add_argument(
        "--fulltext", action="store_true", help="search document bodies (needs a synced mirror)"
    )
    p_search.add_argument("--regex", action="store_true", help="treat the query as a regex")
    p_search.add_argument(
        "--limit",
        type=int,
        default=20,
        help=f"results per page (default: 20, at most {MAX_SEARCH_LIMIT})",
    )
    add_read_flags(p_search)
    p_search.set_defaults(func=cmd_search)

    p_meta = sub.add_parser("meta", help="title, status, and what obsoletes what")
    p_meta.add_argument("number")
    add_read_flags(p_meta)
    p_meta.set_defaults(func=cmd_meta)

    p_sections = sub.add_parser("sections", help="list headings with line numbers")
    p_sections.add_argument("number")
    add_read_flags(p_sections)
    p_sections.set_defaults(func=cmd_sections)

    p_get = sub.add_parser("get", help="read an RFC, ideally one section at a time")
    p_get.add_argument("number")
    p_get.add_argument("--section", help="section number (e.g. 6.1) or heading text")
    p_get.add_argument("--lines", help="line range START:END, for RFCs without headings")
    p_get.add_argument(
        "--max-lines", type=int, help="cap how many lines come back, from wherever the read starts"
    )
    p_get.add_argument(
        "--full",
        action="store_true",
        help=f"read more than {WHOLE_DOCUMENT_LINE_LIMIT} lines at once, up to the whole document",
    )
    p_get.add_argument("--raw", action="store_true", help="keep page headers and footers")
    add_read_flags(p_get)
    p_get.set_defaults(func=cmd_get)

    p_sync = sub.add_parser("sync", help="download the corpus for full-text search (512 MB)")
    p_sync.add_argument(
        "--index",
        action="store_true",
        help="download the prebuilt section index instead: ranked search and reads, no mirror",
    )
    p_sync.add_argument("--bwlimit", default="2M", help="rsync bandwidth limit (default: 2M)")
    p_sync.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    p_sync.add_argument("--dry-run", action="store_true")
    p_sync.set_defaults(func=cmd_sync)

    p_index = sub.add_parser("index", help="build the section index from a synced mirror")
    index_sub = p_index.add_subparsers(dest="index_command", required=True)
    p_build = index_sub.add_parser("build", help="index every section of the mirror")
    p_build.add_argument("--output", help="where to write it (default: inside the mirror)")
    p_build.add_argument(
        "--tokenizer",
        default=DEFAULT_TOKENIZER,
        help=f"FTS5 tokenizer (default: {DEFAULT_TOKENIZER!r})",
    )
    add_read_flags(p_build)
    p_build.set_defaults(func=cmd_index_build)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except RFCError as exc:
        print(f"rfc: {exc}", file=sys.stderr)
        return 1
    except BrokenPipeError:
        return 0
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
