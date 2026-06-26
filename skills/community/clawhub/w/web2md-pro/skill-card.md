## Description: <br>
Convert a web URL into clean, readable Markdown for saving articles, extracting page content, batch-converting reading lists, or preparing content for LLM context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbeiganlinniang](https://clawhub.ai/user/linbeiganlinniang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to turn web articles and reading lists into Markdown files for offline reading, archiving, personal knowledge bases, or LLM context preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external web2md pip package that was not included in the reviewed artifact. <br>
Mitigation: Install in a virtual environment, pin the package version, and review the package before use. <br>
Risk: The skill can fetch untrusted URLs and write Markdown files to user-selected output paths. <br>
Mitigation: Review source URLs, batch input files, and output directories before running commands. <br>


## Reference(s): <br>
- [Web to Markdown Pro ClawHub release](https://clawhub.ai/linbeiganlinniang/web2md-pro) <br>
- [web2md product site](https://web2md.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples; generated agent work may create Markdown files from web pages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch web pages from user-provided URLs and write Markdown output to a requested path or output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
