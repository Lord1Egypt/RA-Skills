## Description:

Render JSON schemas to images and generate schemas from prompts using declare-render and AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cai-zhuo](https://clawhub.ai/user/cai-zhuo)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to render declare-render JSON schemas into PNG or JPG images, validate schema files, and generate renderable schemas from natural-language prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or invoking an unverified npm package can introduce supply-chain risk.

Mitigation: Verify the `materials-cli` package and publisher before use, and prefer a pinned or project-local install.

Risk: Generation prompts and schema content may be sent to OpenAI or the configured base URL.

Mitigation: Do not include secrets, credentials, or confidential data in prompts or schemas submitted through the AI generation workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cai-zhuo/skills/test-materials)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON schema examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce image-rendering commands and schema-generation guidance for PNG or JPG outputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
