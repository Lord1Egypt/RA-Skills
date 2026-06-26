## Description: <br>
Generates WeChat article images, including covers, comparison visuals, and chart-style graphics, from local HTML templates and Python commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingyu525](https://clawhub.ai/user/jingyu525) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Creators, developers, and social media teams use this skill to generate WeChat-ready article covers, comparison images, and simple data visualizations without calling an image generation model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local browser and file operations can expose sensitive generated content if served from the wrong directory or left running. <br>
Mitigation: Use trusted local paths, serve only the intended output directory, and stop the local server after screenshots are complete. <br>
Risk: Shell-based browser commands and screenshot steps can behave unexpectedly with untrusted or complex file paths. <br>
Mitigation: Use simple trusted file paths and review generated commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jingyu525/wechat-image-generator) <br>
- [Project homepage](https://github.com/jingyu525/wechat-image-generator) <br>
- [Publisher profile](https://clawhub.ai/user/jingyu525) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated local HTML/image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local 1200x675 HTML templates for screenshot capture; requires python3 and a browser screenshot workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
