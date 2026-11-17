## Description:

Spec Coding guides agents through spec-driven programming by generating feature, API, or component specifications from requirements, or by reverse-engineering specifications from existing code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to draft structured specifications before implementation, fill in specs for legacy code, and review code against agreed feature, API, or component requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reverse-engineering specifications may require the agent session to inspect source code or business requirements that contain sensitive project information.

Mitigation: Only provide code and requirements that are appropriate to share in the active agent session.

Risk: Generated specifications may omit requirements, misread existing behavior, or produce acceptance criteria that do not match product intent.

Mitigation: Review generated specs with the relevant stakeholders before treating them as approved implementation or validation criteria.

Risk: The provided export example includes privacy-sensitive concepts such as user data exports and temporary download links.

Mitigation: Add project-specific privacy, access-control, and retention requirements before adopting similar examples in production specs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pupuking723/skills/spec-coding)
- [Template Guide](assets/templates/README.md)
- [Feature Spec Template](assets/templates/feature-spec.md)
- [API Spec Template](assets/templates/api-spec.md)
- [Component Spec Template](assets/templates/component-spec.md)
- [Feature Spec Example](assets/examples/feature-example.md)

## Skill Output:

**Output Type(s):** [markdown, code, guidance]

**Output Format:** [Markdown documents with tables, checklists, and fenced code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes draft, review, approved, in-progress, and done status markers for specification lifecycle tracking.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
