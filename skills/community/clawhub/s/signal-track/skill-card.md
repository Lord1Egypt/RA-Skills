## Description:

signal-track helps agents track persistent topics such as stocks, companies, AI, and policy events for recurring updates, trend monitoring, structured summaries, and recent-news lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas-acc](https://clawhub.ai/user/lucas-acc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use signal-track to create and manage persistent topic monitoring, retrieve followed topic feeds, search news cards, fetch article content, and produce decision-relevant summaries for fast-moving domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a YouNews API key on the command line and stores it in plaintext local configuration.

Mitigation: Use a disposable or low-privilege API key where possible, avoid pasting secrets into shell history, restrict permissions on the OpenClaw or legacy config file, and revoke or rotate the key if exposure is suspected.

## Reference(s):

- [signal-track ClawHub Skill Page](https://clawhub.ai/lucas-acc/skills/signal-track)
- [YouNews](https://younews.cn/)
- [YouNews API Base URL](https://younews.k.sohu.com/)
- [CLI Test Instructions](docs/testing/cli-test-instructions.md)
- [Security Checklist](docs/testing/security-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON-style text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a YouNews API key and local configuration before authenticated CLI commands can return topic, news card, or article data.]

## Skill Version(s):

0.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
