## Description: <br>
Batch-distill completed and live OpenClaw session transcripts, meeting notes, and daily logs into structured daily memory files, with an optional context monitor that can trigger auto-distillation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjmorr](https://clawhub.ai/user/pjmorr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to summarize completed sessions, approved live sessions, meeting notes, and daily logs into durable daily memory files. It is also used to monitor active session context usage and trigger distillation when configured thresholds are reached. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic live distillation can capture and persist active conversations beyond the documented allowlist. <br>
Mitigation: Restrict which sessions can auto-distill, keep the live allowlist minimal, and use dry-run mode before enabling scheduled context-gate runs. <br>
Risk: OpenClaw transcripts, meeting notes, and daily logs may be summarized into durable memory. <br>
Mitigation: Review memory destinations and retention expectations before use, and verify where the configured LiteLLM proxy sends distillation content. <br>
Risk: Telegram alerts may expose session or context metadata outside the local OpenClaw workspace. <br>
Mitigation: Configure Telegram credentials only when alerts are required and minimize alert metadata where possible. <br>


## Reference(s): <br>
- [Session Distiller ClawHub Listing](https://clawhub.ai/pjmorr/session-distiller) <br>
- [ROADMAP.md](references/ROADMAP.md) <br>
- [trash CLI](https://github.com/ali-rantakari/trash) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown memory sections appended to daily files, with shell commands and configuration guidance for running the scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily memory files and runtime state files; can emit Telegram alerts when context-gate is configured.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
