## Description:

Guides an agent through a design-first brainstorming workflow before implementing new features, building components, adding functionality, or changing behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn feature ideas into approved Chinese design specifications before implementation. It helps inspect workspace context, clarify requirements, compare approaches, document the selected design, and optionally request supporting design images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly take over feature work by requiring a mandatory design-first workflow before implementation.

Mitigation: Install it only when that workflow is intended, and keep user approval gates before design finalization and implementation.

Risk: The skill writes or overwrites design documents under the configured SDD workspace.

Mitigation: Verify that .sdd-workspace points to the intended project and review proposed overwrite summaries before accepting updates.

Risk: The skill may launch background image generation after writing project files, which can create unexpected files or consume resources.

Mitigation: Constrain or disable background image generation when file creation or resource use must be tightly controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mahingbun-dev/skills/sdd-brainstorming)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown design specifications with concise conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image placeholder references and follow-up image generation requests for design diagrams.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
