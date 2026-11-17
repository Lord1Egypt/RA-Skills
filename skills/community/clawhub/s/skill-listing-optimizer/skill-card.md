## Description:

Audits Amazon product listing images for non-square dimensions, pads corrected images to a 2000x2000 white background, and can push updated image URLs to live listings through SP-API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

External marketplace operators and developers use this skill to audit Amazon listing image slots, create square replacement images, and submit reviewed image updates through SP-API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write changes to live Amazon listings through SP-API.

Mitigation: Use constrained SP-API credentials, test on a small SKU set first, and review audit results before running image pushes.

Risk: The image push flow starts a temporary public HTTP server to host replacement images.

Mitigation: Avoid running the pusher on a network-reachable machine until hosting is replaced with controlled storage or hardened with strict path validation and access limits.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/zero2ai-hub/skills/skill-listing-optimizer)
- [Publisher profile](https://clawhub.ai/user/zero2ai-hub)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, API calls]

**Output Format:** [Markdown guidance with inline shell commands; scripts emit JSON audit reports and JPEG image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, python3, Pillow, amazon-sp-api, and constrained Amazon SP-API credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
