## Description: <br>
Provides context-aware Python linting with pattern-based heuristics for reviewing GitHub pull requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claytantor](https://clawhub.ai/user/claytantor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to lint Python projects and GitHub pull request changes, including checks for secrets, FastAPI documentation, React hook dependency patterns, and standard Pylint findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub Actions workflows run with repository permissions and may read repository secrets. <br>
Mitigation: Review workflow files before committing them, pin copied workflow sources to a reviewed commit when downloading, and grant only the permissions required for PR linting. <br>
Risk: GitHub tokens, bot tokens, or webhook URLs passed on the command line can be exposed through process listings or shell history. <br>
Mitigation: Use least-privilege tokens and prefer environment-backed configuration for notification credentials instead of direct command-line arguments. <br>
Risk: Optional notifications can send lint report details to external Telegram, Discord, Slack, or email services. <br>
Mitigation: Enable notification channels only when the repository owner accepts sharing those report details with the selected service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/claytantor/pylinter-assist) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and agent guidance with optional JSON or text lint output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can post pull request comments, write lint-report.json artifacts, and provide setup commands when configured.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release evidence, SKILL.md, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
