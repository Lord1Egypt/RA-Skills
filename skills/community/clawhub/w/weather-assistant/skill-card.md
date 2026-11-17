## Description:

Weather Assistant helps agents query wttr.in weather for configured cities, manage city settings, and produce scheduled daily WeChat weather pushes with a quote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryaction](https://clawhub.ai/user/jerryaction)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal automation users can use this skill to get on-demand weather summaries, maintain a configured city list, and receive a daily morning weather message through WeChat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run shell commands using user-editable city query values, creating command-injection risk.

Mitigation: Only use trusted city query values, avoid special shell characters in `query`, and prefer validating or URL-encoding city names before invoking weather requests.

Risk: The scheduled WeChat push can send content to configured recipients and reads a local quote file.

Mitigation: Confirm the daily WeChat cron job, recipient, account settings, and quote-file access before installation or use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown weather summaries with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query wttr.in, read a local quote file, and produce scheduled WeChat delivery content.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
