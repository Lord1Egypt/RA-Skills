## Description: <br>
Captures learnings, errors, and corrections so coding agents can record failures, user corrections, missing capabilities, knowledge gaps, and recurring better approaches for later review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fedrov2025](https://clawhub.ai/user/fedrov2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain structured markdown logs for corrections, command failures, feature requests, and reusable learnings. It also provides optional hook and OpenClaw setup guidance for prompting agents to review and promote high-value learnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent agent-memory workflows can capture sensitive material if users log secrets, credentials, raw transcripts, customer data, or sensitive command output. <br>
Mitigation: Keep learning files free of sensitive data and review entries before sharing them across sessions or promoting them into agent instruction files. <br>
Risk: Broad hook activation can inject reminders into more sessions than intended. <br>
Mitigation: Keep hooks project-local where possible, enable them intentionally, and use the minimal hook configuration when broad activation is unnecessary. <br>
Risk: Unreviewed learnings can introduce incorrect or misleading guidance into future agent behavior. <br>
Mitigation: Review and scan learnings before promoting them to AGENTS.md, CLAUDE.md, SOUL.md, TOOLS.md, or a reusable skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fedrov2025/self-improving-agent-3-0-2) <br>
- [OpenClaw integration](references/openclaw-integration.md) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [Usage examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local learning files and may emit short hook reminders when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact _meta.json lists package version 3.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
