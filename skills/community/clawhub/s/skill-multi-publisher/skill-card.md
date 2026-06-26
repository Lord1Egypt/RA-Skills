## Description: <br>
One-command publish a Claude Code skill to major marketplaces including GitHub, ClawHub, and community directories, with validation, generated support files, repository creation, publishing, and pull request submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongsheng123132](https://clawhub.ai/user/dongsheng123132) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill maintainers use this skill to validate and publish Claude Code skills across GitHub, ClawHub, and community marketplace repositories. It is intended for release workflows that may create public repositories, publish package metadata, or open marketplace pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make public external changes under the user's GitHub and ClawHub accounts. <br>
Mitigation: Verify the active GitHub and ClawHub accounts, require a dry run, and obtain explicit confirmation before creating repositories, pushing commits, publishing, or opening pull requests. <br>
Risk: Publishing the wrong directory can expose secrets, credentials, or private files. <br>
Mitigation: Inspect the exact skill directory before publication and remove secrets, private files, and unrelated artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongsheng123132/skill-multi-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/dongsheng123132) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, checklists, generated file content, and publication summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify files, initialize Git repositories, push commits, publish to ClawHub, and open pull requests when used with authenticated CLIs.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
