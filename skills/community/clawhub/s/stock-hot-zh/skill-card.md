## Description:

Scans real-time unusual activity in popular stocks and crypto assets through AISA for market momentum, top movers, and news-driven moves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and market analysts use this skill to ask an agent for current hot stocks, crypto movers, momentum summaries, and news-driven market activity. The output is informational and is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An undocumented AISA_BASE_URL setting can redirect requests that carry the AISA_API_KEY.

Mitigation: Keep AISA_BASE_URL unset unless the alternate endpoint is intentionally trusted, and use a narrowly scoped key with spending or usage limits.

Risk: Market reports can be incomplete, stale, or mistaken and may be misread as trading advice.

Mitigation: Treat outputs as informational only and verify important financial decisions against independent, authoritative market data.

Risk: Running the skill from an untrusted shell, wrapper, or CI environment can expose the configured AISA key.

Mitigation: Run it only in trusted environments and avoid passing production credentials through untrusted automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/stock-hot-zh)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown report with tables and an optional compact JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; supports stocks, crypto, or both as the scan focus.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
