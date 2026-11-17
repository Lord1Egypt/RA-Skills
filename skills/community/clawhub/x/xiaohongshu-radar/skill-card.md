## Description:

Searches public Xiaohongshu posts, retrieves post details, comments, creator posts and engagement metrics, and returns structured JSON for trend, competitor, creator and sentiment research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

Creators, brand teams and analysts use this skill to research public Xiaohongshu content, compare creators or competitors, and understand audience response. It requires a Guaikei API token and returns structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags possible privacy exposure when search keywords and links are sent to an external service or request details are shared with support; its analysis of 13 files is incomplete.

Mitigation: Review the privacy implications before installing, use only non-sensitive public-data queries, and check request details before sharing them with support.

## Reference(s):

- [Guaikei service](https://www.guaikei.com)
- [Routing guide](references/routing.md)
- [Request and output contract](references/contract.md)
- [Command options](references/options.md)
- [Error guide](references/errors.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured public post, comment and creator data; analysis may summarize trends, competitors and audience response.]

## Skill Version(s):

1.2.2 (source: evidence.release.version, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
