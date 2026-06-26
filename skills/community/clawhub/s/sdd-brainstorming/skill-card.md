## Description: <br>
Guides agents through a Chinese-language SDD brainstorming process before implementation, using structured questions, design approval, and specification writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahingbun-dev](https://clawhub.ai/user/mahingbun-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to turn new or updated feature ideas into approved Chinese-language design specifications before implementation. It is intended for OpenClaw workspaces that use an SDD spec directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may write or overwrite SDD specification files in the configured workspace. <br>
Mitigation: Confirm the selected feature folder and review proposed updates before allowing the skill to write spec-design.md. <br>
Risk: The background /gen-image step may create files, incur cost, or send project and design details to an image-generation tool without a separate image-count limit. <br>
Mitigation: Review or disable the image-generation step before use in sensitive projects, and set explicit limits for generated images. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mahingbun-dev/sdd-brainstorming) <br>
- [Publisher profile](https://clawhub.ai/user/mahingbun-dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese-language Markdown specifications with structured prompts and optional image references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes spec-design.md under the configured workspace spec directory and may launch background design-image generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
