## Description: <br>
Real-time web dashboard for OpenClaw sessions and background tasks. Mobile-responsive with auto-refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jorgermp](https://clawhub.ai/user/jorgermp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw sessions, sub-agents, Discord activity, and cron jobs through a local web dashboard and status API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An unauthenticated local or LAN-accessible dashboard can expose OpenClaw session metadata and prompt-derived task descriptions. <br>
Mitigation: Run the dashboard on localhost only, behind authentication, or on a trusted isolated network. <br>
Risk: Session prompts may contain secrets, customer data, internal instructions, or other sensitive content. <br>
Mitigation: Avoid using this skill with sensitive sessions, or redact sensitive task descriptions before exposing the dashboard. <br>


## Reference(s): <br>
- [Task Monitor ClawHub Page](https://clawhub.ai/jorgermp/task-monitor) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Web dashboard HTML, JSON API responses, Markdown dashboard files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dashboard refreshes periodically and may return cached status data.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter, package.json, and changelog report 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
