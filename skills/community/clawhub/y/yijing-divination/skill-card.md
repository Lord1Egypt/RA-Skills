## Description: <br>
易经占卜系统。支持铜钱法、蓍草法起卦，生成本卦、互卦、变卦，提供Oracle Voice诠释。当用户请求占卜、问卦、易经解读、或寻求决策指引时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RyanChromium](https://clawhub.ai/user/RyanChromium) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
External users and agents use this skill for reflective I Ching divination: generating hexagrams with coin or yarrow methods, then composing a poetic Oracle Voice interpretation of the user's question. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User question text may be placed into a shell command when invoking the divination script. <br>
Mitigation: Invoke scripts/divine.py with safe argument passing and avoid substituting raw user text into shell command strings. <br>
Risk: Divination-style output could be mistaken for advice in financial, medical, legal, safety, or other high-stakes contexts. <br>
Mitigation: Use the skill only for reflective or entertainment-style interpretation and avoid presenting results as decisions or professional guidance. <br>
Risk: The release has a suspicious security verdict and should be reviewed before installation. <br>
Mitigation: Review and scan the skill before deployment, paying particular attention to command invocation paths. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/RyanChromium/yijing-divination) <br>
- [Hexagram metadata](references/hexagrams_metadata.json) <br>
- [Full hexagram data](assets/hexagrams_full.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON from the divination script plus Markdown or plain-text Oracle Voice interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes generated main, nuclear, and relating hexagrams; may include a visual hexagram rendering and reflective interpretive prose.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
