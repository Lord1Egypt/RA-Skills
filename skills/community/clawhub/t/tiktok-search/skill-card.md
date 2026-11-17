## Description:

Search TikTok videos, collect creator videos, retrieve detail data and comments for one known video, and run product, trend, competitor, and content insights through Gecho Bridge MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and social-media researchers use this skill to search TikTok, collect video and creator metadata, inspect one known video, and run product, trend, competitor, or content insight workflows through Gecho Bridge MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on a third-party MCP server and Chrome extension using the user's logged-in TikTok browser session.

Mitigation: Install and use it only when comfortable allowing that integration to read TikTok pages available in the browser session.

Risk: Search, video, and insight workflows can fail when Gecho Bridge MCP, the Chrome extension, or the TikTok browser session is not ready.

Mitigation: Confirm Node/npx, Gecho Bridge MCP, the logged-in Gecho Chrome extension, and an active logged-in TikTok tab before use.

Risk: Collected TikTok result sets may be saved locally.

Mitigation: Choose an appropriate save directory and handle generated files according to the user's data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gecho-ai/skills/tiktok-search)
- [Gecho website](https://gecho.ai/)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw setup video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes setup video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise summaries, setup commands, saved file paths, and bounded result samples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON result files produced by Gecho MCP tools; successful insight starts return a jobId for later status checks.]

## Skill Version(s):

1.1.38 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
