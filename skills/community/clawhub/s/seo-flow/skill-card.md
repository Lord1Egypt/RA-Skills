## Description:

FLOW framework integration for evidence-led SEO using the Find, Leverage, Optimize, Win, and Local stages, with stage-specific prompts from the FLOW knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, marketers, and content teams use this skill to select FLOW-stage guidance and prompts for keyword research, authority building, content optimization, conversion work, and local SEO. It helps agents produce concise SEO strategy, audit, brief, and rewrite guidance grounded in supplied evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional /seo flow sync command updates prompt text from a third-party repository.

Mitigation: Run the dry-run sync first, review the reported destination and files, and proceed only if the update is limited to the intended skill prompt library.

Risk: SEO outputs may include claims or recommendations that affect public content or marketing decisions.

Mitigation: Use supplied evidence, verify cited statistics against the bibliography or current source material, and review recommendations before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-flow)
- [Publisher profile](https://clawhub.ai/user/asale-ai)
- [FLOW Framework](references/flow-framework.md)
- [FLOW Prompt Library Index](references/prompts/README.md)
- [FLOW Bibliography](references/bibliography.md)
- [FLOW prompt source](https://github.com/AgriciDaniel/flow)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown with concise analysis, prompt selections, tables, checklists, attribution text, and occasional shell command blocks for sync operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stage-specific prompt files are loaded on demand; optimize-stage responses select exactly two or three relevant prompts.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
