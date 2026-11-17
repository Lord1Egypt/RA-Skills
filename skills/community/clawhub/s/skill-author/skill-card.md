## Description:

Author, harden, and publish agent skills for ClawHub — write skills that conform to ClawHub conventions (frontmatter, structure, naming, versioning, licensing), run pre-publish hardening, and remediate clawhub.ai security-audit findings. Use when creating a skill for ClawHub, preparing a new version to publish, or when given a clawhub.ai/<owner>/<slug>/security-audit page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshinejnjn](https://clawhub.ai/user/sunshinejnjn)

### License/Terms of Use:

BSD 3-Clause

## Use Case:

Developers and skill authors use this agent skill to create ClawHub-compatible skills, review them before release, and address findings from ClawHub security audits. It provides authoring guidance, hardening checklists, and publishing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has medium confidence and partial coverage, so some referenced guidance and shell examples were not fully inspected.

Mitigation: Review the referenced guidance, especially shell examples, before following the steps; treat the benign verdict as favorable but incomplete.

## Reference(s):

- [Authoring guide](references/authoring-guide.md)
- [Audit patterns and fixes](references/audit-patterns.md)
- [Publish checklist](references/publish-checklist.md)
- [ClawHub skill page](https://clawhub.ai/sunshinejnjn/skills/skill-author)

## Skill Output:

**Output Type(s):** [Markdown guidance, Skill files, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell examples and skill-file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content and file paths depend on the operator's skill and chosen scope.]

## Skill Version(s):

1.2.3 (source: frontmatter, VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
