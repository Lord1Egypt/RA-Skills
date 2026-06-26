## Description: <br>
Readme Maker is a README-themed local CLI that records, lists, searches, and exports README-related notes and command inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers can use this skill as a local activity log for README-related checks, notes, and exports. Do not treat it as a substantive README generator or validator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User inputs may include secrets, private repository text, or unreleased business details that are stored locally and can later be searched or exported. <br>
Mitigation: Use the skill only for non-sensitive README notes, and avoid passing tokens, credentials, private source content, or confidential project details. <br>
Risk: The skill presents README generation and validation commands, but security evidence says the implemented behavior is primarily logging and exporting raw inputs. <br>
Mitigation: Review any README guidance independently and use a real README generator, markdown linter, or validator when correctness matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/readme-maker) <br>
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and local export files in JSON, CSV, or TXT] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores command inputs locally under ~/.local/share/readme-maker and can later search or export those entries.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
