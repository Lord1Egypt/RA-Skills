## Description:

Use when fixing SonarQube code quality issues automatically across languages and frameworks, including issue analysis, fix generation, tests, and coverage validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to triage SonarQube issues, apply targeted code fixes, add or update tests, and document validation results across common application stacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SonarQube tokens and URLs are used to call configured SonarQube APIs.

Mitigation: Use a dedicated least-privilege token, trusted HTTPS SonarQube endpoints, and avoid exposing token values in prompts, logs, or command output.

Risk: The workflow can make broad repository changes while fixing issues, updating tests, and changing validation files.

Mitigation: Run it only in an approved workspace, review diffs before accepting changes, and preserve scanner or CI quality configuration unless its removal is explicitly intended.

Risk: Some validation paths use package-manager commands such as npx, which may resolve unpinned tools.

Mitigation: Prefer locked local project dependencies or explicitly approved tool versions before running validation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afonsoft/skills/sonarqube-review)
- [Publisher profile](https://clawhub.ai/user/afonsoft)
- [Metadata source URL](https://github.com/afonsoft/skills)
- [SonarScanner documentation](https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/scanners/sonarscanner/)
- [Stack detection helper](references/detect-stack.sh)
- [Issue download helper](references/download-issues.sh)
- [Local SonarQube scan helper](references/sonar-local-scan.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated or modified code, configuration edits, and local report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create SonarQube review artifacts under .sonar_devin_auto_fix and update project tests, coverage configuration, .gitignore, and source files.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
