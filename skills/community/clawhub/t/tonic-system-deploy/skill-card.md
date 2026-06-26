## Description: <br>
Software deployment workflow for systems with separate UAT and PROD environments, covering bug fix deployment planning, UAT-first and PROD-first flow selection, emergency hotfixes, rollbacks, nightly deploy pipelines, approval gates, human checkpoints, automation nodes, Telegram notifications, and rollback procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonylnng](https://clawhub.ai/user/tonylnng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, release managers, and operations teams use this skill to choose and execute the appropriate UAT/PROD deployment workflow for bug fixes, emergency hotfixes, rollbacks, multi-service releases, and scheduled nightly deploys with human approval gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow concerns high-impact production releases where incorrect execution could cause outages, regressions, or unsafe production changes. <br>
Mitigation: Require explicit release-owner approval before production actions, keep credentials and production access outside the skill, and follow the documented approval, monitoring, smoke test, and rollback checkpoints. <br>
Risk: Choosing the wrong flow when UAT and PROD versions diverge can create false confidence or introduce regressions. <br>
Mitigation: Perform the version check before selecting a flow, use PROD-first handling when UAT is ahead of PROD, and validate in the target environment before merging changes onward. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tonylnng/tonic-system-deploy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with decision trees, tables, checklists, notification templates, and inline command or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes human approval checkpoints, rollback guidance, freeze policy guidance, and deployment notification templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
