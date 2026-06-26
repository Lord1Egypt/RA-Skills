## Description: <br>
Make your skills easy to understand and impossible to ignore <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TunaIssaCoding](https://clawhub.ai/user/TunaIssaCoding) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill authors use this skill to turn a skill directory into clearer user-facing documentation, then publish it to GitHub and ClawdHub with an assisted command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publishing workflow can expose unintended files by creating or using a git repository, creating a public GitHub repository, pushing code, and publishing to ClawdHub. <br>
Mitigation: Inspect the skill directory before publication, remove secrets and private files, and confirm .gitignore excludes credentials, build artifacts, and other non-public content. <br>
Risk: The workflow can modify SKILL.md and README.md as part of documentation preparation. <br>
Mitigation: Review generated descriptions and README changes before approving publication. <br>


## Reference(s): <br>
- [GitHub documentation best practices](https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs) <br>
- [Publisher skill page](https://clawhub.ai/TunaIssaCoding/publisher) <br>
- [Publisher profile](https://clawhub.ai/user/TunaIssaCoding) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-line prompts with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify SKILL.md, create or update README.md, initialize or use git, create a public GitHub repository, push code, and publish to ClawdHub after user approval.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
