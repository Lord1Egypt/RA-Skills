# Mentor Skill Compliance And Packaging

Use this reference before generating, auditing, or exporting a scholar-specific
mentor skill. The goal is to make MentorForge outputs portable across agents and
hard to accidentally overstate.

## Non-Installation Rule

By default, MentorForge must not install generated mentor skills into Codex,
Claude Code, ClawHub, or any other runtime. Generate the package in the requested
output folder, validate it, and report the path plus validation status. Install
only when the user explicitly asks.

## Required Package Shape

Every generated mentor skill package must contain:

```text
<skill-name>/
  SKILL.md
  distillation-manifest.json
  agents/
    openai.yaml
  references/
    evidence-snapshot.md
    publication-index.md
    research-taste-profile.md
    fulltext-distillation.md
    validation.md
```

Recommended but optional:

```text
  references/access-issues.md
  references/forward-test-results.md
  exports/
```

The folder basename should match the `SKILL.md` frontmatter `name`.

## Frontmatter Portability

`SKILL.md` YAML frontmatter must be ASCII-only for cross-platform portability.
Avoid Chinese, emoji, arrows, em dashes, mathematical symbols, smart quotes, and
other non-ASCII characters in frontmatter. Put those in the Markdown body.

Frontmatter should contain only:

```yaml
---
name: scholar-slug-research-mentor
description: Use this skill when ...
---
```

## Version Gates

Version claims are compliance claims, not prose labels.

### v0 Homepage/Profile Distillation

Minimum:

- Public homepage, CV, profile, lab page, or user-provided public notes.
- `distillation-manifest.json` records source types and limitations.
- `SKILL.md` calls itself v0 or base/profile version.

### v1 Metadata/Abstract Distillation

Minimum:

- At least 20 publication records, unless the scholar has a smaller complete
  corpus and the manifest explains that limitation.
- Representative abstracts or reliable official metadata for the scoped research
  direction.
- Methodology claims based only on abstracts/metadata must be tagged as strong
  inference or speculative extension, not direct full-text evidence.

### v2 Full-Paper Distillation

Minimum:

- At least 10 representative open/public full-text papers extracted by default.
  Use a higher threshold such as 20-40 for broad senior researchers when
  available.
- Representative papers cover the user's requested direction, or at least two
  directions when generating a broad base mentor.
- Core methodology claims cite repeated full-text signals from introductions,
  methods, experiments, limitations, appendices, project pages, dataset cards,
  or benchmark protocols.
- Full-text extraction failures and fallback sources are recorded.

If these checks fail, lower the claim to v1 or v1.5 and state why.

### v3 Validated Cyber Mentor

Minimum:

- Meets v2.
- Independent forward tests on at least three realistic tasks:
  idea critique, experiment design, paper feedback, literature strategy, or a
  boundary/impersonation test.
- Validation records the prompt, output summary, pass/fail judgment, and needed
  revisions.

## Required Manifest

Create `distillation-manifest.json` with this shape:

```json
{
  "schema_version": "1.0",
  "target": {
    "name": "Scholar Name",
    "slug": "scholar-slug",
    "homepage": "https://example.edu"
  },
  "skill_name": "scholar-slug-research-mentor",
  "version_claimed": "v2",
  "created_at": "2026-07-02T00:00:00Z",
  "source_materials": {
    "root": "source_materials/scholar-slug",
    "publication_index": "source_materials/scholar-slug/publications/publication-index.json",
    "fulltext_dir": "source_materials/scholar-slug/fulltext"
  },
  "evidence": {
    "publication_count": 160,
    "records_with_pdf_url": 137,
    "abstracts_count": 30,
    "pdf_downloaded": 32,
    "fulltext_extracted": 32,
    "representative_papers": 32,
    "directions_covered": ["computer-vision", "ai4medicine"]
  },
  "fallback": {
    "used": true,
    "attempts": [
      "certifi SSL context",
      "manual arXiv/project-page recovery"
    ],
    "unresolved": []
  },
  "validation": {
    "status": "pass",
    "target_version_checked": "v2",
    "forward_tests": 0,
    "notes": "v2 package; not v3 until forward-tested."
  }
}
```

Use lower counts honestly. Do not fabricate abstracts, PDFs, or full-text
coverage to satisfy a version gate.

## Agent Fallback Requirements

When collection or PDF download fails, try at least three recovery routes before
downgrading the version:

1. Fix local script conditions: certificates, `certifi`, user-agent, timeouts,
   retry count, or parallel small-batch download.
2. Search alternate lawful sources: arXiv, project pages, institutional pages,
   repositories, publisher open PDFs, DOI landing pages, OpenAlex, Semantic
   Scholar, Crossref, or official dataset/model pages.
3. Use the agent's own browsing/search ability on `agent-fallback-queue.md`.

Record all successful manual fallback sources in `evidence-snapshot.md` or
`access-issues.md`. If fallback remains weak, lower the version claim.

## Cross-Platform Export

Exporting is separate from installation. When the user asks for export, create
platform-specific files under an output folder:

- `codex/`: full `SKILL.md` package with `agents/openai.yaml`.
- `claude/`: `CLAUDE.md` plus references.
- `clawhub/`: platform manifest plus skill content.
- `plain-prompt/`: a compact runtime prompt and evidence index.

Do not assume a Codex skill package is automatically usable by every platform.

## Completion Checklist

Before reporting completion:

1. Run `scripts/validate_mentor_skill.py <skill-dir> --target-version <vN> --strict`.
2. Report the exact package path.
3. Report the validated version, not just the intended version.
4. State evidence coverage counts.
5. State whether full-text extraction and fallback were used.
6. State that the package was not installed unless explicitly requested.
