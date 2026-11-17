## Description:

Scan trending stocks and crypto movers with live AISA market signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and market-focused agents use this skill to scan current stock and crypto momentum, top movers, and news-driven market activity. The output is informational only and not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An undocumented endpoint override can redirect the AISA_API_KEY to another server.

Mitigation: Use the default AISA endpoint unless a trusted AISA-compatible endpoint is intentionally configured.

Risk: Runtime behavior can vary if dependencies are installed from an unpinned version range.

Mitigation: Prefer a release that pins dependencies before deploying in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/stock-hot-aisa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with optional JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; can focus on stocks, crypto, or both.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
