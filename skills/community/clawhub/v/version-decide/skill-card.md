## Description:

Recommends one next SemVer version for an upcoming release based on code changes, with a concise rationale and standards references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elisabeth15501](https://clawhub.ai/user/elisabeth15501)

### License/Terms of Use:

MIT

## Use Case:

Developers deciding the next release version use this skill to classify code changes and obtain one SemVer recommendation, including pre-release and 0.x cases. It is not intended for CalVer or looking up published versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local project version metadata is read to determine the current version.

Mitigation: Keep access limited to the documented read-only discovery workflow.

Risk: A wrong compatibility classification could produce an unsuitable release version.

Mitigation: Review the recommendation and confirm ambiguous breaking changes before publishing.

Risk: The bundled Python calculator is executed during version analysis.

Mitigation: Restrict execution to the bundled calculator; do not grant write, network, or package-install permissions.

## Reference(s):

- [Version Decider on ClawHub](https://clawhub.ai/elisabeth15501/skills/version-decide)
- [Version decision tables](references/decision-tables.md)
- [Versioning standards comparison](references/standards-comparison.md)
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown with one version recommendation, rationale, and next-step command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request confirmation when a breaking change is uncertain.]

## Skill Version(s):

1.1.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
