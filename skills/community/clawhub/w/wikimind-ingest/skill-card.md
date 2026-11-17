## Description:

Ingests articles, docs, notes, and web pages into a local LLM-WikiMind knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hal-9909](https://clawhub.ai/user/hal-9909)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to save selected articles, docs, notes, and web pages into a local WikiMind knowledge base as classified Markdown entries for later agent retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists selected content into a local searchable wiki, which can capture confidential or unwanted text if inputs are not reviewed.

Mitigation: Confirm the content, title, domain, source URL, and destination path before ingesting; avoid storing secrets or confidential material.

Risk: Fallback file writes and index updates modify the local WikiMind workspace.

Mitigation: Prefer the scoped wiki-kb MCP tool when available and review proposed file paths and qmd update commands before execution.

Risk: The workflow depends on qmd and ClawHub tooling installed outside the skill artifact.

Mitigation: Install dependencies from trusted, pinned versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hal-9909/skills/wikimind-ingest)
- [Skill repository](https://github.com/HAL-9909/llm-wikimind-skill)
- [LLM-WikiMind](https://github.com/HAL-9909/llm-wikimind)
- [LLM-WikiMind quick start](https://github.com/HAL-9909/llm-wikimind#quick-start)
- [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown pages with YAML frontmatter, shell commands, and brief status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write WikiMind files, update the qmd search index, and append an ingest log when used.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
