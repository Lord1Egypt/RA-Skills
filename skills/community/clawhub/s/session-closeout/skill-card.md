## Description: <br>
Run a structured end-of-session closeout that checks repo hygiene, refreshes a master task list, appends a closeout block to daily memory, and verifies automation health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkfaris94](https://clawhub.ai/user/jkfaris94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run an end-of-session workspace closeout, summarize repository and task status, and record next-session context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace-local scripts or hooks may execute during closeout and do more than bookkeeping. <br>
Mitigation: Run only in trusted workspaces, and inspect or disable scripts/build-master-todo.py and scripts/closeout-hooks.sh before use in an untrusted repository. <br>
Risk: The closeout process writes session notes and may refresh task files in the workspace. <br>
Mitigation: Review generated memory and task-list changes before committing or sharing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jkfaris94/session-closeout) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Plain text key=value summary and Markdown closeout block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append to memory/YYYY-MM-DD.md and can source workspace-local hooks when present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
