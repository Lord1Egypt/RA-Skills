## Description:

Guides skill authors through auditing, sanitizing, verifying, and publishing agent skills to ClawHub, SkillHub, and GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this workflow to audit source content for personal data, credentials, and other publishing concerns, then prepare and verify a release. Publishing stages include explicit approval gates before external publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious, citing reported source-file overwrite and safeguard concerns; scan coverage is incomplete (7 of 9 components) and some checks were partial.

Mitigation: Review the reported overwrite behavior, approval safeguards, and network permissions before use. Inspect proposed file changes and require explicit approval before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haiyangchenbj/skills/skill-audit-publish)
- [Publish rules](references/publish-rules.md)
- [SkillHub publishing guide](references/skillhub-publish.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Audit summaries and approval details in text or Markdown, publishing files, and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Files and summaries depend on the source skill and selected publishing stages.]

## Skill Version(s):

1.5.12 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
