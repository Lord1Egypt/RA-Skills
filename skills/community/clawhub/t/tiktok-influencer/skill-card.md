## Description:

Collect public videos from a TikTok creator with Gecho Bridge MCP. Returns video metadata, captions, engagement metrics, publish times, and links. Requires the Gecho Chrome extension, an active TikTok session, and the Gecho Bridge MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect and summarize public TikTok creator video data through the Gecho Bridge MCP workflow. It is suited for creator research, influencer review, and recent posting analysis when the user has the required Gecho extension, Gecho account, TikTok browser session, and MCP server configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow relies on the Gecho Chrome extension, a logged-in Gecho account, an active TikTok browser session, and the Gecho Bridge MCP server.

Mitigation: Confirm those prerequisites before installation or use, and resolve any login, CAPTCHA, verification, region, cookie, or blocked-page prompts manually in Chrome before running the tool.

Risk: Saved JSON exports may contain creator metadata, captions, links, and engagement metrics.

Mitigation: Treat saved exports as local data files and store or share them according to the user's data-handling requirements.

Risk: The tool may fail, time out, or return no collectable videos when prerequisites are missing or the TikTok page is not usable.

Mitigation: Report the exact failure state, avoid inventing results, and follow the documented setup and troubleshooting guidance before retrying in a later turn.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gecho-ai/skills/tiktok-influencer)
- [Gecho Website](https://gecho.ai/)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw Setup Video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes Setup Video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and summarized JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs should summarize only the most useful creator-video fields, include the total count and saved file path when available, and avoid pasting full raw JSON into chat.]

## Skill Version(s):

1.1.38 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
