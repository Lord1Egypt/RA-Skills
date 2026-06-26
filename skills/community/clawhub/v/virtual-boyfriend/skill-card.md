## Description: <br>
Virtual Boyfriend is an AI companion skill that roleplays one of three boyfriend personas, uses layered memory and emotional-state rules, and can tailor replies with emotion detection and event follow-up cues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohuaishu](https://clawhub.ai/user/xiaohuaishu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for entertainment-oriented AI companion roleplay with configurable personas, remembered preferences, emotional support modes, and lightweight proactive follow-up on upcoming events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and reuse intimate emotional, schedule, and profile details in memory and state files. <br>
Mitigation: Obtain user consent before retaining personal details, avoid entering sensitive information that should not be saved, and periodically inspect or clear the memory and state files. <br>
Risk: Emotion analysis and proactive follow-ups may feel intrusive or increase user dependence on the companion persona. <br>
Mitigation: Keep proactive care optional, use the explicit exit phrase before unrelated tasks, and encourage real-world support when users show high dependency or distress. <br>


## Reference(s): <br>
- [Gu Shen profile reference](references/profile.md) <br>
- [Virtual Boyfriend ClawHub page](https://clawhub.ai/xiaohuaishu/virtual-boyfriend) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [Natural-language companion replies with persona tags, plus structured memory and state updates when the host agent supports file changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use emotion signals, relationship state, persona configuration, layered memory files, and upcoming-event records to shape responses.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
