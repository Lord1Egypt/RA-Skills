## Description:

The Skill Base CLI skill guides agents to use the `skb` command to search, install, update, publish, import from GitHub, and configure Skill Base skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ginuim](https://clawhub.ai/user/ginuim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Skill Base through the `skb` CLI, including configuring a server URL, searching for skills, installing or updating skills, publishing local skill folders, and importing public GitHub-hosted skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install or run an unpinned npm CLI that can change installed skills.

Mitigation: Use a pinned and verified `skill-base-cli` version, avoid global installation where possible, and confirm target directories before any install or update.

Risk: Publishing commands can upload local skill content to the configured Skill Base server.

Mitigation: Confirm the server URL, login state, and exact local folder contents before running `skb publish`.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ginuim/skills/skill-base-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command-oriented guidance for installing, configuring, updating, publishing, and troubleshooting Skill Base CLI usage.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
