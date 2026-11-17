## Description:

Provides usage guidance and API references for @ht-smart/basic components, including tables, trees, forms, modals, drawers, dictionaries, selectors, layouts, upload components, and related enterprise UI utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaowenqiang123](https://clawhub.ai/user/xiaowenqiang123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to look up @ht-smart/basic component usage patterns, prop APIs, examples, and integration notes while building enterprise React interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated component guidance may be applied to destructive callbacks such as delete operations without enough confirmation or recovery behavior.

Mitigation: Require product-specific confirmation, authorization, and recovery expectations before wiring delete callbacks into production workflows.

Risk: Upload examples may be adapted for sensitive files without validating endpoint suitability or data-handling requirements.

Mitigation: Confirm upload endpoints, storage policies, and access controls before sending sensitive files through components based on the examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaowenqiang123/skills/smart-web-components-usage)
- [api-pro-table.md](artifact/api-pro-table.md)
- [api-pro-tree.md](artifact/api-pro-tree.md)
- [api-form.md](artifact/api-form.md)
- [api-dict.md](artifact/api-dict.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with TypeScript and TSX examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only responses; no executable runtime behavior is included in the skill.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
