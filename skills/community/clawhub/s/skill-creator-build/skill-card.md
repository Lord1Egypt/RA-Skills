## Description:

Build generates a customized project-building skill that guides an agent and user through project planning, technical decisions, staged implementation, validation, and project closeout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balancegsr](https://clawhub.ai/user/balancegsr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and project builders use this skill to create a tailored build-management skill for software, agent-skill, tooling, or technical delivery projects. It is best suited when a user wants systematic project guidance rather than one-off coding assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation wording for build and project-management intent.

Mitigation: Install it deliberately for workspaces where systematic build-process guidance should take priority over ad-hoc coding.

Risk: The skill can create workspace directories, generated skills, and persistent local project notes after confirmation.

Mitigation: Use the ZIP delivery option when you want to inspect or share generated files before placing them in a workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/balancegsr/skills/skill-creator-build)
- [README](README.md)
- [Engineering checklist template](references/templates/guides/engineering_checklist.md)
- [Full project review template](references/templates/guides/project_review_full.md)
- [Lite project review template](references/templates/guides/project_review_lite.md)
- [Full build skill template](references/templates/skill/full.md)
- [Lite build skill template](references/templates/skill/lite.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational guidance plus generated Markdown skill files, reference files, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local workspace directories and persistent project notes after user preview and delivery confirmation.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
