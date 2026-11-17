## Description:

Guides an agent to trace a decision's downstream effects, including actor responses, feedback loops, reversals, and uncertainty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to analyze consequential decisions whose immediate effects are clear but downstream effects are uncertain. It guides the agent through a consequence cascade that considers other actors, affected groups, reversals, and confidence limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to fetch changing remote instructions automatically, so behavior may change between runs without a user review step.

Mitigation: Prefer a version that keeps runtime instructions local, make update checks optional, and review changes before adopting them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/deciqai/skills/second-order-thinking)
- [Sources — second-order-thinking](references/sources.md)
- [Howard Marks, I Beg to Differ](https://www.oaktreecapital.com/insights/memo/i-beg-to-differ)
- [International Energy Agency, Electricity 2024](https://www.iea.org/reports/electricity-2024)
- [Stack Overflow 2024 Developer Survey](https://survey.stackoverflow.co/2024/)
- [US Prohibition worked example](examples/us-prohibition-1920.md)
- [Hanoi Rat Bounty worked example](examples/hanoi-rat-bounty-1902.md)
- [AI Buildout worked example](examples/ai-buildout-power-and-code-2024-2026.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a structured consequence cascade and confidence notes.]

## Skill Version(s):

1.0.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
