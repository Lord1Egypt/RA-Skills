## Description:

Compatibility entry for existing SignalDig social-research users that routes social-data requests to the unified research-growth-signals Skill and its research_social_signals tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerrykik](https://clawhub.ai/user/jerrykik)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this compatibility entry to preserve existing social-research workflows while routing requests through the maintained SignalDig Growth Research Skill. It is useful during migration from legacy social-platform-specific tooling to the unified research_social_signals tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Actual data access, spend, and budget behavior depend on the referenced research-growth-signals skill and unified SignalDig MCP rather than this compatibility entry.

Mitigation: Review and approve the referenced research-growth-signals skill and unified SignalDig MCP before using this entry for sensitive or paid social research.

Risk: If the maintained SignalDig skill or MCP connection is unavailable, attempts to continue with legacy platform tools or simulated results could mislead users.

Mitigation: Stop and tell the user to install or update the unified SignalDig skill and connection; do not fall back to legacy social-platform-specific tools or simulate results.

## Reference(s):

- [SignalDig homepage](https://signaldig.com/)
- [ClawHub skill page](https://clawhub.ai/jerrykik/skills/research-social-signals)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown or text guidance that delegates to the maintained research-growth-signals skill and unified research_social_signals tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No independent MCP contract, setup guide, parameter guide, execution examples, or executable code are shipped by this compatibility entry.]

## Skill Version(s):

1.6.8 (source: server release evidence, skill frontmatter, metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
