## Description:

A Chinese text-adventure game skill that helps agents create custom scenarios, process free-form player actions, and return structured story responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[810722796-lgtm](https://clawhub.ai/user/810722796-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and game-focused agent workflows use this skill to generate and run interactive Chinese text adventures from custom plots or themes. It supports formatted narrative output, player status summaries, inventory display, and local save/load behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gameplay text, player state, and custom script content may be saved locally.

Mitigation: Avoid entering secrets or sensitive personal information unless local storage is acceptable, and review saved content before sharing files.

Risk: The documented LLM extension path could send gameplay content to a remote API if a user implements it.

Mitigation: Require explicit consent for remote API calls and document the model provider, data handling, and credential requirements before enabling the extension.

Risk: Future named save-slot support could read or write unintended files if save names are accepted unchecked.

Mitigation: Validate save-slot names, restrict them to safe characters, and keep save/load operations inside the intended save directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/810722796-lgtm/skills/text-adventure-game-skill)
- [Artifact README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Warhammer 40K template](artifact/data/templates/warhammer_40k.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown-formatted Chinese narrative text, with optional Python code and configuration guidance for extensions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include scene headers, separators, numbered choices, player status, inventory, and save/load command guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
