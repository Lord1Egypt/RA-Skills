## Description:

Finds well-funded crypto and web3 teams and helps agents build prospecting lists with verified individual Telegram contacts for outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shwchlorine](https://clawhub.ai/user/shwchlorine)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to research funded crypto and web3 startups, verify individual Telegram contacts, and maintain outreach lead lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects and stores individual Telegram handles for crypto prospecting.

Mitigation: Confirm privacy, platform, and anti-spam permissions before collection or retention, and limit stored contact data to the approved outreach scope.

Risk: The auto-hunt workflow can keep background hunters running persistently.

Mitigation: Disable the auto-hunt cron and HEARTBEAT instructions by default, and require explicit per-run limits plus current-user stop authority.

Risk: The artifact includes hard-coded personal filesystem paths for CSV storage.

Mitigation: Replace hard-coded paths with current workspace paths before running and review expected file writes.

## Reference(s):

- [Hunter Subagent Task Template](references/hunter-task.md)
- [Auto-Hunt Setup](references/auto-hunt-setup.md)
- [Crypto Contact Research Workflow](references/workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/shwchlorine/skills/web3-target-team-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command snippets and CSV row formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update crypto prospecting CSV rows when the user permits file writes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
