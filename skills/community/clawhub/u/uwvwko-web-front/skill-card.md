## Description:

Generates static front-end web pages from user requests, saves HTML/CSS/JS project files, opens local previews, and uses bundled design learning notes to guide page quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uwvwko-zzz](https://clawhub.ai/user/uwvwko-zzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content creators use this skill to generate static website prototypes, landing pages, forms, portfolio pages, and small interactive pages from natural-language requirements. It also supports local project management tasks such as listing, opening, modifying, renaming, and deleting generated website folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delete and rename workflows could remove or move unintended files if project names or paths are unsafe.

Mitigation: Use the skill only in a disposable or well-contained website directory, validate simple project names, and review exact paths before delete or rename operations.

Risk: Generated checkout examples may look like production payment flows without providing production-grade payment handling.

Mitigation: Treat included checkout pages as front-end prototypes and add separately reviewed payment integration before any real transaction use.

Risk: Generated front-end code can contain incorrect layout, accessibility, browser compatibility, or interaction behavior.

Mitigation: Review generated HTML/CSS/JavaScript, test responsive behavior and accessibility, and scan files before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uwvwko-zzz/skills/uwvwko-web-front)
- [Design patterns learning notes](learning/design-patterns.md)
- [Advanced CSS techniques learning notes](learning/advanced-techniques.md)
- [Components learning notes](learning/components.md)
- [Typography learning notes](learning/typography.md)
- [CSS-Tricks](https://css-tricks.com)
- [Tailwind UI](https://tailwindui.com)
- [CodePen](https://codepen.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local static website files under html/<project>/ and may provide OS-specific browser preview commands.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
