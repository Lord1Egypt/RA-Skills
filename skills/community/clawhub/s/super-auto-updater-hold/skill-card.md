## Description: <br>
Ensures Clawdbot and installed skills stay current by configuring automated update checks and clear update summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to set up scheduled updates for Clawdbot and installed skills, including summaries of version changes and failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended daily updates can change Clawdbot or installed skills without manual review. <br>
Mitigation: Use the dry-run command first, choose an intentional schedule and timezone, keep a rollback plan, and install only when unattended updates are desired. <br>
Risk: Updating all installed skills can pull changes from skills that are outside the user's current trust boundary. <br>
Mitigation: Limit updates to trusted skills where possible and review delivered summaries for changed versions and failures. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>
- [ClawHub Skill Page](https://clawhub.ai/subaru0573/skills/super-auto-updater-hold) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions, cron configuration, optional helper script guidance, and update summary formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
