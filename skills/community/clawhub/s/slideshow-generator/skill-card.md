## Description: <br>
Create HTML slideshows from Markdown with live preview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, presenters, and content authors use this skill to draft, refine, organize, and export presentation content from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation text entered into the skill is retained in local log files. <br>
Mitigation: Avoid entering secrets or highly confidential material, and periodically review or delete ~/.local/share/slideshow-generator. <br>
Risk: The install path is not specified in the evidence, so the invoked CLI could differ from the reviewed script. <br>
Mitigation: Verify the installed slideshow-generator command resolves to the reviewed artifact before relying on it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/slideshow-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/xueyetianya) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, HTML, JSON, CSV, shell commands, files] <br>
**Output Format:** [Command-line text with timestamped log files and optional JSON, CSV, plain-text, or HTML exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entered presentation text locally under ~/.local/share/slideshow-generator and writes export files in that data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
