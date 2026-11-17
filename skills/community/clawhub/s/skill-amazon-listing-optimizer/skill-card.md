## Description:

Audit Amazon product listing images for non-square dimensions, auto-pad them to a 2000x2000 white background, and push corrected images to live listings via SP-API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

External marketplace operators and developers use this skill to audit Amazon listing image slots, generate square product-image assets, and submit corrected image URLs through Amazon SP-API. It is intended for e-commerce automation workflows that manage live listing media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can modify live Amazon listing images through SP-API.

Mitigation: Use least-privilege Amazon credentials, test changes on one SKU first, and review proposed listing updates before broad execution.

Risk: The image upload workflow exposes a public unauthenticated local HTTP server while Amazon crawls the image URLs.

Mitigation: Run the workflow in a locked-down environment, avoid exposing the server to the internet when possible, and prefer controlled signed object-storage URLs for image hosting.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zero2ai-hub/skills/skill-amazon-listing-optimizer)
- [Zero2AI publisher profile](https://clawhub.ai/user/zero2ai-hub)
- [skill-amazon-spapi](https://github.com/Zero2Ai-hub/skill-amazon-spapi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, audit reports, and generated JPEG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and python3; scripts may read Amazon SP-API credentials and can modify live Amazon listings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
