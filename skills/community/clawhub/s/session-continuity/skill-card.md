## Description: <br>
Session Continuity helps OpenClaw agents save and resume named task checkpoints across session endings, context loss, compaction, crashes, and multi-day workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve unfinished task state, list saved checkpoints, and resume work from a structured briefing instead of reconstructing context manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext checkpoint files can contain sensitive task context, credentials, or personal data. <br>
Mitigation: Avoid saving secrets or sensitive personal data, and periodically review checkpoint files before sharing or retaining the workspace. <br>
Risk: Autosave behavior can persist session details without a visible user prompt. <br>
Mitigation: Review autosave.md and autosave-log.md regularly, and use the skill only in workspaces where local autosaves are acceptable. <br>
Risk: Checkpoint names are used as file names and are not safely confined by the helper script. <br>
Mitigation: Use simple kebab-case names without path separators, and treat resume or delete actions carefully until name validation is added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/session-continuity) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [proactive-agent WAL Protocol](https://github.com/hal-lobster/proactive-agent) <br>
- [Checkpoint Format](references/checkpoint-format.md) <br>
- [Resume Flow](references/resume-flow.md) <br>
- [Auto-Checkpoint Signals](references/auto-checkpoint-signals.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown checkpoint files and text resume briefings with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes named checkpoint files and autosave artifacts under memory/checkpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
