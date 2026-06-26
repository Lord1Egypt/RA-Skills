## Description: <br>
Stream long-running task progress into the OpenClaw chat UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiyooYin](https://clawhub.ai/user/LiyooYin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to run or tail long-running jobs and stream concise progress summaries, parsed metrics, and final status updates into an OpenClaw chat session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Run mode launches a local command and streams its output into chat. <br>
Mitigation: Use run mode only with trusted commands and review the command and working directory before execution. <br>
Risk: Log output may contain API keys, credentials, private data, or sensitive prompts. <br>
Mitigation: Prefer tail mode when only monitoring an existing log, avoid sensitive logs, and remove generated status and log files when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LiyooYin/task-progress-stream) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown progress summaries, JSON status files, Markdown status files, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Periodic updates are injected at a configurable interval and status files are written under the configured output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
