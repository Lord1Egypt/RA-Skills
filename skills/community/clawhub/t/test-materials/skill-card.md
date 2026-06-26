## Description: <br>
Render JSON schemas to images and generate schemas from prompts using declare-render and AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cai-zhuo](https://clawhub.ai/user/cai-zhuo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to render declare-render JSON schemas to PNG or JPG images, generate schemas from natural-language prompts with OpenAI, and validate render-data schema files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an OpenAI API key and send prompt content to an external AI provider. <br>
Mitigation: Use a limited API key and avoid submitting confidential data unless provider use is approved. <br>
Risk: Installing or running an unpinned CLI package can execute unintended package versions. <br>
Mitigation: Verify that materials-cli is the intended trusted package and prefer a pinned version before installation. <br>
Risk: Passing secrets through command-line flags may expose them in shell history or process listings. <br>
Mitigation: Provide credentials through approved environment variables or secret-management tooling instead of command-line arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cai-zhuo/test-materials) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON schema guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference generated or validated declare-render JSON schema files and image outputs produced through materials-cli.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
