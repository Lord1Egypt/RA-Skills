## Description:

Provides agent access to SiYuan Note for reading, searching, writing, syncing conversations, creating documents, clipping articles, and rendering note templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jueduilunhui](https://clawhub.ai/user/jueduilunhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to let an agent search, read, create, and update SiYuan notes. It supports conversation syncing, standalone document creation, article clipping, and template-rendered note content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can read from and write to the configured SiYuan workspace, including synced conversation content.

Mitigation: Use only a workspace intended for agent access, avoid syncing secrets or full private transcripts, and review generated note changes.

Risk: Auto-sync behavior may move private conversation data into SiYuan without enough review.

Mitigation: Keep auto-sync disabled unless explicitly needed and scope synced content to reviewed summaries or approved messages.

Risk: Security evidence flags credential-bearing debug or test scripts in the package.

Mitigation: Remove or ignore debug and test scripts unless exposed tokens have been rotated and the package has been cleaned.

Risk: The SiYuan API token grants authenticated access to note data.

Mitigation: Prefer SIYUAN_API_TOKEN from the environment, avoid committing tokens in config files, and rotate tokens after accidental exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jueduilunhui/skills/siyuan-note-enhanced)
- [SiYuan Chrome extension](https://github.com/siyuan-note/siyuan-chrome)
- [SiYuan API documentation](https://github.com/siyuan-note/siyuan/blob/master/API.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, a running SiYuan API, and SIYUAN_API_TOKEN for authenticated note operations.]

## Skill Version(s):

2.0.0 (source: server release metadata, _meta.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
