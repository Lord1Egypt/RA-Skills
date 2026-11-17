## Description:

Add frontend pages to WCS (Warehouse Control System) applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers working on WCS Vue2 frontends use this skill to add business list pages that follow existing API, routing, table, dialog, import/export, and i18n conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated page work can use the wrong backend endpoint shape or permission policy string if those details are assumed.

Mitigation: Confirm backend endpoint shapes, dictionary keys, and permission policy strings before applying the skill's page, API, route, and i18n guidance.

Risk: New files, routes, or i18n keys can duplicate or conflict with existing WCS frontend implementation history.

Mitigation: Check for existing files, deleted paths, route names, API names, and i18n keys before creating or modifying frontend assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/wcs-add-frontend-page)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline JavaScript, Vue, shell command, route, and i18n snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for missing endpoint, dictionary, or collision details before proposing repository changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
