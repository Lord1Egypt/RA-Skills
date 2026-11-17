## Description:

Get TikTok video detail data and comments from a known TikTok video URL with the official Gecho Bridge MCP tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect available metadata, engagement context, comments, and replies for a specific TikTok video URL through Gecho Bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow grants Gecho's MCP server and Chrome extension access to a logged-in TikTok browser session.

Mitigation: Use it only with accounts and videos the user is authorized to access, and review the Gecho package and extension provenance before installation.

Risk: Raw collected TikTok metadata and comments may be saved locally when a save directory is available.

Mitigation: Choose an approved local save directory and handle exported JSON according to the user's data handling requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gecho-ai/skills/tiktok-video)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [Gecho Website](https://gecho.ai/)
- [OpenClaw Setup Video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes Setup Video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell command blocks and optional local JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided TikTok video URL, optional comment target count up to 200, and optional absolute save directory.]

## Skill Version(s):

1.1.38 (source: evidence release and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
