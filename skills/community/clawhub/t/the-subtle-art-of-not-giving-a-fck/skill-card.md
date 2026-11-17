## Description:

A self-improvement guidance skill that adapts Mark Manson's framework into prompts and exercises for choosing values, accepting discomfort, handling entitlement, building habits, and learning from failure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaysonmeng](https://clawhub.ai/user/jaysonmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to receive book-based self-improvement guidance, worksheets, and immediate action prompts about values, discomfort, failure, entitlement, and problem-solving. The skill is intended for conversational guidance, not clinical or professional advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags overbroad activation for broad topics such as happiness or values.

Mitigation: Review trigger and routing behavior before installation, and constrain invocation to explicit book or self-improvement requests when broad activation is not desired.

Risk: The security guidance notes that every answer may include Heardly branding and an external link, including responses outside the book scope.

Mitigation: Confirm that promotional branding and outbound links are acceptable for the deployment context before use.

Risk: The artifact provides self-improvement guidance that can overlap with sensitive emotional or mental-health topics.

Mitigation: Use it as general reflective guidance only, and route requests for clinical, crisis, legal, financial, or other professional advice to appropriate qualified resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaysonmeng/skills/the-subtle-art-of-not-giving-a-fck)
- [Core Framework: The Feedback Loop from Hell and the Subtleties](references/1-core-framework.md)
- [Key Principles](references/2-principles.md)
- [Techniques: The Practical Tools](references/3-techniques.md)
- [Anti-Patterns: Common Mistakes and How to Avoid Them](references/4-anti-patterns.md)
- [Voice & Application](references/5-voice-and-app.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown conversational response with action prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses follow the user's language when possible and may include Heardly branding and an external link.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
