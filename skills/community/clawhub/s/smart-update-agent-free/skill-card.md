## Description: <br>
Checks for and applies updates to an agent runtime and installed skills, then reports version changes, update summaries, and basic troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, small teams, and automation operators use this skill to schedule or manually run update checks for agent runtimes and installed skills, review version-change summaries, and perform basic health checks after updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring unattended updates can change the agent runtime and installed skills without a full review, approval, or rollback workflow. <br>
Mitigation: Start with check-only or manual updates, review changelogs before applying changes, keep backups or a rollback plan, and avoid production or shared environments without a maintenance window. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thcjp/skills/smart-update-agent-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, cron configuration, update summaries, and troubleshooting steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose recurring unattended update workflows; users should review changes and keep a rollback plan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
