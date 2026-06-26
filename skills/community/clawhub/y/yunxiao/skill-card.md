## Description: <br>
Helps an agent manage Yunxiao project work items, including listing projects, viewing work items, and creating or updating tasks, requirements, defects, and risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengerzh](https://clawhub.ai/user/fengerzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, project managers, and delivery teams use this skill through an agent to query Yunxiao projects and work items, then create or update work items after choosing the target project. It is intended for users who can provide an appropriate Yunxiao organization ID, user ID, and personal access token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a stored Yunxiao access token to read and modify project data. <br>
Mitigation: Use a least-privilege token, keep config.json out of source control, and rotate the token if it is exposed. <br>
Risk: Create and update actions can change project work items when triggered by broad project-management requests. <br>
Mitigation: Require explicit user confirmation before running any create or update action, including the target project and work item changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengerzh/yunxiao) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text or JSON returned by Python CLI scripts, with Markdown command examples in the skill guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local config.json values for Yunxiao organization ID, user ID, token, and optional default project settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
