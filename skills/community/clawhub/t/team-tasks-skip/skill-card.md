## Description:

Coordinates multi-agent development pipelines through shared JSON task files for project initialization, task assignment, status tracking, session-based dispatch, and result collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zdp1117](https://clawhub.ai/user/zdp1117)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate code, test, documentation, and review agents across sequential, dependency-based, or debate workflows while recording task status and outputs for handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hard-coded external Telegram destinations may route agent communications to unintended destinations.

Mitigation: Install only when you control those destinations, or remove or replace them before use.

Risk: Unsafe project-file path construction can read or overwrite JSON files outside the task directory.

Mitigation: Use simple project slugs and avoid confidential project data until project-name validation is fixed.

Risk: Concurrent multi-agent writes can lose or corrupt task state.

Mitigation: Use one coordinator for state updates or add locking before relying on concurrent writers.

## Reference(s):

- [README](README.md)
- [Agent Teams Enhancement Spec](SPEC.md)
- [Claude Code Agent Teams Reference Notes](docs/AGENT_TEAMS_OFFICIAL_DOCS.md)
- [Agent Teams Gap Analysis](docs/GAP_ANALYSIS.md)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Claude Code Agent Teams Documentation](https://docs.anthropic.com/en/docs/claude-code/agent-teams)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists project coordination state as local JSON files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
