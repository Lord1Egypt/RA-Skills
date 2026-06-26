## Description: <br>
Prepare Claw skills for public release by auditing structure, security, portability, documentation, testing, git hygiene, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acastellana](https://clawhub.ai/user/acastellana) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and maintainers use this skill to prepare Claw skills for public release, including audits for structure, secrets, portability, documentation quality, testing readiness, git hygiene, and metadata completeness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publish workflow can commit and push an entire skill directory to GitHub. <br>
Mitigation: Run it only in a dedicated clean skill directory, inspect git status and git diff before publishing, and confirm the active GitHub account and repository visibility. <br>
Risk: Built-in secret checks are limited and may not cover every file type or historical commit. <br>
Mitigation: Run a full secret scan across all file types and review git history before pushing. <br>
Risk: Force mode can skip confirmation prompts during publishing. <br>
Mitigation: Avoid --force unless the target directory, git remote, and changes have already been manually reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/acastellana/skill-publisher-claw-skill) <br>
- [Publisher profile](https://clawhub.ai/user/acastellana) <br>
- [GitHub Issues](https://github.com/acastellana/skill-publisher-claw-skill/issues) <br>
- [Claw Docs](https://docs.clawd.bot) <br>
- [Versioning guide](docs/versioning.md) <br>
- [Deprecation process](docs/deprecation.md) <br>
- [README quality guide](docs/readme-quality.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and generated or modified skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local shell scripts that inspect or modify skill directories and git state.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
