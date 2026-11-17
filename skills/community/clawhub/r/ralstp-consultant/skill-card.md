## Description:

Analyzes complex multi-actor planning problems with RALSTP concepts to identify agents, dependencies, landmarks, difficulty, and decomposition options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thedragosexperience](https://clawhub.ai/user/thedragosexperience)

### License/Terms of Use:


## Use Case:

External users, developers, and planners use this skill to analyze multi-step workflows with multiple actors, dependencies, resource contention, or complex orchestration needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formal PDDL difficulty scores may be rough heuristics rather than precise implementations of the thesis metric.

Mitigation: Use the scores as advisory signals and review the underlying agent, dependency, and landmark analysis before making operational decisions.

Risk: Planning recommendations for sensitive or complex operations may be incomplete or misleading if applied without domain review.

Mitigation: Have a knowledgeable reviewer validate the output before applying it to sensitive operational plans.

## Reference(s):

- [Road Traffic Accident Management PDDL instances](https://github.com/potassco/pddl-instances/tree/master/ipc-2014/domains/road-traffic-accident-management-temporal-satisficing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with optional shell command guidance for local PDDL analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include conceptual planning analysis or heuristic PDDL analysis results; review outputs before applying them to sensitive operational plans.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
