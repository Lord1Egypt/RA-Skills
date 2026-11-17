"""pv_netio - network layer (v6.4.0 split of verify_pmids.py).

Transport (circuit breaker, retries, UA rotation), the registry fetchers
(NCBI esummary, Europe PMC, Crossref, OpenAlex) and the pre-flight probe
state. Stdlib-only; the main module re-exports every public name."""

import re
import json
import os
import time
import sys
import urllib.parse
import urllib.request
import urllib.error
import http.client
import sqlite3
import csv
import zipfile
import html
import random
import io
import itertools
from collections import defaultdict
from html.parser import HTMLParser
from difflib import SequenceMatcher
from pathlib import Path
import xml.etree.ElementTree as ET

# cross-module imports (explicit — underscore names are excluded
# from `import *`, so every private helper is named here)
from pv_meta import (_OPENALEX_BASE, _TEXT_NUM_RE, _TOOL_VERSION, _UA_BROWSER, _UA_TOOL, _clean_doi)

_OPTS = {"ncbi_key": "", "mailto": "", "meta_source": "auto", "timeout": 20}

_CIRCUIT_THRESHOLD = 2  # call-level consecutive transport failures per host

_BREAKER_COOLDOWN_S = 30  # half-open: after this, admit one probe call

_HOST_FAILS = defaultdict(int)

_BREAKER_REJECTS = defaultdict(int)   # calls refused by an open breaker, per host (v5.8.0 visibility)

_HOST_OPENED_AT = {}

class CircuitOpenError(RuntimeError):
    """Host circuit breaker is open after repeated transport failures."""

def _host_key(url: str) -> str:
    """'https://eutils.ncbi.nlm.nih.gov' from a full URL (scheme://host granularity)."""
    parts = url.split("/")
    return "/".join(parts[:3]) if len(parts) > 2 else url

def _api_get(url: str, max_retries: int = 3, timeout=None) -> bytes:
    """HTTP GET hardened for the field: UA rotation on 403/406, Retry-After
    compliance on 429, per-host circuit breaker.

    Breaker accounting is per LOGICAL call (one exhausted call = +1), never
    per retry attempt -- per-attempt counting would open the breaker on the
    first slow call. HTTP status errors never count as transport failures.
    """
    timeout = _OPTS["timeout"] if timeout is None else timeout
    hk = _host_key(url)
    if _HOST_FAILS[hk] >= _CIRCUIT_THRESHOLD:
        opened_at = _HOST_OPENED_AT.get(hk)
        if opened_at is None:
            _HOST_OPENED_AT[hk] = time.time()
            _BREAKER_REJECTS[hk] += 1
            raise CircuitOpenError(
                f"无法连接 {hk}（已连续 {_CIRCUIT_THRESHOLD} 次传输失败），"
                f"本批次跳过该数据源——受影响的引用将标记为待确认，不会误报不存在。"
                f"建议：确认网络/代理后重试；或 --timeout {_OPTS['timeout'] * 2:.0f} 放宽超时；"
                f"或 --meta-source europepmc 改走 Europe PMC 兜底源。")
        if time.time() - opened_at >= _BREAKER_COOLDOWN_S:
            # half-open: admit one probe call; success resets below
            _HOST_FAILS[hk] = _CIRCUIT_THRESHOLD - 1
            _HOST_OPENED_AT.pop(hk, None)
        else:
            _BREAKER_REJECTS[hk] += 1
            raise CircuitOpenError(
                f"{hk} 刚刚连续失败，稍候 {_BREAKER_COOLDOWN_S:.0f}s 会自动重试——"
                f"本批次先跳过它。建议：--meta-source europepmc 改走 Europe PMC 兜底源。")
    last_err = None
    transport = False
    for attempt in range(max_retries):
        ua = _UA_TOOL if attempt == 0 else _UA_BROWSER  # 403/406 → 换浏览器 UA 重试
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read()
            _HOST_FAILS[hk] = 0  # success resets the breaker
            _HOST_OPENED_AT.pop(hk, None)
            return body
        except urllib.error.HTTPError as e:
            last_err, transport = e, False  # HTTP responses never trip the breaker
            if e.code == 429 and attempt < max_retries - 1:
                wait = 2.0
                try:
                    wait = min(5.0, max(1.0, float(e.headers.get("Retry-After", 2.0))))
                except (TypeError, ValueError):
                    pass
                if "api.openalex.org" in url:
                    wait = max(wait, 5.0)   # OpenAlex common pool refills slower
                time.sleep(wait)
            elif e.code in (403, 406) and attempt < max_retries - 1:
                time.sleep(0.8)
            elif e.code >= 500 and attempt < max_retries - 1:
                time.sleep(2 ** attempt)      # transient server errors: back off
            elif e.code < 500:
                raise                          # deterministic 4xx: no point retrying
        except (urllib.error.URLError, OSError, TimeoutError, http.client.HTTPException) as e:
            last_err, transport = e, True
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    if transport:
        _HOST_FAILS[hk] += 1
    if last_err is None:  # e.g. max_retries=0 — never raise None
        raise RuntimeError(f"no attempts made for {url}")
    raise last_err

def _breaker_summary_line() -> str:
    """End-of-run visibility for circuit-breaker skips (v5.8.0): the run
    used to open the breaker silently and the only symptom was a pile of
    unknowns; now one [WARN] line names the hosts, the skip counts and the
    recovery path."""
    if not _BREAKER_REJECTS:
        return ""
    parts = ", ".join(f"{h.split('//')[-1]} x{n}" for h, n in
                      sorted(_BREAKER_REJECTS.items(), key=lambda kv: -kv[1]))
    return (f"circuit breaker skipped {sum(_BREAKER_REJECTS.values())} call(s) "
            f"to still-down host(s): {parts} — those citations stay unknown; "
            f"re-run later (unknowns are never cached)")

def _ncbi_params(extra: dict = None) -> str:
    """E-utilities common params: api_key (when configured) + tool/email etiquette."""
    params = {"tool": "pubmed-verifier"}
    params.update(extra or {})
    if _OPTS["ncbi_key"]:
        params["api_key"] = _OPTS["ncbi_key"]
    if _OPTS["mailto"]:
        params["email"] = _OPTS["mailto"]
    return urllib.parse.urlencode(params)

def _parse_esummary(batch: list, data: dict) -> dict:
    """Map an esummary JSON response onto {pmid: metadata_dict}.

    A 200 response whose body is valid JSON but lacks the `result` map is a
    source anomaly (schema change / silently degraded service), NOT an
    answer: those are marked network_error so they are never classified as
    "PMID not found" and never poison the cache. Individual PMIDs missing
    from a well-formed `result` map ARE an authoritative not-found.
    """
    out = {}
    if not isinstance(data, dict) or "result" not in data:
        for pmid in batch:
            out[pmid] = {"valid": False, "network_error": True,
                         "error": f"esummary 响应异常（缺少 result 结构）：{str(data)[:80]}"}
        return out
    for pmid in batch:
        if pmid in data.get("result", {}):
            article = data["result"][pmid]
            if "error" not in article:
                # Retraction signal from the registry itself (v2.7.0):
                # "Retracted Publication" marks the retracted paper;
                # "Retraction of Publication" (the notice) does NOT flag.
                pubtypes = [" ".join(str(p).split()).lower() for p in article.get("pubtype", []) or []]
                retracted = "retracted publication" in pubtypes
                # Registered DOI: articleids[] is authoritative. elocationid
                # can be a composite string (e.g. eLife "pii: X. doi: Y")
                # that is NOT a bare DOI -- parsing it whole caused false
                # splice flags on perfectly correct DOIs (v2.4.0 review P0,
                # real-data tested on PMID 42770840).
                doi = ""
                for rec in article.get("articleids", []) or []:
                    if isinstance(rec, dict) and rec.get("idtype") == "doi":
                        doi = str(rec.get("value", "") or "")
                        break
                if not doi:
                    m = re.search(r'doi:\s*(\S+)', article.get("elocationid", "") or "")
                    doi = m.group(1) if m else ""
                out[pmid] = {
                    "title": article.get("title", ""),
                    "authors": [a.get("name", "") for a in article.get("authors", [])],
                    "journal": article.get("source", ""),
                    "pubdate": article.get("pubdate", ""),
                    "volume": article.get("volume", ""),
                    "pages": article.get("pages", ""),
                    "doi": doi,
                    "retracted": retracted,
                    "retraction_type": ("retraction" if retracted else ""),
                    "retraction_note": ("PubMed publication type: Retracted Publication"
                                        if retracted else ""),
                    "valid": True,
                    "source": "ncbi",
                }
            else:
                out[pmid] = {"valid": False, "error": article["error"], "source": "ncbi"}
        else:
            out[pmid] = {"valid": False, "error": "PMID not found in API response", "source": "ncbi"}
    return out

def fetch_summaries(pmids: list, batch_size: int = 50) -> dict:
    """Fetch article summaries from PubMed. Primary source: NCBI esummary.

    With --meta-source auto (default), a batch whose NCBI call FAILS
    (transport error, circuit breaker, exhausted retries) is retried against
    Europe PMC before being reported as unreachable. A definite "not found"
    answer from NCBI is authoritative and never re-queried.
    Entries that could not be verified carry network_error=True and are
    classified as unknown -- a network failure is never "invalid".
    """
    if _OPTS["meta_source"] == "europepmc":
        # Explicitly forced: never touch NCBI (deterministic for testing and
        # for users who must avoid NCBI altogether).
        return fetch_summaries_europepmc(pmids, batch_size=min(batch_size, 25),
                                         primary_label="Europe PMC")
    results = {}
    batch_interval = 0.12 if _OPTS["ncbi_key"] else 0.4
    use_fallback = _OPTS["meta_source"] == "auto"
    n_batches = -(-len(pmids) // batch_size) if pmids else 0
    for i in range(0, len(pmids), batch_size):
        batch = pmids[i:i + batch_size]
        if n_batches > 2:
            print(f"  PubMed progress: batch {i // batch_size + 1}/{n_batches}"
                  f" fetched...", file=sys.stderr, flush=True)
        ids_str = ",".join(batch)
        url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
               + _ncbi_params({"db": "pubmed", "id": ids_str, "retmode": "json"}))
        try:
            data = json.loads(_api_get(url))
            results.update(_parse_esummary(batch, data))
        except Exception as e:
            if use_fallback:
                results.update(fetch_summaries_europepmc(batch))
            else:
                for pmid in batch:
                    results[pmid] = {"valid": False, "error": str(e), "network_error": True}
        time.sleep(batch_interval)
    return results

def _retry_sweep(info_map: dict, keys: list, fetch_fn, retries: int,
                 label: str, failed_pred=None) -> tuple:
    """In-batch retry sweep (v5.7.0): re-fetch only the entries a fetch stage
    lost to the network, after a short cool-off, instead of leaving the user
    to re-run the whole command. Returns (merged_map, recovered_count).

    A sweep never makes a run worse than its first pass: a still-open circuit
    breaker aborts the sweep and the first-pass answers stand; entries that
    fail again simply keep their first-pass unknown."""
    if retries <= 0 or not keys:
        return info_map, 0
    failed = [k for k in keys
              if (failed_pred(info_map.get(k)) if failed_pred
                  else (not info_map.get(k) or info_map[k].get("network_error")))]
    if not failed:
        return info_map, 0
    print(f"[NOTE] {label}: retrying {len(failed)} network-failed call(s) "
          f"({retries} sweep{'s' if retries > 1 else ''}, 2s cool-off)",
          file=sys.stderr, flush=True)
    recovered = 0
    time.sleep(2.0)
    for sweep in range(retries):
        try:
            again = fetch_fn(failed)
        except CircuitOpenError:
            break   # breaker still open — first-pass answers stand
        still_failed = []
        for k in failed:
            v = again.get(k)
            if v and not (failed_pred(v) if failed_pred else v.get("network_error")):
                info_map[k] = v
                recovered += 1
            else:
                still_failed.append(k)
        if not still_failed:
            break
        failed = still_failed
        if sweep < retries - 1:
            time.sleep(2.0 * (sweep + 2))
    if recovered:
        print(f"[NOTE] {label}: retry recovered {recovered}/{recovered + len(failed)} "
              f"call(s)", file=sys.stderr, flush=True)
    return info_map, recovered

def fetch_summaries_europepmc(pmids: list, batch_size: int = 25,
                              primary_label: str = "NCBI 与 Europe PMC") -> dict:
    """Europe PMC fallback source (free, no key, mirrors PubMed).

    Returns an entry for every requested PMID: matched records map to the
    same metadata shape (source='europepmc'); records absent from a
    well-formed reply are reported not-found via this source; a failed or
    malformed call marks the whole batch network_error=True (unknown, never
    invalid).
    """
    results = {}
    for i in range(0, len(pmids), batch_size):
        batch = pmids[i:i + batch_size]
        q = " OR ".join(f"EXT_ID:{p}" for p in batch)
        params = urllib.parse.urlencode({
            "query": f"({q}) AND SRC:MED", "format": "json",
            "pageSize": str(batch_size), "resultType": "lite"})
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{params}"
        got = {}
        try:
            data = json.loads(_api_get(url))
            if not isinstance(data, dict) or "resultList" not in data:
                raise ValueError(f"响应缺少 resultList 结构：{str(data)[:80]}")
            for h in data.get("resultList", {}).get("result", []):
                pmid = str(h.get("id", "")).strip()
                if not pmid.isdigit():
                    continue
                epmc_retracted = "retracted publication" in str(h.get("pubType", "") or "").lower()
                got[pmid] = {
                    "title": h.get("title", ""),
                    "authors": [a.strip() for a in (h.get("authorString") or "").split(",") if a.strip()],
                    "journal": h.get("journalTitle", ""),
                    "pubdate": h.get("pubYear", ""),
                    "volume": h.get("journalVolume", ""),
                    "pages": h.get("pageInfo", ""),
                    "doi": h.get("doi", "") or "",
                    # v5.2.0: citation count rides the same lite response —
                    # a rough impact signal, None when the profile omits it
                    "cited_by_count": (int(h["citedCount"])
                                       if str(h.get("citedCount", "")).isdigit() else None),
                    "retracted": epmc_retracted,
                    "retraction_type": ("retraction" if epmc_retracted else ""),
                    "retraction_note": ("Europe PMC publication type: retracted publication"
                                        if epmc_retracted else ""),
                    "valid": True,
                    "source": "europepmc",
                }
        except Exception as e:
            for pmid in batch:
                results[pmid] = {"valid": False, "network_error": True,
                                 "error": f"{primary_label} 均不可达（最后错误：{e}）。"
                                          f"未判定——网络故障不会判为「PMID不存在」"}
            continue
        for pmid in batch:
            if pmid in got:
                results[pmid] = got[pmid]
            else:
                results[pmid] = {"valid": False, "error": "PMID not found (europepmc)",
                                 "source": "europepmc"}
        time.sleep(0.35)  # be polite to EBI when walking large batches
    return results

def fetch_doi_metadata(doi: str) -> dict:
    """Fetch metadata from Crossref API by DOI. With --mailto set, requests
    join the Crossref polite pool (?mailto=) for more generous rate limits."""
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}"
    if _OPTS["mailto"]:
        url += f"?mailto={urllib.parse.quote(_OPTS['mailto'])}"
    try:
        data = json.loads(_api_get(url, timeout=15))
        msg = data.get("message", {})
        authors = []
        for a in msg.get("author", []):
            family = a.get("family", "")
            given = a.get("given", "")
            authors.append(f"{family} {given}".strip())
        year = ""
        pub_date = msg.get("published-print") or msg.get("published-online") or msg.get("created", {})
        parts = pub_date.get("date-parts", [[]])
        if parts and parts[0]:
            year = str(parts[0][0])
        # Retraction detection (v2.3.0, ported from cite-holmes): Crossref
        # lists withdrawal events in updated-by[]; any entry typed
        # "retraction" (or "removal" — the paper was withdrawn from the
        # record entirely, v5.1.0) means the paper is unusable.
        # Corrections and other update types do NOT count. (In filters the
        # key is hyphenated update-type; response items carry plain "type".)
        retracted, retraction_note, retraction_date = False, "", ""
        retraction_type = ""
        update_dois = []
        retraction_notice_doi = ""
        for u in msg.get("updated-by", []) or []:
            if not isinstance(u, dict):
                continue
            ud = str(u.get("DOI", "") or "").strip()
            if ud:
                update_dois.append(ud)
            utype = str(u.get("type") or u.get("update-type") or "").lower()
            if utype in ("retraction", "removal"):
                retracted = True
                retraction_type = utype
                retraction_notice_doi = ud   # THE notice, not update_dois[0]
                retraction_note = (f"{'removed' if utype == 'removal' else 'retracted'}"
                                   f" by DOI {u.get('DOI', '?')}")
                upd = (u.get("updated") or {}).get("date-time") or (u.get("updated") or {}).get("date-parts")
                if upd:
                    retraction_date = str(upd)
                break
        return {
            "valid": True,
            "title": msg.get("title", [""])[0] if msg.get("title") else "",
            "authors": authors,
            "journal": msg.get("container-title", [""])[0] if msg.get("container-title") else "",
            "pubdate": year,
            "doi": doi,
            "retracted": retracted,
            "retraction_type": retraction_type,
            "retraction_note": retraction_note,
            "retraction_date": retraction_date,
            # v5.3.0: DOIs of the notices themselves + the notice abstract
            # (JATS tags stripped) — the abstract is where an actual REASON
            # lives when the registry carries one
            "update_dois": update_dois,
            "retraction_notice_doi": retraction_notice_doi,
            "abstract": re.sub(r"<[^>]+>", " ", msg.get("abstract", "") or "")[:400].strip(),
            "source": "crossref",
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}

def search_pubmed(query: str, max_results: int = 5,
                   raise_on_error: bool = False) -> list:
    """Search PubMed and return article summaries."""
    params = _ncbi_params({"db": "pubmed", "term": query, "retmode": "json",
                           "retmax": str(max_results)})
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{params}"
    try:
        data = json.loads(_api_get(url, timeout=15))
        ids = data["esearchresult"]["idlist"]
        if ids:
            return [{"pmid": pid, **fetch_summaries([pid]).get(pid, {})} for pid in ids]
    except Exception:
        if raise_on_error:
            raise
    return []

def resolve_doi(doi: str, timeout=None) -> dict:
    """Resolve a DOI against the Crossref works API (v2.8.0).

    Returns {'status': 'resolved'|'not_found'|'error', 'meta': dict|None,
    'error': str}. A 404 is an authoritative not-found (fabrication signal);
    any transport/other failure is an 'error' and never counts against the DOI.
    """
    url = f"https://api.crossref.org/works/{urllib.parse.quote(_clean_doi(doi), safe='')}"
    if _OPTS["mailto"]:
        url += f"?mailto={urllib.parse.quote(_OPTS['mailto'])}"
    try:
        data = json.loads(_api_get(url, timeout=timeout if timeout is not None else _OPTS["timeout"]))
        msg = data.get("message", {})
        year = ""
        pub_date = msg.get("published-print") or msg.get("published-online") or msg.get("created", {})
        parts = pub_date.get("date-parts", [[]])
        if parts and parts[0]:
            year = str(parts[0][0])
        # Retraction signal rides the same response (updated-by) — without it
        # the --dois pipeline would be blind to retractions (v2.8.0 review P1).
        # v5.1.0: removals count too (paper withdrawn from the record), and
        # the structured type/date ride along — same shape as fetch_doi_metadata.
        retracted, retraction_note, retraction_date = False, "", ""
        retraction_type = ""
        update_dois = []
        retraction_notice_doi = ""
        for u in msg.get("updated-by", []) or []:
            if not isinstance(u, dict):
                continue
            ud = str(u.get("DOI", "") or "").strip()
            if ud:
                update_dois.append(ud)
            utype = str(u.get("type") or u.get("update-type") or "").lower()
            if utype in ("retraction", "removal"):
                retracted = True
                retraction_type = utype
                retraction_notice_doi = ud   # THE notice, not update_dois[0]
                retraction_note = (f"{'removed' if utype == 'removal' else 'retracted'}"
                                   f" by DOI {u.get('DOI', '?')}")
                upd = (u.get("updated") or {}).get("date-time") or (u.get("updated") or {}).get("date-parts")
                if upd:
                    retraction_date = str(upd)
                break
        meta = {
            "title": msg.get("title", [""])[0] if msg.get("title") else "",
            "journal": msg.get("container-title", [""])[0] if msg.get("container-title") else "",
            "year": year,
            "authors": [f"{a.get('family', '')} {a.get('given', '')}".strip()
                        for a in msg.get("author", [])],
            "type": msg.get("type", ""),
            "retracted": retracted,
            "retraction_type": retraction_type,
            "retraction_note": retraction_note,
            "retraction_date": retraction_date,
            "update_dois": update_dois,
            "retraction_notice_doi": retraction_notice_doi,
            "abstract": re.sub(r"<[^>]+>", " ", msg.get("abstract", "") or "")[:400].strip(),
        }
        return {"status": "resolved", "meta": meta, "error": ""}
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"status": "not_found", "meta": None,
                    "error": "DOI not found in Crossref (404)"}
        return {"status": "error", "meta": None, "error": f"crossref HTTP {e.code}"}
    except (urllib.error.URLError, OSError, TimeoutError, http.client.HTTPException,
            json.JSONDecodeError, ValueError, CircuitOpenError) as e:
        return {"status": "error", "meta": None, "error": str(e)}

def fetch_openalex_doi(doi: str, timeout=None) -> dict:
    """Resolve a DOI against OpenAlex (v4.1.0) — the fallback for DOIs that
    do not live in Crossref (DataCite, Zenodo, SSRN, Chinese registries).

    Returns a meta dict shaped like resolve_doi's, or {} when OpenAlex also
    reports the DOI unknown (404) or is unreachable — a fallback failure
    never manufactures evidence, it just leaves the Crossref-404 semantics
    untouched."""
    url = f"{_OPENALEX_BASE}/works/https://doi.org/{urllib.parse.quote(_clean_doi(doi), safe='')}"
    if _OPTS["mailto"]:
        url += f"?mailto={urllib.parse.quote(_OPTS['mailto'])}"
    try:
        data = json.loads(_api_get(url, timeout=timeout if timeout is not None else _OPTS["timeout"]))
    except urllib.error.HTTPError:
        return {}
    except (urllib.error.URLError, OSError, TimeoutError, http.client.HTTPException,
            json.JSONDecodeError, ValueError, CircuitOpenError):
        return {}
    authors = [a.get("author", {}).get("display_name", "")
               for a in data.get("authorships", []) if isinstance(a, dict)]
    src_obj = (data.get("primary_location") or {}).get("source") or {}
    meta = {
        "title": data.get("display_name", "") or data.get("title", ""),
        "journal": src_obj.get("display_name", "") or "",
        "year": str(data.get("publication_year") or ""),
        "authors": [a for a in authors if a],
        "type": data.get("type", ""),
        "retracted": bool(data.get("is_retracted")),
        "retraction_type": ("retraction" if data.get("is_retracted") else ""),
        # v5.2.0: OpenAlex carries the citation count natively
        "cited_by_count": (int(data["cited_by_count"])
                           if str(data.get("cited_by_count", "")).isdigit() else None),
        "retraction_note": "retracted (OpenAlex retraction state)" if data.get("is_retracted") else "",
        "registry": "openalex",
    }
    return meta

def search_openalex_title(query: str, max_results: int = 3,
                          raise_on_error: bool = False,
                          timeout=None) -> list:
    """Search OpenAlex works by free-text title (v4.1.0). Raises on network
    failure (callers decide honesty), returns a list of work dicts."""
    params = urllib.parse.quote(query, safe="")
    url = f"{_OPENALEX_BASE}/works?search={params}&per-page={max_results}"
    if _OPTS["mailto"]:
        url += f"&mailto={urllib.parse.quote(_OPTS['mailto'])}"
    try:
        data = json.loads(_api_get(url, timeout=timeout if timeout is not None else _OPTS["timeout"]))
    except Exception:
        if raise_on_error:
            raise
        return []
    return data.get("results", []) or []

def _cjk_query_from_raw(raw: str) -> str:
    """Heuristic CJK title query from a plain-text reference entry.

    Academic reference lines follow "作者. 标题. 刊名, 年." — so after
    stripping numbering / PMID / DOI / URL noise, the title is the first
    sentence-sized segment: skip a short comma-bearing leading segment
    (the author list) and take the next one; a comma-free leading segment
    IS the title (author-less entries). Quoted via chr() to survive every
    patching/quoting layer."""
    _punct = r"[\[\]{}()（）<>《》;;,，.。:：!！?？|/" + chr(34) + chr(39) + "]"
    t = _TEXT_NUM_RE.sub("", raw or "", count=1)
    t = re.sub(r'PMID[\s]*\d{4,9}', ' ', t, flags=re.IGNORECASE)
    t = re.sub(r'(?:https?://\S+|\bdoi\s*[:：]?\s*10\.\S+|10\.\d{4,9}/\S+)',
               ' ', t, flags=re.IGNORECASE)
    t = re.sub(r'arXiv[\s]*\S+', ' ', t, flags=re.IGNORECASE)
    # segment on sentence periods BEFORE stripping them (the title is a
    # segment, not the whole line)
    segments = [s.strip() for s in re.split(r'[.。]', t) if s.strip()]
    if not segments:
        return ""
    title_seg = segments[0]
    # author-like: short (a bare Chinese name is <=6 chars) or comma-bearing
    if len(segments) >= 2 and len(title_seg) <= 20 and (
            "，" in title_seg or "," in title_seg
            or len(title_seg.replace(" ", "")) <= 6):
        title_seg = segments[1]
    title_seg = re.sub(_punct + "+", " ", title_seg)
    title_seg = re.sub(r'\b[JMRDSC]\b', ' ', title_seg)   # GB/T type tags
    title_seg = " ".join(title_seg.split())
    return title_seg[:40].strip()


# __all__ recalculated at the true end of the module so every
# late-appended name is exported to `import *` consumers
_NAMES = [n for n in dir() if not n.startswith('__')]
__all__ = _NAMES
del _NAMES
