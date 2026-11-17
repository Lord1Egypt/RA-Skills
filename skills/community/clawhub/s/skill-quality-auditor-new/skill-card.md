## Description:

Audit another Codex skill for structural compliance, trigger quality, instruction clarity, reuse of scripts or references, and overall maintainability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aidenchangzy](https://clawhub.ai/user/aidenchangzy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this agent skill to review Codex skill folders for structural compliance, trigger quality, workflow clarity, resource use, and maintainability before release or iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's assessment can be mistaken for a security guarantee.

Mitigation: Treat output as a quality review only and run separate security review before deployment.

Risk: The helper reads local skill files from a path supplied by the user.

Mitigation: Run it only on skill folders intended for review and inspect the generated findings before acting on them.

Risk: Audit verdicts may be incomplete when a skill has borderline or missing context.

Mitigation: Follow the skill guidance to inspect SKILL.md and referenced resources before making a final release decision.

## Reference(s):

- [Skill Audit Rubric](references/rubric.md)
- [ClawHub Skill Page](https://clawhub.ai/aidenchangzy/skills/skill-quality-auditor-new)
- [Publisher Profile](https://clawhub.ai/user/aidenchangzy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown assessment with verdict, score summary, strengths, weaknesses, and next fixes; optional JSON from the bundled audit helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper reads a local skill folder supplied by the user and emits deterministic quality findings for human review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
