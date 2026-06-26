## Description: <br>
Tistory API CLI is an unofficial command-line tool for reading, updating, deleting, listing categories, and uploading images for Tistory blogs with Korean error messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blog operators use this skill to install and run a Tistory command-line workflow for post management, category lookup, and image upload from a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can update or delete live Tistory blog posts. <br>
Mitigation: Review command targets before execution, keep backups of important post content, and test destructive commands on non-critical posts first. <br>
Risk: Tistory API tokens may grant access to blog operations. <br>
Mitigation: Store tokens in environment variables or a secret manager, avoid committing credentials, and rotate tokens if they are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chloepark85/tistory-api-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and environment variable names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Korean-language CLI examples and setup guidance for pipx, uv, or pip.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
