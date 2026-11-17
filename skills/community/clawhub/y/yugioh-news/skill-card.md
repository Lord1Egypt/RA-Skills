## Description:

This skill helps create a daily Beijing-time OpenClaw task that searches and summarizes the previous day's Yu-Gi-Oh! Japanese news in Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangrongyong](https://clawhub.ai/user/jiangrongyong)

### License/Terms of Use:


## Use Case:

OpenClaw users who follow Yu-Gi-Oh! Japanese news use this skill to schedule a daily summary of prior-day card reveals, rules updates, tournament information, and product release news. The scheduled task posts a concise Chinese summary to the current conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates an indefinite daily automated task that posts to the current conversation without documented limits or removal steps.

Mitigation: Before enabling it, confirm which account or profile the cron job runs under, how to list and remove the job, and whether the schedule should expire or require manual approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiangrongyong/skills/yugioh-news)
- [Publisher Profile](https://clawhub.ai/user/jiangrongyong)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and scheduled prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese news summaries in the current conversation when the scheduled task runs.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
