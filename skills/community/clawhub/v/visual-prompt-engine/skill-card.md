## Description: <br>
Generate diverse, non-repetitive image prompts powered by real visual references from Dribbble and design platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdullah4AI](https://clawhub.ai/user/Abdullah4AI) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to generate design-informed image prompts from visual references, prompt patterns, and precise visual vocabulary. It is useful when an agent needs to improve prompt variety, avoid repeated visual tropes, or turn a creative goal into a structured image prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch public Dribbble references during reference collection. <br>
Mitigation: Use manual import or run fetching only in environments where outbound access to public design references is acceptable. <br>
Risk: The skill keeps local JSON files, including prompt history, for deduplication. <br>
Mitigation: Avoid sensitive creative briefs and periodically review or clear local prompt-history data according to your retention needs. <br>
Risk: The optional cron refresh creates recurring background updates. <br>
Mitigation: Enable scheduled refresh only when recurring reference updates are desired and approved. <br>


## Reference(s): <br>
- [Prompt Patterns](references/prompt-patterns.md) <br>
- [Style Card Schema](references/style-card-schema.md) <br>
- [Visual Vocabulary](references/visual-vocabulary.md) <br>
- [Dribbble Popular Shots](https://dribbble.com/shots/popular) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with optional shell commands and JSON file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local style-card and prompt-history JSON files to select references and avoid repetitive prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
