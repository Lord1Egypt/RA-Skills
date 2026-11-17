"""pv_cli - the command-line entry layer (v6.4.0 split).

main() and its flag validation: argparse wiring, the orchestration pass
and the exit-code policy. Imports the (already complete) main module for
its whole API surface; `python3 verify_pmids.py` reaches here through the
thin __main__ wrapper, and vp.main() through the wrapper function."""
import sys

from verify_pmids import *  # noqa: F401,F403
from verify_pmids import (
    _cache_init, _cache_load, _cache_path, _cache_save_fresh,     _cited_sort_key, _input_guard_note, _retraction_reason_from_notice, _second_opinion_title,     _sequence_similarity, apply_retraction_cap, classify_unverified, cross_check_citation,     find_pmid_by_doi, keyword_match, run_check_net, run_claims_lint,     run_doctor, run_self_check, suggest_correct_pmid, suggest_retraction_replacements,     verify_arxiv_entry, verify_doi_entry, verify_title_entry)

def _validate_args(args) -> None:
    """Immediate flag validation with the written error contract (v5.8.0):
    hard errors print [ERROR] and exit 2 before any work starts; soft
    out-of-range values print [WARN] and proceed with the clamped value."""
    def _hard(msg):
        print(f"[ERROR] {msg}", file=sys.stderr)
        sys.exit(2)

    if args.timeout is None or args.timeout <= 0:
        _hard(f"--timeout must be a positive number of seconds (got {args.timeout!r})")
    if getattr(args, "cache_days", 30) < 0:
        _hard(f"--cache-days must be >= 0 (got {args.cache_days})")
    thr = getattr(args, "threshold", 0.2)
    if not (0.0 <= thr <= 1.0):
        _hard(f"--threshold is a 0..1 similarity cutoff (got {thr})")
    if args.workers < 1:
        _hard(f"--workers must be >= 1 (got {args.workers})")
    if args.workers > 8:
        print(f"[WARN] --workers {args.workers} exceeds the polite ceiling; clamping to 8",
              file=sys.stderr)
        args.workers = 8
    ret = getattr(args, "retries", 1)
    if ret < 0:
        _hard(f"--retries must be >= 0 (got {ret})")
    if ret > 3:
        print(f"[WARN] --retries {ret} exceeds the supported range; clamping to 3",
              file=sys.stderr)
        args.retries = 3
    me = getattr(args, "max_entries", 0)
    if me and me < 0:
        _hard(f"--max-entries must be >= 0 (0 = unlimited) (got {me})")
    # v7.0.0 (test-line P1): --title is a direct claim for ONE PMID entry
    if getattr(args, "title", None):
        if getattr(args, "claims", None) or getattr(args, "claims_file", None):
            _hard("--title is a lightweight direct claim — it cannot be combined "
                  "with --claims/--claims-file (give the metadata in one place)")
        pmids = getattr(args, "pmids", None) or ""
        if len([p for p in pmids.split(",") if p.strip()]) != 1:
            _hard("--title applies to exactly one PMID — pass one entry in --pmids "
                  "or use --claims/--claims-file for batches")
    elif getattr(args, "journal", None) or getattr(args, "year", None):
        _hard("--journal/--year are companions to --title — a claim without a title "
              "caps the verdict at partial; pass --title as well")

def main():
    parser = argparse.ArgumentParser(
        description=f"PMID Citation Verifier v{_TOOL_VERSION} -- Five-state verification of PMIDs, DOIs and arXiv IDs with retraction detection for every citation, DOI-native verification, delta audits against a baseline, audit/BibTeX/CSV export, plain-text reference list parsing, formatted reference list export (GB/T 7714 / Vancouver / APA / AMA), and dual-source network hardening")

    # v5.4.0: 38 flags read badly as one flat list — grouped by
    # task domain so --help scans top-to-bottom instead of alphabetically
    g_inputs = parser.add_argument_group('inputs — what to verify', '--source/--pmids/--dois/--arxivs scan or verify directly; --claims/--claims-file add expected metadata; --bibliography audits .bib/.ris; --parse-text/--stdin take a pasted reference list')
    g_verify = parser.add_argument_group('verification depth', '--quick bundles the pre-submission pass; --verify-doi cross-checks Crossref; --suggest proposes correct PMIDs; cache flags control freshness')
    g_output = parser.add_argument_group('output & exports', 'reports, streaming lines, the submission evidence pack, formatted reference lists and offline claims tooling')
    g_net = parser.add_argument_group('network & performance', 'registry selection, timeouts, concurrency and the large-input guard')
    g_inst = parser.add_argument_group('institutional & diagnostics', 'polite-pool identity, rate-limit key and the environment self-check')

    g_inputs.add_argument("--source", help="File or directory to scan for PMIDs")
    g_inputs.add_argument("--pmids", help="Comma-separated PMIDs to verify directly")
    g_inputs.add_argument("--claims", help="JSON string with claimed metadata: [{pmid,title,authors,journal,year},...]")
    g_inputs.add_argument("--claims-file", help="JSON or CSV file with claimed metadata")
    g_inputs.add_argument("--title", help="v7.0.0 lightweight direct claim for ONE --pmids entry "
                                          "(no claims file needed): expected title for the five-state verdict")
    g_inputs.add_argument("--journal", help="optional companion to --title: expected journal")
    g_inputs.add_argument("--year", help="optional companion to --title: expected year")
    g_verify.add_argument("--verify-doi", action="store_true",
                        help="Also verify DOIs via Crossref; flags RETRACTED papers (verdict capped at partial)")
    g_verify.add_argument("--match-keywords", action="store_true", 
                        help="Check topic relevance via keyword matching (auxiliary, not PMID correctness)")
    g_verify.add_argument("--threshold", type=float, default=0.2, help="Keyword match threshold (default: 0.2)")
    g_verify.add_argument("--suggest", action="store_true", help="Auto-suggest correct PMIDs for mismatches (slower, uses extra API calls)")
    g_verify.add_argument("--no-cache", action="store_true", help="Disable cache, always query API")
    g_verify.add_argument("--cache-days", type=int, default=30, help="Cache validity in days (default: 30)")
    g_output.add_argument("--output", help="Output file (.json or .html)")
    g_output.add_argument("--format", choices=["json", "html", "markdown", "text"], default="text", help="Output format")
    g_inst.add_argument("--ncbi-api-key", default="",
                        help="NCBI E-utilities API key (or env NCBI_API_KEY): rate limit 3->10 req/s, batch ~3x faster")
    g_inst.add_argument("--mailto", default="",
                        help="Contact email (or env PUBMED_VERIFIER_MAILTO): Crossref polite pool + NCBI etiquette")
    g_net.add_argument("--meta-source", choices=["auto", "ncbi", "europepmc"], default="auto",
                        help="Metadata source: auto = NCBI with Europe PMC fallback (default)")
    g_net.add_argument("--timeout", type=float, default=20, help="Per-request timeout seconds (default: 20)")
    g_net.add_argument("--retries", type=int, default=1, metavar="N",
                        help="Batch-end retry sweeps for fetches the network lost "
                             "(default: 1; 0 = off, max 3) — only network-failed "
                             "calls re-run, verified answers are never re-fetched")
    g_output.add_argument("--export-audit", metavar="PATH",
                        help="Write a self-contained JSON audit working-paper: tool identity, redacted invocation, per-citation evidence chain and verdict trace")
    g_output.add_argument("--export-ris", metavar="PATH",
                        help="Write verified bibliography as RIS (correct = TY JOUR, "
                             "partial = TY DATA with note; Zotero/EndNote/Mendeley)")
    g_output.add_argument("--export-csl", metavar="PATH",
                        help="Write verified bibliography as CSL JSON — imports "
                             "directly into Zotero (File > Import); "
                             "Mendeley and Pandoc read the same file")
    g_output.add_argument("--export-bibtex", metavar="PATH",
                        help="Export verified references as BibTeX (correct included; partial commented; retracted/excluded counted)")
    g_output.add_argument("--export-csv", metavar="PATH",
                        help="Export a spreadsheet-friendly audit table (key, verdict, flags, fields, details)")
    g_net.add_argument("--workers", type=int, default=4, metavar="N",
                        help="Parallel Crossref resolutions for --dois batches (default 4, max 8)")
    g_inputs.add_argument("--dois", metavar="DOI_LIST",
                        help="Comma-separated DOIs to verify natively via Crossref (existence + registered metadata; 404 = fabrication signal)")
    g_inputs.add_argument("--arxivs", metavar="ARXIV_LIST",
                        help="Comma-separated arXiv IDs to verify against the official arXiv API (nonexistent = fabrication signal)")
    g_output.add_argument("--diff", metavar="BASELINE_JSON",
                        help="Compare this run to a previous audit working-paper: newly retracted, degraded, improved, new, dropped")
    g_inputs.add_argument("--bibliography", metavar="FILE",
                        help="Verify a bibliography file (.bib BibTeX / .ris RIS): entries "
                             "route by PMID (field or note) > DOI > arXiv eprint/ID pattern")
    g_net.add_argument("--check-net", action="store_true",
                        help="Probe the four data sources + arXiv (5s each) and print "
                             "reachability + next steps — run this when results "
                             "come back unknown on a constrained network")
    g_inputs.add_argument("--parse-text", metavar="FILE",
                        help="Verify a plain-text reference list copied from a paper draft "
                             "(numbered [1]/1. entries, or one per line): inline PMID/DOI/arXiv "
                             "IDs route exactly; title-only entries resolve via PubMed title "
                             "search (results marked resolved_by=title_search)")
    g_inputs.add_argument("--stdin", action="store_true",
                        help="Read a pasted reference list from stdin (same parsing as "
                             "--parse-text): `pbpaste | verify_pmids.py --stdin` / "
                             "`git show HEAD:refs.bib.txt | verify_pmids.py --stdin`")
    g_inst.add_argument("--doctor", action="store_true",
                        help="Environment self-check: tool/Python versions, cache state, "
                             "key/mailto/proxy configuration; add --check-net to include "
                             "the four-data-source + arXiv probe. Read-only, safe to share.")
    g_inst.add_argument("--self-check", action="store_true",
                        help="Verify this copy offline: runs the core promises "
                             "(five-state ladder, plaintext parsing, CSL export, "
                             "version carriers) with zero network and prints one "
                             "OK/FAIL line each. Exit 0 = this copy is intact.")
    g_output.add_argument("--sort", choices=["severity", "cited"], default="severity",
                          help="Report row order: severity (default — retraction/splice/"
                               "mismatch first, the HTML layout) or cited (citation count "
                               "descending, from the Europe PMC/OpenAlex paths; entries "
                               "without a count keep their severity position at the back)")
    g_output.add_argument("--jsonl", metavar="PATH",
                        help="Write results as JSON Lines (one citation per line) — "
                             "stream-friendly for agent pipelines; pair with --output "
                             "for the full report")
    g_net.add_argument("--max-entries", type=int, default=2000, metavar="N",
                        help="Warn when the total de-duplicated input (PMIDs+DOIs+arXiv IDs+"
                             "title-search entries) exceeds N (default 2000) — large runs take "
                             "hours and lean on rate limits; 0 disables the guard")
    g_verify.add_argument("--quick", action="store_true",
                        help="Pre-submission final pass in one flag: --no-cache + "
                             "--verify-doi + --suggest combined (fresh registries, "
                             "DOI cross-check, correct-PMID suggestions)")
    g_output.add_argument("--format-references", metavar="PATH",
                        help="Write verified entries as a formatted reference list — "
                             "GB/T 7714-2015 / Vancouver / APA 7 / AMA 11 / Harvard / "
                             "Chicago 17 via --citation-style; "
                             "correct = numbered list, partial = review section, "
                             "retracted = excluded with a warning")
    g_output.add_argument("--claims-template", metavar="SRC,OUT",
                        help="Reverse-generate a claims CSV skeleton from a "
                             "plain-text reference list, .bib or .ris: every "
                             "routable field the parsers can see is filled, you "
                             "fill the gaps, then run --claims-file for exact "
                             "five-state verification (format: SRC,OUT)")
    g_output.add_argument("--report-bundle", metavar="DIR",
                        help="Write the complete submission evidence pack into DIR: "
                             "audit.json + report.html + verified-refs.bib/.ris + "
                             "audit-table.csv + references-gbt.txt + manifest.txt — "
                             "one command, everything a reviewer may ask for")
    g_output.add_argument("--citation-style",
                        choices=["gbt", "gbty", "vancouver", "apa", "ama",
                                 "harvard", "chicago"],
                        default="gbt",
                        help="Style for --format-references (default: gbt = GB/T 7714-2015 "
                             "numeric; gbty = GB/T author-date; harvard/chicago = author-date, "
                             "unnumbered, sorted by first author)")
    g_output.add_argument("--lint-claims", metavar="FILE",
                        help="Offline lint of a claims file (JSON/CSV/BibTeX/RIS): ID shapes, "
                             "missing titles, unknown columns, duplicate keys — no network")
    parser.add_argument("--version", action="version", version=f"pubmed-verifier {_TOOL_VERSION}")
    args = parser.parse_args()
    # v5.3.0 audit P1-1: these must be set BEFORE the --doctor dispatch,
    # or doctor always reports key/mailto as unset
    _OPTS["ncbi_key"] = args.ncbi_api_key or os.environ.get("NCBI_API_KEY", "")
    _OPTS["mailto"] = (args.mailto or os.environ.get("PUBMED_VERIFIER_MAILTO", "")
                       or os.environ.get("MAILTO", ""))
    _OPTS["meta_source"] = args.meta_source
    _OPTS["timeout"] = args.timeout
    if getattr(args, "self_check", False):
        sys.exit(run_self_check())
    if args.doctor:
        sys.exit(run_doctor(net=args.check_net))
    if args.check_net:
        sys.exit(run_check_net())
    if args.lint_claims:
        sys.exit(run_claims_lint(args.lint_claims))
    if args.claims_template:
        parts = args.claims_template.split(",", 1)
        if len(parts) != 2:
            print("--claims-template needs SRC,OUT (comma-separated)", file=sys.stderr)
            sys.exit(1)
        sys.exit(run_claims_template(parts[0].strip(), parts[1].strip()))
    # v5.8.0: immediate flag validation — out-of-range values fail loudly
    # (or clamp with a [WARN]) instead of silently skewing the run
    _validate_args(args)

    # Collect PMIDs with optional claimed metadata
    pmid_entries = []  # list of (pmid, source_file, context, claimed_dict)
    explicit_claims = {}
    explicit_arxiv = {}   # claims keyed by arxiv_id (v3.1.0)
    explicit_doi = {}     # claims keyed by clean DOI (v3.4.0)
    title_queue = []      # markerless text entries for title search (v4.0.0)

    # Load explicit claims from --claims or --claims-file
    if args.claims_file:
        filepath = args.claims_file
        if filepath.lower().endswith(".csv"):
            explicit_claims = _load_csv_claims(filepath)
            explicit_arxiv.update(getattr(_load_csv_claims, "arxiv_rows", {}))
            explicit_doi.update(getattr(_load_csv_claims, "doi_rows", {}))
            if not explicit_claims and not explicit_arxiv and not explicit_doi:
                print(f"No valid PMIDs found in CSV file: {filepath}", file=sys.stderr)
                sys.exit(1)
        else:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    claims_data = json.load(f)
                if not isinstance(claims_data, list):
                    raise ValueError("claims file must be a JSON array of objects")
                for item in claims_data:
                    if not isinstance(item, dict):
                        continue
                    pmid = str(item.get("pmid", "")).strip()
                    if pmid.isdigit():
                        explicit_claims[pmid] = _pmid_claim_from_item(item)
                    elif str(item.get("arxiv_id", "") or "").strip():
                        aid = str(item["arxiv_id"]).strip()
                        if aid.lower().startswith("arxiv:"):
                            aid = aid[6:].strip()
                        explicit_arxiv[aid.lower()] = _arxiv_claim_from_item(item)
                    elif str(item.get("doi", "") or "").strip():
                        cd = _clean_doi(str(item["doi"]))
                        if cd:
                            explicit_doi[cd] = _doi_claim_from_item(item)
            except (json.JSONDecodeError, ValueError, OSError) as e:
                print(f"[ERROR] reading claims file: {e}", file=sys.stderr)
                sys.exit(1)
    elif args.claims:
        try:
            claims_data = json.loads(args.claims)
            if not isinstance(claims_data, list):
                raise ValueError("--claims must be a JSON array of objects")
            for item in claims_data:
                if not isinstance(item, dict):
                    continue
                pmid = str(item.get("pmid", "")).strip()
                if pmid.isdigit():
                    explicit_claims[pmid] = _pmid_claim_from_item(item)
                elif str(item.get("arxiv_id", "") or "").strip():
                    aid = str(item["arxiv_id"]).strip()
                    if aid.lower().startswith("arxiv:"):
                        aid = aid[6:].strip()
                    explicit_arxiv[aid.lower()] = _arxiv_claim_from_item(item)
                elif str(item.get("doi", "") or "").strip():
                    cd = _clean_doi(str(item["doi"]))
                    if cd:
                        explicit_doi[cd] = _doi_claim_from_item(item)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[ERROR] parsing --claims JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # v7.0.0 (test-line P1): lightweight direct claim — one PMID + --title.
    # Deliberately NOT an explicit claim row: a bare title claim rides the
    # same semantics as a scanned inline claim (title ✓ with authors/journal/
    # year unclaimed upgrades via route=existence_title_match), so the quick
    # one-liner answers "is this the right paper?" with correct — while a
    # wrong title still grades mismatch. Adding --year/--journal claims
    # fields explicitly and keeps the conservative full-verdict cap (partial
    # without authors), same as --claims-file rows.
    direct_claim = None
    if getattr(args, "title", None):
        direct_claim = {
            "claimed_title": args.title,
            "claimed_authors": [],
            "claimed_journal": getattr(args, "journal", "") or "",
            "claimed_year": str(getattr(args, "year", "") or ""),
            "claimed_doi": "",
        }

    # Collect PMIDs from sources
    # v5.0.0 --quick: the pre-submission final pass as one flag — fresh
    # registries, DOI cross-check and correct-PMID suggestions without
    # remembering the combination. Explicit user flags always win (set
    # first, never unset).
    if getattr(args, "quick", False):
        args.no_cache = True
        args.verify_doi = True
        args.suggest = True
    # v5.0.0 --stdin: a pasted reference list arrives as parse-text via a
    # temp file (same numbered/heading parser); the report label reads
    # "stdin" instead of a random temp name.
    if getattr(args, "stdin", False):
        if args.parse_text:
            print("[ERROR] --stdin and --parse-text are mutually exclusive",
                  file=sys.stderr)
            sys.exit(1)
        pasted = sys.stdin.read()
        if not pasted.strip():
            print("[ERROR] --stdin received no input (nothing on stdin)",
                  file=sys.stderr)
            sys.exit(1)
        _tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", prefix="pv_stdin_",
            encoding="utf-8", delete=False)
        _tmp.write(pasted)
        _tmp.close()
        args.parse_text = _tmp.name
        args._stdin_label = True
        atexit.register(
            lambda n=_tmp.name: (os.path.exists(n) and os.unlink(n)) or None)
    doi_inputs = []   # (clean_doi, source_label, claimed_dict|None) — v2.8.0/v3.4.0
    if args.dois:
        for d in args.dois.split(","):
            cd = _clean_doi(d)
            if cd:
                doi_inputs.append((cd, "cli", explicit_doi.get(cd)))
    if args.pmids and args.source:
        print("[WARN] both --pmids and --source given; --source is ignored "
              "entirely (its PMIDs and DOIs are NOT scanned).", file=sys.stderr)
    # Standalone arXiv inputs (v3.0.0) + claims keyed by arxiv_id (v3.1.0)
    arxiv_inputs = []   # (arxiv_id, source_label, claimed_dict|None)
    if args.arxivs:
        for a in args.arxivs.split(","):
            a = a.strip()
            if a:
                arxiv_inputs.append((a, "cli", explicit_arxiv.get(a.lower())))
    # BibTeX bibliography input (v3.6.0): entries route PMID > DOI > arXiv,
    # each carrying its claimed metadata for the full cross-check
    if args.bibliography:
        bib_fmt = ("ris" if args.bibliography.lower().endswith(".ris")
                   else "bib" if args.bibliography.lower().endswith(".bib")
                   else sniff_bibliography_format(args.bibliography))
        if bib_fmt == "ris":
            raw_entries, bib_issues = parse_ris(args.bibliography)
            bib_entries = [dict(e, fields=ris_to_bib_fields(e["fields"]))
                           for e in raw_entries]
        else:
            # explicit .bib and sniffed-bib both land here; a sniffed-unknown
            # file fails BibTeX parsing with the usual report (v3.6.0 shape)
            bib_entries, bib_issues = parse_bibtex(args.bibliography)
        for msg in bib_issues:
            print(f"  bibliography: {msg}", file=sys.stderr)
        bib_src = os.path.basename(args.bibliography)
        bib_routed = {"pmid": 0, "doi": 0, "arxiv": 0}
        bib_skipped = []
        for e in bib_entries:
            kind, ident, claimed = bib_entry_route(e["fields"])
            if kind == "none":
                bib_skipped.append(f"{e['citekey']} (line {e['line']})")
                continue
            bib_routed[kind] += 1
            label = f"{bib_src}#{e['citekey']}"
            if kind == "pmid":
                pmid_entries.append((ident, label, "", claimed))
            elif kind == "doi":
                doi_inputs.append((ident, label, claimed))
            else:
                arxiv_inputs.append((ident, label, claimed))
        if bib_entries:
            print(f"Bibliography {bib_src}: {len(bib_entries)} entries — "
                  f"{bib_routed['pmid']} PMID / {bib_routed['doi']} DOI / "
                  f"{bib_routed['arxiv']} arXiv routed"
                  + (f", {len(bib_skipped)} skipped: {', '.join(bib_skipped)}"
                     if bib_skipped else ""), flush=True)
    # Plain-text reference list input (v4.0.0): a draft reference list copied
    # out of a manuscript. Inline IDs route exactly (PMID > DOI > arXiv);
    # markerless entries with a parseable title go through PubMed title
    # search and carry resolved_by=title_search in their result.
    if args.parse_text:
        text_entries, text_issues = parse_plaintext_references(args.parse_text)
        for msg in text_issues:
            print(f"  parse-text: {msg}", file=sys.stderr)
        text_src = ("stdin" if getattr(args, "_stdin_label", False)
                   else os.path.basename(args.parse_text))
        routed = {"pmid": 0, "doi": 0, "arxiv": 0, "title": 0}
        for i, e in enumerate(text_entries, 1):
            claimed = {"claimed_title": e["claimed_title"],
                       "claimed_authors": e["claimed_authors"],
                       "claimed_journal": e["claimed_journal"],
                       "claimed_year": e["claimed_year"]}
            label = f"{text_src}#{i}"
            if e["pmid"]:
                pmid_entries.append((e["pmid"], label, e["raw"], claimed))
                routed["pmid"] += 1
            elif e["doi"]:
                doi_inputs.append((e["doi"], label, claimed))
                routed["doi"] += 1
            elif e["arxiv_id"]:
                arxiv_inputs.append((e["arxiv_id"], label, claimed))
                routed["arxiv"] += 1
            else:
                e["_label"] = label
                title_queue.append(e)
                routed["title"] += 1
        if text_entries:
            print(f"Text reference list {text_src}: {routed['pmid']} PMID / "
                  f"{routed['doi']} DOI / {routed['arxiv']} arXiv / "
                  f"{routed['title']} title-search routed", flush=True)
    if args.pmids:
        for p in args.pmids.split(","):
            p = p.strip()
            if p.isdigit():
                if direct_claim and p == args.pmids.split(",")[0].strip():
                    # v7.0.0 quick lane: src="cli-quick" is deliberately NOT in
                    # the explicit set, so the v4.9 existence_title_match upgrade
                    # applies (a bare title claim behaves like a scanned inline
                    # claim — wrong title still grades mismatch)
                    pmid_entries.append((p, "cli-quick", "", direct_claim))
                else:
                    pmid_entries.append((p, "cli", "", explicit_claims.get(p, {})))
    elif args.source:
        source = args.source
        if os.path.isfile(source):
            found = extract_pmids_from_file(source)
            for pmid, ctx in found:
                claimed = explicit_claims.get(pmid, parse_citation_context(ctx))
                pmid_entries.append((pmid, source, ctx, claimed))
            for doi, dctx in extract_dois_from_file(source):
                cd = _clean_doi(doi)
                doi_inputs.append((cd, source, explicit_doi.get(cd)))
            for aid, actx in extract_arxivs_from_file(source):
                arxiv_inputs.append((aid, source, explicit_arxiv.get(aid.lower())))
        elif os.path.isdir(source):
            file_map = extract_pmids_from_directory(source)
            for fpath, items in file_map.items():
                for pmid, ctx in items:
                    claimed = explicit_claims.get(pmid, parse_citation_context(ctx))
                    pmid_entries.append((pmid, fpath, ctx, claimed))
            for root, dirs, files in os.walk(source):
                for fname in files:
                    if fname.lower().endswith((".html", ".md", ".txt", ".htm",
                                               ".json", ".docx", ".pptx", ".nxml", ".jats", ".xml")):
                        for doi, dctx in extract_dois_from_file(os.path.join(root, fname)):
                            cd = _clean_doi(doi)
                            doi_inputs.append((cd, os.path.join(root, fname), explicit_doi.get(cd)))
                        for aid, actx in extract_arxivs_from_file(os.path.join(root, fname)):
                            arxiv_inputs.append((aid, os.path.join(root, fname),
                                                 explicit_arxiv.get(aid.lower())))
        else:
            print(f"[ERROR] {source} not found", file=sys.stderr)
            sys.exit(1)
    elif explicit_claims or explicit_arxiv or explicit_doi:
        # Only --claims provided, no --source or --pmids
        for pmid, claimed in explicit_claims.items():
            pmid_entries.append((pmid, "claims", "", claimed))
        for aid, claimed in explicit_arxiv.items():
            arxiv_inputs.append((aid, "claims", claimed))
        for cd, claimed in explicit_doi.items():
            doi_inputs.append((cd, "claims", claimed))
    elif not pmid_entries and not doi_inputs and not arxiv_inputs and not title_queue:
        if explicit_claims is not None or explicit_doi is not None:
            print("No usable claims in the input — check the claims payload "
                  "or file (--lint-claims validates files offline).",
                  file=sys.stderr)
        else:
            parser.print_help()
        sys.exit(1)

    # v3.6.0: explicit CLI/claims inputs outrank bibliography duplicates in
    # the DOI/arXiv dedup — a claims-file DOI keeps its 404=invalid semantics
    # even when a .bib carries the same DOI
    doi_inputs = [t for t in doi_inputs if t[1] in ("cli", "claims")] + \
                 [t for t in doi_inputs if t[1] not in ("cli", "claims")]
    arxiv_inputs = [t for t in arxiv_inputs if t[1] in ("cli", "claims")] + \
                   [t for t in arxiv_inputs if t[1] not in ("cli", "claims")]
    if not pmid_entries and not doi_inputs and not arxiv_inputs and not title_queue:
        print("No PMIDs, DOIs or arXiv IDs found.")
        sys.exit(0)

    # Deduplicate, preserving all source contexts and claims
    seen = {}
    for pmid, src, ctx, claimed in pmid_entries:
        if pmid not in seen:
            seen[pmid] = []
        seen[pmid].append((src, ctx, claimed))

    unique_pmids = list(seen.keys())
    # v5.2.0 quantified-input guard: a vague "large scans take hours" helped
    # nobody — the guard counts the actual de-duplicated workload and says so
    _input_guard_note(len(unique_pmids) + len(doi_inputs) + len(arxiv_inputs)
                      + len(title_queue), getattr(args, "max_entries", 0))
    # v5.7.0 retry-sweep guard: clamp to the sane range
    args.retries = max(0, min(int(args.retries or 0), 3))
    if unique_pmids:
        print(f"Found {len(pmid_entries)} PMID citations ({len(unique_pmids)} unique). Verifying...")
    if doi_inputs:
        print(f"Found {len(doi_inputs)} DOI citations to verify via Crossref...")

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
    _recovered_total = 0
    if uncached_pmids:
        fresh = fetch_summaries(uncached_pmids)
        # v5.7.0 in-batch retry: re-fetch only the PMIDs the first pass lost
        # to the network; cache save sees only recovered/valid entries
        fresh, _rec = _retry_sweep(fresh, uncached_pmids, fetch_summaries,
                                   args.retries, "PMID metadata")
        _recovered_total += _rec
        # Save to cache (network failures excluded -- they are not answers)
        if use_cache:
            _cache_save_fresh(db_path, fresh)
    else:
        fresh = {}

    # Merge cached + fresh
    summaries = {}
    for pmid in unique_pmids:
        summaries[pmid] = cached.get(pmid) or fresh.get(pmid, {"valid": False, "error": "No API response"})

    # Build results with three-state verdict
    results = []
    audit_entries = []
    stats = {"total": len(pmid_entries), "correct": 0, "mismatch": 0, "partial": 0,
             "invalid": 0, "unknown": 0, "unmatched": 0, "retracted": 0, "doi_splice": 0}

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
                if info.get("cited_by_count") is not None:
                    entry["cited_by_count"] = info["cited_by_count"]
                entry["authors"] = ", ".join(info["authors"][:3])
                entry["authors_truncated"] = len(info.get("authors", [])) > 3
                entry["doi"] = info.get("doi", "")
                entry["volume"] = info.get("volume", "")
                entry["pages"] = info.get("pages", "")
                entry["meta_source"] = info.get("source", "ncbi")

                # DOI cross-verification (optional, via Crossref)
                if args.verify_doi and info.get("doi"):
                    doi_meta = fetch_doi_metadata(info["doi"])
                    if doi_meta.get("valid"):
                        entry["doi_verified"] = True
                        # Crossref prefixes retracted titles ("RETRACTED:",
                        # "RETRACTED ARTICLE:") -- strip before comparing so
                        # a confirmed retraction never also reads as a
                        # title mismatch.
                        cr_title = re.sub(r'^\s*RETRACTED(\s+ARTICLE)?\s*:\s*',
                                          "", doi_meta.get("title", ""), flags=re.IGNORECASE)
                        entry["crossref_title"] = doi_meta.get("title", "")
                        entry["doi_title_match"] = _sequence_similarity(
                            cr_title, info["title"]) >= 0.90
                        if doi_meta.get("retracted"):
                            entry["retracted"] = True
                            entry["retraction_note"] = doi_meta.get("retraction_note", "")
                            entry["retraction_type"] = doi_meta.get("retraction_type", "retraction")
                            entry["retraction_date"] = doi_meta.get("retraction_date", "")
                            entry["retraction_source"] = "crossref updated-by"
                            if doi_meta.get("retraction_notice_doi"):
                                entry["retraction_notice_doi"] = doi_meta["retraction_notice_doi"]
                    else:
                        entry["doi_verified"] = False
                        entry["doi_note"] = "crossref unreachable (network) — not a verdict"

                # DOI↔PMID cross-check (v2.4.0): a claimed DOI that differs
                # from the DOI registered for this PMID is a splice/fabrication
                # signal (a real DOI attached to the wrong paper). Uses only
                # the esummary field -- no extra API call, no --verify-doi needed.
                if claimed.get("claimed_doi") and info.get("doi"):
                    entry["claimed_doi"] = claimed["claimed_doi"]
                    entry["doi_cross_match"] = dois_match(claimed["claimed_doi"], info["doi"])
                    if not entry["doi_cross_match"]:
                        entry["doi_splice_suspect"] = True

                # Retraction signal, source-independent (v2.7.0): the
                # registry pubtype flags every PMID with no DOI and no
                # --verify-doi needed (survives the cache); Crossref
                # updated-by (checked above) remains the detail source.
                if info.get("retracted") and not entry.get("retracted"):
                    entry["retracted"] = True
                    entry["retraction_note"] = info.get("retraction_note", "")
                    entry["retraction_type"] = info.get("retraction_type", "retraction")
                    entry["retraction_source"] = "registry pubtype"

                # v5.3.0: retraction reason — resolved AFTER all retraction
                # sources attached (Crossref updated-by or registry pubtype),
                # so BOTH paths get it. Notice DOI preference: the dedicated
                # notice DOI when Crossref named one, else the entry DOI.
                # One extra Crossref call per RETRACTED entry — retractions
                # are rare and the circuit breaker caps abuse; a failed
                # lookup leaves the reason empty (honest).
                if (entry.get("retracted") and not entry.get("retraction_reason")
                        and (entry.get("doi") or entry.get("retraction_notice_doi"))):
                    notice_doi = (entry.get("retraction_notice_doi")
                                  or entry.get("doi", ""))
                    nmeta = fetch_doi_metadata(notice_doi)
                    reason, notice_title = _retraction_reason_from_notice(nmeta)
                    if reason:
                        entry["retraction_reason"] = reason
                    if notice_title:
                        entry["retraction_notice_title"] = notice_title[:200]
                    entry["retraction_reason_doi"] = notice_doi

                # v4.7.0: a live PMID with no usable claimed metadata
                # (title/authors) is an EXISTENCE check — registry record
                # attached, answered (existence), never "insufficient"
                if not (claimed.get("claimed_title") or claimed.get("claimed_authors")):
                    entry["valid"] = True
                    entry["verdict"] = "correct"
                    entry["existence_confirmed"] = True
                    entry["details"] = ("PMID exists — no claimed metadata to "
                                        "cross-check; registry record attached "
                                        "(existence confirmation only)")
                    entry["title"] = info.get("title", "")
                    entry["journal"] = info.get("journal", "")
                    entry["pubdate"] = info.get("pubdate", "")
                    # v4.8.0: info["authors"] is a LIST from the registry —
                    # join like the main loop does (a raw list here crashed
                    # generate_bibtex's .split() downstream, T28)
                    _ex_auth = info.get("authors", "")
                    entry["authors"] = (", ".join(_ex_auth[:3])
                                        if isinstance(_ex_auth, list) else _ex_auth)
                    if info.get("cited_by_count") is not None:
                        entry["cited_by_count"] = info["cited_by_count"]
                    entry["meta_source"] = info.get("source", "")
                    # full-shape cross so the common post-checks pass unchanged
                    cross = {"verdict": "correct", "details": entry["details"],
                             "confidence": 1.0, "title_match": None,
                             "author_match": None, "journal_match": None,
                             "year_match": None,
                             "route": "existence_only"}
                    if info.get("retracted") and not entry.get("retracted"):
                        entry["retracted"] = True
                        entry["retraction_note"] = info.get("retraction_note", "")
                        entry["retraction_type"] = info.get("retraction_type", "retraction")
                        entry["retraction_source"] = "registry pubtype"
                        entry["verdict"], entry["details"] = apply_retraction_cap(
                            entry["verdict"], entry["details"])
                    stats["existence_only"] = stats.get("existence_only", 0) + 1
                else:
                    # Cross-check claimed vs actual
                    cross = cross_check_citation(claimed, {
                        "title": info["title"],
                    "authors": info["authors"],
                    "journal": info["journal"],
                    "pubdate": info["pubdate"],
                })
                # v4.7.0 MECHANISM — mismatch accusation gate: a mismatch is
                # an accusation; it requires the parser to have recovered a
                # STRUCTURED claim (title AND authors co-present) or the user
                # to have explicitly endorsed the metadata. Any heuristic
                # single-field claim (unknown export shapes, fragments,
                # metadata residue) degrades to unknown with a next action —
                # so NO future export format can manufacture false
                # mismatches the way the "- DOI:" rows did.
                if (cross["verdict"] == "mismatch"
                        and not (claimed.get("claimed_title")
                                 and claimed.get("claimed_authors"))
                        and src not in ("cli", "claims", "cli-quick")):
                        # v7.0.0: "cli-quick" (--title direct claim) joins the
                        # explicit set HERE — the title is user-typed verbatim,
                        # not heuristic context parsing, so a wrong title is a
                        # REAL mismatch, never degraded to unknown (the v3.8
                        # guard only exists for parsed-context ambiguity)
                    cross["verdict"] = "unknown"
                    cross["details"] = (
                        cross["details"] + "; claimed metadata incomplete "
                        "(title/authors not both recoverable from this "
                        "context) — no mismatch accusation from heuristic "
                        "parsing; feed --claims-file for a decisive verdict")
                    stats["mismatch_gated"] = stats.get("mismatch_gated", 0) + 1
                    # v4.8.0: the gate keeps the verdict honest, but a
                    # title-only claim can still be corroborated (or surfaced
                    # as a wrong-PMID signal) via PubMed's own title search
                    _second_opinion_title(cross, claimed, pmid, stats)

                # v4.9.0 verdict-ladder monotonicity: a partial whose ONLY
                # gap is the missing author claim (title matched; journal/
                # year never claimed) ranks BELOW a bare existence
                # confirmation — stronger evidence, lower verdict. On
                # scanned sources such entries upgrade to correct (labeled
                # route=existence_title_match). The "never claimed" test
                # reads the CLAIMED fields, not cross's journal/year_match
                # (those are False for unclaimed too, not None). An entry
                # that claims journal/year/author anything keeps its
                # partial — those claims were checked and something
                # differed, a REAL doubt.
                if (cross["verdict"] == "partial"
                        and cross.get("title_match") is True
                        and not claimed.get("claimed_authors")
                        and not claimed.get("claimed_journal")
                        and not claimed.get("claimed_year")
                        and src not in ("cli", "claims")
                        and pmid not in explicit_claims):   # mixed mode: a
                        # claims row rides a scanned src but IS user-explicit
                        # metadata — full verdicts there, never this upgrade
                    cross["verdict"] = "correct"
                    cross["details"] = (
                        "Title matches the registry record; no authors were "
                        "claimed in this context (existence + inline title "
                        "verification). Feed --claims-file with the authors "
                        "for a full five-state verdict.")
                    cross["route"] = "existence_title_match"
                    cross["confidence"] = max(
                        float(cross.get("confidence") or 0), 0.8)
                    stats["existence_title_match"] = stats.get(
                        "existence_title_match", 0) + 1

                if entry.get("doi_splice_suspect"):
                    splice_note = ("claimed DOI differs from the DOI registered for this PMID "
                                   "（声称DOI与该PMID登记DOI不符——拼接伪造信号）")
                    cross["details"] = (cross["details"] + "; " if cross["details"] else "") + splice_note
                    stats["doi_splice"] = stats.get("doi_splice", 0) + 1
                    if cross["verdict"] == "correct":
                        cross["verdict"] = "partial"
                if entry.get("retracted"):
                    cross["verdict"], cross["details"] = apply_retraction_cap(
                        cross["verdict"], cross["details"])
                    stats["retracted"] = stats.get("retracted", 0) + 1
                entry["verdict"] = cross["verdict"]
                entry["details"] = cross["details"]
                entry["confidence"] = round(cross["confidence"], 2)
                entry["title_match"] = cross["title_match"]
                entry["author_match"] = cross["author_match"]
                entry["journal_match"] = cross["journal_match"]
                entry["year_match"] = cross["year_match"]
                if cross.get("author_check"):
                    entry["author_check"] = cross["author_check"]
                reg_year = any(ch.isdigit() for ch in str(info.get("pubdate", "")))
                entry["fields"] = {
                    # bool only when the field was actually compared (claimed
                    # AND present in the registry); otherwise None (= "—")
                    "title": cross["title_match"]
                             if (claimed.get("claimed_title") and info.get("title")) else None,
                    "author": (None if str(cross.get("author_check", "")).startswith("skipped")
                               else cross["author_match"])
                              if (claimed.get("claimed_authors") and info.get("authors")) else None,
                    "journal": cross["journal_match"]
                               if (claimed.get("claimed_journal") and info.get("journal")) else None,
                    "year": cross["year_match"]
                            if (claimed.get("claimed_year") and reg_year) else None,
                }

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
                entry["verdict"], entry["details"] = classify_unverified(info)
                entry["error"] = info.get("error", "Unknown")
                entry["meta_source"] = info.get("source", "")
                if info.get("network_error"):
                    entry["network_error"] = True
                    entry["verdict"] = "unknown"
                    stats["unknown"] += 1          # keep verdict stats reconcilable
                    stats["network_errors"] = stats.get("network_errors", 0) + 1
                else:
                    stats["invalid"] += 1

            if entry.get("valid"):
                audit_entries.append({
                    "pmid": pmid,
                    "source_file": entry["source_file"],
                    "claimed": claimed,
                    "registered": {
                        "title": entry.get("title", ""), "journal": entry.get("journal", ""),
                        "pubdate": entry.get("pubdate", ""),
                        "authors": info.get("authors", []),
                        "doi": entry.get("doi", ""), "registry": entry.get("meta_source", ""),
                    },
                    "evidence": cross,
                    "doi_cross": {
                        "claimed_doi": entry.get("claimed_doi", ""),
                        "registered_doi": entry.get("doi", ""),
                        "match": entry.get("doi_cross_match"),
                        "splice_suspect": entry.get("doi_splice_suspect", False)},
                    "retraction": {
                        "flagged": entry.get("retracted", False),
                        "type": entry.get("retraction_type", ""),
                        "note": entry.get("retraction_note", ""),
                        "date": entry.get("retraction_date", ""),
                        "reason": entry.get("retraction_reason", ""),
                        "notice_title": entry.get("retraction_notice_title", ""),
                        "notice_doi": entry.get("retraction_reason_doi", ""),
                        "source": entry.get("retraction_source",
                                            "crossref updated-by" if entry.get("retracted") else "")},
                    "verdict": {"final": entry["verdict"], "details": entry["details"],
                                "confidence": entry.get("confidence")},
                })
            else:
                audit_entries.append({
                    "pmid": pmid,
                    "source_file": entry["source_file"],
                    "claimed": claimed,
                    "registered": None,
                    "verdict": {"final": entry["verdict"], "details": entry["details"]},
                    "error": entry.get("error", ""),
                    "network_error": entry.get("network_error", False),
                })
            results.append(entry)

    # Standalone DOI verification pipeline (v2.8.0/v2.9.0)
    doi_seen = set(r.get("doi") for r in results if r.get("doi"))
    unique_dois = []
    seen_d = set()
    for d, src, claimed in doi_inputs:
        if d in doi_seen or d in seen_d:
            continue
        seen_d.add(d)
        unique_dois.append((d, src, claimed))
    doi_processed = len(unique_dois)
    resolutions = {}
    workers = max(1, min(args.workers, 8))
    if unique_dois and workers > 1 and len(unique_dois) > 1:
        doi_t0 = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(resolve_doi, d): d for d, _, _ in unique_dois}
            done = 0
            for fut in concurrent.futures.as_completed(futs):
                d = futs[fut]
                try:
                    resolutions[d] = fut.result()
                except Exception as e:
                    resolutions[d] = {"status": "error", "meta": None, "error": str(e)}
                done += 1
                if done % 25 == 0 or done == len(unique_dois):
                    elapsed = time.time() - doi_t0
                    rate = done / elapsed if elapsed > 0 else 0.0
                    eta = (len(unique_dois) - done) / rate if rate > 0 else 0.0
                    print(f"  DOI progress: {done}/{len(unique_dois)} resolved"
                          f" ({elapsed:.0f}s elapsed, ~{eta:.0f}s left)...",
                          file=sys.stderr, flush=True)
    elif unique_dois:
        for d, _, _ in unique_dois:
            resolutions[d] = resolve_doi(d)
    # v5.7.0 in-batch retry: re-resolve only the DOIs the first pass lost to
    # the network (status=error, never a definitive 404=not_found)
    _doi_failed = [d for d, _, _ in unique_dois
                   if resolutions.get(d, {}).get("status") == "error"]
    if _doi_failed:
        def _resolve_subset(subset):
            return {d: resolve_doi(d) for d in subset}
        resolutions, _rec = _retry_sweep(resolutions, _doi_failed, _resolve_subset,
                                         args.retries, "DOI resolution",
                                         failed_pred=lambda v: not v or v.get("status") == "error")
        _recovered_total += _rec
    # Phase 2 (v2.9.0): link resolved DOIs back to PMIDs — parallel EPMC queries
    resolved_dois = [d for d, _, _ in unique_dois
                     if resolutions.get(d, {}).get("status") == "resolved"]
    pmid_map = {}
    if resolved_dois:
        if workers > 1 and len(resolved_dois) > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
                pmid_map = dict(zip(resolved_dois, ex.map(find_pmid_by_doi, resolved_dois)))
        else:
            for d in resolved_dois:
                pmid_map[d] = find_pmid_by_doi(d)
    # Phase 3: batch-fetch full PubMed records for linked PMIDs (cache-aware,
    # 50/batch) — the linking stage never pays per-PMID serial costs
    linked_pmids = sorted({p for p in pmid_map.values() if p})
    pmid_info_map = fetch_summaries(linked_pmids) if linked_pmids else {}
    if linked_pmids:
        pmid_info_map, _rec = _retry_sweep(pmid_info_map, linked_pmids,
                                           fetch_summaries, args.retries,
                                           "linked PMID metadata")
        _recovered_total += _rec
    stats["retried_recovered"] = _recovered_total
    # Phase 4: build entries serially (stats stay main-thread)
    # v4.7.0 (--source only): a scanned DOI whose linked PMID is already
    # verified in the PMID leg merges into that citation — one paper, one
    # finding; explicit --dois/claims DOIs are never merged
    _pmid_verified = {str(_r["pmid"]) for _r in results if _r.get("pmid")}
    if args.source and not (args.dois or explicit_doi):
        for _i, (_doi, _s, _c) in enumerate(unique_dois):
            _linked = str(pmid_map.get(_doi, "") or "")
            if _linked and _linked in _pmid_verified:
                unique_dois[_i] = (_doi, "merge:" + _linked, _c)
                stats["doi_merged_into_pmid"] = stats.get("doi_merged_into_pmid", 0) + 1
                print(f"  note: DOI {_doi} links to already-verified PMID "
                      f"{_linked} — merged (one paper, one finding)",
                      file=sys.stderr, flush=True)
    unique_dois = [t for t in unique_dois if not t[1].startswith("merge:")]
    doi_processed = len(unique_dois)
    for doi, src, claimed in unique_dois:
        entry, audit_item = verify_doi_entry(
            doi, src, resolution=resolutions.get(doi),
            linked_pmid=pmid_map.get(doi, ""), linked_info=pmid_info_map.get(pmid_map.get(doi, ""), {}),
            claimed=claimed)
        # v3.4.0: claimed verdicts counted explicitly first (same shape as the
        # arXiv loop — the v3.3.0 double-count lesson), then unknown buckets
        if entry["verdict"] == "correct":
            stats["correct"] = stats.get("correct", 0) + 1
        elif entry["verdict"] == "mismatch":
            stats["mismatch"] = stats.get("mismatch", 0) + 1
        elif entry["verdict"] == "partial":
            stats["partial"] = stats.get("partial", 0) + 1
        if entry["verdict"] == "invalid":
            stats["invalid"] += 1
        elif entry.get("network_error"):
            stats["unknown"] += 1
            stats["network_errors"] = stats.get("network_errors", 0) + 1
        elif entry["verdict"] not in ("correct", "mismatch", "partial"):
            stats["unknown"] += 1   # existence-only (resolved) or scanned-404 suspect
            if entry.get("resolved"):
                stats["doi_resolved"] = stats.get("doi_resolved", 0) + 1
        if entry.get("retracted"):
            stats["retracted"] = stats.get("retracted", 0) + 1
        results.append(entry)
        audit_entries.append(audit_item)

    # arXiv verification pipeline (v3.0.0) — serial with 3s politeness
    # (official arXiv etiquette: same client >= 3s between calls)
    arxiv_seen = set(r.get("arxiv_id", "").lower() for r in results if r.get("arxiv_id"))
    arxiv_total = len({a.lower() for a, _, _ in arxiv_inputs} | arxiv_seen)
    arxiv_processed = 0
    arxiv_t0 = time.time()
    last_call = 0.0
    for aid, src, claimed_aid in arxiv_inputs:
        if aid.lower() in arxiv_seen:
            print(f"  note: duplicate arXiv ID {aid} merged into the first "
                  f"occurrence (later claims ignored)", file=sys.stderr, flush=True)
            continue
        arxiv_seen.add(aid.lower())
        arxiv_processed += 1
        wait = 3.0 - (time.time() - last_call)
        if wait > 0:
            time.sleep(wait)
        last_call = time.time()
        entry, audit_item = verify_arxiv_entry(aid, src, claimed=claimed_aid,
                                               link_pmid=find_pmid_by_doi)
        if entry["verdict"] == "correct":
            stats["correct"] = stats.get("correct", 0) + 1
        elif entry["verdict"] == "mismatch":
            stats["mismatch"] = stats.get("mismatch", 0) + 1
        elif entry["verdict"] == "partial":
            # v3.3.0: a DOI-pairing cap lands here — counting it as unknown
            # would inflate the "existence-checked only" disclosure pool
            stats["partial"] = stats.get("partial", 0) + 1
        if (entry.get("fields") or {}).get("doi") is False:
            stats["arxiv_doi_mismatch"] = stats.get("arxiv_doi_mismatch", 0) + 1
        if entry["verdict"] == "invalid":
            stats["invalid"] += 1
            stats["arxiv_invalid"] = stats.get("arxiv_invalid", 0) + 1
            stats.setdefault("arxiv_invalid_list", []).append(entry.get("arxiv_id", ""))
        elif entry.get("network_error"):
            stats["unknown"] += 1
            stats["network_errors"] = stats.get("network_errors", 0) + 1
        elif entry["verdict"] not in ("correct", "mismatch", "partial"):
            # v3.3.0 P1 fix (latent since v3.0.0): correct/mismatch/partial
            # entries used to fall into this else and were ALSO counted as
            # unknown — inflating the "existence-checked only" disclosure
            stats["unknown"] += 1
        if arxiv_processed % 5 == 0 or arxiv_processed == arxiv_total:
            elapsed = time.time() - arxiv_t0
            rate = arxiv_processed / elapsed if elapsed > 0 else 0.0
            eta = (arxiv_total - arxiv_processed) / rate if rate > 0 else 0.0
            print(f"  arXiv progress: {arxiv_processed}/{arxiv_total} verified"
                  f" ({elapsed:.0f}s elapsed, ~{eta:.0f}s left)...",
                  file=sys.stderr, flush=True)
        if entry["verdict"] == "invalid":
            print(f"  ⚠ INVALID arXiv ID: {entry.get('arxiv_id')} — fabrication signal",
                  flush=True)
        results.append(entry)
        audit_entries.append(audit_item)
    if arxiv_processed:
        stats["total"] = stats.get("total", 0) + arxiv_processed
    if doi_processed:
        stats["total"] = stats.get("total", 0) + doi_processed

    # Title-search verification for markerless text entries (v4.0.0):
    # weaker evidence than a supplied ID — a clean cross-check is correct
    # with resolved_by=title_search; anything else stays honestly unknown.
    text_processed = 0
    for te in title_queue:
        _text_label = ("stdin" if getattr(args, "_stdin_label", False)
                       else (args.parse_text or "text"))
        entry, audit_item = verify_title_entry(te, _text_label)
        text_processed += 1
        if entry["verdict"] == "correct":
            stats["correct"] = stats.get("correct", 0) + 1
        elif entry["verdict"] == "partial":
            stats["partial"] = stats.get("partial", 0) + 1
            if entry.get("retracted"):
                stats["retracted"] = stats.get("retracted", 0) + 1
        elif entry.get("network_error"):
            stats["unknown"] += 1
            stats["network_errors"] = stats.get("network_errors", 0) + 1
        else:
            stats["unknown"] += 1
        results.append(entry)
        audit_entries.append(audit_item)
    if text_processed:
        stats["total"] = stats.get("total", 0) + text_processed
        n_resolved = sum(1 for r in results if r.get("resolved_by") == "title_search")
        print(f"Title-search leg: {text_processed} entries — {n_resolved} resolved, "
              f"{text_processed - n_resolved} honestly unknown (supply a PMID/DOI "
              f"for a decisive verdict)", flush=True)

    # Retraction replacement suggestions (v4.2.0, --suggest): retracted
    # entries get same-topic live candidates, honestly labeled
    if args.suggest:
        suggest_retraction_replacements(results)

    # v5.4.0: --sort cited — a researcher's "which of these carries weight"
    # ordering. Applied AFTER stats are counted (pure presentation) and
    # affects the terminal/JSON/JSONL/markdown reports; the HTML report
    # ALWAYS keeps its own severity layout (the detail-row design assumes
    # retraction/splice rows first).
    if getattr(args, "sort", "severity") == "cited":
        results.sort(key=_cited_sort_key, reverse=True)

    # Delta audit against a previous working-paper (v2.8.0)
    deltas = None
    if args.diff:
        deltas = diff_against_baseline(results, args.diff)
        if deltas.get("error"):
            print(f"Diff error: {deltas['error']}", file=sys.stderr)
            deltas = None
        else:
            stats["deltas"] = deltas["counts"]

    stats["submission_readiness"] = {}
    ready, ready_line = readiness_summary(stats)
    stats["submission_readiness"] = {"ready": ready, "summary": ready_line}
    repro = {
        "command": "verify_pmids.py " + " ".join(_redacted_argv()),
        "version": _TOOL_VERSION,
        "sources": "eutils.ncbi.nlm.nih.gov · www.ebi.ac.uk (Europe PMC) · api.crossref.org · api.openalex.org · export.arxiv.org — all HTTPS",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Finding ledger (v4.6.0): explicit bookkeeping before the report files
    ledger = finding_ledger(results, stats)
    if results:
        print("\n" + "=" * 60)
        print(f"Finding ledger — {len(results)} findings")
        print(f"  ✓ answered:          {len(ledger['answered'])} "
              f"(correct/mismatch/invalid)")
        print(f"  ◐ partially answered: {len(ledger['partially'])} "
              f"(partial — manual review items)")
        print(f"  ✗ unresolved:         {len(ledger['unresolved'])}")
        for u in ledger["unresolved"][:5]:
            print(f"      - {u['key']}: {u['why']}")
            print(f"        next: {u['next']}")
        if len(ledger["unresolved"]) > 5:
            print(f"      … +{len(ledger['unresolved']) - 5} more (see report)")
        print(f"  budget: {ledger['budget']['citations_checked']} citations checked, "
              f"{ledger['budget']['network_errors']} network errors")

    # v5.8.0: breaker visibility before any serialization, so
    # stats.breaker_skipped lands in JSON/JSONL/HTML/bundle like every
    # other stats field; the [WARN] keeps the end-of-run visibility
    _bs = _breaker_summary_line()
    if _bs:
        print(f"[WARN] {_bs}", file=sys.stderr)
        stats["breaker_skipped"] = sum(_BREAKER_REJECTS.values())

    # Output
    if args.output:
        ext = Path(args.output).suffix.lower()
        # Explicit --format wins; otherwise derive from the file extension
        # (.json -> json, .html/.htm -> html). Anything else is refused
        # rather than silently writing HTML into a .txt.
        if args.format == "json" or ext == ".json":
            output_text = generate_json_report(results, stats)
        elif args.format == "markdown" or ext in (".md", ".markdown"):
            output_text = generate_markdown_report(results, stats,
                                                   args.source or args.pmids or "claims", deltas)
        elif args.format == "html" or ext in (".html", ".htm"):
            output_text = generate_html_report(results, stats, args.source or args.pmids or "claims", repro,
                                               deltas)
        else:
            print("Unsupported --output extension (use .json or .html); "
                  "omit --output for terminal text output.", file=sys.stderr)
            sys.exit(1)
        Path(args.output).write_text(output_text, encoding="utf-8")
        print(f"Report written to {args.output}")

    if args.jsonl:
        # v5.3.0: one citation per line — stream-friendly for agent
        # pipelines (jq, log shippers, incremental consumers). The stats
        # block goes out as the final {"_stats": ...} line so a stream
        # never needs buffering to know the totals.
        lines = [json.dumps(r, ensure_ascii=False) for r in results]
        lines.append(json.dumps({"_stats": stats}, ensure_ascii=False))
        Path(args.jsonl).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"JSONL written to {args.jsonl} ({len(results)} results + 1 stats line)")

    if args.export_audit:
        Path(args.export_audit).write_text(
            generate_audit_report(audit_entries, stats, args, deltas), encoding="utf-8")
        print(f"Audit trail written to {args.export_audit}")

    if args.export_bibtex:
        Path(args.export_bibtex).write_text(
            generate_bibtex(results), encoding="utf-8")
        print(f"BibTeX written to {args.export_bibtex} "
              f"(correct included; partial commented; others excluded)")

    if args.export_ris:
        Path(args.export_ris).write_text(
            generate_ris(results), encoding="utf-8")
        print(f"RIS written to {args.export_ris} "
              f"(correct = TY JOUR, partial = TY DATA)")

    if args.export_csl:
        Path(args.export_csl).write_text(
            generate_csl_json(results), encoding="utf-8")
        print(f"CSL JSON written to {args.export_csl} "
              f"(imports into Zotero via File > Import; partial entries carry a "
              f"verify-manually note, others excluded)")

    if args.format_references:
        Path(args.format_references).write_text(
            generate_reference_list(results, args.citation_style), encoding="utf-8")
        _n_ok = sum(1 for r in results if r.get("verdict") == "correct")
        print(f"Reference list ({args.citation_style}) written to "
              f"{args.format_references} ({_n_ok} verified "
              f"{'entry' if _n_ok == 1 else 'entries'})")

    if args.report_bundle:
        try:
            _bundle_files = write_report_bundle(results, stats, args, deltas,
                                                audit_entries, args.report_bundle)
            print(f"Evidence pack written to {args.report_bundle} "
                  f"({len(_bundle_files)} files):")
            for _bf in _bundle_files:
                print(f"  {_bf}")
        except OSError as e:
            print(f"report-bundle failed: {e}", file=sys.stderr)
            sys.exit(1)

    if args.export_csv:
        Path(args.export_csv).write_text(
            generate_csv_report(results), encoding="utf-8")
        print(f"CSV audit table written to {args.export_csv}")

    if not args.output:
        # Text output
        correct = stats.get("correct", 0)
        mismatch = stats.get("mismatch", 0)
        partial = stats.get("partial", 0)
        unknown = stats.get("unknown", 0)
        print(f"\n{'='*60}")
        print(f"Readiness: {ready_line}")
        if deltas and "error" not in deltas:
            cnt = deltas["counts"]
            print(f"Delta vs baseline: {cnt.get('newly_retracted', 0)} newly retracted, "
                  f"{cnt.get('degraded', 0)} degraded, {cnt.get('improved', 0)} improved, "
                  f"{cnt.get('new', 0)} new, {cnt.get('dropped', 0)} dropped")
            for item in deltas["newly_retracted"]:
                print(f"  ⚠ NEWLY RETRACTED: {item['key']} — {item['title']}")
        print(f"Results: {correct}/{stats['total']} correct, {mismatch} mismatch, "
              f"{stats['invalid']} invalid, {partial} partial, {unknown} unknown")
        if stats.get("unmatched"):
            print(f"Relevance warnings: {stats['unmatched']}")
        if stats.get("network_errors"):
            print(f"⚠ Network: {stats['network_errors']} citation(s) could NOT be verified "
                  f"(data sources unreachable; reported as unknown, NOT invalid)"
                  + (f" — {stats.get('retried_recovered', 0)} more recovered by the "
                     f"in-batch retry sweep (--retries)" if stats.get("retried_recovered") else ""))
        if stats.get("retracted"):
            print(f"⚠ Retracted: {stats['retracted']} citation(s) point to RETRACTED papers "
                  f"(verdict capped at partial — human review required)")
        if stats.get("doi_splice"):
            print(f"⚠ DOI splice: {stats['doi_splice']} citation(s) claim a DOI that differs from "
                  f"the one registered for their PMID (fabrication signal; capped at partial)")
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
            
            if r.get("arxiv_id"):
                key_label = f"arXiv {r['arxiv_id']}"
            elif r.get("doi") and not r.get("pmid"):
                key_label = f"DOI {r['doi']}"
            else:
                key_label = f"PMID {r['pmid']}"
            line = f"{icon} {key_label} ({r['source_file']}) [{verdict}]"
            if r.get("valid"):
                line += f"\n   Actual: {r.get('title', '')[:90]}"
                if r.get("claimed_title"):
                    line += f"\n   Claimed: {r['claimed_title'][:90]}"
                if r.get("details"):
                    line += f"\n   Details: {r['details']}"
                fld = r.get("fields") or {}
                if fld:
                    marks = {True: "✓", False: "✗", None: "—"}
                    ev = " · ".join(f"{k} {marks.get(fld.get(k), '—')}"
                                    for k in ("title", "author", "journal", "year"))
                    line += f"\n   Evidence: {ev}"
                if r.get("replacement_note"):
                    line += f"\n   ♻ {r['replacement_note']}"
                if r.get("suggested_pmids"):
                    for s in r["suggested_pmids"][:2]:
                        line += f"\n   → Suggest: PMID {s['pmid']} - {s['title']}"
                if r.get("match_score") is not None and r["match_score"] < args.threshold:
                    line += f" [ relevance={r['match_score']:.0%} ]"
            else:
                line += f"\n   Error: {r.get('error', '?')}"
            print(line)


    # Exit codes: 2 = verification incomplete (network); 1 = problems found
    # (invalid / mismatch / retracted / DOI-splice); 0 = clean. Network-
    # incomplete outranks problem-found so automation never mistakes
    # "could not verify" for "all verified".
    if stats.get("network_errors"):
        sys.exit(2)
    sys.exit(1 if stats["invalid"] > 0 or stats.get("mismatch", 0) > 0
             or stats.get("retracted", 0) > 0 or stats.get("doi_splice", 0) > 0
             or stats.get("arxiv_doi_mismatch", 0) > 0 else 0)
