## Description:

Autonomous research pipeline skill for Claude Code that orchestrates literature review, hypothesis generation, experiment design, code generation and sandbox execution, statistical analysis, paper writing, multi-agent peer review, and conference-ready LaTeX export from a research topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical writers use ResearchClaw to run an end-to-end research workflow from topic selection through experiment execution, analysis, paper drafting, review, and LaTeX export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create files and run generated experiment code.

Mitigation: Use a restricted disposable workspace, keep manual gate review enabled, and prefer simulated mode unless a real sandbox is available.

Risk: SSH or local subprocess execution can affect external systems or the host workspace.

Mitigation: Run with restricted accounts and permissions, and review execution settings before enabling SSH or subprocess modes.

Risk: Configuration may require an LLM API key.

Mitigation: Use environment variables for API keys instead of storing secrets directly in configuration files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python examples, configuration guidance, and generated research artifact descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create staged research artifacts, experiment code, JSON summaries, LaTeX tables, paper drafts, charts, and pipeline summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
