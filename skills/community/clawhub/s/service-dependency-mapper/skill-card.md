## Description:

Auto-discover and map service dependencies from code, configs, and runtime data, then generate dependency graphs, identify critical paths, find single points of failure, and assess blast radius for each service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, SREs, and incident responders use this skill to map service dependencies, visualize architecture, identify fragile paths, and estimate blast radius before or during reliability planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discovery output can expose internal service names, URLs, connection strings, or deployment topology.

Mitigation: Run the skill only in the intended repository and Kubernetes context, and review generated maps before sharing them outside the approved team.

Risk: Dependency and blast-radius conclusions may be incomplete when code, configuration, runtime traffic, or cluster access is partial.

Mitigation: Validate proposed dependency graphs and critical paths with service owners, telemetry, and current deployment data before using them for incident or architecture decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/service-dependency-mapper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, code snippets, dependency graphs, diagram formats, tables, and analysis notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Mermaid, DOT, PlantUML, or D2 diagram text and blast-radius or architecture health tables.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
