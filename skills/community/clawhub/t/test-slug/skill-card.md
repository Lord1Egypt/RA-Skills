## Description: <br>
Publishes a local skill to ClawHub using specified slug, name, version, path, and optional changelog parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhaichao87](https://clawhub.ai/user/wuhaichao87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to prepare and publish local skill directories to ClawHub with release metadata such as slug, display name, version, source path, and changelog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact embeds a ClawHub API token and can upload local files with limited user control over what is sent. <br>
Mitigation: Inspect the exact files before use, remove the embedded token, authenticate explicitly with your own credential, and add a dry-run or confirmation step before publishing. <br>
Risk: Running the publisher on the wrong directory may send unintended local skill files. <br>
Mitigation: Use it only on a clean skill directory and review the selected files before any upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhaichao87/test-slug) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs command-line usage patterns and Python invocation guidance for publishing skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
