## Description:

XiaChat CLI helps agents guide command-line use of XiaChat for SOUL profile management, personality matching, AI avatar pre-chat, Soul Square persona chat, JSON output, and scriptable workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhijun](https://clawhub.ai/user/lizhijun)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they want an agent to provide XiaChat CLI setup guidance, command examples, and workflow steps for personality profiles, matching, avatar pre-chat, persona chat, and credit checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance installs an unpinned global npm CLI.

Mitigation: Install in a least-privileged or isolated environment and pin or verify the npm package before global installation.

Risk: Using the CLI can send selected SOUL profiles, imported chat transcripts, match interactions, and API-authenticated requests to XiaChat services.

Mitigation: Avoid importing conversations without consent, limit sensitive data, and confirm that the user is comfortable sending the selected data to XiaChat.

Risk: The workflow requires a XiaChat API key.

Mitigation: Store the API key securely, avoid exposing it in shared shell history or logs, and rotate it if disclosure is suspected.

## Reference(s):

- [ClawHub XiaChat CLI skill page](https://clawhub.ai/lizhijun/skills/xiachat-cli)
- [XiaChat home](https://xiachat.com)
- [XiaChat Soul Square](https://xiachat.com/square)
- [XiaChat SOUL profiles](https://xiachat.com/soul)
- [XiaChat match center](https://xiachat.com/match)
- [XiaChat API settings](https://xiachat.com/settings/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance commonly includes API key setup, npm installation commands, XiaChat CLI command examples, and jq-compatible JSON workflow snippets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
