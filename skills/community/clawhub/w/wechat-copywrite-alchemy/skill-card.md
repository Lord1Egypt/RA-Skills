## Description:

Analyzes multiple articles from an author to reconstruct thinking patterns and writing style, then generates a dedicated writing-style prompt and installable persona sub-skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operators, and writing-style researchers use this skill to analyze a body of author articles, build a reusable persona, and generate future content in a consistent style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent author-style personas with strong identity-style instructions.

Mitigation: Review generated personas before use and avoid cloning living or identifiable authors without permission.

Risk: The skill may fetch public-platform content through RedFox and read user-specified local article files or folders.

Mitigation: Use only intended public sources or approved local files, and confirm collected material before generating a persona.

Risk: Generated style clones could be used for deceptive attribution.

Mitigation: Do not present generated content as if it were written by the original author.

Risk: The workflow depends on a RedFox API key.

Mitigation: Keep REDFOX_API_KEY scoped and revocable, and do not expose it in prompts, logs, code, or generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/wechat-copywrite-alchemy)
- [RedFoxHub](https://redfox.hk)
- [Core Workflow](references/core_workflow.md)
- [Writing Style and Thinking Framework](references/7-dimensions-framework.md)
- [Persona Template](references/persona-template.md)
- [Writing Formulas](references/writing-formulas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated prompt text and local skill-file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a persistent local author-style sub-skill and requires REDFOX_API_KEY for RedFox platform collection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
