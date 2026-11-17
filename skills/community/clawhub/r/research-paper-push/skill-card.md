## Description:

Create scheduled research-paper alerts using OpenAlex and OpenClaw cron for journal, conference, or topic subscriptions, test queries, subscription management, and concise Chinese summaries of newly matched papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjuncher](https://clawhub.ai/user/zjuncher)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and research-support agents use this skill to monitor new papers by topic, journal, or conference, schedule daily OpenClaw cron alerts, and produce concise Chinese summaries of matching OpenAlex results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or remove scheduled OpenClaw cron jobs for recurring paper alerts.

Mitigation: Confirm the user wants scheduling changes before running add, update, or remove actions that affect cron jobs.

Risk: The skill stores subscription state and recipient identifiers in local data files.

Mitigation: Treat generated data/*.json files as local user data and exclude them from published skill artifacts.

Risk: Research topics are sent to OpenAlex when queries run.

Mitigation: Confirm the research topics are suitable for an external OpenAlex query and do not store tokens or private channel credentials in the skill folder.

## Reference(s):

- [OpenAlex API](https://api.openalex.org)
- [OpenAlex Works API](https://api.openalex.org/works)
- [ClawHub skill page](https://clawhub.ai/zjuncher/skills/research-paper-push)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text Chinese paper summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local subscription JSON under data/ and named OpenClaw cron jobs when scheduling is requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
