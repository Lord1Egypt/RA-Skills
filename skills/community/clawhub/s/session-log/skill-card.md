## Description: <br>
Session Log creates local timestamped Markdown session files for OpenClaw agents and records short topic summaries so session history survives resets and can feed daily reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meigesir](https://clawhub.ai/user/meigesir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local session logging to OpenClaw workspaces, including per-agent logs and daily report inputs across resets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local session logs persist conversation summaries on disk and may capture sensitive information if users record it. <br>
Mitigation: Keep the sessions folder in a controlled workspace, avoid recording secrets or sensitive personal data, and define retention rules before broad use. <br>
Risk: Daily report workflows can aggregate logs from multiple agents and widen access to conversation summaries. <br>
Mitigation: Limit report access to intended readers and document which agent workspaces are included. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown instructions with bash commands and generated Markdown session files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped local session files in a user-selected sessions directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
