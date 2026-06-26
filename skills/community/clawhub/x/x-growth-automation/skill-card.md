## Description: <br>
Set up a reusable X/Twitter growth automation system with OpenClaw, Bird CLI, X API, dry-run/live rollout, anti-repetition controls, and niche-specific posting policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roskva000](https://clawhub.ai/user/roskva000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scaffold and configure a reusable X/Twitter growth automation project for their own account. It helps collect setup decisions, generate project files, configure cadence and source options, and choose a dry-run or explicitly approved live rollout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live X/Twitter posting can publish unwanted or excessive content if enabled without clear approval, cadence limits, and review. <br>
Mitigation: Start in dry-run, require explicit user approval before live posting, configure daily and monthly caps, and review generated drafts and schedules. <br>
Risk: Credentials for X/Bird access could be exposed if shared in chat or copied from another project. <br>
Mitigation: Keep credentials out of chat and store them only in a local secret file or secret manager. <br>
Risk: Reply automation has higher operational risk because reply targets may be restricted or unsuitable. <br>
Mitigation: Keep reply automation disabled by default, validate targets where possible, apply per-day caps, and log posted, skipped, and failed outcomes. <br>
Risk: Automated posting can repeat similar drafts or repost the same source when deduplication is weak. <br>
Mitigation: Use idempotent slot keys based on stable fields and apply recent-post similarity checks plus source deduplication. <br>


## Reference(s): <br>
- [X Growth Automation on ClawHub](https://clawhub.ai/roskva000/x-growth-automation) <br>
- [Setup Questionnaire](references/setup-questionnaire.md) <br>
- [Rollout Modes](references/rollout-modes.md) <br>
- [Operational Hardening](references/operational-hardening.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to start from dry-run defaults, require explicit approval for live publishing, and keep credentials outside chat.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
