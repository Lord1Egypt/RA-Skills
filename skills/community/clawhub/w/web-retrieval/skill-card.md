## Description:

Expert web fetching and crawling using Scrapling for web retrieval tasks, JS-rendered pages, anti-bot sites, bulk URL fetching, and site crawling with static GET, browser automation, stealth mode, and checkpoint/resume support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanford](https://clawhub.ai/user/seanford)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch individual pages, extract text or HTML with selectors, and crawl URL lists or same-domain sites when normal web retrieval is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch and crawl URLs through the host network, including internal, localhost, private-network, cloud metadata, or token-bearing URLs if directed there.

Mitigation: Restrict target URLs to intended public destinations and avoid sensitive network locations unless that access is explicitly authorized.

Risk: Fetched or crawled remote content can be written to local output paths.

Mitigation: Direct output only to approved temporary or workspace paths and treat retrieved content as untrusted until reviewed.

Risk: Stealth and challenge-solving modes may retrieve sites that actively discourage automated access.

Mitigation: Use stealth features only where automated retrieval is permitted and consistent with the target site's terms and policy requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seanford/skills/web-retrieval)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, Shell commands, Code, Guidance]

**Output Format:** [Markdown, plain text, raw HTML, JSON crawl results, shell commands, and Python usage examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch output can be returned on stdout or written to a local file; crawl output can be written as per-page Markdown files or a single JSON array.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
