## Description:

Fetches web page content with local HTML parsing by default, optional remote cleanup through Jina Reader, content trimming, and configurable domain allowlisting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vimself](https://clawhub.ai/user/vimself)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve readable page content while preferring local parsing for privacy and using optional remote cleanup when token reduction is more important. It is useful for web research workflows that need plain text or JSON output with configurable length limits and domain controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted URL fetching can expose internal services or sensitive network-only content from the agent environment.

Mitigation: Run the skill in a network-restricted sandbox and configure an explicit domain allowlist before operational use.

Risk: Remote cleanup mode sends URL and page content through a third-party service.

Mitigation: Use local mode for sensitive URLs and avoid remote mode when page contents are confidential.

Risk: Unpinned dependencies can change parsing or request behavior over time.

Mitigation: Pin the requests and beautifulsoup4 dependency versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vimself/skills/smart-web-fetch-safe)
- [Publisher profile](https://clawhub.ai/user/vimself)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Plain text or JSON; remote mode may return Markdown-style cleaned content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is truncated by the max character setting; the default maximum is 10000 characters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
