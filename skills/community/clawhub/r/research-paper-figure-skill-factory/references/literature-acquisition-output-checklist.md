# Literature Acquisition Output Checklist — v1.13

Use this checklist whenever the Skill Builder layer performs or skips literature acquisition.

For each corpus item, record:

- stable identifier: DOI, arXiv ID, PubMed ID, ACL anthology ID, URL, or uploaded filename;
- source route: open-access PDF, conference page, author page, institutional repository, user upload, metadata-only page, or other lawful route;
- acquisition status: downloaded, user-uploaded, metadata-only, inaccessible, duplicate, excluded;
- access basis: open access, user-authorized, metadata-only, unavailable;
- inspection level: full figure images viewed, captions only, metadata only, or mixed;
- notes: relevance, key figure patterns, limitations, and next action.

State footer must surface:

- `acquisition_mode`;
- `retrieval_log` summary;
- corpus coverage summary: candidate PDF count, accessible PDF count, processed PDF count, skipped PDF count, and skipped reasons;
- `figure_inspection.status`;
- `workflow_shortcut` if any builder step was skipped.

When shortcutting, distinguish:

- partial builder shortcut, often skipping B2-B5 but still generating the specialized skill in B6-B9;
- full production fast-track, skipping B1-B9 and using a fallback skill/taxonomy.


## v1.13 host capability checklist

Every acquisition or download plan must state:

- `host_capabilities.web_search`;
- `host_capabilities.pdf_download`;
- `host_capabilities.pdf_open`;
- `host_capabilities.pdf_figure_inspection`;
- `host_capabilities.file_upload`;
- what will be done if a capability is unavailable.

## v1.13 local corpus artifact checklist

When B3 is executed, verify and report:

- `local_corpus.root_dir` exists or is explicitly planned if file writing is unavailable;
- `papers/` contains every legally downloaded or user-uploaded PDF referenced in the manifest;
- `retrieval_manifest.csv` and `retrieval_manifest.json` exist and contain matching item counts;
- `acquisition_report.md` summarizes queries, sources, date range, inclusion/exclusion rules, download results, limitations, and next actions;
- `failed_or_blocked_items.md` lists paywalled, inaccessible, duplicate, excluded, or metadata-only items;
- `figure_inspection_queue.md` lists which PDFs/figures should be inspected in B4;
- `corpus_coverage_report.md` or acquisition report section records full-feasible corpus coverage, chunking/resume status, skipped reasons, and whether any sample is pilot/limited only;
- `local_corpus.ready_for_extraction` is true only if local PDFs/user uploads or an explicitly accepted metadata/caption fallback are sufficient for B4 extraction. `local_corpus.ready_for_taxonomy` is deprecated and must not be used as an active gate.

Minimum manifest columns:

`item_id,title,authors,year,venue,presentation_status,presentation_status_evidence,stable_id,landing_url,pdf_url,source_route,access_basis,acquisition_status,local_pdf_path,inspection_level,inclusion_reason,limitations,next_action`

## v1.13 B4 extraction artifact checklist

After B3 acquisition, B4 must create an `extracted/` directory and record paper cards, figure inventory, caption inventory, label summary, panel notes, visual observations, evidence map, extraction summary, and extraction report. B5 taxonomy must cite these artifacts and cannot be generated from the manifest alone.

For large local corpora, B4 must report processed PDF count, skipped PDF count, failure reasons, and multi-label coverage. Representative rendered pages/contact sheets are audit aids only and cannot be used as the corpus count.

## v1.0.0 oral-corpus evidence checklist

When the default corpus is used, B3 output must show:

- [ ] Resolved recent two-year window.
- [ ] CS top-conference venue set.
- [ ] `presentation_filter: oral_required`.
- [ ] Official oral-status evidence source for every included item.
- [ ] `oral_status_verified: true` for every counted oral paper.
- [ ] Unverified oral candidates moved to blocked/unverified lists.
- [ ] Spotlight/award/highly-cited papers labeled only as user-approved fallback, not oral substitutes.
- [ ] Manifest includes official evidence URL or local evidence path.
