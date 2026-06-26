## Description: <br>
Onboard a repo by assessing architecture and dependencies, setting up roadmap and kanban execution workflow, and generating an actionable onboarding report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill when entering an unfamiliar repository to capture architecture, dependencies, setup commands, project-management structure, and first execution steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow references local scripts that are not bundled with the skill. <br>
Mitigation: Review or replace those script paths before execution, or use the documented manual fallback on a branch or disposable copy. <br>
Risk: The optional daily PM audit installs recurring automation. <br>
Mitigation: Enable the cron job only after inspecting the cron script and confirming how to disable it. <br>
Risk: Generated onboarding and planning documents may contain incomplete or incorrect repository guidance. <br>
Mitigation: Review generated reports and roadmap files before relying on them for execution. <br>


## Reference(s): <br>
- [Repo Onboarding Report Template](references/onboarding-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command blocks and generated JSON/Markdown repository documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates onboarding, roadmap, kanban, architecture, and dependency documentation in the target repository.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
