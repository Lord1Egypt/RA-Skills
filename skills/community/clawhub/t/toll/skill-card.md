## Description:

Track and display token usage statistics and estimated USD costs from Claude Code and Codex CLI sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fullstop000](https://clawhub.ai/user/fullstop000)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local Claude Code and Codex CLI usage, including session counts, token totals, cache hit rates, and estimated USD costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path may use an unverified remote installer.

Mitigation: Review the installer source before running it, or prefer a pinned release such as cargo install toll --version 1.0.5 when available.

Risk: The tool reads local Claude Code and Codex CLI session logs to calculate usage and costs.

Mitigation: Run it only in environments where local session log access is acceptable and review outputs before sharing them.

## Reference(s):

- [toll ClawHub skill page](https://clawhub.ai/fullstop000/skills/toll)
- [toll project homepage](https://github.com/Fullstop000/toll)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI command output, explanatory text, and optional JSON or CSV from the toll command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local Claude Code and Codex CLI session logs through the toll CLI; cost estimates may be approximate for inferred model pricing.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
