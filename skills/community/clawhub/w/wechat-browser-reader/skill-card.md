## Description:

Read WeChat Official Account articles (mp.weixin.qq.com) via Chrome DevTools browser automation when HTTP-based extractors fail due to captcha, JavaScript encryption, or anti-scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmlgit](https://clawhub.ai/user/zmlgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve, summarize, or present WeChat Official Account article content through a real Chrome browser when direct HTTP extraction is blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chrome remote debugging allows powerful control over the connected browser session.

Mitigation: Use a temporary Chrome debugging profile on a trusted machine and avoid connecting the skill to personal logged-in browser sessions.

Risk: Leaving the debug browser open can expose continued browser automation access.

Mitigation: Close the debug browser when extraction is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmlgit/skills/wechat-browser-reader)
- [Publisher profile](https://clawhub.ai/user/zmlgit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with article fields, extracted text, and optional browser setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include title, author, content length, full article text, summaries, troubleshooting steps, and Chrome remote debugging setup guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
