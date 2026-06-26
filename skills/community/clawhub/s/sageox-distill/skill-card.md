## Description: <br>
SageOx Distill syncs repository context, indexes GitHub PRs and issues, and runs the SageOx distillation pipeline to keep a team's knowledge base current. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[galexy](https://clawhub.ai/user/galexy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team maintainers use this skill to keep SageOx-enabled repositories synchronized, index GitHub activity, and generate daily distilled knowledge-base source files for later summary workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository and GitHub activity may be sent to SageOx and Claude/Anthropic-backed processing. <br>
Mitigation: Use the skill only with repositories and GitHub data the user is comfortable sharing, and start with a non-sensitive test repository until permissions and data handling are clear. <br>
Risk: The skill can install and run the ox CLI from GitHub Releases. <br>
Mitigation: Review the bundled install and update scripts before use, keep the pinned checksum verification intact, and avoid substituting package-manager installs for the documented pinned curl flow. <br>
Risk: The workflow requires authenticated ox, GitHub CLI, and Claude credentials. <br>
Mitigation: Use least-privilege accounts where possible, confirm credentials before running the pipeline, and avoid using repositories that contain secrets or restricted data. <br>


## Reference(s): <br>
- [SageOx homepage](https://sageox.ai) <br>
- [SageOx Summary skill](https://clawhub.ai/skills/sageox-summary) <br>
- [Installing ox](references/INSTALL.md) <br>
- [SageOx ox releases](https://github.com/sageox/ox/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status lines and Markdown guidance with bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports one line per team after distillation; successful all-team runs may return a single `all ok` line.] <br>

## Skill Version(s): <br>
0.2.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
