## Description:

Generate diverse, non-repetitive image prompts using Dribbble-derived visual references, style cards, prompt patterns, and design vocabulary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdullah4ai](https://clawhub.ai/user/abdullah4ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, and agent users use this skill to create specific, varied image-generation prompts grounded in real visual references. It is also useful for refreshing local design-reference JSON data and building style cards for prompt diversity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public Dribbble/reference metadata, imported titles, descriptions, and URLs may contain untrusted or misleading content.

Mitigation: Treat scraped and imported metadata as untrusted, review generated prompts and source URLs before giving an agent tool access, and avoid following unknown links automatically.

Risk: Optional HTML scraping adds network access and third-party dependencies.

Mitigation: Prefer manual import or RSS where practical, and use a virtual environment with pinned requests and beautifulsoup4 versions when HTML scraping is enabled.

Risk: Local JSON files can accumulate stale, unwanted, or sensitive prompt-history and reference data.

Mitigation: Review data/references.json, data/style_cards.json, and data/prompt_history.json before deployment or sharing, and remove entries that should not guide future prompts.

## Reference(s):

- [Visual Prompt Engine on ClawHub](https://clawhub.ai/abdullah4ai/skills/visual-prompt-engine)
- [Prompt Patterns](artifact/references/prompt-patterns.md)
- [Visual Vocabulary](artifact/references/visual-vocabulary.md)
- [Style Card Schema](artifact/references/style-card-schema.md)
- [Dribbble Popular Shots](https://dribbble.com/shots/popular)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown or plain text image prompts, with optional inline shell commands and JSON configuration guidance for reference collection.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local JSON files for references, style cards, and prompt history.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
