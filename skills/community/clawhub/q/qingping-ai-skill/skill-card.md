## Description: <br>
Generates AI images through the Qingping AI API and downloads the resulting PNG files locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lusyoe](https://clawhub.ai/user/lusyoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate design assets, creative images, covers, wallpapers, and other AI-created images from prompts using Qingping AI models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and API-key-backed usage are sent to a third-party Qingping/lusyoe service. <br>
Mitigation: Use a revocable API key, avoid sensitive prompts, and install only if the service is trusted for the intended data. <br>
Risk: The downloader trusts API-returned file names and image URLs before writing files locally. <br>
Mitigation: Review generated file paths and prefer adding filename sanitization and expected HTTPS image-domain restrictions before broad deployment. <br>
Risk: API keys may be exposed if placed in shared shell profiles or committed configuration. <br>
Mitigation: Store QINGPING_API_KEY in a private environment or secrets manager and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lusyoe/qingping-ai-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lusyoe) <br>
- [Qingping platform](https://auth.lusyoe.com/profile) <br>
- [Qingping homepage](https://claw.lusyoe.com) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [PNG image files saved locally with console status text and returned file paths when used as Python code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QINGPING_API_KEY and sends prompts to the Qingping API before downloading generated images into the qingping-ai directory.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
