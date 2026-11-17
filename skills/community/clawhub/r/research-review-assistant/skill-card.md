## Description:

Research Review Assistant helps agents retrieve academic papers, summarize methods and findings, rank relevance, iterate with user feedback, and draft literature review reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research-support agents use this skill to gather recent literature for a topic, produce structured paper summaries, identify trends and gaps, and generate review drafts that can be revised through feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation metadata can pull unrelated unpinned npm packages.

Mitigation: Review package metadata before installation and remove the npm dependencies or replace them with properly pinned Python requirements.

Risk: Paper retrieval uses plaintext HTTP for arXiv access.

Mitigation: Change arXiv requests to HTTPS before relying on generated review content.

Risk: Generated literature summaries may contain incomplete or misleading interpretations of retrieved papers.

Mitigation: Have a qualified reviewer check source papers, relevance scores, and citations before using the review in research, publication, or grant materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/research-review-assistant)
- [Artifact README](artifact/README.md)
- [arXiv API endpoint used by artifact](http://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown literature review reports, optional LaTeX or grant-reference formatting, command examples, and saved Markdown files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports max_papers, summary_length, iteration_rounds, and command-line field, paper-count, version, and save options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
