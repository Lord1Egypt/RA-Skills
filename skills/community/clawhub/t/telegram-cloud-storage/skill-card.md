## Description:

Telegram Cloud Storage uses Teldrive to turn Telegram into cloud storage with a local API and web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oki3505f](https://clawhub.ai/user/oki3505f)

### License/Terms of Use:


## Use Case:

Developers and technical users use this skill to install and operate a local Teldrive service that stores, lists, uploads, downloads, renames, and deletes files backed by Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads and runs an unverified prebuilt Teldrive executable from GitHub.

Mitigation: Review the upstream release and source before installation, pin expected hashes where possible, and install only in an isolated environment you trust.

Risk: The skill handles Telegram API, database, JWT, token, and session credentials.

Mitigation: Use a dedicated database user, generate a strong new JWT secret, restrict permissions on config and token files, and avoid running the service as root.

Risk: Agent-triggered file operations can upload, download, delete, or rename storage objects.

Mitigation: Review commands before execution and limit agent access to credentials and storage scopes appropriate for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oki3505f/skills/telegram-cloud-storage)
- [Teldrive project](https://github.com/tgdrive/teldrive)
- [Teldrive 1.8.0 binary release download](https://github.com/tgdrive/teldrive/releases/download/1.8.0/teldrive-1.8.0-linux-amd64.tar.gz)
- [Telegram API credentials](https://my.telegram.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash and Python command examples, plus JSON responses from the local client.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included client can call a local Teldrive API when the service and credentials are configured.]

## Skill Version(s):

1.8.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
