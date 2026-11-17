"""Offline evidence packaging and checks. Semantic judgments belong to the host.

No keywords, sentiment models, network requests, or implied market estimates.
Public functions accept JSON-compatible values and never modify their inputs.
"""

from __future__ import annotations

import copy
import hashlib
import html
import math
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import PurePosixPath
from urllib.parse import quote, urlsplit


QUESTIONS = [
    ("Q01", "What are people discussing?"),
    ("Q02", "Which tools do they use, compare, or abandon?"),
    ("Q03", "What specific problems do they describe?"),
    ("Q04", "Which problems recur and have concrete consequences?"),
    ("Q05", "What questions do people repeatedly ask?"),
    ("Q06", "What do they explicitly wish a product could do?"),
    ("Q07", "Who has the need, for which project, budget, and stage?"),
    ("Q08", "How do they work around it, and what does that cost?"),
    ("Q09", "What distinguishes interest, willingness to pay, and actual payment?"),
    ("Q10", "When is the problem minor, already solved, or not worth paying for?"),
    ("Q11", "Which open, self-hosted, or customizable alternatives matter?"),
    ("Q12", "Who builds their own tools, and what happened in practice?"),
    ("Q13", "What do users criticize about competitors and substitutes?"),
    ("Q14", "What do users praise about competitors and substitutes?"),
]
INTERPRETATIONS = {
    "reported_behavior", "wish", "suggestion", "question", "reported_outcome",
    "reported_payment", "praise", "complaint", "secondhand", "promotion", "unknown",
}
STATUSES = {"accepted", "hypothesis", "rejected", "needs_context", "inconclusive"}
DISPOSITIONS = {"include", "defer", "reject", "needs_evidence"}


def _date(value):
    if not value:
        return None
    try:
        result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return result.replace(tzinfo=timezone.utc) if result.tzinfo is None else result
    except (ValueError, TypeError):
        return None


def _temporal(record, window):
    date = _date(record.get("published_at"))
    if date is None:
        return "unknown_date"
    start, end = _date(window.get("start")), _date(window.get("end"))
    if (start and date < start) or (end and date >= end):
        return "outside_window"
    return "in_window"


def _index(records):
    """Keep one evidence identity; do not merge similar text or author handles."""
    indexed = {}
    for record in records:
        eid = record.get("evidence_id")
        if not isinstance(eid, str) or not eid:
            raise ValueError("Every record needs a nonempty evidence_id")
        current = indexed.get(eid)
        if current is not None:
            for field in ("platform", "native_id", "author_id", "conversation_id", "text"):
                if current.get(field) != record.get(field):
                    raise ValueError(f"Conflicting duplicate evidence identity: {eid} ({field})")
            merged = copy.deepcopy(record)
            merged["raw"] = copy.deepcopy(current.get("raw", []))
            for ref in record.get("raw", []):
                if ref not in merged["raw"]:
                    merged["raw"].append(copy.deepcopy(ref))
            indexed[eid] = merged
        else:
            indexed[eid] = copy.deepcopy(record)
    return indexed


def _author(record):
    value = record.get("author_id")
    return (record.get("platform"), str(value)) if value not in (None, "") else None


def _references(record):
    """Explicit parent/quote/reshare identities supplied by collectors."""
    ids = []
    if record.get("parent_id"):
        ids.append(str(record["parent_id"]))
    metadata = record.get("metadata") or {}
    for ref in metadata.get("referenced_tweets", []):
        if isinstance(ref, dict) and ref.get("id"):
            ids.append(str(ref["id"]))
    ids.extend(str(eid) for eid in metadata.get("missing_context_ids", []))
    return [(record.get("platform"), eid) for eid in dict.fromkeys(ids)]


def _context_details(subject, native):
    found, missing, cycles, conflicts = {}, set(), set(), set()
    pending = [(subject, frozenset({subject["evidence_id"]}))]
    expanded = set()
    while pending:
        cursor, ancestors = pending.pop()
        if cursor["evidence_id"] in expanded:
            continue
        expanded.add(cursor["evidence_id"])
        for key in _references(cursor):
            parent = native.get(key)
            if parent is None:
                missing.add(f"{key[0]}:{key[1]}")
            elif parent["evidence_id"] in ancestors:
                cycles.add(parent["evidence_id"])
            else:
                if str(cursor.get("parent_id")) == key[1] and parent.get("conversation_id") != cursor.get("conversation_id"):
                    conflicts.add(cursor["evidence_id"])
                found[parent["evidence_id"]] = parent
                pending.append((parent, ancestors | {parent["evidence_id"]}))
    return found, missing, cycles, conflicts


def _statistics(records):
    rows = list(records)
    return {
        "evidence_records": len(rows),
        "context_only_records": sum(bool((r.get("metadata") or {}).get("context_only")) for r in rows),
        "known_authors": len({_author(r) for r in rows if _author(r) is not None}),
        "unknown_author_records": sum(_author(r) is None for r in rows),
        "conversations": len({(r.get("platform"), r.get("conversation_id"))
                              for r in rows if r.get("conversation_id")}),
        "platforms": sorted({str(r.get("platform", "unknown")) for r in rows}),
    }


def _questions(config):
    custom = config.get("questions") or {}
    if isinstance(custom, list):
        custom = {entry["id"]: entry.get("question", entry.get("text", ""))
                  for entry in custom if isinstance(entry, dict) and "id" in entry}
    if not isinstance(custom, dict):
        raise ValueError("questions must be an object or a list of id/question objects")
    return [{"id": qid, "question": custom.get(qid) or question} for qid, question in QUESTIONS]


def _coverage(config, records, reviewed=None):
    supplied = config.get("coverage") or []
    if isinstance(supplied, dict):
        supplied = [{"platform": key, **(value if isinstance(value, dict) else {"status": value})}
                    for key, value in supplied.items()]
    result = []
    platforms = {r.get("platform", "unknown") for r in records}
    platforms.update(j.get("platform", "unknown") for j in config.get("sources", []))
    platforms.update(j.get("platform", "unknown") for j in supplied)
    for platform in sorted(platforms):
        rows = [r for r in records if r.get("platform") == platform]
        jobs = [copy.deepcopy(j) for j in supplied if j.get("platform") == platform]
        result.append({
            "platform": platform, "sample_records": len(rows),
            "context_only_records": sum(bool((r.get("metadata") or {}).get("context_only")) for r in rows),
            "known_authors": _statistics(rows)["known_authors"],
            "reviewed_records": (sum(r["evidence_id"] in reviewed for r in rows)
                                 if reviewed is not None else None),
            "collection_status": "reported_per_job" if jobs else "unknown",
            "jobs": jobs,
        })
    return result


def build_packets(records, config):
    """Return full-text, bounded discussion packets and an unfilled findings template.

    Limits split packets, never truncate a record. Ancestors may repeat as context.
    Explicit analysis.evidence_ids select subjects; absent selection includes all
    dated records in the requested window (undated records only if unbounded).
    Packaging is not evidence of a human or model having read the records.
    """
    indexed = _index(records)
    rows = list(indexed.values())
    window = config.get("window") or {}
    for boundary in ("start", "end"):
        if window.get(boundary) and _date(window[boundary]) is None:
            raise ValueError(f"Invalid window.{boundary}")
    if window.get("start") and window.get("end") and _date(window["start"]) >= _date(window["end"]):
        raise ValueError("window.start must precede window.end")
    settings = config.get("analysis") or {}
    max_records = settings.get("max_packet_records", 80)
    max_chars = settings.get("max_packet_chars", 24000)
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 1 for v in (max_records, max_chars)):
        raise ValueError("Packet limits must be positive integers")
    selected = settings.get("evidence_ids")
    if selected is not None:
        if not isinstance(selected, list) or any(eid not in indexed for eid in selected):
            raise ValueError("analysis.evidence_ids must contain existing evidence IDs")
        subjects = set(selected)
        selection = "explicit evidence IDs supplied by host"
    else:
        bounded = bool(window.get("start") or window.get("end"))
        subjects = {r["evidence_id"] for r in rows if not (r.get("metadata") or {}).get("context_only")
                    and (_temporal(r, window) == "in_window"
                         or (not bounded and _temporal(r, window) == "unknown_date"))}
        selection = "all available records in scope; no semantic filtering"
    native = {(r.get("platform"), str(r.get("native_id"))): r for r in rows}
    groups = defaultdict(list)
    for record in rows:
        if record["evidence_id"] in subjects:
            groups[(str(record.get("platform")), str(record.get("conversation_id") or record["evidence_id"]))].append(record)
    packets = []
    for (platform, conversation), group in sorted(groups.items()):
        group.sort(key=lambda r: (r.get("published_at") or "", r["evidence_id"]))
        chunks, chunk, chars = [], [], 0
        for record in group:
            size = len(record.get("text") or "")
            if chunk and (len(chunk) >= max_records or chars + size > max_chars):
                chunks.append(chunk)
                chunk, chars = [], 0
            chunk.append(record)
            chars += size
        if chunk:
            chunks.append(chunk)
        for chunk in chunks:
            included = {r["evidence_id"]: r for r in chunk}
            missing, cycles, conflicts = set(), set(), set()
            for subject in chunk:
                related, absent, looped, mismatched = _context_details(subject, native)
                included.update(related)
                missing.update(absent)
                cycles.update(looped)
                conflicts.update(mismatched)
            subject_ids = [r["evidence_id"] for r in chunk]
            packet_records = []
            for record in sorted(included.values(), key=lambda r: (r.get("published_at") or "", r["evidence_id"])):
                item = copy.deepcopy(record)
                item["packet_role"] = "subject" if item["evidence_id"] in subject_ids else "context"
                item["temporal_scope"] = _temporal(item, window)
                packet_records.append(item)
            digest = hashlib.sha256("\n".join(subject_ids).encode()).hexdigest()[:16]
            packets.append({
                "packet_id": f"packet-{digest}", "platform": platform,
                "conversation_id": conversation, "subject_ids": subject_ids,
                "records": packet_records, "missing_context": sorted(missing),
                "context_cycles": sorted(cycles),
                "context_identity_conflicts": sorted(conflicts),
                "oversized": len(packet_records) > max_records or sum(len(r.get("text") or "") for r in packet_records) > max_chars,
                "read_status": "unreviewed",
            })
    return {
        "schema_version": "1.0", "project": config.get("project"),
        "scope": {"domain": config.get("domain"), "window": copy.deepcopy(window),
                  "selection": selection, "selected_records": len(subjects),
                  "not_selected_records": len(rows) - len(subjects)},
        "sample": _statistics(rows), "coverage": _coverage(config, rows),
        "questions": _questions(config), "packets": packets,
        "findings_template": {"schema_version": "1.0", "findings": [],
                              "reviewed_evidence_ids": [], "question_answers": {}, "key_findings": []},
    }


def _finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _one_of(value, options):
    return isinstance(value, str) and value in options


def _score(card, where, errors, indexed):
    if card is None:
        return {"value": None, "known_weight": 0, "total_weight": None}
    if not isinstance(card, dict) or not isinstance(card.get("dimensions"), list) or not card["dimensions"]:
        errors.append(f"{where}: scorecard needs a nonempty dimensions list")
        return {"value": None, "known_weight": 0, "total_weight": None}
    total_weight = known_weight = weighted = 0.0
    names = set()
    for dimension in card["dimensions"]:
        if not isinstance(dimension, dict):
            errors.append(f"{where}: invalid score dimension")
            continue
        name, value, weight = dimension.get("name"), dimension.get("value"), dimension.get("weight", 1)
        if not isinstance(name, str) or not name or name in names:
            errors.append(f"{where}: score dimensions need unique names")
        names.add(name if isinstance(name, str) else "")
        if not _finite_number(weight) or weight <= 0:
            errors.append(f"{where}: score weights must be finite and positive")
            continue
        total_weight += weight
        evidence_ids = dimension.get("evidence_ids", [])
        if not isinstance(evidence_ids, list):
            errors.append(f"{where}: score evidence_ids must be a list")
            evidence_ids = []
        for eid in evidence_ids:
            if not isinstance(eid, str) or eid not in indexed:
                errors.append(f"{where}: score references missing or uncited evidence {eid}")
        if value is None:
            continue
        if not _finite_number(value) or not 0 <= value <= 5:
            errors.append(f"{where}: score values must be null or a finite number from 0 to 5")
            continue
        if not dimension.get("rationale") or not evidence_ids:
            errors.append(f"{where}: known score needs rationale and evidence_ids")
        known_weight += weight
        weighted += value * weight
    value = round(weighted / total_weight, 6) if total_weight and known_weight == total_weight else None
    if "total" in card:
        given = card["total"]
        if (value is None and given is not None) or (value is not None and (not _finite_number(given) or not math.isclose(given, value, abs_tol=1e-6))):
            errors.append(f"{where}: score total disagrees with weighted values or converts unknown to zero")
    return {"value": value, "known_weight": known_weight, "total_weight": total_weight}


def validate_findings(findings, records):
    """Check identities, exact snippets and arithmetic; never certify meaning.

    Returns {valid, errors, warnings, statistics, finding_statistics}. A passing
    result is structural validation, not independent semantic review.
    """
    errors, warnings = [], []
    try:
        indexed = _index(records)
    except (ValueError, AttributeError, TypeError) as exc:
        return {"valid": False, "errors": [str(exc)], "warnings": [], "statistics": {}, "finding_statistics": {}}
    if isinstance(findings, list):
        findings = {"findings": findings}
    if not isinstance(findings, dict) or not isinstance(findings.get("findings"), list):
        return {"valid": False, "errors": ["findings must be an object with a findings list"], "warnings": [], "statistics": {}, "finding_statistics": {}}
    rows = list(indexed.values())
    native = {(r.get("platform"), str(r.get("native_id"))): r for r in rows}
    for eid, record in indexed.items():
        if eid != f"{record.get('platform')}:{record.get('native_id')}":
            errors.append(f"{eid}: evidence identity differs from platform:native_id")
    reviewed = findings.get("reviewed_evidence_ids")
    if reviewed is not None:
        if not isinstance(reviewed, list) or any(not isinstance(eid, str) or eid not in indexed for eid in reviewed):
            errors.append("reviewed_evidence_ids must contain existing evidence IDs")
            reviewed = []
        reviewed = set(reviewed)
    else:
        warnings.append("Actual reading coverage is unknown; collected records are not reviewed records")
    stats = _statistics(rows)
    stats["reviewed_records"] = len(reviewed) if reviewed is not None else None
    stats["reading_coverage_basis"] = "host_declared" if reviewed is not None else "unknown"
    finding_stats, ids = {}, set()

    def citation(cite, where, expected_role=None):
        if not isinstance(cite, dict):
            errors.append(f"{where}: citation must be an object")
            return None
        eid, snippet = cite.get("evidence_id"), cite.get("quote")
        if not isinstance(eid, str) or eid not in indexed:
            errors.append(f"{where}: unknown evidence_id {eid}")
            return None
        record = indexed[eid]
        if not isinstance(snippet, str) or not snippet.strip() or snippet not in (record.get("text") or ""):
            errors.append(f"{where}: quote is not a nonempty verbatim snippet of {eid}")
        for field in ("platform", "native_id", "author_id", "url", "conversation_id", "parent_id"):
            if field in cite and cite[field] != record.get(field):
                errors.append(f"{where}: citation {field} does not match {eid}")
        if not _one_of(cite.get("role", expected_role or "support"), {"support", "counter", "context"}):
            errors.append(f"{where}: invalid citation role")
        if expected_role and cite.get("role", expected_role) != expected_role:
            errors.append(f"{where}: citation role must be {expected_role}")
        if not _one_of(cite.get("interpretation"), INTERPRETATIONS):
            errors.append(f"{where}: interpretation must distinguish wishes, suggestions, behavior and payment")
        if reviewed is not None and eid not in reviewed:
            errors.append(f"{where}: cited evidence is absent from reviewed_evidence_ids")
        if not record.get("raw"):
            warnings.append(f"{eid}: no raw provenance reference; snippet match alone does not verify origin")
        else:
            for ref in record["raw"]:
                if not isinstance(ref, dict):
                    errors.append(f"{eid}: malformed raw provenance")
                    continue
                path = ref.get("path", "")
                if not isinstance(path, str) or not path or PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts or "\\" in path or re.match(r"^[a-zA-Z]:", path):
                    errors.append(f"{eid}: raw path must remain relative to the run directory")
                if not isinstance(ref.get("sha256"), str) or not re.fullmatch(r"[0-9a-fA-F]{64}", ref["sha256"]):
                    errors.append(f"{eid}: malformed raw sha256")
                if not isinstance(ref.get("locator"), str) or not ref["locator"].startswith("$"):
                    errors.append(f"{eid}: raw locator must identify a response location")
        return record

    for index, finding in enumerate(findings["findings"]):
        if not isinstance(finding, dict):
            errors.append(f"finding {index}: expected an object")
            continue
        fid = finding.get("id")
        where = str(fid or f"finding {index}")
        if not isinstance(fid, str) or not fid or fid in ids:
            errors.append(f"{where}: finding IDs must be nonempty and unique")
        if isinstance(fid, str):
            ids.add(fid)
        if not finding.get("title") or not finding.get("claim"):
            errors.append(f"{where}: title and claim are required")
        if not _one_of(finding.get("status"), STATUSES):
            errors.append(f"{where}: invalid or missing finding status")
        if not _one_of(finding.get("disposition"), DISPOSITIONS):
            errors.append(f"{where}: key finding needs an explicit disposition")
        if finding.get("disposition") != "include" and not finding.get("disposition_reason"):
            errors.append(f"{where}: deferred or excluded findings need a disposition_reason")
        support, counter, cited = {}, {}, {}
        for field, role in (("evidence", None), ("counterevidence", "counter")):
            citations = finding.get(field, [])
            if not isinstance(citations, list):
                errors.append(f"{where}: {field} must be a list")
                continue
            for cite in citations:
                record = citation(cite, where, role)
                if record:
                    cited[record["evidence_id"]] = record
                    target = counter if cite.get("role", role or "support") == "counter" else support
                    if cite.get("role", role or "support") != "context":
                        target[record["evidence_id"]] = record
        if _one_of(finding.get("status"), {"accepted", "hypothesis"}) and not support:
            errors.append(f"{where}: accepted findings and hypotheses need supporting evidence")
        if not counter and not finding.get("counterevidence_search"):
            warnings.append(f"{where}: counterevidence search is not documented")
        missing = []
        for record in cited.values():
            related, absent, cycles, conflicts = _context_details(record, native)
            missing.extend(absent)
            if conflicts:
                errors.append(f"{where}: parent and reply have conflicting conversation identities")
            if cycles:
                errors.append(f"{where}: cited discussion contains a context-reference cycle")
            for parent in related.values():
                if reviewed is not None and parent["evidence_id"] not in reviewed:
                    warnings.append(f"{where}: context {parent['evidence_id']} is available but not declared reviewed")
        if missing:
            if finding.get("context_review") == "complete":
                errors.append(f"{where}: context declared complete but parents are missing")
            if not finding.get("context_limitations"):
                errors.append(f"{where}: missing parent context must be recorded in context_limitations")
        if finding.get("status") == "accepted" and finding.get("review_status") != "reviewed":
            errors.append(f"{where}: accepted finding needs host-declared review_status=reviewed")
        computed = _statistics(support.values())
        computed["counterevidence_records"] = len(counter)
        computed["missing_context"] = sorted(set(missing))
        computed["score"] = _score(finding.get("scorecard"), where, errors, cited)
        claimed_counts = finding.get("counts", {})
        if not isinstance(claimed_counts, dict):
            errors.append(f"{where}: counts must be an object")
        else:
            for key, value in claimed_counts.items():
                if key not in computed or value != computed[key] or isinstance(value, bool):
                    errors.append(f"{where}: count assertion {key} differs from unique cited evidence")
        quantities = finding.get("quantities", [])
        if not isinstance(quantities, list):
            errors.append(f"{where}: quantities must be a list")
            quantities = []
        for quantity in quantities:
            if not isinstance(quantity, dict):
                errors.append(f"{where}: quantities must be objects")
                continue
            citation(quantity, where)
            kind = quantity.get("kind")
            if kind == "personal_share":
                if quantity.get("scope") != "individual" or not quantity.get("denominator_description"):
                    errors.append(f"{where}: personal share must describe an individual's denominator")
                if not _finite_number(quantity.get("value")) or not 0 <= quantity["value"] <= 100:
                    errors.append(f"{where}: personal_share value must be between 0 and 100")
            elif kind == "sample_fraction":
                numerator, denominator = quantity.get("numerator_ids"), quantity.get("denominator_ids")
                if not isinstance(numerator, list) or not isinstance(denominator, list):
                    errors.append(f"{where}: sample_fraction needs numerator_ids and denominator_ids")
                    continue
                if (not denominator or any(not isinstance(eid, str) or eid not in indexed for eid in numerator + denominator)
                        or not set(numerator) <= set(denominator)):
                    errors.append(f"{where}: sample_fraction must use a nonempty identified sample")
                    continue
                if any((indexed[eid].get("metadata") or {}).get("context_only") for eid in denominator):
                    errors.append(f"{where}: context-only records cannot define the primary sample denominator")
                if reviewed is None or any(eid not in reviewed for eid in denominator):
                    errors.append(f"{where}: sample denominator must be declared reviewed")
                if quantity.get("scope") != "observed_sample" or not _one_of(quantity.get("unit"), {"records", "known_authors"}):
                    errors.append(f"{where}: fractions describe records or known authors in the observed sample only")
                if quantity.get("unit") == "known_authors":
                    numerator_set = {_author(indexed[eid]) for eid in numerator if _author(indexed[eid]) is not None}
                    denominator_set = {_author(indexed[eid]) for eid in denominator if _author(indexed[eid]) is not None}
                else:
                    numerator_set, denominator_set = set(numerator), set(denominator)
                percentage = 100 * len(numerator_set) / len(denominator_set) if denominator_set else None
                if percentage is None or not _finite_number(quantity.get("value")) or not math.isclose(quantity["value"], percentage, abs_tol=1e-6):
                    errors.append(f"{where}: sample_fraction value differs from its explicit denominator")
            elif not _one_of(kind, {"reported_cost", "reported_time", "reported_count"}):
                errors.append(f"{where}: unknown quantity kind")
        question_ids = finding.get("question_ids", [])
        if not isinstance(question_ids, list) or any(not isinstance(qid, str) or qid not in dict(QUESTIONS) for qid in question_ids):
            errors.append(f"{where}: question_ids must use Q01 through Q14")
        finding_stats[where] = computed
    answers = findings.get("question_answers", {})
    if not isinstance(answers, dict):
        errors.append("question_answers must be an object")
        answers = {}
    for qid, answer in answers.items():
        if qid not in dict(QUESTIONS) or not isinstance(answer, dict):
            errors.append(f"{qid}: invalid question answer")
            continue
        if not _one_of(answer.get("status"), {"answered", "partial", "unknown"}):
            errors.append(f"{qid}: question status must be answered, partial or unknown")
        linked = answer.get("finding_ids", [])
        if not isinstance(linked, list) or any(not isinstance(fid, str) or fid not in ids for fid in linked):
            errors.append(f"{qid}: question references an unknown finding")
        if _one_of(answer.get("status"), {"answered", "partial"}) and (not linked or not answer.get("answer")):
            errors.append(f"{qid}: an answer needs text and supporting finding_ids")
    key_findings = findings.get("key_findings", [])
    if not isinstance(key_findings, list):
        errors.append("key_findings must be a list")
        key_findings = []
    for key in key_findings:
        if not isinstance(key, dict) or not _one_of(key.get("disposition"), DISPOSITIONS):
            errors.append("key_findings entries need an explicit disposition")
            continue
        linked = key.get("finding_ids", [])
        if not isinstance(linked, list) or any(not isinstance(fid, str) or fid not in ids for fid in linked):
            errors.append("key_findings references an unknown finding")
        if key.get("disposition") == "include" and not linked:
            errors.append("Included key finding has no destination finding")
        if key.get("disposition") != "include" and not key.get("reason"):
            errors.append("Deferred/excluded key finding needs a reason")
    return {"valid": not errors, "errors": list(dict.fromkeys(errors)),
            "warnings": list(dict.fromkeys(warnings)), "statistics": stats,
            "finding_statistics": finding_stats,
            "semantic_review": "not_performed_by_validator"}


def _md(value):
    # Plain Markdown text is not an HTML attribute. Escaping apostrophes first
    # would create &#x27; which the later Markdown escaping breaks into literal
    # entity text; keep quotes readable while still neutralizing HTML tags.
    text = html.escape(str(value) if value is not None else "Unknown", quote=False)
    return re.sub(r"([\\`*_{}\[\]()#+.!|>~-])", r"\\\1", text)


def _source_link(record):
    url = record.get("url") or ""
    try:
        parsed = urlsplit(url)
        if parsed.scheme in {"http", "https"} and parsed.hostname and not parsed.username and not parsed.password:
            return f"[{_md(record['evidence_id'])}](<{quote(url, safe=':/?&=%#@+;,~!$')}>)"
    except (ValueError, TypeError):
        pass
    return _md(record["evidence_id"]) + " (source link unavailable)"


def render_report(findings, records, config):
    """Render only supplied judgments and verified arithmetic into Markdown."""
    check = validate_findings(findings, records)
    if not check["valid"]:
        raise ValueError("Invalid findings: " + "; ".join(check["errors"]))
    if isinstance(findings, list):
        findings = {"findings": findings}
    indexed = _index(records)
    reviewed_ids = findings.get("reviewed_evidence_ids")
    coverage_config = dict(config)
    lines = [f"# {_md(config.get('project') or 'Evidence research')}", "",
             "This report describes the observed sample. It does not estimate market prevalence.", "",
             "## Scope and coverage", "", f"Domain: {_md(config.get('domain'))}", "",
             f"Window: {_md((config.get('window') or {}).get('start'))} to {_md((config.get('window') or {}).get('end'))} (end excluded).", "",
             f"Unique records: {check['statistics']['evidence_records']}; known platform-scoped authors: {check['statistics']['known_authors']}; records with unknown author: {check['statistics']['unknown_author_records']}.", "",
             f"Declared reviewed records: {_md(check['statistics']['reviewed_records'])}. Reading coverage is supplied by the analyst, not inferred from collection.", "",
             "| Platform | Available records | Context only | Declared reviewed | Collection status |",
             "| --- | ---: | ---: | ---: | --- |"]
    coverage_gaps = []
    for entry in _coverage(coverage_config, list(indexed.values()), set(reviewed_ids) if reviewed_ids is not None else None):
        statuses = "; ".join(str(j.get("job_id", "job")) + ": " + str(j.get("status", "unknown")) for j in entry["jobs"]) or "unknown"
        lines.append(f"| {_md(entry['platform'])} | {entry['sample_records']} | {entry['context_only_records']} | {_md(entry['reviewed_records'])} | {_md(statuses)} |")
        for job in entry["jobs"]:
            for gap in job.get("gaps", []):
                coverage_gaps.extend(["", f"Coverage gap ({_md(entry['platform'])}): {_md(gap)}"])
    lines.extend(coverage_gaps)
    lines.extend(["", "## Findings", ""])
    if not findings["findings"]:
        lines.extend(["No reviewed findings have been supplied. Demand and payment remain unknown.", ""])
    for finding in findings["findings"]:
        fid = finding["id"]
        stats = check["finding_statistics"][fid]
        lines.extend([f"### {_md(fid)}: {_md(finding['title'])}", "", _md(finding["claim"]), "",
                      f"Status: {_md(finding['status'])}; disposition: {_md(finding['disposition'])}; review: {_md(finding.get('review_status'))}.", "",
                      f"Supporting records: {stats['evidence_records']}; known platform-scoped authors: {stats['known_authors']}; unknown-author records: {stats['unknown_author_records']}; counterevidence records: {stats['counterevidence_records']}.", ""])
        for field in ("segment", "task", "consequence", "workaround", "buyer", "payer", "payment_evidence", "uncertainty", "context_limitations", "counterevidence_search", "recommendation", "next_test", "disposition_reason"):
            if field in finding or field in {"segment", "task", "buyer", "payer", "uncertainty", "counterevidence_search", "next_test"}:
                lines.extend([f"{_md(field.replace('_', ' ').capitalize())}: {_md(finding.get(field))}", ""])
        lines.extend([f"Decision aid score (0–5, analyst-supplied dimensions): {_md(stats['score']['value'])}. Known weight: {_md(stats['score']['known_weight'])} / {_md(stats['score']['total_weight'])}. This is not a probability.", ""])
        if finding.get("scorecard"):
            lines.extend(["| Dimension | Value | Weight | Analyst rationale | Evidence IDs |", "| --- | ---: | ---: | --- | --- |"])
            for dimension in finding["scorecard"]["dimensions"]:
                lines.append(f"| {_md(dimension['name'])} | {_md(dimension.get('value'))} | {_md(dimension.get('weight', 1))} | {_md(dimension.get('rationale'))} | {_md(', '.join(dimension.get('evidence_ids') or []))} |")
            lines.append("")
        for cite in finding.get("evidence", []) + finding.get("counterevidence", []):
            record = indexed[cite["evidence_id"]]
            role = cite.get("role", "counter" if cite in finding.get("counterevidence", []) else "support")
            lines.extend([f"{_md(role)} / {_md(cite['interpretation'])}: {_source_link(record)}; author: {_md(record.get('author_id'))}; date: {_md(record.get('published_at'))}; scope: {_md(_temporal(record, config.get('window') or {}))}", ""])
            lines.extend("> " + _md(part) for part in cite["quote"].splitlines())
            lines.append("")
            if cite.get("note"):
                lines.extend(["Analyst interpretation: " + _md(cite["note"]), ""])
        for quantity in finding.get("quantities", []):
            lines.extend([f"Quantity: {_md(quantity.get('value'))}; kind: {_md(quantity.get('kind'))}; scope: {_md(quantity.get('scope'))}; denominator: {_md(quantity.get('denominator_description') or quantity.get('denominator_ids'))}.", ""])
            lines.extend([_source_link(indexed[quantity["evidence_id"]]), ""])
            lines.extend("> " + _md(part) for part in quantity["quote"].splitlines())
            lines.append("")
    lines.extend(["## Fourteen questions and gaps", ""])
    for question in _questions(config):
        answer = findings.get("question_answers", {}).get(question["id"], {})
        lines.extend([f"### {question['id']}: {_md(question['question'])}", "",
                      f"Status: {_md(answer.get('status', 'unknown'))}", "",
                      _md(answer.get("answer", "Not assessed; evidence is insufficient to answer.")), "",
                      "Findings: " + _md(", ".join(answer.get("finding_ids", [])) or None), "",
                      "Gap: " + _md(answer.get("gap") or answer.get("gaps") or ("Not specified" if answer else "No reviewed answer supplied")), ""])
    lines.extend(["## Key finding destinations", "", "| Finding | Destination | Reason / next test |", "| --- | --- | --- |"])
    for finding in findings["findings"]:
        lines.append(f"| {_md(finding['id'])} | {_md(finding['disposition'])} | {_md(finding.get('disposition_reason') or finding.get('next_test'))} |")
    for key in findings.get("key_findings", []):
        lines.append(f"| {_md(key.get('id') or key.get('title'))} | {_md(key['disposition'])}: {_md(', '.join(key.get('finding_ids', [])))} | {_md(key.get('reason'))} |")
    lines.extend(["", "## Validation limits", "", "Identity, exact snippets and arithmetic checked offline. Semantic entailment, claimed reading, payment truth, and source-file hashes require separate review.", ""])
    if "coverage" in findings:
        lines.extend(["Collection coverage comes from the run configuration/outcomes; any coverage supplied by the analyst in findings is ignored.", ""])
    lines.extend("- " + _md(warning) for warning in check["warnings"])
    return "\n".join(lines).rstrip() + "\n"
