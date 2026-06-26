## Description: <br>
Extracts PNG/JPG images from a URL and generates a PDF while preserving the source image order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JerryLiu3502](https://clawhub.ai/user/JerryLiu3502) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to convert webpage-hosted images, especially article images, into a local PDF file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted URL can trigger unintended local shell command execution. <br>
Mitigation: Use only fully trusted URLs, review before installing, and prefer a patched implementation that validates URLs and avoids shell interpolation. <br>
Risk: Network fetches and file generation can overwrite or create local files unexpectedly. <br>
Mitigation: Run in a constrained working directory and prefer a patched implementation with timeouts and overwrite protection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JerryLiu3502/url-images-to-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and a generated PDF file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a PDF in the working directory and uses a temporary image download directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
