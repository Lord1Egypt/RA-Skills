## Description:

Connects OpenClaw-style runs to VizClaw live rooms for room creation, JSONL and websocket bridging, trigger and agent event streaming, and overview-mode visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[araa47](https://clawhub.ai/user/araa47)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create VizClaw rooms and stream OpenClaw-style run events from JSONL logs, stdin, local websockets, or OpenClaw Gateway connections. It helps visualize agent lifecycle, task, tool, skill, report, heartbeat, reminder, and completion events while allowing overview mode to reduce streamed text detail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed mode can stream OpenClaw run content, including sensitive prompts, tool outputs, reports, or private project data, to VizClaw.

Mitigation: Use overview mode for normal operation and avoid streaming secrets or data the user is not allowed to share.

Risk: The documented remote uv command runs a mutable hosted script from vizclaw.com.

Mitigation: Prefer pinned or reviewed local versions when available, and run the remote URL only after deciding the hosted script source is trusted.

Risk: The authoritative security verdict is suspicious because the skill streams detailed agent content by default and recommends remote code execution.

Mitigation: Review the skill before installation and follow the provided security guidance for sensitive runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/araa47/skills/vizclaw)
- [VizClaw hosted connect script](https://vizclaw.com/skills/vizclaw/scripts/connect.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can emit room codes, session IDs, viewer URLs, status text, and JSON event payloads sent to VizClaw.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
