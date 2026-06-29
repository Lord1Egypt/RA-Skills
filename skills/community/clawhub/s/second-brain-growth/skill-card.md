## Description: <br>
Evaluates second-brain effective knowledge growth and health across Hbrain, Codex interactive use, Hermes reporting, and OpenClaw handoffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to audit a local Hbrain/llm-wiki second-brain for deposition, connection, recall, transformation, and knowledge debt. It supports interactive chat diagnoses, optional Markdown reports, and Hermes/OpenClaw handoff summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local Hbrain knowledge base that may contain personal or sensitive notes. <br>
Mitigation: Review the documented Hbrain paths before use and run it only in workspaces where local note inspection is intended. <br>
Risk: Hermes cron setup can create recurring analysis and saved reports under documented _meta directories. <br>
Mitigation: Approve scheduled runs and persistent report paths only when recurring analysis and report files are desired. <br>
Risk: The skill includes hard-coded local filesystem paths for the publisher's Hbrain layout. <br>
Mitigation: Adjust paths for the deployment environment before running commands or automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/second-brain-growth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with optional YAML handoff block and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default user-facing summaries are in Chinese; persistent reports are optional when requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
