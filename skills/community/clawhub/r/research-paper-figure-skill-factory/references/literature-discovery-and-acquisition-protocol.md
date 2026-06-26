# Literature Discovery and Acquisition Protocol

This protocol moves the skill origin from already-provided paper material to lawful literature discovery.

## Purpose

Build a useful reference corpus before designing figures or constructing a domain-specific figure taxonomy.

## Allowed sources

- User-uploaded PDFs or notes.
- Open-access PDFs from arXiv, PubMed Central, conference proceedings, institutional repositories, publisher OA pages, or author pages.
- DOI/URL landing pages, abstracts, metadata, and citations when full text is not accessible.
- Papers the user explicitly has rights to provide.

## Disallowed sources

- Paywall bypass, login bypass, DRM bypass, or credential sharing.
- Sci-Hub, piracy mirrors, or other unauthorized full-text sources.
- Claiming to have read a full paper when only abstract/metadata was available.

## Acquisition workflow

1. Define the corpus goal: topic, target venue/field, figure families, date range if relevant.
2. Build search queries from user keywords, seed papers, and domain synonyms.
3. Search and collect candidates.
4. Download only open-access or user-authorized PDFs.
5. Record each item as `downloaded`, `metadata_only`, `needs_user_upload`, or `excluded`.
6. Keep a retrieval log with title, year, venue/source, URL/DOI when known, access status, and reason for inclusion.
7. If access is limited, continue with abstracts/metadata but mark the limitation in state.

## Default recommendation

When the user provides no corpus and no local index exists, start by defining the full target corpus scope and acquisition plan. A small pilot of 5-8 highly relevant open-access papers is allowed only for planning/search-query calibration or an explicitly user-approved pilot run. It cannot support a production-grade generated skill by itself when more relevant PDFs can be lawfully obtained or already exist locally.

When the workspace already contains local PDFs, a paper index, or prior retrieval manifests, enumerate the full relevant candidate set first and process all accessible relevant PDFs as far as feasible. Do not substitute an arbitrary small sample for the builder-time evidence base.


## Acquisition mode state

Record one of these modes in state:

- `auto_download`: the host legally obtained open-access or user-authorized PDFs.
- `user_upload_required`: the user must upload PDFs or provide permitted links before full-text analysis.
- `metadata_only`: only abstracts/metadata/landing pages are available.
- `mixed`: the corpus contains a combination of full PDFs, metadata-only items, and/or user-uploaded files.

Never hide access limitations. If full text is not available, state exactly what was used.

## Figure inspection handoff

When the guide will build a taxonomy from papers, record whether actual figure images were inspected. Use `figure_inspection.status` from the session schema. Captions-only evidence is useful but must not be described as a full visual analysis.


## v1.6 acquisition output checklist

When reporting literature discovery/acquisition, include DOI/URL or stable identifier when available, source route, acquisition status, access basis, and figure-inspection status. If full figures were not viewed, mark the taxonomy as provisional and record the limitation in `figure_inspection.status` and `taxonomy_source_limitations`.

## v1.9 role in specialized skill generation

This protocol is not optional background work. In the normal path for generating a specialized figure-making skill, literature/source acquisition is the first substantive step after defining the target figure class. The acquired corpus feeds figure inspection, taxonomy construction, pattern extraction, prompt libraries, examples, and the generated skill package.

If the environment supports web access and file download, begin acquisition from lawful open-access or user-authorized sources. If not, output a concrete acquisition plan with recommended venues, queries, seed papers, and upload requests.

## v1.11 Corpus Artifact First, retained and clarified through v1.16

B3 must produce visible artifacts, not only a prose plan, when the host has the ability to search/download/write files. Use this directory pattern by default, changing the slug to match the target figure class:

```text
/mnt/data/<target-skill-slug>-corpus/
  papers/
  metadata/
    retrieval_manifest.csv
    retrieval_manifest.json
    acquisition_report.md
    failed_or_blocked_items.md
    figure_inspection_queue.md
```

Do not mark B3 complete unless either:

1. PDFs were downloaded or user-uploaded and the manifest points to local files; or
2. downloads are unavailable/blocked and the acquisition report plus upload/link request has been created; or
3. the user explicitly accepts a metadata-only/caption-only fallback.

For production-grade specialized skill generation, B3 must also record corpus coverage: total candidate PDFs, accessible PDFs, processed/selected PDFs, skipped PDFs, skipped reasons, and whether the processing plan is full-feasible, chunked/resumable, or intentionally sampled.

For default recent-two-year CS top-conference oral corpora, each manifest row must include the evidence source for `presentation_status` such as official conference program, OpenReview decision page, CVF page, ACL anthology notes, proceedings page, or user-provided source.

## v1.16 builder-time acquisition rule

For specialized skill generation, literature discovery and acquisition are builder-time operations. Once the target figure class is confirmed, B2 and B3 must run in `research-paper-figure-skill-factory` itself when capabilities allow. Do not defer initial acquisition to the generated specialized skill. The generated skill may later refresh or extend the corpus, but the first taxonomy must come from the builder-time corpus/evidence or be labeled limited/pilot/fallback.

## v1.0.0 default corpus scope: recent two-year CS top-conference oral papers

When this guide is generating a specialized research-figure-making skill and the user does not specify a different corpus scope, B2 and B3 must default to a **recent two-year computer-science top-conference oral corpus**.

Default rules:

- `year_window: last_2_conference_years`.
- Resolve the actual years at execution time. Prefer the two most recent complete conference years; include the current year only if official oral lists are already published and record that decision.
- As of 2026-04-27, the default complete-year window is 2024-2025 unless official 2026 oral lists are available.
- `field_scope: computer_science_top_conferences`.
- `presentation_filter: oral_required`.
- Spotlight, award, highly cited, or representative non-oral papers are not default-corpus substitutes; they require explicit user approval and must be labeled fallback.
- Every included item must record official oral evidence in the manifest.

Default venue families:

- ML / AI: NeurIPS, ICML, ICLR, AAAI, IJCAI.
- CV: CVPR, ICCV, ECCV.
- NLP: ACL, EMNLP, NAACL.
- Data mining / IR / Web: KDD, SIGIR, The Web Conference / WWW.
- Systems / HCI only when relevant: OSDI, SOSP, NSDI, CHI, UIST.

For method-framework figure skills, prioritize venues with many method diagrams: CVPR/ICCV/ECCV, NeurIPS/ICML/ICLR, ACL/EMNLP/NAACL, then KDD/SIGIR/The Web Conference.

Official oral evidence sources include official conference programs, schedules, oral-paper lists, OpenReview decision pages, CVF or ACL Anthology pages that mark oral status, conference proceedings pages, or user-provided official sources. Do not infer oral status from memory, citations, popularity, social media, or unofficial lists.

The retrieval manifest must include `oral_status_verified`, `official_oral_evidence_source_type`, `official_oral_evidence_url` or `official_oral_evidence_local_path`, and `fallback_reason_if_not_oral`. Items lacking verified official oral evidence must be excluded from the default oral corpus or moved to the unverified/fallback list.
