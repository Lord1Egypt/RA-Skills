## Description: <br>
Audit Amazon product listing images for non-square dimensions, auto-pad them to a 2000x2000 white background, and push corrected images to live listings via SP-API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketplace operators and e-commerce automation developers use this skill to find Amazon listing image slots that are non-square or undersized, produce fixed square images, and submit corrected image URLs through Amazon SP-API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can alter live Amazon listing image attributes through SP-API. <br>
Mitigation: Use least-privilege SP-API credentials, test on one SKU first, and back up listing attributes before bulk updates. <br>
Risk: The bundled image push flow exposes an unauthenticated public HTTP server with a reported path-traversal risk. <br>
Mitigation: Avoid exposing the local server on untrusted networks; prefer a controlled object store or presigned URLs for Amazon image crawling. <br>
Risk: SP-API credentials are required for listing reads and writes. <br>
Mitigation: Keep credentials outside any served directory and restrict credential permissions to the minimum needed listing operations. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Zero2Ai-hub/skill-amazon-listing-optimizer) <br>
- [Zero2Ai-hub publisher profile](https://clawhub.ai/user/Zero2Ai-hub) <br>
- [Related skill-amazon-spapi integration](https://github.com/Zero2Ai-hub/skill-amazon-spapi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks, JSON audit reports, generated JPEG image files, and SP-API listing update calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local image_fix files and can update live Amazon listing image attributes when run with valid SP-API credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
