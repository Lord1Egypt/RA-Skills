## Description: <br>
CLI task timer for AI agents - benchmark learning progression with auto-save logs and visualizations, with ClawVault integration for persistent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use TaskTime CLI to time work, inspect task history, generate reports, and save completed task metadata to local storage or ClawVault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A global npm CLI install adds executable code to the agent environment. <br>
Mitigation: Install only when a global TaskTime CLI is acceptable for the target environment. <br>
Risk: Completed task names, notes, timing metadata, and reports may be saved persistently and potentially synced to ClawVault. <br>
Mitigation: Avoid secrets, customer data, and confidential project details in task descriptions or notes; use --no-vault for work that should stay out of remote memory. <br>


## Reference(s): <br>
- [TaskTime CLI on ClawHub](https://clawhub.ai/G9Pedro/tasktime) <br>
- [ClawVault](https://clawvault.dev) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell command examples and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the tasktime or tt CLI and may create local JSON task logs and ClawVault-synced task records.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
