## Description:

Fetches static web pages, extracts the main content, and converts HTML to Markdown with optional JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuxiangfanclaw](https://clawhub.ai/user/shuxiangfanclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve article-like content from blogs, news pages, announcements, and similar static web pages, then return cleaned Markdown or structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs reachable from the user's machine or agent runtime.

Mitigation: Use it only on sites you are authorized to access, and do not allow untrusted content to choose target URLs.

Risk: Stealth mode is intended to bypass anti-bot protections without clear safeguards.

Mitigation: Avoid stealth mode unless you have explicit permission and the target site's terms permit this access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuxiangfanclaw/skills/scrapling-fetch-basic)
- [Publisher profile](https://clawhub.ai/user/shuxiangfanclaw)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown text by default, or pretty-printed JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a URL, optional maximum character count, basic or stealth fetch mode, JSON output, and debug output.]

## Skill Version(s):

1.0.0 (source: frontmatter, metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
