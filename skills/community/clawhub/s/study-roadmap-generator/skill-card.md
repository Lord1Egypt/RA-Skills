## Description:

Generates Chinese-language structured study roadmaps from a learner's goal, current level, and available time, including phases, weekly plans, resources, common blockers, and daily pacing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seulkilu](https://clawhub.ai/user/seulkilu)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and agents use this skill to turn broad study goals, current level, and time constraints into Chinese-language roadmaps with success criteria, phased plans, weekly schedules, resources, blockers, and adjustment notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may trigger the skill in general study-planning requests.

Mitigation: Review or narrow trigger phrasing before deployment in agents that support many planning workflows.

Risk: The skill forces Chinese-language output, which may be unsuitable in multilingual workflows.

Mitigation: Use it for Chinese-language roadmap workflows or localize the output-language rules before deployment.

Risk: Generated learning resources and milestones may not match a learner's current constraints or external requirements.

Mitigation: Have users verify resources, deadlines, and success criteria before relying on the roadmap.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seulkilu/skills/study-roadmap-generator)
- [patterns.md](references/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Chinese plain text or Markdown-style tables; optional JSON from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Six-section roadmap structure covering learner profile, success criteria, phase plan, learning stack, common blockers, and dynamic adjustment notes.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
