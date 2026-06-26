## Description: <br>
Automates OpenClaw workspace health checks and repairs common workspace issues such as redundant files, naming problems, script permissions, and Git commits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyi881](https://clawhub.ai/user/zhangyi881) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace maintainers use this skill to inspect an OpenClaw workspace, calculate a health score, identify missing or nonconforming files, and optionally apply automated fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair mode can broadly move files, change permissions, and commit all Git changes without review. <br>
Mitigation: Run the health check without --fix first, use it only from the intended workspace root, and enable --fix only when the repository is backed up or clean and automatic changes are acceptable. <br>
Risk: Automatic Git commits may include unrelated workspace changes. <br>
Mitigation: Review git status before using --fix and inspect the resulting commit before sharing or pushing changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhangyi881/workspace-auto-maintenance) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with optional command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May exit with status codes indicating errors, warnings, or a clean workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
