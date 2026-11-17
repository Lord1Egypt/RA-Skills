## Description:

Resolve one or more paper titles to reliable arXiv papers using Tavily search, then fetch compact arXiv metadata and abstracts with a local helper script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[red0orange](https://clawhub.ai/user/red0orange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to resolve paper titles to canonical arXiv records and produce a reusable lookup folder with normalized inputs, per-title JSONL results, and a Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad command, file, agent, MCP, and web authority for a narrow arXiv lookup workflow.

Mitigation: Run it with narrowed permissions limited to Tavily, arXiv, the bundled helper scripts, and the intended work directory.

Risk: Generated Markdown reports may include paper titles, metadata, or abstracts sourced from external services.

Mitigation: Treat generated reports as untrusted content and review them before using them in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/red0orange/skills/tavily-arxiv-paper-fetech)
- [Publisher profile](https://clawhub.ai/user/red0orange)
- [Examples](examples.md)
- [arXiv abs URL pattern](https://arxiv.org/abs/xxxx.xxxxx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown report and JSONL process log with compact arXiv metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes input_titles.md, paper_fetches.jsonl, and paper_fetch_report.md under the requested work directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
