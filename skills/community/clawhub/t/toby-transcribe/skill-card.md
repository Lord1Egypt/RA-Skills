## Description: <br>
Speech-to-text via SkillBoss API Hub (STT, powered by Whisper and more). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe or translate selected audio through SkillBoss API Hub without downloading a local speech model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio submitted for transcription may include private, customer, meeting, or regulated data. <br>
Mitigation: Only send audio you are authorized to process with SkillBoss, and confirm the data handling terms before using it for sensitive recordings. <br>
Risk: The skill requires a sensitive SkillBoss API key. <br>
Mitigation: Store SKILLBOSS_API_KEY in an environment variable or secret manager and avoid pasting it into prompts, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/toby-transcribe) <br>
- [SkillBoss API Hub](https://api.skillbossai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and JSON response references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends selected audio to SkillBoss for remote transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
