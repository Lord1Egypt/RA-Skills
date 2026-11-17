## Description:

Helps users plan and track a rocket mass heater project by researching local regulations and materials, generating customized build plans, creating material lists and safety checklists, maintaining build logs, setting reminders, and monitoring post-build performance while humans perform all physical construction work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan and track a rocket mass heater build for off-grid or lower-cost heating. The agent produces localized research prompts, material lists, safety checklists, build logs, reminders, and performance tracking while a human performs all physical construction and operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce construction-ready guidance for a fire-producing heater.

Mitigation: Treat output as preliminary educational material only and require local permits, chimney and structural inspection, code-compliant rated materials, and qualified HVAC or fire-safety review before building, connecting, or firing a heater.

Risk: The install command uses an unpinned npx invocation.

Mitigation: Prefer a pinned or preinstalled trusted ClawHub installer before installing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/rocket-mass-heater-construction)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with checklists, logs, templates, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create filesystem-based project logs, material lists, reminders, and performance trackers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
