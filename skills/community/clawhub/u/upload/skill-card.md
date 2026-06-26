## Description: <br>
Guides an agent through uploading local files to GitHub with Git commands, including repository setup, branch workflows, large-file handling, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DuanC-Chao](https://clawhub.ai/user/DuanC-Chao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare a local project for Git version control and publish changes to a GitHub remote with clear, traceable commits. It is most useful when an agent needs procedural guidance for initialization, staging, committing, pulling, pushing, branch management, Git LFS, and common upload errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may run Git commands from the wrong project folder or push to the wrong GitHub remote. <br>
Mitigation: Confirm the current directory, inspect `git status`, and verify the remote URL before adding, committing, pulling, or pushing. <br>
Risk: The upload workflow may publish secrets, private data, generated files, or other content that should not be stored in GitHub history. <br>
Mitigation: Review `.gitignore`, repository visibility, and staged files before committing; remove unintended files from tracking before pushing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DuanC-Chao/upload) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; review commands and repository targets before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
