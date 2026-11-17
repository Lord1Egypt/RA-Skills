## Description:

Downstream skill execution preflight layer. It inspects a target skill, extracts explicit and implicit confirmation fields, normalizes candidate parameters, resolves ambiguity, applies risk gating, and returns a structured confirmation payload before handing off to the downstream skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pm-geeker](https://clawhub.ai/user/pm-geeker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before running downstream skills to convert user intent, downstream metadata, and risk gates into confirmed execution-ready parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session-level confirmation state and audit logs may contain user inputs and selected parameters.

Mitigation: Avoid entering secrets unless the host environment protects logs appropriately.

Risk: A confirmation flow could be mistaken for downstream authorization.

Mitigation: Keep downstream skill authorization checks in place; this skill confirms parameters but does not replace authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pm-geeker/skills/skill-param-confirmer)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown prompts and JSON handoff payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes numbered confirmation menus, blocking reasons, session state, and audit fields when applicable.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
