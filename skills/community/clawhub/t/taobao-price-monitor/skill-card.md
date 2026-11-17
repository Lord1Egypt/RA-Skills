## Description:

Taobao Price Monitor helps agents query Taobao/Tmall product prices from item URLs, while server security evidence notes that the current artifact provides basic price lookup rather than the full monitoring, alerting, history, and comparison system described.

This skill is for research and development only.

## Publisher:

[275254cl-hash](https://clawhub.ai/user/275254cl-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up Taobao/Tmall item price details from product URLs and to draft lightweight price-checking workflows. The artifact should be treated as a basic lookup helper, with claimed monitoring, alerting, history, export, and comparison features requiring verification before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests TAOBAO_COOKIE, which may expose account access if reused from a sensitive Taobao session.

Mitigation: Use a dedicated low-risk Taobao session, store the cookie only in the intended local environment, and rotate or revoke it after testing.

Risk: The public description claims monitoring, alerts, history, comparison, export, and API features that are not fully present in the current artifact.

Mitigation: Treat the artifact as a basic price lookup helper until each claimed workflow is independently verified.

Risk: Local API access or exported price data could expose shopping activity or monitored product lists.

Mitigation: Keep any local API bound to the local machine and avoid sharing exported data unless it has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/275254cl-hash/skills/taobao-price-monitor)
- [Publisher profile](https://clawhub.ai/user/275254cl-hash)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON price result examples and shell/configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require python3, requests, curl, and an optional TAOBAO_COOKIE value for some requests.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
