## Description:

Creates animated single-file HTML presentation decks at 1280×720 with transitions and keyboard navigation, once the required sn-ppt-entry and sn-ppt-story prerequisites have prepared the task and outline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Presentation authors and agents use this skill to turn an approved outline into a polished, animated HTML deck. It requires sn-ppt-entry and sn-ppt-story to prepare the task files and outline first.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renderer disables browser safeguards while loading online scripts.

Mitigation: Restore certificate validation, CSP enforcement, and Chromium sandboxing before using confidential slides; prefer locally bundled fonts and libraries for offline use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sensenova-skills/skills/sn-ppt-dazzle)
- [Publisher profile](https://clawhub.ai/user/sensenova-skills)
- [Style families](references/style-families.md)
- [Fancy cookbook](references/fancy-cookbook.md)

## Skill Output:

**Output Type(s):** [HTML, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Single-file animated HTML deck, with optional local image assets and rendered screenshots; planning notes in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deck uses a 1280×720 canvas and supports keyboard navigation; page content follows the supplied outline.]

## Skill Version(s):

2026.10.29 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
