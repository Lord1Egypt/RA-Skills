## Description: <br>
Use when the user wants to interact with YoudaoNote (Youdao Cloud Notes) by listing, reading, creating, searching, clipping web pages, or saving Markdown and mindmap notes via the youdaonote CLI tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangcheng](https://clawhub.ai/user/huangcheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate YoudaoNote from an agent-assisted terminal workflow, including managing notes, searching content, saving Markdown or mindmap notes, and clipping webpages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow runs a remote installer through a shell with full execution privileges. <br>
Mitigation: Download and inspect the installer before running it, and install only from a trusted YoudaoNote CLI source. <br>
Risk: The skill requires a YoudaoNote API key and can access note contents. <br>
Mitigation: Use a limited or revocable API key when possible, keep the key out of shared terminals, logs, and repositories, and avoid storing secrets or confidential CI artifacts in notes. <br>


## Reference(s): <br>
- [YoudaoNote CLI installer](https://artifact.lx.netease.com/download/youdaonote-cli/install.sh) <br>
- [YoudaoNote API dashboard](https://mopen.163.com/#/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with command examples, configuration steps, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include commands that read, create, search, clip, or save notes through the youdaonote CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
