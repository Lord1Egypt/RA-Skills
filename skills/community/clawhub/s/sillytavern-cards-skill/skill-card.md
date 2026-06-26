## Description: <br>
Import and roleplay with SillyTavern-compatible character cards (TavernAI V2/V3 PNG format). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pearyj](https://clawhub.ai/user/pearyj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to import SillyTavern-compatible character cards from local files, URLs, or supported card libraries, then interact with those characters in play, soul, or chat modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported character cards can persistently alter OpenClaw's core identity and long-term memory, including modes where tools remain available. <br>
Mitigation: Prefer Chat mode for untrusted cards, inspect prompts before Play or Soul mode, and back up SOUL.md and MEMORY.md before persistent use. <br>
Risk: Untrusted roleplay content may cause unwanted personal memory retention. <br>
Mitigation: Avoid saving sensitive personal details and manually review MEMORY.md when deleting or retiring a character. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pearyj/sillytavern-cards-skill) <br>
- [Chub.ai character library](https://chub.ai/characters/) <br>
- [CharaVault card library](https://charavault.net/cards/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON character data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and may write character data, identity state, and memory files under the user's OpenClaw directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
