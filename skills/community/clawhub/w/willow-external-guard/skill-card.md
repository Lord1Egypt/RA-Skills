## Description:

Willow External Guard scans and wraps untrusted external content before LLM processing to help detect prompt injection, role hijack, leak attacks, and approval-bypass attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudi193-cmd](https://clawhub.ai/user/rudi193-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining Willow use this skill to check untrusted web, message, corpus, and sub-agent text before summarization, ingestion, or action. It helps route findings to proceed, confirm, or block decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wrap mode can still emit content after the scanner identifies a blocked pattern.

Mitigation: Run a scan first, check the verdict and exit code, and refuse BLOCKED content before sending it to an LLM or knowledge base.

Risk: The guard is a helper scanner rather than a complete enforcement boundary.

Mitigation: Use it as part of a defense-in-depth review process and keep human confirmation for suspicious content where the workflow calls for it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rudi193-cmd/skills/willow-external-guard)
- [Publisher profile](https://clawhub.ai/user/rudi193-cmd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and scanner verdict text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce CLEAN, SUSPICIOUS, or BLOCKED verdicts and sandwich-wrapped text for downstream review.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
