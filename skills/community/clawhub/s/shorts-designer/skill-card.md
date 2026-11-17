## Description:

Agentic AI Shorts Designer generates customized shorts designs for print-on-demand and manufacturing-on-demand using prompts, reference images, and garment parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and print-on-demand or manufacturing teams use this skill to draft and preview custom shorts with specified materials, fit, text, and logos through the Craftsman Agent service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design prompts, reference images, and manufacturing details are sent to an external service.

Mitigation: Do not submit confidential designs, customer data, private image URLs, or regulated manufacturing details without trusting the service and its data handling.

Risk: Generated workspace share links may expose design results to others with access to the link.

Mitigation: Check how share links are controlled before sharing sensitive designs.

Risk: Running an unpinned CLI package may introduce supply-chain risk.

Mitigation: Prefer the documented HTTP API or a pinned, verified CLI package version over unpinned npx execution.

## Reference(s):

- [ClawHub shorts-designer release](https://clawhub.ai/ai-hub-admin/skills/shorts-designer)
- [Craftsman shorts designer](https://craftsman-agent.aiagenta2z.com/app/clothing-designer/shorts)
- [OneKey Gateway access keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Markdown guidance with JSON requests, shell examples, and design workspace links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Design previews and multi-view assets may be available through an external workspace link.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
