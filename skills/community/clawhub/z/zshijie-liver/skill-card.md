## Description:

Resolves supported Z视介 live TV channel requests or common program aliases to the correct channel ID and returns a Markdown link to the live page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jkbwfi](https://clawhub.ai/user/jkbwfi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to open supported Z视介 live channels by channel name, channel ID, or common aliases such as 跑男 and 奔跑吧 that map to 浙江卫视.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may open the default browser automatically when resolving a live channel.

Mitigation: Use or request --no-open when only a Markdown response, JSON result, or link is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jkbwfi/skills/zshijie-liver)
- [Channel/cid mapping](artifact/references/channel_map.md)
- [Z视介 live page URL template](https://zmtv.cztv.com/cmsh5-share/prod/cztv-tvLive/index.html?pageId={cid})

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Short Markdown card with a clickable live-page link; the helper script can also emit JSON or a URL-only string.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Resolves fixed channel and cid mappings for supported Z视介 live channels and may open the default browser unless disabled.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
