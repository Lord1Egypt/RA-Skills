## Description:

TokenSave analyzes explicitly requested session token waste and API cost issues, including duplicate tool calls, context bloat, model mismatch, and heartbeat waste, with a local zero-config analyze mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raydatalab](https://clawhub.ai/user/raydatalab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill after an explicit request to run TokenSave against a specific local session or request dump. The skill returns a token waste and cost report with guidance the user can give to an agent to reduce avoidable spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analyze mode reads local session transcripts and request dumps.

Mitigation: Run it only after an explicit user request and prefer a specific session ID, file, or directory target over auto-detection.

Risk: The tool is installed from an unpinned external Python package.

Mitigation: Install it in an isolated Python environment and verify the tokensave package source and version before use.

Risk: Pipeline mode can process API requests and requires an API key plus network access.

Mitigation: Treat pipeline mode separately from local analysis and enable it only with deliberate API-key and network configuration.

Risk: Waste findings such as near-duplicate detection may include false positives.

Mitigation: Use the report as diagnostic guidance and review suggested changes before applying them to agent behavior.

## Reference(s):

- [TokenSave GitHub Homepage](https://github.com/raydatalab/tokensave)
- [ClawHub Skill Page](https://clawhub.ai/raydatalab/skills/tokensave)
- [ClawHub Publisher Profile](https://clawhub.ai/user/raydatalab)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response with pasted CLI report output and concise remediation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analyze mode uses local session data; pipeline mode is separate and may require an API key and network access.]

## Skill Version(s):

0.4.5 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
