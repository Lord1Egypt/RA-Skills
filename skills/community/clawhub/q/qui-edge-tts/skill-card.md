## Description: <br>
Converts requested text into speech through the SkillBoss API Hub TTS service, with support for voice, language, speed, pitch, volume, format, and subtitle options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agent operators use this skill to turn requested text, summaries, or messages into audio for accessibility, multitasking, and voice-output workflows. It also supports customized voice, language, prosody, output format, and subtitle settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested text is sent to an external SkillBoss/HeyBoss TTS service and may include private content. <br>
Mitigation: Install only if the service is trusted for the text being spoken, avoid sending sensitive content when possible, and clean up generated files that contain private information. <br>
Risk: The skill requires SKILLBOSS_API_KEY, and an exposed key could allow unauthorized service use. <br>
Mitigation: Use a scoped API key, provide it through the environment, keep it out of committed files and shared shell history, and rotate it if exposed. <br>
Risk: Generated audio or subtitle files can retain spoken content on disk. <br>
Mitigation: Store outputs only in intended locations and delete temporary audio or subtitle files when they are no longer needed. <br>


## Reference(s): <br>
- [node-edge-tts Reference](references/node_edge_tts_guide.md) <br>
- [Voice testing](https://tts.travisvn.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Audio files, JSON, Shell commands, Configuration] <br>
**Output Format:** [MEDIA path or MP3 audio file, with optional JSON subtitle file and CLI/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and internet access; generated audio and subtitle files may need cleanup when they contain private content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
