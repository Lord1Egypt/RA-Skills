## Description:

Advanced usage statistics and high-fidelity visual reporting for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vintlin](https://clawhub.ai/user/vintlin)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to summarize local agent-session usage, token counts, model mix, estimated cost, cache savings, and recent usage trends as text summaries or visual reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the local/no-network claims are stronger than the code supports.

Mitigation: Review before installing in strict no-network or high-assurance privacy environments, and avoid relying on the privacy claim without local validation.

Risk: The skill scans local OpenClaw/Clawdbot session logs and maintains a local usage database.

Mitigation: Run it in a dedicated virtual environment and set OPENCLAW_WORKSPACE to a directory you control.

Risk: The security guidance calls out log-derived HTML before Chromium rendering as an area needing validation or escaping.

Mitigation: Escape or validate log-derived report content before rendering with Chromium.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vintlin/skills/usage-visualizer)
- [Publisher profile](https://clawhub.ai/user/vintlin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands, JSON status output, text summaries, and generated PNG report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image mode writes a local PNG report; text mode can emit plain text or JSON.]

## Skill Version(s):

1.1.3 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
