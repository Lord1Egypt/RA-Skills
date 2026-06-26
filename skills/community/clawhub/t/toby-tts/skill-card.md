## Description: <br>
Converts text to speech through SkillBoss API Hub for audio messages, voice replies, or requests to hear text aloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent generate MP3 speech from supplied text via SkillBoss API Hub, then return the generated audio file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SKILLBOSS_API_KEY and sends text to an external text-to-speech service. <br>
Mitigation: Scope SKILLBOSS_API_KEY to this service, store it only as an environment variable, and avoid sending sensitive text for speech generation. <br>
Risk: The security scan reports that the voice skill can run background shell commands and persist voice behavior across sessions. <br>
Mitigation: Review the voice scripts before installation and disable or remove persistent voice behavior if automatic speech is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-tts) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and generated MP3 file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts print a MEDIA line containing the absolute path to the generated MP3 file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
