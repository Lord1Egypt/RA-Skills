## Description: <br>
Covers launching vvvv gamma from the command line or programmatically -- normal startup, opening specific .vl patches, command-line arguments, package repositories, and key filesystem paths (install directory, user data, sketches, exports, packages). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tebjan](https://clawhub.ai/user/tebjan) <br>

### License/Terms of Use: <br>
CC-BY-SA-4.0 <br>


## Use Case: <br>
Developers and engineers use this skill to start vvvv gamma, open .vl patches, choose startup arguments, configure package repositories, and locate installation or user data directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest launching a vvvv executable, opening .vl files, or loading package repositories from paths that come from untrusted projects. <br>
Mitigation: Confirm the vvvv.exe path, .vl files, and package repository paths before allowing an agent to run commands or change startup configuration. <br>


## Reference(s): <br>
- [vvvv Command-Line Arguments Reference](artifact/cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Windows shell commands and path examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and release changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
