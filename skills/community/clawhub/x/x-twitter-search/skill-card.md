## Description:

Search X/Twitter in real-time using Grok or X API. Find tweets, trends, and discussions with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueberrywoodsym](https://clawhub.ai/user/blueberrywoodsym)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to search recent public X/Twitter posts, trends, and discussions from an agent workflow, with optional time, handle, exclusion, JSON, compact, and links-only controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an xAI or X API credential to make search requests.

Mitigation: Install it only in environments where using that credential for X/Twitter search is acceptable, and keep API keys out of committed files and shared logs.

Risk: Manual installation from an unpinned repository can run code different from the reviewed release.

Mitigation: Prefer the ClawHub install path or a pinned reviewed commit.

## Reference(s):

- [xAI Documentation](https://docs.x.ai)
- [xAI Console](https://console.x.ai)
- [X Developer Console](https://console.x.com)
- [ClawHub Skill Page](https://clawhub.ai/blueberrywoodsym/skills/x-twitter-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted search results, plain links, or JSON depending on command options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can include tweet text, usernames, dates, links, citations, and X API engagement metrics.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
