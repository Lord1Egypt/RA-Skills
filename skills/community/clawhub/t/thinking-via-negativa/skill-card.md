## Description:

Use when the reflex is to add a feature, layer, or process, preferring removal of harmful or nonessential elements first with an irreversibility guard before deletion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, maintainers, and technical decision makers use this skill to challenge proposed additions and identify evidence-backed removals or simplifications before adding new surface area.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can steer an agent toward deleting or simplifying behavior that may still be necessary.

Mitigation: Require evidence for removal, preserve load-bearing controls, and keep a rollback path for any non-trivial change.

Risk: Over-application could treat useful safety checks, validation, tests, retries, or rate limits as mere complexity.

Mitigation: Presume such controls are necessary until proven otherwise and falsify the recommendation when removal lacks non-use or harm evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-via-negativa)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured text or Markdown guidance with goal, proposed addition, removal candidates, action, verification plan, and do-not-touch fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance-only skill; no code, installer, network behavior, persistence, or credential handling is identified in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
