## Description:

Convert native WeChat Mini Program projects into uni-app + Vue3 + TypeScript cross-platform projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate native WeChat Mini Program projects into runnable uni-app projects using Vue 3 and TypeScript. It supports project analysis, configuration migration, page and component conversion, utility migration, API namespace changes, and final verification guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write a converted project tree to an output directory selected by the user.

Mitigation: Confirm the output path is new or backed up before running conversion work.

Risk: Post-conversion npm install and npx commands may use unpinned package versions.

Mitigation: Run package commands as separate manual steps, pin versions where possible, and use a project or container without unrelated credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/wmp-to-uniapp)
- [WeChat Mini Program to uni-app Mapping Reference Table](references/mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, configuration snippets, and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read a user-provided source project and write converted files to a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
