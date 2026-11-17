## Description:

Helps agents create customized skirt designs for print-on-demand and manufacturing using prompts, garment options, and reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers and creators use this skill to turn skirt specifications, customization requests, and reference images into clothing design drafts and shareable previews for print or manufacturing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design prompts, reference image URLs, and workspace metadata are sent to an external design service.

Mitigation: Avoid confidential designs and personal images unless sharing them is permitted by policy.

Risk: The OneKey access key is required to use the hosted service.

Mitigation: Store the key as a secret and do not include it in prompts or shared outputs.

Risk: Running an unpinned OneKey CLI through npx introduces supply-chain uncertainty.

Mitigation: Use a pinned or verified OneKey CLI version.

## Reference(s):

- [ClawHub skirt-designer release](https://clawhub.ai/ai-hub-admin/skills/skirt-designer)
- [Craftsman Skirt Designer](https://craftsman-agent.aiagenta2z.com/app/clothing-designer/skirt)
- [OneKey access keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands]

**Output Format:** [Markdown with JSON requests and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return a shareable workspace link to generated design previews, multi-view images, and a 3D viewer when available.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
