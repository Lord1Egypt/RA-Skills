## Description:

Tidal Lock helps agents analyze software architecture coupling, map unhealthy component dependencies, and recommend decoupling strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers, architects, and engineering teams use this skill during architecture reviews to identify tightly coupled components, understand coupling forces, and prioritize practical decoupling or consolidation decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to inspect project structure and git history, which may expose repository-sensitive design or history details.

Mitigation: Run it only in repositories the agent is authorized to inspect and limit analysis to relevant project files and history.

Risk: Coupling scores and decoupling recommendations may be incomplete if deploy relationships, failure data, or repository history are unavailable.

Mitigation: Review the generated analysis with project maintainers before using it to plan architecture changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcools1977/skills/tidal-lock)
- [ClawHub publisher profile](https://clawhub.ai/user/jcools1977)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown architecture analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include coupling scores, lock severity levels, affected component pairs, coupling trends, and decoupling recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
