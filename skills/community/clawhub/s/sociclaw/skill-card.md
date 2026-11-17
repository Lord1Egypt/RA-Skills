## Description:

An autonomous social media manager agent that researches, plans, and posts content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sociclaw](https://clawhub.ai/user/sociclaw)

### License/Terms of Use:


## Use Case:

External users and teams use Sociclaw to plan X/Twitter content, generate posts and optional image prompts, and sync draft workflows to Trello or Notion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional image, provisioning, and top-up flows can send credentials and image data to configurable endpoints.

Mitigation: Use only trusted HTTPS endpoints for image, provisioning, and top-up APIs, and install the skill in an isolated environment with trusted configuration.

Risk: Provisioned API keys and wallet-related state may be stored locally without strong protections.

Mitigation: Protect local state files, rotate provisioned API keys if state may have been exposed, and avoid sharing runtime directories.

Risk: Image input settings can broaden which local or remote images are sent to the configured image API.

Mitigation: Keep image input directories narrow, leave remote logo URL fetching disabled unless needed, and require an allowlist for remote image hosts.

Risk: The USDC top-up workflow can direct users to send funds through the configured payment flow.

Mitigation: Review the top-up endpoint, deposit address, exact amount, and transaction flow before sending funds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sociclaw/skills/sociclaw)
- [SociClaw website](https://sociclaw.com)
- [README](artifact/README.md)
- [Skill contract](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown responses with inline commands and local JSON, Markdown, SQLite, and image files when features are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local runtime state, content plans, brand profiles, persistent memory, generated image backups, and top-up session state.]

## Skill Version(s):

0.1.9 (source: server release metadata, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
