## Description: <br>
Team Builder generates an OpenClaw multi-agent SaaS team workspace with role directories, inboxes, dashboards, product knowledge templates, cron checks, dual development tracks, onboarding, configurable models, and optional Telegram integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beyound87](https://clawhub.ai/user/beyound87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to bootstrap a persistent OpenClaw multi-agent team for SaaS product work, including coordination, growth, content, analysis, delivery, and full-stack implementation workflows. It is intended for users who want generated workspace files and scripts they can review before applying OpenClaw configuration and scheduled tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scripts can make persistent global OpenClaw configuration changes and create recurring cron jobs. <br>
Mitigation: Review apply-config.js and create-crons.sh or create-crons.ps1 before execution, back up ~/.openclaw/openclaw.json, and enable only the agents and jobs you need. <br>
Risk: Optional Telegram bot tokens may be stored in OpenClaw configuration. <br>
Mitigation: Configure Telegram integration only when needed, restrict token access, and rotate or remove tokens after testing. <br>
Risk: Deep Dive scans may store project code structure and operational details in the generated workspace. <br>
Mitigation: Run scans only on projects whose details may be stored in the workspace, and review generated product knowledge before sharing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/beyound87/team-builder) <br>
- [README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Coding Behavior Fallback](references/coding-behavior-fallback.md) <br>
- [Shared Templates](references/shared-templates.md) <br>
- [Soul Templates](references/soul-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Workspace files, Markdown instructions, JavaScript configuration scripts, and shell or PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates an OpenClaw workspace and reviewable scripts; applying configuration and cron jobs is a separate manual step.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
