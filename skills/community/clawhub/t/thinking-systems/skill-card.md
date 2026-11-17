## Description:

When behavior is emergent across components, this skill guides the agent to map boundaries, stocks and flows, feedback loops, delays, archetypes, and ranked leverage points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical decision makers use this skill to analyze recurring cross-component problems, identify structural drivers, and choose interventions with attention to leverage and side effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may over-apply systems mapping to a local, linear bug or single bottleneck where a narrower diagnostic method is more appropriate.

Mitigation: Use the skill's falsification and stop checks: drop to local debugging when one component fully explains the issue, switch to theory-of-constraints for a fixed bottleneck, and avoid adding loops after a chosen intervention and watch signals are set.

Risk: The agent may treat a quick parameter tweak as the primary intervention even when the mapped structure points to a higher-leverage change.

Mitigation: Rank interventions by goals, rules, loops, structure, then parameters, and include side-effect checks for feedback, delayed reversal, and cross-component impact before choosing an action.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured text or Markdown with named fields for system boundary, stocks and flows, loops, archetype, structural driver, interventions, chosen action, and watch signals.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external actions, code execution, sensitive access, persistence, or external data use are requested by the skill.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
