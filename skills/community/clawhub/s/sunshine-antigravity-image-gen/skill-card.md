## Description: <br>
Generate images using the internal Google Antigravity API (Gemini 3 Pro Image). High quality, native generation without browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create image files from text prompts through a local Node.js script that uses a configured Google Antigravity OAuth profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local Google Antigravity OAuth profile for authenticated API calls. <br>
Mitigation: Install only when the publisher is trusted, review the auth profile path and project ID before running, and avoid broad auto-invocation. <br>
Risk: A user-supplied output path can write generated image files to local storage. <br>
Mitigation: Choose output paths deliberately and avoid paths that could overwrite important files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/sunshine-antigravity-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration guidance] <br>
**Output Format:** [PNG image file plus stdout status text including a MEDIA path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a local Google Antigravity OAuth profile; supports prompt, output path, and aspect ratio arguments.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
