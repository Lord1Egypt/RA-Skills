## Description:

A privacy-first, consent-based self-improvement skill for AI agents that captures learnings, errors, and best practices with sanitization, duplicate detection, and skill draft generation from recurring patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjfl888](https://clawhub.ai/user/hjfl888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record user-approved project learnings, errors, best practices, improvement suggestions, analytics, exports, and reusable skill drafts. It is intended for consent-based agent self-improvement workflows where records remain reviewable before they influence later guidance or generated skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated skill drafts can be installed locally or published externally, which weakens the advertised local-only storage boundary.

Mitigation: Review each generated skill draft before installation or publication, checking commands, file paths, credentials, network behavior, and copied instructions.

Risk: Local learning records may influence future guidance or generated skills, including any sensitive context that sanitization fails to remove.

Mitigation: Inspect learning records and generated drafts before reuse, and remove secrets, personal data, private paths, and unsupported instructions before confirming writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hjfl888/skills/safe-self-improving)
- [Project homepage](https://github.com/hjfl888/safe-self-improving)
- [Publisher profile](https://clawhub.ai/user/hjfl888)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown and structured text, including learning records, summaries, improvement suggestions, analytics, exports, and generated SKILL.md drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are user-confirmed before being written; exported learning records may be Markdown or JSON.]

## Skill Version(s):

1.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
