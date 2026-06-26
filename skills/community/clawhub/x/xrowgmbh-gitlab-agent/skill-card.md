## Description: <br>
An agent for interacting with GitLab, including gitlab.com and self-hosted instances, without requiring GitLab DUO. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrowgmbh](https://clawhub.ai/user/xrowgmbh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to let an agent triage assigned GitLab issues and merge requests, create branches and merge requests, manage labels and comments, inspect pipelines, and use glab for GitLab API operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad GitLab write authority through the user's token. <br>
Mitigation: Use a least-privileged token, restrict access to intended projects, and require explicit review before pushes, merge requests, labels, comments, pipeline retries, assignments, issue closures, or other state-changing actions. <br>
Risk: Autonomous issue, merge request, label, comment, and pipeline actions can change project workflow state without strong user-control boundaries. <br>
Mitigation: Run the skill only in repositories where this level of automation is acceptable, keep the assignment guard in force, and review GitLab activity logs for agent-authored changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-gitlab-agent) <br>
- [GitLab Default Roles](https://docs.gitlab.com/user/permissions/#default-roles) <br>
- [CI Tools Label Component](https://ci-tools.xrow.de/Components/label) <br>
- [CI Tools Components Catalog for GitLab](https://ci-tools.xrow.de/) <br>
- [OpenClaw Creating Skills](https://docs.openclaw.ai/tools/creating-skills) <br>
- [xrow Public Skills Project](https://gitlab.com/xrow-public/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with GitLab CLI commands and GraphQL or REST examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the glab CLI and GITLAB_TOKEN for authenticated GitLab operations.] <br>

## Skill Version(s): <br>
1.58.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
