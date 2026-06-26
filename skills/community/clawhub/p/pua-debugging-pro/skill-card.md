## Description: <br>
Professional anti-giveup debugging protocol for coding tasks where the agent starts looping, deflecting to users, or trying to end early without evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Doraemon-Claw](https://clawhub.ai/user/Doraemon-Claw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill during repeated debugging failures to enforce evidence-first diagnosis, bounded escalation, explicit verification, and clear blocked-state reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent debugging and may lead an agent to run checks, propose changes, or continue work longer than expected. <br>
Mitigation: Keep normal approval boundaries for production changes, secrets, network access, and commands that modify the environment; review proposed changes and validation results before relying on them. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/Doraemon-Claw/pua-debugging-pro) <br>
- [Checklist & Report Templates](references/checklist-template.md) <br>
- [Postmortem One-Pager](assets/postmortem-onepager.md) <br>
- [Upstream Inspiration](https://github.com/tanweai/pua) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown progress updates, escalation reports, checklists, and recommended validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Markdown-only workflow; no hidden code, persistence, or unusual permissions identified by the security review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
