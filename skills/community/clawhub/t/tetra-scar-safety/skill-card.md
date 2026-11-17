## Description:

Agent safety that learns from incidents, with a reflex arc that blocks repeat threats without LLM calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aibenyclaude-coder](https://clawhub.ai/user/aibenyclaude-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to check shell commands, file writes, network requests, and commits against built-in threat patterns and incident-derived scars before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A usage example can read a user's real SSH private key if copied exactly.

Mitigation: Replace the example with a single-quoted inert placeholder before publishing or running it.

Risk: Directory audit results may be incomplete for dangerous commands compared with the advertised built-in rule groups.

Mitigation: Treat audit findings as a partial signal and review high-risk commands with the direct safety check path before execution.

Risk: The audit command reads local files while looking for secrets.

Mitigation: Run audits only on narrow, intended project paths and avoid broad scans of unrelated sensitive directories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aibenyclaude-coder/skills/tetra-scar-safety)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python examples, JSON-like safety results, and JSONL scar records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local files for scar memory and directory audits; no external service calls are described.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
