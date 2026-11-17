## Description:

Search YouTube Shorts by keyword with the official Gecho Bridge MCP tool and return ranked videos, engagement data, details, comments, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gecho-ai](https://clawhub.ai/user/gecho-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and social media teams use this skill to search YouTube Shorts by keyword through Gecho Bridge and review ranked videos with engagement data, comments, details, links, and saved result paths when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup examples install the Gecho Bridge MCP package through npx with an unpinned latest version.

Mitigation: Prefer a reviewed, exact package version or the managed bundle plugin, and re-review the MCP package before upgrades.

Risk: The workflow relies on the Gecho Chrome extension and a logged-in YouTube browser session.

Mitigation: Install only when the publisher is trusted, review extension permissions, and consider using a separate browser profile or account for research workflows.

Risk: YouTube login, CAPTCHA, consent, region, timeout, or enrichment failures can produce failed or partial results.

Mitigation: Resolve browser prompts manually before use and present partial-result or failure status explicitly instead of treating incomplete data as complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gecho-ai/skills/youtube-shorts-search)
- [Gecho Website](https://gecho.ai/)
- [Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)
- [Gecho Chrome Extension](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- [OpenClaw Setup Video](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- [Hermes Setup Video](https://www.youtube.com/watch?v=zHKnuWnxt_c)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and summarized MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report up to 20 ranked YouTube Shorts records from the MCP workflow and should summarize the most useful 3 to 5 items in chat.]

## Skill Version(s):

1.1.38 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
