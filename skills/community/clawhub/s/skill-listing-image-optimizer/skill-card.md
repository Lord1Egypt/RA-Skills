## Description: <br>
Audit Amazon product listing images for non-square dimensions, auto-pad them to 2000x2000 white background, and push corrected images to live listings via SP-API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketplace operators and developers use this skill to audit Amazon listing image dimensions, generate square 2000x2000 image files, and submit corrected image URLs through SP-API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The push workflow can update live Amazon listings. <br>
Mitigation: Review target SKUs and image slots before execution, use least-privilege or test SP-API credentials where possible, and avoid bulk live pushes without a rollback plan. <br>
Risk: The image push script serves local files on a public interface with weak path containment. <br>
Mitigation: Run it only in a controlled environment, keep credential files outside the served directory, and prefer an allowlisted hosted image store for internet-reachable pushes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Zero2Ai-hub/skill-listing-image-optimizer) <br>
- [Related SP-API skill](https://github.com/Zero2Ai-hub/skill-amazon-spapi) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow can create JSON audit reports and fixed JPEG image files, and can submit listing image updates through SP-API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
