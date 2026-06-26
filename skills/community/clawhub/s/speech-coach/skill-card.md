## Description: <br>
speech-coach is a text-only public speaking coach with a 15-step curriculum, scenario practice, script annotation, seven-dimension scoring, and local progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and coaches use this skill to practice public speaking through text conversation, structured lessons, realistic workplace scenarios, and annotated speech drafts. It supports body-language concepts through quizzes and script markup, not audio or video assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves coaching profile and progress history as plaintext local files. <br>
Mitigation: Avoid entering sensitive workplace or personal details, and review or delete ~/.openclaw/workspace/speech-coach when the retained history is no longer needed. <br>
Risk: The skill cannot hear audio or see posture, gestures, facial expression, or eye contact. <br>
Mitigation: Use body-language steps as knowledge checks and script-annotation review, then verify physical delivery through offline practice, recordings, or human feedback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chameleon-nexus/speech-coach) <br>
- [Publisher profile](https://clawhub.ai/user/chameleon-nexus) <br>
- [README](artifact/README.md) <br>
- [Curriculum](artifact/curriculum.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style coaching dialogue with inline shell commands and local JSON progress data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only coaching; progress tracker stores profile and scoring history under ~/.openclaw/workspace/speech-coach.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
