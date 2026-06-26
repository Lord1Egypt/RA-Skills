## Description: <br>
Track smoking and nicotine use, reduce consumption, or quit with neutral logs, trigger mapping, and adaptive plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to keep neutral local records of smoking or nicotine use, identify triggers, and choose logger, reduction, or quit-mode next steps. It provides coaching and tracking support, not medical diagnosis or emergency care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update sensitive local notes about smoking, nicotine use, triggers, and plans under ~/smoking/. <br>
Mitigation: Review each proposed file write before confirming, keep the files only on trusted devices, and delete or pause the local files when that history should no longer be retained. <br>
Risk: Users may treat coaching content as medical advice during health-sensitive situations. <br>
Mitigation: Use the skill for tracking and behavior-change support only, and seek immediate professional care for chest pain, severe breathing issues, pregnancy-related concerns, self-harm thoughts, dangerous medication interactions, or other urgent medical concerns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/smoking) <br>
- [Skill homepage](https://clawic.com/skills/smoking) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text coaching, local note templates, tracking prompts, and plan updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill with no declared external network requests; proposed writes are local notes under ~/smoking/ and require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
