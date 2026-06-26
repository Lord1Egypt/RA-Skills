## Description: <br>
Save web articles locally with images by downloading images, generating Markdown, and optionally converting articles to PDF, including WeChat Official Account workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barryqin9999](https://clawhub.ai/user/barryqin9999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content workflows use this skill to archive web or WeChat articles locally with linked images, Markdown files, and optional PDF or HTML outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article content may be fetched through external services and saved persistently. <br>
Mitigation: Use only URLs intended for external processing and confirm the output directory before running the workflow. <br>
Risk: Saved article files may be sent to Feishu as part of the documented workflow without clear recipient scoping. <br>
Mitigation: Confirm the Feishu recipient and sharing intent each time, and avoid private or sensitive articles unless external sharing is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/barryqin9999/save-article-with-images) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown instructions with inline shell and Python code blocks, plus generated article files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local article directories with images, Markdown, HTML, PDF, and metadata files.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
