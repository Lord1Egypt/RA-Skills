## Description:

Automates a Notion-to-X/Twitter posting pipeline by pulling approved tweets from a Notion database, scheduling one-shot cron jobs, and posting through the X/Twitter API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:


## Use Case:

External developers and social content operators use this skill to manage approved posts in a Notion content calendar, schedule precise posting times, and publish text-only tweets while tracking status back in Notion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local credential files and uses 1Password/OpenClaw credentials.

Mitigation: Install only in an environment where those credential sources are intentionally available, and use least-privilege Notion and X/Twitter credentials.

Risk: The skill can create scheduled OpenClaw cron jobs and post publicly to the configured X/Twitter account.

Mitigation: Review the Notion queue, account configuration, scheduled times, and generated cron jobs before enabling posting; use the dry-run mode for operational checks.

Risk: The skill modifies the configured Notion database while tracking posted or failed tweets.

Mitigation: Test against a staging Notion database or backup the production database before first use.

Risk: The security summary reports undocumented credential sources and hard-coded out-of-package execution paths.

Mitigation: Fix the documentation/authentication mismatch and replace hard-coded external paths with package-relative or user-configurable paths before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/tweet-pipeline)
- [Notion database query endpoint used by the artifact](https://api.notion.com/v1/databases/{TWEET_DB}/query)
- [X/Twitter tweet creation endpoint used by the artifact](https://api.x.com/2/tweets)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to run Python scripts that read a Notion tweet queue, schedule one-shot OpenClaw cron jobs, post text tweets to X/Twitter, and update Notion status fields.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
