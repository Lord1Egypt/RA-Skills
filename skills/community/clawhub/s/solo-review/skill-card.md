## Description:

Final code review and quality gate that runs tests, checks coverage, audits security, verifies acceptance criteria, and generates a ship-ready report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill as a final quality gate before shipping or after deployment. It reviews test, build, lint, security, acceptance-criteria, documentation, commit, and visual/E2E evidence and produces a go/no-go report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit and commit documentation, requirements, planning files, and future-agent guidance as part of its review workflow.

Mitigation: Require explicit approval before write or git commit actions, and review generated diffs before accepting them.

Risk: The skill may run dependency installs, test suites, audits, builds, and production log commands that can execute project code or access operational environments.

Mitigation: Run dependency and production-log checks only in isolated environments with scoped credentials and least-privilege access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fortunto2/skills/solo-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Files, Configuration instructions, Guidance]

**Output Format:** [Markdown review report with command evidence, file references, and optional documentation or planning file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run project checks and, when directed by its workflow, update review-related documentation, planning checkboxes, and commits.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
