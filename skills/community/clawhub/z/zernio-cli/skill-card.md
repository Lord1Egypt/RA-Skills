## Description:

Schedule and manage social media posts across 14 platforms from the CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikipalet](https://clawhub.ai/user/mikipalet)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agents use this skill to operate the Zernio CLI for social account discovery, profile management, post scheduling, post status checks, analytics retrieval, and media upload workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can create, schedule, retry, or delete social media posts through the user's Zernio account.

Mitigation: Use a tightly scoped API key and require confirmation of profile, account, and post IDs before publishing, retrying, or deleting content.

Risk: API credentials may be stored in ~/.zernio/config.json or provided through environment variables.

Mitigation: Keep the config file private, use secret-management controls for ZERNIO_API_KEY, and rotate keys if they may have been exposed.

Risk: Custom API URLs and media uploads can send credentials or selected local files to external endpoints.

Mitigation: Use only trusted HTTPS API URLs and verify local media paths before uploading files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikipalet/skills/zernio-cli)
- [Zernio documentation](https://docs.zernio.com)
- [Zernio website](https://zernio.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; CLI command results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZERNIO_API_KEY for authenticated API access; browser login or auth:set may store credentials in ~/.zernio/config.json.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
