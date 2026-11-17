## Description:

Audit Amazon product listing images for non-square dimensions, auto-pad them to 2000x2000 white background, and push corrected images to live listings via SP-API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

External Amazon sellers and marketplace operations teams use this skill to audit listing image dimensions, generate square replacement images, and update selected live listing image slots through Amazon SP-API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upload workflow can expose files from the chosen image directory through a public HTTP server.

Mitigation: Run it only from a dedicated directory containing the exact fixed listing images, and prefer S3 or another presigned HTTPS hosting flow for production updates.

Risk: The skill can modify live Amazon listings through SP-API.

Mitigation: Require explicit human confirmation for each live listing update and review the SKU, slot, and generated image before pushing changes.

Risk: Credentials and dependencies affect the safety of SP-API operations.

Mitigation: Keep credential files outside working image directories, set AMAZON_SPAPI_PATH explicitly, and pin Node and Python dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-listing-image-optimizer)
- [Publisher profile](https://clawhub.ai/user/zero2ai-hub)
- [Related Amazon SP-API skill](https://github.com/Zero2Ai-hub/skill-amazon-spapi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and generated report or image files from the scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and python3; runtime scripts may call Amazon SP-API and create local JPEG outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
