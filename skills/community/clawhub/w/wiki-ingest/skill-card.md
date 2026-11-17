## Description:

Ingests new source material into a persistent Markdown knowledge wiki by summarizing sources, updating relevant pages, maintaining links and indexes, and recording contradictions or open questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teki-ai](https://clawhub.ai/user/teki-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers maintaining Markdown, Obsidian-style, or git-backed knowledge wikis use this skill to ingest articles, notes, transcripts, reports, papers, or meeting summaries while preserving source summaries, cross-links, indexes, logs, and unresolved tensions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally makes persistent edits to Markdown or Obsidian-style wiki files, which can alter shared or git-backed knowledge bases.

Mitigation: Specify the target wiki before use and request a proposed change list or diff before applying updates to shared or git-backed notes.

Risk: New source material can conflict with existing wiki content or include uncertain claims.

Mitigation: Keep source claims, existing wiki beliefs, current synthesis, contradictions, and open questions visibly separated in the generated updates.

## Reference(s):

- [Ingest Patterns](references/ingest-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/teki-ai/skills/wiki-ingest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown page updates with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source summaries, wiki page updates, index.md and log.md entries, internal links, and contradiction notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
