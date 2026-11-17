## Description:

Builds TierVibe tier lists through a one-question-at-a-time interview, then prepares a launcher handoff that opens the populated board in the user's browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edison7009](https://clawhub.ai/user/edison7009)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create new TierVibe ranking boards with custom tiers, text or image cards, markdown explanations, and a browser-based import handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create local launcher or manifest files as part of the handoff.

Mitigation: Review generated local files before opening them, and keep the launcher scoped to the intended TierVibe import URL.

Risk: User-provided local images may be embedded in the board and uploaded to TierVibe's CDN when the user publishes.

Mitigation: Do not include private or sensitive images unless the user is comfortable publishing or uploading them through TierVibe.

Risk: External image URLs can fail or cause publishing issues when their hosts block cross-origin canvas use.

Mitigation: Prefer user-provided local images embedded as data:image URLs when appropriate, or have the user replace external placeholders in the TierVibe editor.

## Reference(s):

- [TierVibe import page](https://tiervibe.com/t/import)
- [ClawHub skill page](https://clawhub.ai/edison7009/skills/tierlist-maker)
- [Data schema](references/data-schema.md)
- [Import flow](references/import-flow.md)
- [Text and image cards](references/text-cards.md)
- [Tier presets and colors](references/tier-config.md)
- [Explanations markdown](references/explanations.md)
- [Worked example](examples/ai-models-tierlist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown conversation with generated JSON payloads and local launcher HTML handoff]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local handoff files such as launcher.html, and may embed user-provided local images as data:image URLs when file access is available.]

## Skill Version(s):

1.0.11 (source: server release metadata; artifact frontmatter lists 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
