## Description: <br>
Person-driven roleplay agent using actor-direction principles to build emotionally intelligent personas, run scene-based interactions, and generate natural dialogue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[defineagain](https://clawhub.ai/user/defineagain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, roleplay users, and creative agents use this skill to define scene-driven personas, generate in-character dialogue, set up emotionally grounded scenes, and record character arc notes after debriefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update local roleplay memory and persona files that may contain sensitive scene material. <br>
Mitigation: Require explicit user confirmation before any memory or persona update, and avoid using the skill for highly sensitive personal material. <br>
Risk: The artifact contains anti-safety wording around difficult roleplay material. <br>
Mitigation: Treat those statements as creative-writing posture only; platform rules, user boundaries, and applicable safety policies remain authoritative. <br>
Risk: Local file paths used by helper scripts are under-scoped and may not match the installing environment. <br>
Mitigation: Review script paths before execution and limit file access to the intended persona and memory directories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/defineagain/roleplay-agent) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [SOUL.md](artifact/SOUL.md) <br>
- [Beat Writing Format](artifact/assets/beat_format.md) <br>
- [Persona Template](artifact/personas/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown dialogue, persona templates, scene setup prompts, and arc log notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local persona memory files when the user approves debrief logging.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
