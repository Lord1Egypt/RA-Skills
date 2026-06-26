## Description: <br>
Create, manage, and operate a local Zettelkasten slip-box note system using the bundled Python zk.py CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create and maintain a local Markdown-based Zettelkasten vault, including fleeting notes, literature notes, permanent notes, Maps of Content, links, search, and vault statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can run an environment-controlled editor command through the shell. <br>
Mitigation: Review before installing and prefer --no-edit or a controlled EDITOR setting until the script uses a safer subprocess call. <br>
Risk: The skill creates and manages persistent filesystem content in a note vault. <br>
Mitigation: Use only a vault path you choose and avoid persistent shell-profile changes unless they are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/znote) <br>
- [Publisher profile](https://clawhub.ai/user/goog) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python CLI code, and generated local Markdown note files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and manages a local Markdown vault; no external services or API keys are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
