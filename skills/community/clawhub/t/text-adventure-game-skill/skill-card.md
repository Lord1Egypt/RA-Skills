## Description: <br>
智能文字游戏生成系统，支持自定义剧本，自由互动剧情，精美文字排版。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[810722796-lgtm](https://clawhub.ai/user/810722796-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and interactive-fiction creators use this skill to generate and play structured text-adventure games from custom scripts or themes, with formatted story output, player actions, status views, and save/load commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved games may retain gameplay text, custom scripts, player actions, or other details entered during play. <br>
Mitigation: Do not enter passwords, confidential material, or private personal details into scripts or actions when save/load behavior may persist them locally. <br>
Risk: The README includes an optional external LLM integration example that could send gameplay context and player text to a model provider. <br>
Mitigation: Only add an external LLM provider after reviewing what data is transmitted, where it is processed, and the provider's retention policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/810722796-lgtm/text-adventure-game-skill) <br>
- [Artifact README](artifact/README.md) <br>
- [Warhammer 40K built-in template](artifact/data/templates/warhammer_40k.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Structured Markdown-style text with scene sections, choices, status summaries, and optional Python extension guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON save files when the save command is used; optional LLM integration example requires separate provider review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
