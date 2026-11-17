## Description:

Extracts images from a webpage URL and generates a PDF while preserving the source order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryliu3502](https://clawhub.ai/user/jerryliu3502)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to extract PNG/JPG images from supported article pages and package them into a PDF file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted URL could cause unintended shell command execution through the current curl invocation.

Mitigation: Run only on trusted URLs in a low-privilege or sandboxed environment until the script validates http/https URLs and replaces shell interpolation with argument-safe process APIs or native Node HTTP fetching.

Risk: The skill fetches remote webpage and image content from the network.

Mitigation: Review target URLs before use and avoid pages from unknown or untrusted sources.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Console text with a generated PDF file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes a PDF to the current working directory or specified output path and may download up to 50 images.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
