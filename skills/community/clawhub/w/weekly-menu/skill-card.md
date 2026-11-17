## Description:

Generates a weekly meal plan with images, recipes, shopping lists, and a Feishu document with Xiaohongshu source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beginnerrudy](https://clawhub.ai/user/beginnerrudy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan a week of home-cooked meals, collect recipe inspiration, and generate a shareable Feishu document with images, checkboxes, source links, and shopping-list support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu credentials and folder tokens may be exposed or overused if read from broad local configuration or memory.

Mitigation: Store Feishu credentials and folder tokens in a scoped connector or secret store, and grant only the permissions needed for weekly menu document creation.

Risk: Document delete and move examples could be used without enough user control if treated as available actions.

Mitigation: Remove those examples unless they become explicit features, and require clear user confirmation before any destructive or relocation action.

Risk: External recipe searches and image downloads can introduce untrusted or invalid content into the generated menu document.

Mitigation: Keep source links visible, verify downloaded images before upload, and review generated recipes before sharing or relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beginnerrudy/skills/weekly-menu)
- [Feishu Document Creation Recipe Guide](references/feishu-doc-recipe.md)
- [Meal Profile Template](references/profile-template.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Chat response with a Feishu document link, generated Feishu document content, YAML profile/history updates, and shell/API command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates external Feishu documents and local meal profile/history files when run with configured credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
