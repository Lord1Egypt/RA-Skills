## Description:

Rss Ai Reader helps agents set up RSS/Atom monitoring that fetches feeds, generates Chinese summaries with Claude or OpenAI, deduplicates items with SQLite, and sends updates through Feishu, Telegram, or email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benzema216](https://clawhub.ai/user/benzema216)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure recurring RSS and Atom feed monitoring, summarize new items with an LLM, and deliver concise updates to team or personal notification channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run code from an external GitHub repository that may not be pinned.

Mitigation: Review or pin the repository before installing, and run it in a virtual environment or container under a non-admin account.

Risk: The workflow uses LLM API keys and notification credentials for enabled delivery channels.

Mitigation: Provide only the credentials needed for enabled channels and avoid broad or privileged tokens.

Risk: Private RSS content may be sent to LLM and notification providers during summarization and delivery.

Mitigation: Avoid feeding sensitive private RSS content unless the user is comfortable with those providers receiving that data.

## Reference(s):

- [Configuration Guide](artifact/references/config_guide.md)
- [ClawHub Skill Listing](https://clawhub.ai/benzema216/skills/rss-ai-reader)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include feed configuration, scheduler settings, credential environment variables, and notification channel setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
