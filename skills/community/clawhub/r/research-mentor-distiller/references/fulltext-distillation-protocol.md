# Full-Text Distillation Protocol

Use this protocol when the user wants a precise mentor skill from papers rather
than a lightweight homepage or abstract distillation.

## Collection Ladder

1. Run `scripts/collect_publications.py` first when the user provides a scholar
   name, homepage, or Semantic Scholar author id.
2. Inspect `crawl-report.md` before trusting the index. Check author ambiguity,
   source counts, missing abstracts, and PDF coverage.
3. If coverage is weak, use `agent-fallback-queue.md` for manual browser/search
   fallback. Search for public paper pages, arXiv pages, project pages, code,
   and lawful open PDFs.
4. Record every manual fallback source in the evidence snapshot with confidence.
5. Do not use paywalled full text unless the user provides lawful access.

Do not stop at the first script failure. Before downgrading a target v2
distillation, attempt at least three recovery routes:

- repair download conditions such as SSL certificates, `certifi`, user-agent,
  timeout, retry count, or smaller parallel batches;
- search alternate lawful sources such as arXiv, project pages, institutional
  pages, repositories, DOI landing pages, publisher open PDFs, OpenAlex,
  Semantic Scholar, or Crossref;
- manually recover representative papers from `agent-fallback-queue.md` using
  browser/search ability.

If full-text coverage remains below the required threshold, explicitly lower the
version claim to v1 or v1.5 and write the unresolved items into
`references/validation.md` and `distillation-manifest.json`.

## Full-Text Extraction

Run `scripts/extract_fulltext.py` after open PDFs are available:

```bash
python scripts/extract_fulltext.py \
  --publication-index source_materials/<scholar>/publications/publication-index.json \
  --output-dir source_materials/<scholar>/fulltext \
  --max-papers 40 \
  --overwrite
```

If PDFs are already in a folder:

```bash
python scripts/extract_fulltext.py \
  --pdf-dir source_materials/<scholar>/papers \
  --output-dir source_materials/<scholar>/fulltext \
  --max-papers 40 \
  --overwrite
```

Read:

- `extraction-report.md` for failures and weak extraction warnings.
- `distillation-workbench.md` for recurring method-tag leads.
- `paper-signal-cards/` for per-paper problem, contribution, data, method,
  evaluation, and limitation signals.
- `fulltext/` for manual checks when signal cards are thin.

## Evidence Priority

Use this order when claims conflict:

1. Full paper sections: introduction, method, experiments, limitations, appendix.
2. Project pages, code repositories, dataset cards, and benchmark protocols.
3. Abstracts and official publication metadata.
4. Homepage publication entries and news blurbs.
5. Agent inference from titles only.

Label confidence:

- **Direct evidence**: explicitly stated in a source or visible in a paper.
- **Strong inference**: repeated across multiple papers, years, or directions.
- **Speculative extension**: useful mentoring rule not directly stated.

## Cross-Direction Methodology Synthesis

After extracting representative papers, build two layers:

### Core Methodology Across Directions

Promote a pattern only if it recurs in at least three papers or at least two
directions. Good core methodology statements have this form:

- "Frame the problem around a capability bottleneck, then construct data or an
  evaluation protocol that makes the bottleneck observable."
- "Prefer supervision sources that scale through natural traces, reports,
  co-occurring modalities, pseudo-labels, or domain knowledge."

For each methodology, record:

- Name.
- Short actionable rule.
- Evidence paper ids or titles.
- Which parts of the papers support it.
- Distinctive tradeoff or anti-pattern.
- Confidence.

### Direction-Specific Methodologies

Separate playbooks when the evidence differs by direction. Use a compact schema:

- Direction:
- Target capability:
- Problem taste:
- Data and supervision pattern:
- Method pattern:
- Evaluation pattern:
- Anti-patterns:
- Representative papers:
- Confidence:

Do not force a direction into the scholar's global taste if it appears only in a
single cluster of papers.

## Agent Fallback Requirements

When script coverage fails, the agent should:

- Search exact paper titles with `PDF`, `arXiv`, `project page`, and the scholar
  name.
- Prefer official publisher pages, arXiv, institutional pages, project pages,
  and repositories.
- Save or cite the URL used for evidence.
- Mark the evidence as fallback-collected.
- State when only abstract-level evidence is available.

## Quality Bar

Before generating or updating a mentor skill:

- Each core methodology should cite multiple papers or clearly say it is low confidence.
- Each direction-specific playbook should name representative papers.
- The final skill should tell the mentor how to use evidence in idea critique,
  experiment design, literature strategy, and paper feedback.
- The final skill should refuse impersonation and private-belief claims.
- A v2 claim requires representative full-text extraction, at least 10 extracted
  papers by default, and enough direction coverage for the requested scope.
- A v3 claim requires v2 plus independent forward tests on at least three
  realistic research tasks.
- Run `scripts/validate_mentor_skill.py <skill-dir> --target-version <vN>`
  before reporting completion.
