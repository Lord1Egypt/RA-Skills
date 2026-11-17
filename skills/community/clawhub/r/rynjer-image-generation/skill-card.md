## Description:

Generates and refines image prompts, estimates costs, recommends sizes, and submits business-ready marketing image jobs through Rynjer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antipas](https://clawhub.ai/user/antipas)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to produce usable marketing visuals for landing pages, ads, blog covers, ecommerce product images, and social posts. It supports a short workflow from rough request to rewritten prompt, cost estimate, image generation, and result polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live generation can spend Rynjer credits without local enforcement of all declared limits.

Mitigation: Estimate cost before generation, use a minimally scoped token, and enforce count and polling limits in the surrounding runtime or server policy.

Risk: Image prompts may include sensitive, regulated, or brand-sensitive content.

Mitigation: Review prompts before live generation and avoid sensitive or regulated content unless the deployment has appropriate policy controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antipas/skills/rynjer-image-generation)
- [README](artifact/README.md)
- [Tool schema](artifact/src/tools.json)
- [Implementation notes](artifact/IMPLEMENTATION.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON tool responses and Markdown guidance with example shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live generation returns request status, usage identifiers, and image URLs when available; mock mode returns local test responses.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
