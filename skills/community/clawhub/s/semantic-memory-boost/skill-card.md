## Description:

Semantic Memory Boost helps an agent improve context relevance by parsing intent, retrieving layered memory, aligning retrieved content, and synthesizing memory-aware responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkes994408-cmd](https://clawhub.ai/user/bkes994408-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they need memory-assisted answers for complex, multi-temporal decisions, project planning, or conflicts between historical context and current requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to read long-term memory and persist conversation insights, which can expose or retain sensitive information without clear consent, scope, or deletion controls.

Mitigation: Require explicit approval for each memory write, keep memory project-scoped, and avoid storing credentials, private personal data, confidential business details, or instructions that could alter future agent behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bkes994408-cmd/skills/semantic-memory-boost)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown response with optional memory summary markers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a [MEM_SUMMARY: ...] marker when the interaction produces reusable memory.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
