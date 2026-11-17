## Description:

Fetches follower counts and social media metrics from supported platforms using profile URLs or nicknames, including Bilibili, YouTube, TikTok, Instagram, Douyin, Kuaishou, Xiaohongshu, and others.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoming0000](https://clawhub.ai/user/guoming0000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve follower counts and account metrics from supported social media profiles by URL or nickname. The agent can run the packaged script, parse the returned JSON, and present the result in a concise user-facing response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist an authenticated Xiaohongshu browser session in a local Chrome profile.

Mitigation: Use an isolated environment or throwaway account and clear ~/.playwright_cdp_profile after use.

Risk: The skill exposes a local browser control port while using Chrome DevTools Protocol mode.

Mitigation: Run it only in a trusted local environment and close the browser session after the metrics request completes.

Risk: URL handling may allow the browser to open URLs outside the intended social platforms until hostname validation is fixed.

Mitigation: Avoid running the skill against untrusted URLs and prefer known profile URLs for supported platforms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoming0000/skills/social-media-metrics)
- [Artifact README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON from the metrics script, typically summarized by the agent as Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require network access, Playwright browser execution, an optional YouTube API key, and a persistent local Chrome profile for Xiaohongshu.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
