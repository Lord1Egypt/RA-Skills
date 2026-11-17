## Description:

Import and roleplay with SillyTavern-compatible character cards (TavernAI V2/V3 PNG format)

This skill is ready for commercial/non-commercial use.

## Publisher:

[pearyj](https://clawhub.ai/user/pearyj)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to import PNG, WEBP, or JSON character cards and chat with those personas across supported messaging channels. It supports local files, URLs, online card search, and play, soul, and chat interaction modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted community character cards can persistently affect the agent's identity and memory in Play or Soul mode.

Mitigation: Prefer /character chat for untrusted cards, inspect card contents before persistent use, and back up SOUL.md and MEMORY.md before enabling Play or Soul mode.

Risk: Soul mode keeps normal assistant capabilities available while a third-party character persona is active.

Mitigation: Use Soul mode only with trusted cards and review tool-using responses before acting on them.

Risk: Arbitrary card URLs and character names with spaces or special characters can increase handling mistakes during import and file operations.

Mitigation: Download cards from trusted sources, quote paths consistently, and normalize character filenames before saving them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pearyj/skills/sillytavern-cards-skill)
- [Chub.ai character library](https://chub.ai)
- [CharaVault card library](https://charavault.net/cards/)
- [AI Character Cards](https://aicharactercards.com)
- [Character Tavern](https://charactertavern.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON character-card data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js. Persistent modes may write character data, identity text, and memory text under the user's OpenClaw directory.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
