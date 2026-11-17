## Description:

Unified World Model fuses text, code, vision-label, and tool-state observations into a grounded state for cross-modal consistency checks, deterministic simulation, forward prediction, and counterfactual analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to combine text, code, vision-label, and tool-state evidence into a shared grounded state for planning, simulation, consistency checking, and what-if analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local learning logs may store usage counts, error notes, and preferences in learned_patterns.json.

Mitigation: Do not record secrets or sensitive operational details in learner notes or preferences, and delete learned_patterns.json to reset local memory.

Risk: Simulation is limited to manually registered transitions, and vision grounding is label-level rather than pixel-level.

Mitigation: Treat unknown actions and high uncertainty as review signals, and validate predictions against fresh observations before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/unified-world-model)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python API references, shell command examples, and JSON state snapshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local learned_patterns.json usage records when the learner helper is invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
