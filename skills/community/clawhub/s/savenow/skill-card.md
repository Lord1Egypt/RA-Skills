## Description: <br>
Save durable notes from the current OpenClaw + Telegram conversation into today's memory/YYYY-MM-DD.md, with a semantic-dedupe preview/apply flow and inline Apply/Cancel buttons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chelebii](https://clawhub.ai/user/chelebii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw and Telegram users use this skill to preserve durable decisions, fixes, conventions, and system notes from an active chat into a daily workspace memory file after preview or auto-save. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads recent OpenClaw Telegram chat history and can save selected notes into a local daily memory file. <br>
Mitigation: Install it only in workspaces where that access is acceptable, and use the default preview flow to review proposed notes before writing. <br>
Risk: Notes may contain sensitive or inaccurate information if the source conversation includes it. <br>
Mitigation: Apply only reviewed previews for sensitive conversations; reserve /savenow auto for trusted conversations. <br>
Risk: Auto mode writes directly without the Apply/Cancel confirmation step. <br>
Mitigation: Prefer /savenow preview for normal use and limit /savenow auto to cases where the conversation and extracted notes are already trusted. <br>


## Reference(s): <br>
- [savenow on ClawHub](https://clawhub.ai/chelebii/savenow) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown chat previews, JSON script summaries, and daily memory Markdown updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default /savenow previews without writing; apply and auto modes can write selected notes to memory/YYYY-MM-DD.md.] <br>

## Skill Version(s): <br>
0.1.1 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
