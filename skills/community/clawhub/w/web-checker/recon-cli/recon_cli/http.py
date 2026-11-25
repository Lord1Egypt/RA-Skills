"""HTTP helpers built on `curl` (with a stdlib fallback).

We prefer curl because it already handles:
  - redirects (-L), HTTP/2, SNI, cert verification
  - clean header dumps (-I)
  - fast, low-overhead requests

If curl is not installed, the urllib-based fallbacks are used instead, so the
tool keeps working on a bare Python install.

Every public function returns (ok: bool, data: str) unless noted otherwise.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import urllib.error
import urllib.request
from typing import Optional, Tuple

from .config import Config

# ---------------------------------------------------------------------------
# curl helpers
# ---------------------------------------------------------------------------


def _curl(*args: str, cfg: Config) -> Tuple[bool, str]:
    curl = shutil.which("curl")
    if not curl:
        return False, "curl not found"
    # Every caller passes the request URL as an http(s) URL argument; refuse
    # anything that curl could otherwise read as an option.
    if not any(a.startswith(("http://", "https://")) for a in args):
        return False, "curl refused: no http(s) URL argument"
    cmd = [
        curl, "-sS",
        "--max-time", str(cfg.timeout),
        "--max-redirs", str(cfg.max_redirects),
        *args,
    ]
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=cfg.timeout + 5
        )
    except Exception as e:  # noqa: BLE001
        return False, f"curl failed: {e}"
    if p.returncode == 0:
        return True, p.stdout
    return False, (p.stderr or p.stdout or f"curl exit {p.returncode}").strip()


def _has_curl() -> bool:
    return shutil.which("curl") is not None


def head(url: str, cfg: Config, follow: bool = False) -> Tuple[bool, str]:
    """Return the response headers (HEAD request, optionally following redirects).

    When ``follow=False`` (default), only the entry-point response is returned.
    Set ``follow=True`` to follow redirect chains up to ``--max-redirs``.
    """
    if not _has_curl():
        return _py_head(url, cfg, follow=follow)
    args = ["-I", url]
    if follow:
        args.insert(0, "-L")
    return _curl(*args, cfg=cfg)


def get(url: str, cfg: Config, follow: bool = False) -> Tuple[bool, str]:
    """Return the response body (GET request, optionally following redirects).

    When ``follow=False`` (default), only the entry-point response is returned.
    Set ``follow=True`` to follow redirect chains up to ``--max-redirs``.
    """
    if not _has_curl():
        return _py_get(url, cfg, follow=follow)
    args = [url]
    if follow:
        args.insert(0, "-L")
    return _curl(*args, cfg=cfg)


def status_code(url: str, cfg: Config) -> Tuple[Optional[int], str]:
    """Return (code, error) - code is None on transport failure."""
    if not _has_curl():
        return _py_status(url, cfg)
    ok, out = _curl("-o", os.devnull, "-w", "%{http_code}", url, cfg=cfg)
    if not ok:
        return None, out
    codes = re.findall(r"^(\d{3})\s*$", out, re.MULTILINE)
    try:
        return int(codes[-1]), ""
    except (IndexError, ValueError):
        return None, out


def _strip_header_blocks(raw: str) -> str:
    """Remove leading HTTP header blocks from a curl ``-D -`` dump.

    Redirects produce several header blocks, each separated by a blank line.
    The body starts after the last block; unlike ``rpartition("\\n\\n")`` this
    does not truncate bodies that contain blank lines of their own.
    """
    body = raw.replace("\r\n", "\n").replace("\r", "\n")
    while True:
        m = re.match(r"HTTP/[^\n]*\n(?:[^\n]*\n)*?\n", body)
        if not m:
            return body
        body = body[m.end():]


def probe(url: str, cfg: Config, body_bytes: int = 2048) -> dict:
    """Fetch following redirects; return final status, content-type, body head.

    Used by sensitive-path probing to tell a *real* file (200 + text/plain,
    short, distinctive) apart from an SPA catch-all (200 + text/html shell).
    """
    res: dict = {"code": None, "content_type": "", "body": ""}
    if not _has_curl():
        return _py_probe(url, cfg, body_bytes)

    ok, out = _curl(
        "-L", "-r", f"0-{body_bytes - 1}",
        "-D", "-",
        "-w", "\n__FINAL__%{http_code} %{content_type}",
        url,
        cfg=cfg,
    )
    if not ok:
        res["body"] = out[:200]
        return res

    # The __FINAL__ trailer (from -w) always lands at the very end.
    m = re.search(r"__FINAL__(\d{3})\s+([^\n]*)\s*$", out)
    if m:
        res["code"] = int(m.group(1))
        res["content_type"] = m.group(2).strip()
        out = out[: m.start()]
    res["body"] = _strip_header_blocks(out)[:body_bytes]
    return res


def follow_redirects(url: str, cfg: Config) -> Tuple[bool, str]:
    """GET following redirects; returns final body."""
    return get(url, cfg, follow=True)


def save(url: str, dest: str, cfg: Config) -> Tuple[bool, str]:
    """Save URL content to disk at ``dest``.

    DESTINATION SCOPE: only writes under the configured output directory
    (defaults to /tmp/recon-cli-output/).  Skips if the destination file
    already exists to avoid data loss from accidental collisions.
    """
    _output_dir = os.path.expanduser(cfg.output_dir if hasattr(cfg, 'output_dir') and cfg.output_dir else '/tmp/recon-cli-output/')
    real_dest = os.path.realpath(dest)
    allowed = os.path.realpath(_output_dir)
    if not real_dest.startswith(allowed + os.sep) and real_dest != allowed:
        return False, f"save() denied: {dest} is outside the output directory"
    if os.path.exists(real_dest):
        return False, f"save() skipped (file exists): {real_dest}"
    if not _has_curl():
        return _py_save(url, dest, cfg)
    return _curl("-L", url, "-o", dest, cfg=cfg)


# ---------------------------------------------------------------------------
# stdlib fallbacks (used if curl is missing)
# ---------------------------------------------------------------------------


def _py_head(url: str, cfg: Config, follow: bool = False) -> Tuple[bool, str]:
    if not follow:
        # Disable default redirect handling to get the entry-point status.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None  # Signal urllib to stop following
        opener = urllib.request.build_opener(NoRedirect)
    else:
        opener = urllib.request.urlopen  # use default (follows redirects)
    req = urllib.request.Request(url, method="HEAD")
    try:
        if follow:
            r = opener(req, timeout=cfg.timeout)
        else:
            r = opener.open(req, timeout=cfg.timeout)
        lines = [f"HTTP/{r.status} {r.reason}"]
        for k, v in r.headers.items():
            lines.append(f"{k}: {v}")
        return True, "\n".join(lines) + "\n"
    except urllib.error.HTTPError as e:
        lines = [f"HTTP/{e.code} {e.reason}"]
        for k, v in e.headers.items():
            lines.append(f"{k}: {v}")
        return True, "\n".join(lines) + "\n"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def _py_get(url: str, cfg: Config, follow: bool = False) -> Tuple[bool, str]:
    if not follow:
        # Disable default redirect handling to get the entry-point response only.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        opener = urllib.request.build_opener(NoRedirect)
    else:
        # Enforce cfg.max_redirects (previously the fallback ignored this limit).
        class CountedRedirect(urllib.request.HTTPRedirectHandler):
            def __init__(self, max_redir: int):
                self.count = 0
                self.max_redir = max_redir
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                if self.count >= self.max_redir:
                    return None  # stop counting at the configured limit
                self.count += 1
                return urllib.request.Request(newurl, method=req.get_method())
        opener = urllib.request.build_opener(CountedRedirect(cfg.max_redirects))
    try:
        if follow:
            r = opener(url, timeout=cfg.timeout)
        else:
            r = opener.open(urllib.request.Request(url), timeout=cfg.timeout)
        return True, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return True, e.read().decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def _py_status(url: str, cfg: Config) -> Tuple[Optional[int], str]:
    try:
        with urllib.request.urlopen(url, timeout=cfg.timeout) as r:
            return r.status, ""
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


def _py_probe(url: str, cfg: Config, body_bytes: int) -> dict:
    res: dict = {"code": None, "content_type": "", "body": ""}
    req = urllib.request.Request(url, headers={"Range": f"bytes=0-{body_bytes - 1}"})
    try:
        with urllib.request.urlopen(req, timeout=cfg.timeout) as r:
            res["code"] = r.status
            res["content_type"] = r.headers.get("Content-Type", "")
            res["body"] = r.read(body_bytes).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        res["code"] = e.code
        res["content_type"] = e.headers.get("Content-Type", "")
        try:
            res["body"] = e.read(body_bytes).decode("utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass
    except Exception as e:  # noqa: BLE001
        res["body"] = f"{type(e).__name__}: {e}"
    return res


def _py_save(url: str, dest: str, cfg: Config) -> Tuple[bool, str]:
    try:
        with urllib.request.urlopen(url, timeout=cfg.timeout) as r, open(dest, "wb") as fh:
            fh.write(r.read())
        return True, ""
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"
