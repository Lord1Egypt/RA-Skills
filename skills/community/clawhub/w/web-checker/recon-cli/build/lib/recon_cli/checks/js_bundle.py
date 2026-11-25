"""JS-bundle check - secret hunt, external deps, XSS-risk patterns.

This is the highest-yield audit check: a lot of real incidents come from
secrets baked into a client bundle. We start with the entry bundle referenced
by the HTML shell, then follow same-origin chunk references discovered inside
it (Vite/Webpack lazy chunks) up to ``cfg.max_js_bundles``.
"""
from __future__ import annotations

import os
import posixpath
import re
from typing import List, Set, Tuple
from urllib.parse import urlsplit

from ..config import Config
from ..finding import CheckResult, Finding, Severity
from ..http import get, save
from .base import Check

# Secret patterns. Order matters: specific → generic.
SECRET_PATTERNS: List[Tuple[str, str]] = [
    ("OpenAI / sk-",            r"sk-[A-Za-z0-9]{16,}"),
    ("Google API key (AIza)",   r"AIza[0-9A-Za-z_-]{30,}"),
    ("GitHub PAT (ghp_)",       r"ghp_[A-Za-z0-9]{20,}"),
    ("Slack token (xox*)",      r"xox[bp]-[A-Za-z0-9-]{10,}"),
    ("JWT (eyJ)",               r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{5,}"),
    ("AWS access key (AKIA)",   r"AKIA[0-9A-Z]{12,}"),
    ("GitHub OAuth client",     r"gho_[A-Za-z0-9]{20,}"),
    ("npm token",               r"npm_[A-Za-z0-9]{20,}"),
    ("generic secret assignment",
     r"\b[A-Z0-9_]*(API_KEY|SECRET|TOKEN|PASSWORD|PRIVATE_KEY)\s*[=:]\s*['\"][^'\"\s]{8,}"),
]

# External URL patterns (excludes XML namespaces + data: URIs)
EXTERNAL_URL_RE = re.compile(r"https?://[A-Za-z0-9._-]+(?:/[A-Za-z0-9._/?=%&-]*)?")
NAMESPACE_DOMAINS = {"www.w3.org", "xmlns.org", "schemas.xmlsoap.org"}

# XSS-risk patterns. A hit is only a *real* finding if untrusted input reaches it.
# All analysis is static — no JavaScript is executed.
XSS_PATTERNS: List[Tuple[str, str]] = [
    ("innerHTML",             r"innerHTML\s*="),
    ("outerHTML",             r"outerHTML\s*="),
    ("document.write",        r"document\.write\s*\("),
    ("eval()",                r"\beval\s*\("),
    ("new Function",          r"new\s+Function\s*\("),
    ("dangerouslySetInnerHTML", r"dangerouslySetInnerHTML"),
    ("insertAdjacentHTML",    r"insertAdjacentHTML\s*\("),
]


def _looks_like_library_code(context: str) -> bool:
    """Heuristics: is this hit inside React/ReactDOM/Vue internals (FP) or app code?"""
    indicators = [
        "throw Error(i(",      # React minified error lookup
        "__html",              # React's own key
        "case `dangerouslySetInnerHTML`", "case `dangerouslySetInnerHTML`:",
        "case\"dangerouslySetInnerHTML\"",
        "case `src`", "case `style`",
        "onScrollEnd",
        "ReactDOM", "reconciler", "Scheduler",
        # minified switch-case style used by React's DOM property handlers
        "case`", "case `",
        # React's property validation block (throws on unknown/DOM-unsafe props)
        "throw Error(91)", "throw Error(137)",
    ]
    hits = sum(1 for i in indicators if i in context)
    # Strong on their own (React's error-throw blocks / the DSH switch cases)
    if any(i in context for i in (
        "case`dangerouslySetInnerHTML",
        "case `dangerouslySetInnerHTML`,",
        "throw Error(91)",
        "throw Error(137)",
        "throw Error(i(",
    )):
        return True
    return hits >= 2


def _find_main_bundle(shell_html: str) -> Tuple[str, str]:
    """Return (bundle_path, bundle_url).

    Prefers the conventional Vite entry bundle (``/assets/index-*.js``) and
    falls back to any ``/assets/*.js`` reference in the shell.
    """
    candidates = re.findall(r'["\'](/assets/index-[A-Za-z0-9_.-]+\.js)["\']', shell_html)
    if not candidates:
        candidates = re.findall(r'["\'](/assets/[A-Za-z0-9_.-]+\.js)["\']', shell_html)
    if not candidates:
        return "", ""
    # pick the first (conventionally the main one)
    path = candidates[0]
    return path, path


# Quoted or parenthesised references to a .js file. Covers script src,
# modulepreload href, Vite dynamic imports (``import("./chunk.js")``), and
# ``__vite__mapDeps`` string tables.
JS_REF_RE = re.compile(r"""["'`]([^"'`\s]+?\.js)(?:[?#][^"'`\s]*)?["'`]""")
ASSET_JS_RE = re.compile(r"""["'`](/assets/[A-Za-z0-9_.-]+\.js)["'`]""")

# Explicit shell tags: these are the authoritative list of eager bundles.
SCRIPT_SRC_RE = re.compile(r"""<script\b[^>]*\bsrc\s*=\s*["']([^"']+)["']""", re.I)
LINK_HREF_RE = re.compile(r"""<link\b[^>]*\bhref\s*=\s*["']([^"']+)["']""", re.I)


def _normalise_ref(ref: str, from_path: str = "", origin: str = "") -> str:
    """Turn a JS reference into a same-origin absolute path (or ``""``)."""
    ref = ref.strip()
    if not ref or ref.startswith(("//", "data:", "blob:")):
        return ""
    if ref.startswith(("http://", "https://")):
        if not origin:
            return ""
        base = urlsplit(origin)
        target = urlsplit(ref)
        if (target.scheme, target.netloc) != (base.scheme, base.netloc):
            return ""
        ref = target.path or "/"
    ref = ref.split("#", 1)[0].split("?", 1)[0]
    if not ref.endswith(".js"):
        return ""
    if ref.startswith("/"):
        path = ref
    else:
        base_dir = posixpath.dirname(from_path) or "/"
        path = posixpath.normpath(posixpath.join(base_dir, ref))
    if not path.startswith("/"):
        path = "/" + path
    return path


def _find_bundles(shell_html: str, origin: str = "") -> List[str]:
    """All same-origin JS paths referenced by the shell, main entry first.

    Explicit ``<script src>`` / ``<link href>`` tags are read first, then any
    remaining ``/assets/*.js`` string in the shell is used as a fallback.
    """
    ordered: List[str] = []
    main, _ = _find_main_bundle(shell_html)
    if main:
        ordered.append(main)
    refs = (
        SCRIPT_SRC_RE.findall(shell_html)
        + LINK_HREF_RE.findall(shell_html)
        + ASSET_JS_RE.findall(shell_html)
    )
    for ref in refs:
        path = _normalise_ref(ref, origin=origin)
        if path and path not in ordered:
            ordered.append(path)
    return ordered


def _discover_chunk_refs(js: str, from_path: str, origin: str = "") -> List[str]:
    """Find same-origin chunk references inside a downloaded bundle."""
    out: List[str] = []
    for ref in JS_REF_RE.findall(js):
        path = _normalise_ref(ref, from_path, origin)
        if path and path != from_path and path not in out:
            out.append(path)
    return out


class JsBundleCheck(Check):
    name = "js_bundle"
    description = "Hunt for secrets / exfil URLs / XSS-risk patterns across JS chunks"

    def run(self, target: str, cfg: Config) -> CheckResult:
        findings: List[Finding] = []
        url = target if target.startswith("http") else f"https://{target}"

        # 1. get shell to find the entry bundle and any eager chunks
        ok, shell = get(url, cfg, follow=True)
        if not ok:
            return CheckResult(self.name, "error", error=shell[:400])

        base = re.match(r"(https?://[^/]+)", url)
        base = base.group(1) if base else url

        queue = _find_bundles(shell, base)
        if not queue:
            findings.append(Finding(self.name, "No /assets/*.js bundle found in shell (maybe server-rendered or no JS)",
                                   Severity.INFO))
            return CheckResult(self.name, "ok", findings, "no bundle detected")

        # 2. download the entry bundle + same-origin lazy chunks (BFS, capped)
        os.makedirs(cfg.scratch_dir, exist_ok=True)
        seen: Set[str] = set()
        bundles: List[Tuple[str, str, int]] = []
        failures: List[str] = []

        while queue and len(bundles) < cfg.max_js_bundles:
            path = queue.pop(0)
            if path in seen:
                continue
            seen.add(path)

            dest = os.path.join(cfg.scratch_dir, f"{len(bundles):02d}-{os.path.basename(path)}")
            ok, err = save(base + path, dest, cfg)
            if not ok:
                failures.append(f"{path}: {err[:120]}")
                continue
            try:
                with open(dest, "r", encoding="utf-8", errors="replace") as f:
                    js = f.read()
            except OSError as e:
                failures.append(f"{path}: {e}")
                continue

            size = os.path.getsize(dest)
            bundles.append((path, js, size))
            for ref in _discover_chunk_refs(js, path, base):
                if ref not in seen and ref not in queue:
                    queue.append(ref)

        if not bundles:
            detail = "; ".join(failures[:3]) or "no bundle could be downloaded"
            return CheckResult(self.name, "error", error=detail[:400])

        total_size = sum(size for _, _, size in bundles)
        findings.append(Finding(
            self.name,
            f"Scanned {len(bundles)} JS bundle(s) ({total_size:,} bytes)",
            Severity.INFO,
            "\n".join(f"{path} ({size:,}B)" for path, _, size in bundles),
            f"Saved under {cfg.scratch_dir}",
        ))
        if len(bundles) > 1:
            findings.append(Finding(
                self.name,
                f"Followed {len(bundles) - 1} lazy-loaded chunk(s)",
                Severity.INFO,
                ", ".join(path for path, _, _ in bundles[1:10]),
                "Vite/Webpack split code into chunks; secrets can hide in any of them.",
            ))
        if failures:
            findings.append(Finding(
                self.name, f"{len(failures)} JS reference(s) could not be downloaded",
                Severity.INFO, "; ".join(failures[:5]),
            ))
        if queue:
            findings.append(Finding(
                self.name, f"JS chunk cap reached ({cfg.max_js_bundles}); {len(queue)} more not scanned",
                Severity.INFO, "Raise --max-js-bundles for deeper coverage.",
            ))

        # 3. secret hunt across every downloaded bundle
        secret_hits = 0
        real_secret_hits = 0
        for path, js, _ in bundles:
            for label, pattern in SECRET_PATTERNS:
                for m in re.finditer(pattern, js):
                    start = max(0, m.start() - 60)
                    end = min(len(js), m.end() + 60)
                    ctx = js[start:end].replace("\n", " ")
                    secret_hits += 1
                    val = m.group(0)
                    where = f" in {path}" if len(bundles) > 1 else ""
                    if re.search(r"(xxxx|<.*>|YOUR_|PLACEHOLDER|TODO|dummy)", val, re.I):
                        findings.append(Finding(self.name, f"{label}{where} (placeholder - likely FP)",
                                               Severity.INFO, ctx,
                                               "Template/placeholder value, not a live secret.",
                                               is_false_positive=True))
                    else:
                        real_secret_hits += 1
                        findings.append(Finding(
                            self.name, f"{label}{where} - verify this is NOT your app's live secret",
                            Severity.HIGH, ctx,
                            "Read surrounding code. If it's YOUR app code assigning it, rotate the key and move to server-side.",
                            extra={"pattern": label, "offset": m.start(), "bundle": path}))
        if secret_hits == 0:
            findings.append(Finding(self.name, "No secret patterns in scanned bundle(s)", Severity.INFO))

        # 4. external URLs (exfil / supply-chain), deduped across bundles
        urls: Set[str] = set()
        for _, js, _ in bundles:
            urls.update(EXTERNAL_URL_RE.findall(js))
        real_urls = [
            u for u in urls
            if u.split("://")[-1].split("/")[0] not in NAMESPACE_DOMAINS
            and "xmlns" not in u and "xmlsoap" not in u
        ]
        real_urls.sort()
        if real_urls:
            for u in real_urls[:20]:
                domain = u.split("://")[-1].split("/")[0]
                if any(t in domain for t in ("analytics", "sentry", "posthog", "mixpanel", "amplitude", "gtm.", "googletagmanager")):
                    cls = "analytics/telemetry"
                    sev = Severity.LOW
                elif any(t in domain for t in ("api", "app", "forms", "spree", "formspree")):
                    cls = "API / form endpoint"
                    sev = Severity.MED
                else:
                    cls = "external"
                    sev = Severity.INFO
                findings.append(Finding(self.name, f"External: {u}  [{cls}]", sev, u,
                                       "Confirm trust. Every external URL is a supply-chain + exfil surface."))
        else:
            findings.append(Finding(self.name, "No external URLs in scanned bundle(s) (self-contained)", Severity.INFO))

        # 5. XSS-risk patterns (with context-based FP triage)
        xss_fps = 0
        xss_real = 0
        for path, js, _ in bundles:
            for label, pattern in XSS_PATTERNS:
                for m in re.finditer(pattern, js):
                    start = max(0, m.start() - 80)
                    end = min(len(js), m.end() + 80)
                    ctx = js[start:end].replace("\n", " ")
                    where = f" in {path}" if len(bundles) > 1 else ""
                    if _looks_like_library_code(ctx):
                        xss_fps += 1
                        findings.append(Finding(self.name, f"{label}{where} (React/lib internals - FP)",
                                               Severity.INFO, ctx,
                                               "Part of the framework's DOM renderer, not your app.",
                                               is_false_positive=True))
                    else:
                        xss_real += 1
                        findings.append(Finding(self.name, f"{label}{where} - check if untrusted input can reach it",
                                               Severity.MED, ctx,
                                               "Read the data flow. Real vuln only if untrusted input reaches it unsanitized."))
        findings.append(Finding(self.name,
                                f"XSS patterns: {xss_real} possible real, {xss_fps} FP (React internals)",
                                Severity.INFO))

        summary = (f"bundles={len(bundles)} ({total_size:,}B); secrets={real_secret_hits}/{secret_hits} real; "
                   f"ext-urls={len(real_urls)}; xss-real={xss_real}, xss-fp={xss_fps}")
        return CheckResult(self.name, "ok", findings, summary)
