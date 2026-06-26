## Description: <br>
Automatically update Clawdbot and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-din](https://clawhub.ai/user/a-din) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and developers use this skill to configure a recurring Clawdbot cron job that updates Clawdbot and installed skills, then reports what changed. It is intended for environments where automatic agent and skill updates are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent scheduled job can change Clawdbot and every installed skill without per-update approval. <br>
Mitigation: Start with dry-runs or manual approval, restrict updates to trusted or pinned sources, review update summaries, and confirm the cron job can be disabled before enabling it. <br>
Risk: Update summaries or logs may expose version, package, or error details to configured delivery channels. <br>
Mitigation: Choose delivery destinations carefully and keep summaries local when update details may be sensitive. <br>
Risk: Automatic updates may fail partially because of permissions, network failures, package conflicts, or source checkout issues. <br>
Mitigation: Review reported failures, run Clawdbot diagnostics, and resolve partial update issues manually before relying on unattended operation. <br>


## Reference(s): <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cron setup, update commands, verification steps, troubleshooting guidance, and summary-message formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
