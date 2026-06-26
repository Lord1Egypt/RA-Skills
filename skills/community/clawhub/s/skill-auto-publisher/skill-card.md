## Description: <br>
Skill Auto Publisher helps agents publish skills to ClawHub by checking name availability, validating metadata, incrementing versions, generating changelogs, requesting user confirmation, publishing with the ClawHub CLI, and recording publish history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianduoduo1422608857](https://clawhub.ai/user/qianduoduo1422608857) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare and publish ClawHub skill releases with metadata validation, version updates, changelog handling, and publish-history tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify and upload local skill files during publishing. <br>
Mitigation: Use it only when intentionally publishing to ClawHub, and verify the active ClawHub account, target directory, included files, version, and changelog before execution. <br>
Risk: Broad activation wording may cause the publishing workflow to be selected when the user only wants publishing advice. <br>
Mitigation: Require explicit user confirmation before running publish commands and avoid using the skill on untrusted or unexpectedly named skill directories. <br>
Risk: Security evidence reports limited built-in safety checks and unsafe interpolation concerns. <br>
Mitigation: Review the generated command inputs and script behavior before installation or use, especially until script-level confirmation and interpolation handling are improved. <br>


## Reference(s): <br>
- [Skill Auto Publisher on ClawHub](https://clawhub.ai/qianduoduo1422608857/skill-auto-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and publish status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update release metadata and publish history files and run ClawHub publish commands after user confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
