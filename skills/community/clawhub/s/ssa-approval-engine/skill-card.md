## Description: <br>
Approval Engine provides rule-driven multi-level approvals, exception detection, automated recovery strategies, and Discord notification integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to add approval controls, exception monitoring, automated recovery, and Discord alerts to workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the rule-evaluation path can execute generated JavaScript. <br>
Mitigation: Review the rule-evaluation path before installation, use only trusted rule files and trusted approval or context inputs, and remove eval-style execution before broader deployment. <br>
Risk: The server security guidance identifies under-scoped Discord and logging data flows. <br>
Mitigation: Restrict Discord channels and bot permissions, avoid sending sensitive customer, order, or complaint details unless approved, and set tight filesystem permissions and retention for local logs and JSON stores. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/ssa-approval-engine) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Approval rules configuration](artifact/config/approval-rules.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces approval workflow, exception handling, recovery, notification, and configuration guidance for agent use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
