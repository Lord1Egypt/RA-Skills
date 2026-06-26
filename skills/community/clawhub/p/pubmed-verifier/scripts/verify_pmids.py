#!/usr/bin/env python3
"""
PMID Citation Verifier — PubMed E-utilities API
Verifies existence, metadata cross-check, and optional content-matching of PMID citations.

Three-state verdict:
  ✅ Correct  — PMID exists AND matches claimed paper
  ⚠️ Mismatch — PMID exists but points to a DIFFERENT paper
  ❌ Invalid  — PMID not found in PubMed

Usage:
  python3 verify_pmids.py --source <file_or_dir> [--match-keywords] [--output report.html]
  python3 verify_pmids.py --pmids 31018962,22213727
  python3 verify_pmids.py --claims-file claims.json --output report.html
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import urllib.request
import urllib.parse
from difflib import SequenceMatcher
from pathlib import Path
from collections import defaultdict


# ── PubMed API helpers ──

def _api_get(url: str, max_retries: int = 3, timeout: int = 20) -> bytes:
    """HTTP GET with retry and exponential backoff. Returns response body."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "pubmed-verifier/2.1"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, OSError) as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # 1s, 2s, 4s
                time.sleep(wait)
            else:
                raise


def fetch_summaries(pmids: list[str], batch_size: int = 50) -> dict:
    """Fetch article summaries from PubMed esummary API. Returns {pmid: metadata_dict}."""
    results = {}
    for i in range(0, len(pmids), batch_size):
        batch = pmids[i:i + batch_size]
        ids_str = ",".join(batch)
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids_str}&retmode=json"
        try:
            data = json.loads(_api_get(url))
            for pmid in batch:
                if pmid in data.get("result", {}):
                    article = data["result"][pmid]
                    if "error" not in article:
                        doi_raw = article.get("elocationid", "")
                        doi = doi_raw.replace("doi: ", "") if doi_raw.startswith("doi: ") else doi_raw
                        results[pmid] = {
                            "title": article.get("title", ""),
                            "authors": [a.get("name", "") for a in article.get("authors", [])],
                            "journal": article.get("source", ""),
                            "pubdate": article.get("pubdate", ""),
                            "volume": article.get("volume", ""),
                            "pages": article.get("pages", ""),
                            "doi": doi,
                            "valid": True,
                        }
                    else:
                        results[pmid] = {"valid": False, "error": article["error"]}
                else:
                    results[pmid] = {"valid": False, "error": "PMID not found in API response"}
        except Exception as e:
            for pmid in batch:
                results[pmid] = {"valid": False, "error": str(e)}
        time.sleep(0.4)  # Respect rate limit
    return results


def fetch_doi_metadata(doi: str) -> dict:
    """Fetch metadata from Crossref API by DOI. Returns dict with title/authors/journal/year."""
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}"
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
        return {
            "valid": True,
            "title": msg.get("title", [""])[0] if msg.get("title") else "",
            "authors": authors,
            "journal": msg.get("container-title", [""])[0] if msg.get("container-title") else "",
            "pubdate": year,
            "doi": doi,
            "source": "crossref",
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}


def search_pubmed(query: str, max_results: int = 5) -> list[dict]:
    """Search PubMed and return article summaries."""
    params = urllib.parse.urlencode({"db": "pubmed", "term": query, "retmode": "json", "retmax": max_results})
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{params}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
        ids = data["esearchresult"]["idlist"]
        if ids:
            return [{"pmid": pid, **fetch_summaries([pid]).get(pid, {})} for pid in ids]
    except Exception:
        pass
    return []


# ── Citation context parsing ──

def parse_citation_context(context: str) -> dict:
    """Parse a citation context string to extract claimed metadata.
    
    Handles common reference formats:
      Author1 A, Author2 B. Title. Journal. Year;Vol(Issue):Pages. PMID: XXXXXXXX
      Author1 A, Author2 B, et al. Title. <i>Journal</i>. Year;Vol:Pages.
      HTML variants with <br>, <sup>, etc.
    
    Returns dict with claimed_title, claimed_authors, claimed_journal, claimed_year.
    """
    claimed = {
        "claimed_title": "",
        "claimed_authors": [],
        "claimed_journal": "",
        "claimed_year": "",
    }
    if not context:
        return claimed

    text = context.strip()
    # Remove HTML tags except <i>...</i> which we need for journal detection
    journal_italic = re.findall(r'<i>([^<]+)</i>', text)
    
    # Extract year (4-digit, 19xx or 20xx)
    year_match = re.search(r'\b((?:19|20)\d{2})\b', text)
    if year_match:
        claimed["claimed_year"] = year_match.group(1)

    # Extract journal from <i>...</i> if present
    if journal_italic:
        claimed["claimed_journal"] = journal_italic[0].strip().rstrip(".")
    
    # Strategy: find PMID position, work backwards
    pmid_match = re.search(r'PMID[:\s]*(\d{4,9})', text, re.IGNORECASE)
    if not pmid_match:
        # Try to parse without PMID anchor
        _parse_freeform_citation(text, claimed)
        return claimed

    # Get text before PMID
    pre_text = text[:pmid_match.start()].strip().rstrip(".")

    # Extract authors (before first period followed by uppercase = title start)
    # Split on ". " — first segment is usually authors, second is title
    segments = re.split(r'\.\s+', pre_text)
    segments = [s.strip() for s in segments if s.strip()]

    if len(segments) >= 2:
        # First segment: authors
        author_str = segments[0]
        claimed["claimed_authors"] = _extract_author_surnames(author_str)
        
        # Second segment: title
        claimed["claimed_title"] = segments[1].strip().rstrip(".")

        # Try to find journal in remaining segments if not already found
        if not claimed["claimed_journal"] and len(segments) >= 3:
            # Journal is typically the segment after title, possibly with year/volume
            for seg in segments[2:]:
                # Skip volume/issue patterns like "2021;17(4):e90285"
                if re.match(r'^\d{4};', seg):
                    continue
                # If it looks like a journal name (words, not just numbers)
                if re.search(r'[a-zA-Z]{3,}', seg) and not re.match(r'^\d', seg):
                    if not claimed["claimed_journal"]:
                        claimed["claimed_journal"] = seg.strip().rstrip(".")
    elif len(segments) == 1:
        # Only one segment — try to split authors from title differently
        _parse_freeform_citation(pre_text, claimed)
    
    return claimed


def _extract_author_surnames(author_str: str) -> list[str]:
    """Extract surname list from author string like 'Ravelli A, Martini A, et al'"""
    surnames = []
    # Split on comma
    parts = author_str.split(",")
    for part in parts:
        part = part.strip()
        if part.lower() in ("et al", "et al.", "et"):
            continue
        # Match "Surname Initials" or just "Surname"
        m = re.match(r'^([A-ZÀ-ÿ][a-zÀ-ÿ]+)', part)
        if m:
            surnames.append(m.group(1))
    return surnames


def _parse_freeform_citation(text: str, claimed: dict) -> None:
    """Fallback parser for less structured citation text."""
    # Try to find year
    if not claimed["claimed_year"]:
        ym = re.search(r'\b((?:19|20)\d{2})\b', text)
        if ym:
            claimed["claimed_year"] = ym.group(1)
    
    # Try to find journal from <i> or known journal patterns
    if not claimed["claimed_journal"]:
        # Common journal abbreviations
        jm = re.search(
            r'(?:in\s+|published\s+in\s+)?'
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*'
            r'(?:\s+(?:Med|J|Clin|Pediatr|Rheumatol|Lancet|BMJ|Nature|Science|Blood|Ann|Arch|Int|Immunol|Allergy|Res|Rev|Dis))'
            r'(?:\s+(?:Online\s+J\.?|J\.?|Dis\.?))?)',
            text
        )
        if jm:
            claimed["claimed_journal"] = jm.group(1).strip()

    # Try to extract authors from beginning of text
    if not claimed["claimed_authors"]:
        author_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z]\.?,?\s*)+)', text)
        if author_match:
            claimed["claimed_authors"] = _extract_author_surnames(author_match.group(1))


# ── Cross-check claimed vs actual ──

def _normalize_text(s: str) -> set[str]:
    """Normalize text to a set of lowercase words for comparison."""
    s = s.lower()
    # Remove punctuation
    s = re.sub(r'[^\w\s]', ' ', s)
    words = set(s.split())
    # Remove common stop words
    stops = {"a", "an", "the", "of", "in", "on", "for", "and", "to", "with", "by",
             "from", "is", "are", "was", "were", "at", "as", "or", "its", "it",
             "this", "that", "which", "be", "has", "have", "had", "not", "but",
             "also", "into", "than", "through", "during", "between", "their", "our",
             "we", "they", "can", "may", "via", "an", "no", "all", "such"}
    return words - stops


def _clean_for_sequencematch(s: str) -> str:
    """Clean title for SequenceMatcher comparison (char-level fuzzy match)."""
    s = s.lower()
    s = re.sub(r'[^\w\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def _sequence_similarity(s1: str, s2: str) -> float:
    """Character-level similarity via SequenceMatcher. Handles '2' vs 'Two' etc."""
    return SequenceMatcher(None, _clean_for_sequencematch(s1), _clean_for_sequencematch(s2)).ratio()


def cross_check_citation(claimed: dict, actual: dict) -> dict:
    """Compare claimed citation metadata against PubMed actual metadata.
    
    Args:
        claimed: {"claimed_title": str, "claimed_authors": list, 
                  "claimed_journal": str, "claimed_year": str}
        actual: {"title": str, "authors": list, "journal": str, "pubdate": str}
    
    Returns:
        {
            "verdict": "correct" | "mismatch" | "partial" | "unknown",
            "title_match": bool,
            "author_match": bool, 
            "journal_match": bool,
            "year_match": bool,
            "confidence": float,
            "details": str,
        }
    """
    result = {
        "verdict": "unknown",
        "title_match": False,
        "author_match": False,
        "journal_match": False,
        "year_match": False,
        "confidence": 0.0,
        "details": "",
    }

    checks_run = 0

    # --- Year match ---
    actual_year = ""
    if actual.get("pubdate"):
        ym = re.search(r'((?:19|20)\d{2})', actual["pubdate"])
        if ym:
            actual_year = ym.group(1)
    
    if claimed.get("claimed_year") and actual_year:
        result["year_match"] = claimed["claimed_year"] == actual_year
        checks_run += 1

    # --- Title match (dual strategy: word overlap + SequenceMatcher) ---
    if claimed.get("claimed_title") and actual.get("title"):
        claimed_words = _normalize_text(claimed["claimed_title"])
        actual_words = _normalize_text(actual["title"])
        
        # Strategy 1: Word-level Jaccard overlap (order-independent)
        if claimed_words and actual_words:
            overlap = claimed_words & actual_words
            union = claimed_words | actual_words
            word_ratio = len(overlap) / len(union) if union else 0
        else:
            word_ratio = 0
        
        # Strategy 2: Character-level SequenceMatcher (handles "2" vs "Two", minor typos)
        seq_ratio = _sequence_similarity(claimed["claimed_title"], actual["title"])
        
        # Combined: accept if EITHER strategy passes threshold
        result["title_match"] = word_ratio >= 0.5 or seq_ratio >= 0.90
        result["_title_word_ratio"] = round(word_ratio, 3)
        result["_title_seq_ratio"] = round(seq_ratio, 3)
        checks_run += 1

    # --- Author match ---
    if claimed.get("claimed_authors") and actual.get("authors"):
        actual_surnames = []
        for a in actual["authors"][:10]:
            parts = a.split()
            if parts:
                # Take last name (surname)
                surname = parts[-1] if len(parts) == 1 else parts[0]
                actual_surnames.append(surname.lower())
        
        claimed_lower = [s.lower() for s in claimed["claimed_authors"]]
        hits = sum(1 for c in claimed_lower if any(c in a for a in actual_surnames))
        
        if len(claimed_lower) >= 2:
            result["author_match"] = hits >= 2
        else:
            result["author_match"] = hits >= 1
        checks_run += 1

    # --- Journal match ---
    if claimed.get("claimed_journal") and actual.get("journal"):
        cj = claimed["claimed_journal"].lower().strip()
        aj = actual["journal"].lower().strip()
        # Direct containment
        result["journal_match"] = cj in aj or aj in cj or cj == aj
        # Also check if significant words overlap
        if not result["journal_match"]:
            cj_words = set(cj.split()) - {"the", "of", "and", "journal", "j"}
            aj_words = set(aj.split()) - {"the", "of", "and", "journal", "j"}
            if cj_words and aj_words:
                overlap = cj_words & aj_words
                result["journal_match"] = len(overlap) / min(len(cj_words), len(aj_words)) >= 0.5
        checks_run += 1

    # --- Compute confidence ---
    match_count = sum([result["title_match"], result["author_match"], 
                       result["journal_match"], result["year_match"]])
    result["confidence"] = match_count / max(checks_run, 1)

    # --- Determine verdict ---
    details_parts = []
    
    if not claimed.get("claimed_title") and not claimed.get("claimed_authors"):
        result["verdict"] = "unknown"
        result["details"] = "Insufficient claimed metadata for cross-check"
        return result

    if result["title_match"] and (result["author_match"] or result["journal_match"]):
        result["verdict"] = "correct"
        if not result["author_match"]:
            details_parts.append("author differs slightly")
        if not result["journal_match"]:
            details_parts.append("journal name variant")
    elif result["author_match"] and result["journal_match"] and not result["title_match"]:
        result["verdict"] = "partial"
        details_parts.append("title differs but author+journal match")
    elif result["title_match"] and not result["author_match"] and not result["journal_match"]:
        result["verdict"] = "partial"
        details_parts.append("title matches but author/journal differ")
    else:
        result["verdict"] = "mismatch"
        if not result["title_match"]:
            details_parts.append("title differs")
        if not result["author_match"]:
            details_parts.append("author differs")
        if not result["journal_match"]:
            details_parts.append("journal differs")
        if not result["year_match"]:
            details_parts.append("year differs")

    result["details"] = "; ".join(details_parts) if details_parts else "all metadata matches"
    return result


# ── Suggest correct PMID ──

def suggest_correct_pmid(claimed: dict) -> list[dict]:
    """Search PubMed for the correct PMID based on claimed metadata.
    Returns top 3 candidates with pmid, title, authors."""
    parts = []
    
    if claimed.get("claimed_authors"):
        parts.append(f'{claimed["claimed_authors"][0]}[au]')
    
    if claimed.get("claimed_title"):
        # Use first 4 significant words from title
        words = [w for w in claimed["claimed_title"].split() 
                 if len(w) > 3 and w.lower() not in {"the", "and", "for", "with", "from", "that", "this"}]
        title_part = " ".join(words[:4])
        if title_part:
            parts.append(title_part)
    
    if claimed.get("claimed_journal"):
        parts.append(f'{claimed["claimed_journal"]}[jour]')
    
    if claimed.get("claimed_year"):
        parts.append(f'{claimed["claimed_year"]}[dp]')
    
    if not parts:
        return []
    
    query = " AND ".join(parts)
    return search_pubmed(query, max_results=3)


# ── PMID extraction ──

PMID_PATTERNS = [
    re.compile(r'PMID[:\s]*(\d{4,9})', re.IGNORECASE),
    re.compile(r'pubmed[:\s]*(\d{4,9})', re.IGNORECASE),
    re.compile(r'https?://pubmed\.ncbi\.nlm\.nih\.gov/(\d+)/', re.IGNORECASE),
]

def extract_pmids_from_file(filepath: str) -> list[tuple[str, str]]:
    """Extract (pmid, context_line) from a file. Returns list of (pmid, surrounding_text)."""
    results = []
    try:
        text = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return results
    for pattern in PMID_PATTERNS:
        for m in pattern.finditer(text):
            pmid = m.group(1)
            start = max(0, m.start() - 200)
            end = min(len(text), m.end() + 40)
            context = text[start:end].replace("\n", " ").strip()
            results.append((pmid, context))
    return results


def extract_pmids_from_directory(dirpath: str, extensions: tuple = (".html", ".md", ".txt", ".htm", ".json")) -> dict:
    """Scan directory for files containing PMIDs. Returns {filename: [(pmid, context)]}."""
    results = {}
    for root, dirs, files in os.walk(dirpath):
        for fname in files:
            if fname.lower().endswith(extensions):
                fpath = os.path.join(root, fname)
                found = extract_pmids_from_file(fpath)
                if found:
                    results[fpath] = found
    return results


# ── Keyword matching (auxiliary, not primary verification) ──

_MEDICAL_ABBREVS: dict[str, list[str]] = {
    "sjia": ["systemic juvenile idiopathic arthritis", "systemic jia"],
    "csle": ["childhood systemic lupus", "childhood-onset sle", "childhood lupus", "pediatric sle", "juvenile sle", "lupus nephritis"],
    "sle": ["lupus", "systemic lupus erythematosus"],
    "jia": ["juvenile idiopathic arthritis", "juvenile arthritis"],
    "jdm": ["juvenile dermatomyositis", "dermatomyositis"],
    "kd": ["kawasaki"],
    "mas": ["macrophage activation syndrome"],
    "igav": ["iga vasculitis", "henoch-schönlein", "henoch schonlein", "hsp", "purpura"],
    "aid": ["autoinflammatory", "autoinflammation", "recurrent fever"],
    "fmf": ["familial mediterranean fever"],
    "caps": ["cryopyrin-associated periodic", "cryopyrin associated"],
    "savi": ["sting-associated vasculopathy", "sting associated", "sting vasculopathy", "sting", "vascular and pulmonary"],
    "traps": ["tnf receptor-associated"],
    "nlrc4": ["nlrc4"],
    "ild": ["interstitial lung disease", "lung disease"],
    "pid": ["primary immunodeficiency", "immunodeficiency"],
    "alps": ["autoimmune lymphoproliferative", "alps"],
    "cvid": ["common variable immunodeficiency"],
    "cgd": ["chronic granulomatous disease"],
    "scid": ["severe combined immunodeficiency"],
    "xla": ["x-linked agammaglobulinemia", "bruton"],
    "itp": ["immune thrombocytopenia", "thrombocytopenic"],
    "evans": ["evans syndrome"],
    "uveitis": ["uveitis"],
    "behcet": ["behçet", "behcet"],
    "ln": ["lupus nephritis", "nephritis"],
    "aiha": ["autoimmune hemolytic", "hemolytic anemia"],
    "lahps": ["lupus anticoagulant", "hypoprothrombinemia"],
    "ivig": ["intravenous immunoglobulin", "immunoglobulin", "ivig", "igg"],
    "cal": ["coronary aneurysm", "coronary artery"],
    "gio": ["glucocorticoid-induced osteoporosis", "osteoporosis", "bone loss", "fracture"],
    "ctd": ["connective tissue disease"],
    "ar": ["autoimmune regulator", "aire", "aps-1"],
    "npsle": ["neuropsychiatric lupus", "cns lupus"],
    "apls": ["antiphospholipid", "antiphospholipid syndrome"],
    "refractory": ["refractory", "resistant"],
    "biologic": ["biologic", "biological", "biologics"],
    "failure": ["failure", "refractory", "resistant"],
    "early": ["early", "initial", "onset"],
    "incomplete": ["incomplete", "atypical"],
    "nephritis": ["nephritis", "renal", "glomerul"],
    "pulmonary": ["pulmonary", "lung", "respiratory"],
    "gi": ["gastrointestinal"],
    "double": ["double", "repeat", "second"],
    "neuro": ["neurologic", "neurological", "nervous system"],
    "shock": ["shock", "toxic shock"],
}


def keyword_match(title: str, keywords: list[str]) -> float:
    """Enhanced keyword overlap score with medical abbreviation expansion.
    NOTE: This checks topic relevance only, NOT PMID correctness.
    Returns 0.0-1.0."""
    if not title or not keywords:
        return 1.0
    title_lower = title.lower()
    hits = 0
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in title_lower:
            hits += 1
            continue
        expansions = _MEDICAL_ABBREVS.get(kw_lower, [])
        if any(exp in title_lower for exp in expansions):
            hits += 1
    return hits / len(keywords) if keywords else 1.0


def extract_keywords_from_path(filepath: str) -> list[str]:
    """Extract disease/topic keywords from filename."""
    name = Path(filepath).stem.lower()
    for prefix in ("ev_", "case_", "paper_", "ref_"):
        name = name.replace(prefix, "")
    parts = re.split(r"[_\-]", name)
    return [p for p in parts if len(p) > 2]


# ── Cache (SQLite) ──

def _cache_path() -> Path:
    """Return cache database path."""
    p = Path.home() / ".cache" / "pubmed-verifier"
    p.mkdir(parents=True, exist_ok=True)
    return p / "cache.db"


def _cache_init(db_path: Path) -> None:
    """Initialize cache database."""
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS pmid_cache (
            pmid TEXT PRIMARY KEY,
            title TEXT, authors TEXT, journal TEXT, pubdate TEXT,
            doi TEXT, valid INTEGER, error TEXT,
            cached_at REAL,
            source TEXT DEFAULT 'pubmed'
        )""")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_cached_at ON pmid_cache(cached_at)")


def _cache_load(db_path: Path, pmids: list[str], max_age_days: int = 30) -> dict:
    """Load cached results for given PMIDs. Returns {pmid: metadata_dict}."""
    results = {}
    cutoff = time.time() - max_age_days * 86400
    try:
        with sqlite3.connect(str(db_path)) as conn:
            placeholders = ",".join("?" * len(pmids))
            rows = conn.execute(
                f"SELECT pmid,title,authors,journal,pubdate,doi,valid,error,cached_at,source "
                f"FROM pmid_cache WHERE pmid IN ({placeholders}) AND cached_at > ?",
                pmids + [cutoff]
            ).fetchall()
        for row in rows:
            pmid, title, authors_json, journal, pubdate, doi, valid, error, cached_at, source = row
            if valid:
                results[pmid] = {
                    "title": title or "",
                    "authors": json.loads(authors_json) if authors_json else [],
                    "journal": journal or "",
                    "pubdate": pubdate or "",
                    "doi": doi or "",
                    "valid": True,
                    "source": source,
                }
            else:
                results[pmid] = {"valid": False, "error": error or "Unknown", "source": source}
    except Exception:
        pass
    return results


def _cache_save(db_path: Path, pmid: str, info: dict) -> None:
    """Save a single PMID result to cache."""
    try:
        with sqlite3.connect(str(db_path)) as conn:
            if info.get("valid"):
                conn.execute(
                    "INSERT OR REPLACE INTO pmid_cache (pmid,title,authors,journal,pubdate,doi,valid,error,cached_at,source) "
                    "VALUES (?,?,?,?,?,?,1,'',?,?)",
                    (pmid, info.get("title", ""), json.dumps(info.get("authors", []), ensure_ascii=False),
                     info.get("journal", ""), info.get("pubdate", ""), info.get("doi", ""),
                     time.time(), info.get("source", "pubmed"))
                )
            else:
                conn.execute(
                    "INSERT OR REPLACE INTO pmid_cache (pmid,title,authors,journal,pubdate,doi,valid,error,cached_at,source) "
                    "VALUES (?,'','','','','',0,?,?,?)",
                    (pmid, info.get("error", "Unknown"), time.time(), info.get("source", "pubmed"))
                )
    except Exception:
        pass


# ── CSV claims loader ──

def _load_csv_claims(filepath: str) -> dict:
    """Load claimed metadata from CSV file. Returns {pmid: claimed_dict}.
    
    Expected columns: pmid, title, authors, journal, year
    Authors can be semicolon-separated or pipe-separated.
    """
    claims = {}
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pmid = str(row.get("pmid", "") or row.get("PMID", "")).strip()
                if not pmid.isdigit():
                    continue
                authors_raw = row.get("authors", "") or row.get("Authors", "") or ""
                # Support semicolon, pipe, or comma separation (but comma conflicts with CSV)
                if ";" in authors_raw:
                    authors = [a.strip() for a in authors_raw.split(";") if a.strip()]
                elif "|" in authors_raw:
                    authors = [a.strip() for a in authors_raw.split("|") if a.strip()]
                else:
                    authors = [a.strip() for a in authors_raw.split(",") if a.strip()]
                claims[pmid] = {
                    "claimed_title": row.get("title", "") or row.get("Title", "") or "",
                    "claimed_authors": authors,
                    "claimed_journal": row.get("journal", "") or row.get("Journal", "") or "",
                    "claimed_year": str(row.get("year", "") or row.get("Year", "") or ""),
                }
    except Exception as e:
        print(f"Error reading CSV claims file: {e}", file=sys.stderr)
    return claims


# ── Report generation ──

def generate_json_report(results: list[dict], stats: dict) -> str:
    return json.dumps({"stats": stats, "results": results}, ensure_ascii=False, indent=2)


def generate_html_report(results: list[dict], stats: dict, source: str) -> str:
    total = stats["total"]
    correct = stats.get("correct", 0)
    mismatch = stats.get("mismatch", 0)
    invalid = stats["invalid"]
    unknown = stats.get("unknown", 0)
    partial = stats.get("partial", 0)
    unmatched = stats.get("unmatched", 0)
    pct = (correct / total * 100) if total else 0

    rows = ""
    for r in results:
        pmid = r["pmid"]
        verdict = r.get("verdict", "")
        if verdict == "correct":
            status_icon = "✅"
            row_class = "correct"
        elif verdict == "mismatch":
            status_icon = "⚠️"
            row_class = "mismatch"
        elif verdict == "partial":
            status_icon = "🔶"
            row_class = "partial"
        elif verdict == "invalid":
            status_icon = "❌"
            row_class = "invalid"
        else:
            status_icon = "❓"
            row_class = "unknown"

        claimed_title = r.get("claimed_title", "")[:80]
        actual_title = r.get("title", r.get("error", "?"))[:80]
        journal = r.get("journal", "")
        date = r.get("pubdate", "")
        source_file = r.get("source_file", "")
        details = r.get("details", "")
        suggested = r.get("suggested_pmids", [])
        suggested_str = ""
        if suggested:
            suggested_str = "<br>".join(
                f'<a href="https://pubmed.ncbi.nlm.nih.gov/{s["pmid"]}/" target="_blank">PMID {s["pmid"]}</a>: {s.get("title","")[:60]}'
                for s in suggested[:3]
            )
        match_score = r.get("match_score")
        match_cell = f'<td>{match_score:.0%}</td>' if match_score is not None else '<td>—</td>'
        
        rows += (
            f'<tr class="{row_class}">'
            f'<td>{status_icon}</td>'
            f'<td>{pmid}</td>'
            f'<td>{source_file}</td>'
            f'<td class="claimed">{claimed_title}</td>'
            f'<td>{actual_title}</td>'
            f'<td>{journal}</td>'
            f'<td>{date}</td>'
            f'<td class="details">{details}</td>'
            f'<td>{suggested_str}</td>'
            f'{match_cell}</tr>\n'
        )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PMID Verification Report</title>
<style>
body{{font-family:-apple-system,sans-serif;margin:20px auto;max-width:1400px;padding:0 16px;background:#faf8f5;color:#2d2a26;line-height:1.5;}}
h1{{color:#20a39e;}} 
.stats{{display:flex;gap:14px;margin:16px 0;flex-wrap:wrap;}}
.stat{{background:#fff;border-radius:8px;padding:12px 20px;border:1px solid #e5e0d8;text-align:center;min-width:80px;}}
.stat .num{{font-size:1.8rem;font-weight:700;}} .stat .label{{font-size:.75rem;color:#6b6560;}}
table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:.78rem;}}
th{{background:#20a39e;color:#fff;padding:8px;text-align:left;position:sticky;top:0;}}
td{{padding:7px 8px;border-bottom:1px solid #e5e0d8;vertical-align:top;}}
tr:nth-child(even){{background:#fafafa;}}
tr.mismatch{{background:#fff8e1;}}
tr.invalid{{background:#ffebee;}}
.claimed{{color:#6b6560;font-style:italic;}}
.details{{font-size:.72rem;color:#8a8580;}}
.footer{{text-align:center;padding:16px;color:#9e9893;font-size:.75rem;border-top:1px solid #e5e0d8;margin-top:20px;}}
.legend{{margin:10px 0;font-size:.82rem;color:#6b6560;}}
</style></head><body>
<h1>📋 PMID Citation Verification Report</h1>
<p>Source: <code>{source}</code></p>
<div class="stats">
<div class="stat"><div class="num">{total}</div><div class="label">Total</div></div>
<div class="stat"><div class="num" style="color:#4a9e3f">{correct}</div><div class="label">Correct</div></div>
<div class="stat"><div class="num" style="color:#e6a817">{mismatch}</div><div class="label">Mismatch</div></div>
<div class="stat"><div class="num" style="color:#d05040">{invalid}</div><div class="label">Invalid</div></div>
<div class="stat"><div class="num" style="color:#888">{unknown}</div><div class="label">Unknown</div></div>
<div class="stat"><div class="num" style="color:#e08a30">{partial}</div><div class="label">Partial</div></div>
{f'<div class="stat"><div class="num" style="color:#8a8580">{unmatched}</div><div class="label">Low Match</div></div>' if unmatched else ''}
<div class="stat"><div class="num">{pct:.1f}%</div><div class="label">Correct Rate</div></div>
</div>
<div class="legend">
✅ Correct: PMID exists & matches claimed paper &nbsp;|&nbsp;
⚠️ Mismatch: PMID exists but points to a different paper &nbsp;|&nbsp;
❌ Invalid: PMID not found &nbsp;|&nbsp;
🔶 Partial: Some metadata matches &nbsp;|&nbsp;
❓ Unknown: Insufficient metadata for cross-check
</div>
<table><tr>
<th></th><th>PMID</th><th>Source</th><th>Claimed Title</th><th>Actual Title</th>
<th>Journal</th><th>Date</th><th>Details</th><th>Suggested</th>{"<th>Relevance</th>" if unmatched else ""}
</tr>
{rows}</table>
<div class="footer">Generated by pubmed-verifier skill (v2.1) · {time.strftime("%Y-%m-%d %H:%M")}</div>
</body></html>"""


# ── Main ──

def main():
    parser = argparse.ArgumentParser(description="PMID Citation Verifier v2.1 — Three-state verification with caching, CSV, and DOI support")
    parser.add_argument("--source", help="File or directory to scan for PMIDs")
    parser.add_argument("--pmids", help="Comma-separated PMIDs to verify directly")
    parser.add_argument("--claims", help="JSON string with claimed metadata: [{pmid,title,authors,journal,year},...]")
    parser.add_argument("--claims-file", help="JSON or CSV file with claimed metadata")
    parser.add_argument("--verify-doi", action="store_true", help="Also verify DOIs via Crossref when available")
    parser.add_argument("--match-keywords", action="store_true", 
                        help="Check topic relevance via keyword matching (auxiliary, not PMID correctness)")
    parser.add_argument("--threshold", type=float, default=0.2, help="Keyword match threshold (default: 0.2)")
    parser.add_argument("--suggest", action="store_true", help="Auto-suggest correct PMIDs for mismatches (slower, uses extra API calls)")
    parser.add_argument("--no-cache", action="store_true", help="Disable cache, always query API")
    parser.add_argument("--cache-days", type=int, default=30, help="Cache validity in days (default: 30)")
    parser.add_argument("--output", help="Output file (.json or .html)")
    parser.add_argument("--format", choices=["json", "html", "text"], default="text", help="Output format")
    args = parser.parse_args()

    # Collect PMIDs with optional claimed metadata
    pmid_entries = []  # list of (pmid, source_file, context, claimed_dict)
    explicit_claims = {}

    # Load explicit claims from --claims or --claims-file
    if args.claims_file:
        filepath = args.claims_file
        if filepath.lower().endswith(".csv"):
            explicit_claims = _load_csv_claims(filepath)
            if not explicit_claims:
                print(f"No valid PMIDs found in CSV file: {filepath}", file=sys.stderr)
                sys.exit(1)
        else:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    claims_data = json.load(f)
                for item in claims_data:
                    pmid = str(item.get("pmid", "")).strip()
                    if pmid.isdigit():
                        explicit_claims[pmid] = {
                            "claimed_title": item.get("title", ""),
                            "claimed_authors": item.get("authors", []) if isinstance(item.get("authors"), list) else [],
                            "claimed_journal": item.get("journal", ""),
                            "claimed_year": str(item.get("year", "")),
                        }
            except Exception as e:
                print(f"Error reading claims file: {e}", file=sys.stderr)
                sys.exit(1)
    elif args.claims:
        try:
            claims_data = json.loads(args.claims)
            for item in claims_data:
                pmid = str(item.get("pmid", "")).strip()
                if pmid.isdigit():
                    explicit_claims[pmid] = {
                        "claimed_title": item.get("title", ""),
                        "claimed_authors": item.get("authors", []) if isinstance(item.get("authors"), list) else [],
                        "claimed_journal": item.get("journal", ""),
                        "claimed_year": str(item.get("year", "")),
                    }
        except json.JSONDecodeError as e:
            print(f"Error parsing --claims JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # Collect PMIDs from sources
    if args.pmids:
        for p in args.pmids.split(","):
            p = p.strip()
            if p.isdigit():
                claimed = explicit_claims.get(p, {})
                pmid_entries.append((p, "cli", "", claimed))
    elif args.source:
        source = args.source
        if os.path.isfile(source):
            found = extract_pmids_from_file(source)
            for pmid, ctx in found:
                claimed = explicit_claims.get(pmid, parse_citation_context(ctx))
                pmid_entries.append((pmid, source, ctx, claimed))
        elif os.path.isdir(source):
            file_map = extract_pmids_from_directory(source)
            for fpath, items in file_map.items():
                for pmid, ctx in items:
                    claimed = explicit_claims.get(pmid, parse_citation_context(ctx))
                    pmid_entries.append((pmid, fpath, ctx, claimed))
        else:
            print(f"Error: {source} not found", file=sys.stderr)
            sys.exit(1)
    elif explicit_claims:
        # Only --claims provided, no --source or --pmids
        for pmid, claimed in explicit_claims.items():
            pmid_entries.append((pmid, "claims", "", claimed))
    else:
        parser.print_help()
        sys.exit(1)

    if not pmid_entries:
        print("No PMIDs found.")
        sys.exit(0)

    # Deduplicate, preserving all source contexts and claims
    seen = {}
    for pmid, src, ctx, claimed in pmid_entries:
        if pmid not in seen:
            seen[pmid] = []
        seen[pmid].append((src, ctx, claimed))

    unique_pmids = list(seen.keys())
    print(f"Found {len(pmid_entries)} PMID citations ({len(unique_pmids)} unique). Verifying...")

    # Initialize cache
    use_cache = not args.no_cache
    db_path = _cache_path()
    if use_cache:
        _cache_init(db_path)
        cached = _cache_load(db_path, unique_pmids, max_age_days=args.cache_days)
        uncached_pmids = [p for p in unique_pmids if p not in cached]
        if cached:
            print(f"Cache: {len(cached)} cached, {len(uncached_pmids)} to query")
    else:
        cached = {}
        uncached_pmids = unique_pmids

    # Query PubMed API for uncached PMIDs
    if uncached_pmids:
        fresh = fetch_summaries(uncached_pmids)
        # Save to cache
        if use_cache:
            for pmid, info in fresh.items():
                _cache_save(db_path, pmid, info)
    else:
        fresh = {}

    # Merge cached + fresh
    summaries = {}
    for pmid in unique_pmids:
        summaries[pmid] = cached.get(pmid) or fresh.get(pmid, {"valid": False, "error": "No API response"})

    # Build results with three-state verdict
    results = []
    stats = {"total": len(pmid_entries), "correct": 0, "mismatch": 0, "partial": 0, 
             "invalid": 0, "unknown": 0, "unmatched": 0}

    for pmid in unique_pmids:
        info = summaries.get(pmid, {"valid": False, "error": "No API response"})
        for src, ctx, claimed in seen[pmid]:
            entry = {
                "pmid": pmid, 
                "source_file": os.path.basename(src), 
                "context": ctx[:200],
                "claimed_title": claimed.get("claimed_title", ""),
            }

            if info.get("valid"):
                entry["valid"] = True
                entry["title"] = info["title"]
                entry["journal"] = info["journal"]
                entry["pubdate"] = info["pubdate"]
                entry["authors"] = ", ".join(info["authors"][:3])
                entry["doi"] = info.get("doi", "")

                # DOI cross-verification (optional, via Crossref)
                if args.verify_doi and info.get("doi"):
                    doi_meta = fetch_doi_metadata(info["doi"])
                    if doi_meta.get("valid"):
                        entry["doi_verified"] = True
                        entry["crossref_title"] = doi_meta.get("title", "")
                    else:
                        entry["doi_verified"] = False

                # Cross-check claimed vs actual
                cross = cross_check_citation(claimed, {
                    "title": info["title"],
                    "authors": info["authors"],
                    "journal": info["journal"],
                    "pubdate": info["pubdate"],
                })
                entry["verdict"] = cross["verdict"]
                entry["details"] = cross["details"]
                entry["confidence"] = round(cross["confidence"], 2)
                entry["title_match"] = cross["title_match"]
                entry["author_match"] = cross["author_match"]
                entry["journal_match"] = cross["journal_match"]
                entry["year_match"] = cross["year_match"]

                stats[cross["verdict"]] = stats.get(cross["verdict"], 0) + 1

                # Auto-suggest correct PMID for mismatches
                if cross["verdict"] == "mismatch" and args.suggest:
                    suggested = suggest_correct_pmid(claimed)
                    if suggested:
                        entry["suggested_pmids"] = [
                            {"pmid": s["pmid"], "title": s.get("title", "")[:80]}
                            for s in suggested if s.get("valid")
                        ]

                # Keyword matching (auxiliary)
                if args.match_keywords:
                    keywords = extract_keywords_from_path(src)
                    score = keyword_match(info["title"], keywords)
                    entry["match_score"] = score
                    if score < args.threshold:
                        stats["unmatched"] += 1
            else:
                entry["valid"] = False
                entry["verdict"] = "invalid"
                entry["error"] = info.get("error", "Unknown")
                entry["details"] = f"PMID not found: {entry['error']}"
                stats["invalid"] += 1

            results.append(entry)

    # Output
    if args.output:
        ext = Path(args.output).suffix.lower()
        if ext == ".json" or args.format == "json":
            output_text = generate_json_report(results, stats)
        else:
            output_text = generate_html_report(results, stats, args.source or args.pmids or "claims")
        Path(args.output).write_text(output_text, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        # Text output
        correct = stats.get("correct", 0)
        mismatch = stats.get("mismatch", 0)
        partial = stats.get("partial", 0)
        unknown = stats.get("unknown", 0)
        print(f"\n{'='*60}")
        print(f"Results: {correct}/{stats['total']} correct, {mismatch} mismatch, "
              f"{stats['invalid']} invalid, {partial} partial, {unknown} unknown")
        if stats.get("unmatched"):
            print(f"Relevance warnings: {stats['unmatched']}")
        print(f"{'='*60}\n")

        for r in results:
            verdict = r.get("verdict", "")
            if verdict == "correct":
                icon = "✅"
            elif verdict == "mismatch":
                icon = "⚠️"
            elif verdict == "partial":
                icon = "🔶"
            elif verdict == "invalid":
                icon = "❌"
            else:
                icon = "❓"
            
            line = f"{icon} PMID {r['pmid']} ({r['source_file']}) [{verdict}]"
            if r.get("valid"):
                line += f"\n   Actual: {r.get('title', '')[:90]}"
                if r.get("claimed_title"):
                    line += f"\n   Claimed: {r['claimed_title'][:90]}"
                if r.get("details"):
                    line += f"\n   Details: {r['details']}"
                if r.get("suggested_pmids"):
                    for s in r["suggested_pmids"][:2]:
                        line += f"\n   → Suggest: PMID {s['pmid']} - {s['title']}"
                if r.get("match_score") is not None and r["match_score"] < args.threshold:
                    line += f" [ relevance={r['match_score']:.0%} ]"
            else:
                line += f"\n   Error: {r.get('error', '?')}"
            print(line)

    # Exit code: non-zero if any invalid or mismatch found
    sys.exit(1 if stats["invalid"] > 0 or stats.get("mismatch", 0) > 0 else 0)


if __name__ == "__main__":
    main()
