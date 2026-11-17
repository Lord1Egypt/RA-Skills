## Description:

Guides agents through using Soulseek GUI and CLI options to search, download, share files, and chat over the peer-to-peer Soulseek network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[svidovich](https://clawhub.ai/user/svidovich)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to set up Soulseek access, search or download files, share selected directories, and communicate through public rooms or private chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Peer-to-peer downloads can expose users or agents to untrusted files.

Mitigation: Do not open or execute downloaded files unless they have been independently verified.

Risk: Sharing broad directories can disclose personal, owner, or partner data.

Mitigation: Share only narrow, dedicated directories and review contents before enabling uploads.

Risk: Soulseek account credentials may be handled through plaintext environment variables or command history.

Mitigation: Use a dedicated Soulseek account and password, and avoid storing credentials in persistent logs or shared shells.

Risk: Global CLI installation can affect the host environment.

Mitigation: Prefer an isolated or pinned CLI installation instead of a global npm install where practical.

## Reference(s):

- [SoulseekQt Downloads](https://www.slsknet.org/news/node/1)
- [soulseek-cli](https://github.com/aeyoll/soulseek-cli)
- [aioslsk](https://github.com/JurgenR/aioslsk)
- [ClawHub Skill Page](https://clawhub.ai/svidovich/skills/use-soulseek)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes peer-to-peer usage guidance for Soulseek GUI, soulseek-cli, and optional custom Python clients.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
