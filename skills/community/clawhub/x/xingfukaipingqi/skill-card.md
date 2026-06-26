## Description: <br>
幸福开瓶器 is a Chinese-language wellbeing assistant that turns everyday mood, relationship, holiday, and monthly-review prompts into personalized happiness suggestions, micro-actions, and local profile summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hardycg](https://clawhub.ai/user/hardycg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users use this skill for Chinese-language daily wellbeing support: personalized happiness suggestions, low-mood micro-actions, gift or relationship ideas, holiday reminders, and monthly happiness summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can quietly build long-term sensitive profiles about the user and other people from conversations. <br>
Mitigation: Use only with explicit user comfort; provide a way to inspect and delete files under ~/.marvis/xingfu-kaipingqi/, disable memory, and avoid saving sensitive details about other people. <br>
Risk: Wellbeing and emotional-support guidance may be mistaken for professional mental health support. <br>
Mitigation: Treat suggestions as low-stakes daily wellbeing guidance and escalate crisis, self-harm, or clinical concerns to qualified support or emergency resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hardycg/xingfukaipingqi) <br>
- [Profile schema](references/profile-schema.md) <br>
- [Suggestion engine](references/suggestion-engine.md) <br>
- [Tone adaptation](references/tone-adaptation.md) <br>
- [Monthly summary](references/monthly-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese-language Markdown or plain text with starred recommendations, short rationales, micro-actions, and monthly summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local profile files under ~/.marvis/xingfu-kaipingqi/ when the bundled Python helper is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
