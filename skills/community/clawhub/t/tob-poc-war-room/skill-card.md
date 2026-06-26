## Description: <br>
POC war-room skill for ToB AI delivery. Use when a user needs to diagnose POC status, track pass rate, classify blockers, build a 48-hour closure plan, detect customer silence risk, generate daily POC war-room reports, or decide when a POC is ready to enter contract closing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[william202404](https://clawhub.ai/user/william202404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, delivery, PM, and technical teams use this skill to triage ToB POC health, classify blockers, plan the next 48 hours, choose customer follow-up actions, and decide whether a POC is ready to hand off to contract-closing diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence POC status, customer follow-up, escalation, and closing-readiness decisions, so unsupported inputs may lead to misleading commercial guidance. <br>
Mitigation: Require concrete POC objective, acceptance criteria, pass rate, blocker ownership, customer feedback or silence duration, and procurement-path evidence before using the report for customer-facing action. <br>
Risk: Server security guidance recommends installation only where the user trusts repo-local tools and understands the effects of maintainer-context commands. <br>
Mitigation: Install in a trusted ClawHub/Convex maintainer context, verify write targets before actions, and keep confirmation steps enabled for commands that affect repositories or releases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/william202404/tob-poc-war-room) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown report with tables, prioritized action lists, customer communication guidance, escalation guidance, and closing-trigger assessment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also emit Node.js CLI usage commands for generating the report from structured POC inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
