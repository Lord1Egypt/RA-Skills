## Description: <br>
Audit Amazon product listing images for non-square dimensions, auto-pad them to 2000x2000 white background, and push corrected images to live listings via SP-API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketplace operators and ecommerce developers use this skill to audit Amazon listing image dimensions, generate square corrected images, and submit image updates through SP-API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live Amazon listing images through SP-API. <br>
Mitigation: Use narrowly scoped SP-API permissions, test on one low-risk SKU first, and review each SKU and image slot before bulk uploads. <br>
Risk: The upload workflow briefly exposes a local image directory through an unauthenticated public HTTP server. <br>
Mitigation: Serve only a dedicated directory containing generated image files, avoid running it from a machine with sensitive files, and close the server after Amazon has crawled the images. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/Zero2Ai-hub/skill-listing-optimizer) <br>
- [Related SP-API Skill](https://github.com/Zero2Ai-hub/skill-amazon-spapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, JSON audit reports, and generated JPEG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and python3; the artifact also expects Pillow, amazon-sp-api, and Amazon SP-API credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
