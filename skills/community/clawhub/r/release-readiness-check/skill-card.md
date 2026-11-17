## Description:

Release Readiness Check runs local static pre-release checks for Dockerfiles, Kubernetes manifests, SQL migrations, OpenAPI compatibility, and .env configuration, then summarizes release risk in a report and gate verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[po-et](https://clawhub.ai/user/po-et)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release engineers, and CI maintainers use this skill before shipping to inspect common deployment, migration, API, and configuration risks and to generate a Markdown or JSON release-readiness report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags under-disclosed filesystem boundary risks around symlink handling and report writing.

Mitigation: Run the skill only on trusted repositories or inside a sandbox, avoid scanning untrusted repositories with preserved symlinks, and write reports outside untrusted worktrees.

Risk: Generated reports may include source snippets or configuration findings.

Mitigation: Review reports before sharing them outside the project team.

Risk: Static heuristic checks can miss runtime, capacity, dependency, and semantic API problems.

Mitigation: Use this as an early release gate and keep specialized testing, monitoring, schema review, and human release review in the deployment process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/po-et/skills/release-readiness-check)
- [Project homepage from ClawHub metadata](https://github.com/po-et/workbuddy-skills)
- [Publisher profile](https://clawhub.ai/user/po-et)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report, optional JSON summary, and terminal status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The --strict mode can fail CI when high findings or unknown checks are present.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter version is 0.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
