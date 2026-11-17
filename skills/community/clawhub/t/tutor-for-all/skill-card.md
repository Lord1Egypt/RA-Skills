## Description:

Helps an agent act as a private learning tutor that creates personalized study plans, tracks progress, answers questions, and recommends learning resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futureidiot](https://clawhub.ai/user/futureidiot)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and learning-support agents use this skill to structure a topic into a curriculum, schedule study sessions, record check-ins, answer questions, and adapt the plan as progress changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learning profiles, schedules, progress records, and Q&A notes persist as local Markdown files and may contain personal learning details.

Mitigation: Avoid entering sensitive personal details, review the local data files periodically, and delete them when resetting or removing the skill.

Risk: Learning-resource recommendations may be stale when the agent relies only on model knowledge.

Mitigation: Enable web search only when current resource recommendations are needed and review recommended resources before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/futureidiot/skills/tutor-for-all)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational text and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local Markdown files for the learner profile, curriculum, schedule, progress log, and session notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
