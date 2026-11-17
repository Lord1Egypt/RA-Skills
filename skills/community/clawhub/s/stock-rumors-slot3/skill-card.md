## Description:

Rumor Scanner - find early signals including M&A rumors, insider activity, analyst upgrades and downgrades, social whispers, and SEC or regulatory activity via the AIsa API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market analysts use this skill to scan for early public-market signals, rank the top findings by impact score, and generate an analyst note. Results are informational only and are not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the AIsa API key to an arbitrary endpoint if AISA_BASE_URL is set.

Mitigation: Use the default trusted AIsa API endpoint unless an alternate endpoint has been reviewed, and run the skill only with an AIsa API key appropriate for this tool.

Risk: Market rumors and early signals may be unconfirmed or misleading.

Mitigation: Treat outputs as informational, verify claims against primary sources before acting, and do not rely on the skill as financial advice.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/aisadocs/skills/stock-rumors-slot3)
- [ClawHub publisher profile](https://clawhub.ai/user/aisadocs)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report with optional JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks the top five signals by impact score and includes evidence quality labels plus an analyst note.]

## Skill Version(s):

1.0.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
