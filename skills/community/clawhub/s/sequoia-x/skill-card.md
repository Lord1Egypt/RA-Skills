## Description:

Sequoia-X helps agents install, configure, and run an A-share quantitative stock-screening workflow with AkShare data, SQLite storage, and Feishu notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djh06](https://clawhub.ai/user/djh06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to set up Sequoia-X, run A-share stock-screening strategies, adjust strategy parameters, and configure Feishu webhook notifications. Outputs should be reviewed as screening signals rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer clones and later runs code from a mutable upstream GitHub repository.

Mitigation: Review the upstream repository before use and pin a reviewed commit or release instead of relying on the moving default branch.

Risk: Python dependencies are installed without exact version pins.

Mitigation: Install in a dedicated virtual environment or container and record reviewed dependency versions for repeatable deployments.

Risk: The Feishu webhook is a sensitive notification endpoint.

Mitigation: Store the webhook outside shared logs or public files, rotate it if exposed, and restrict access to the generated .env file.

Risk: The debug reset workflow can delete the local SQLite market database.

Mitigation: Back up the SQLite database before reset or full-resync commands.

## Reference(s):

- [Strategy Details](references/strategies.md)
- [Sequoia-X upstream repository cloned by installer](https://github.com/sngyai/Sequoia-X.git)
- [ClawHub skill page](https://clawhub.ai/djh06/skills/sequoia-x)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, run, debugging, Feishu webhook configuration, and strategy-tuning guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
