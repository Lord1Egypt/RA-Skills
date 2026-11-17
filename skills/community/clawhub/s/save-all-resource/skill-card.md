## Description:

Opens a visible browser so the user can manually browse a target website while same-origin raw response resources are continuously saved to a local Desktop directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnoder-wgh](https://clawhub.ai/user/cnoder-wgh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to archive same-domain website resources during manual browser exploration for authorized inspection, debugging, or preservation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A visited site could cause writes outside the intended Desktop folder.

Mitigation: Use only trusted or authorized sites and review path containment before using the skill on untrusted websites.

Risk: Raw captured responses may include sensitive information from logged-in or private browsing sessions.

Mitigation: Avoid sensitive sessions and review saved output before sharing or retaining it.

Risk: Continuous capture can consume large amounts of disk space or memory.

Mitigation: Monitor disk usage, close the browser tab to stop capture, and add capture quotas before extended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnoder-wgh/skills/save-all-resource)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Local files with terminal status logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves same-origin HTTP and HTTPS responses under a Desktop directory named for the target domain.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
