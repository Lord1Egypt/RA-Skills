## Description:

Tvs Deep Interview helps agents turn vague requests into verifiable specifications through one-question-at-a-time Socratic interviewing, topology confirmation, ambiguity scoring, and explicit approval gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inksnowhailong](https://clawhub.ai/user/inksnowhailong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product builders, and agent users use this skill to clarify ambiguous requests before implementation. It guides the agent through topology confirmation, focused follow-up questions, ambiguity scoring, and a pending-approval specification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The interview flow may activate on broad Chinese phrases that ask the agent to clarify or avoid assumptions.

Mitigation: Ask the agent to stop the interview or provide explicit implementation instructions when direct execution is intended.

Risk: The approval gate can slow normal implementation work when the request is already clear.

Mitigation: Use the skill for vague or complex requests and bypass it when file paths, acceptance criteria, and execution intent are already explicit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inksnowhailong/skills/tvs-deep-interview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured interview prompts, scoring summaries, progress reports, and pending-approval specification sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces clarification and specification guidance only; no executable payload is present in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
