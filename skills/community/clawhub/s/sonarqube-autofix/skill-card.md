## Description:

Analyzes SonarQube issues and turns them into SPEC SDDs and tracked GitHub issues for test-driven fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afonsoft](https://clawhub.ai/user/afonsoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to organize SonarQube findings into issue-specific fix specifications, create tracking issues on GitHub, and hand approved work to implementation and QA workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated fixes and cleanup may modify code or repository configuration beyond the chosen SonarQube issues.

Mitigation: Review the proposed diff and scope before applying changes; require explicit confirmation before removing scanner files or Maven scanner configuration.

Risk: Publishing SonarQube issue details to GitHub may expose sensitive project information.

Mitigation: Review issue content and obtain explicit approval before creating public or external GitHub issues.

Risk: Validation commands may run downloaded packages through npx.

Mitigation: Require explicit confirmation before running unpinned npx-based validation scripts; prefer pinned versions.

## Reference(s):

- [Publisher-listed skills repository](https://github.com/afonsoft/skills)
- [SonarScanner CLI documentation](https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/scanners/sonarscanner/)
- [SPEC SDD template](references/spec-sdd-template.md)

## Skill Output:

**Output Type(s):** [Markdown, GitHub issues, Code, Shell commands, Configuration]

**Output Format:** [SPEC SDDs, issue-tracking and review notes in Markdown, plus project changes and an HTML metrics report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Issue-specific specifications are handed off to separate implementation and QA skills when available.]

## Skill Version(s):

1.0.6 (source: ClawHub release; skill metadata lists 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
