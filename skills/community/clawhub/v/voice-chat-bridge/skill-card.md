## Description: <br>
Enables agents to transcribe spoken audio, generate Edge TTS voice replies, and serve or share generated audio through local web or optional tunnel modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrickgeek](https://clawhub.ai/user/patrickgeek) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and assistant builders use this skill to add voice-first interaction to an agent workflow. It helps convert incoming audio to text, produce spoken replies, and return generated audio through local playback, a web server, or chat platform links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture or process spoken content and generate stored audio files. <br>
Mitigation: Review the voice configuration before use, avoid sensitive speech in automated workflows, and delete generated voice files when they are no longer needed. <br>
Risk: Optional tunnel modes can expose the local voice service and generated audio beyond the local machine. <br>
Mitigation: Keep the skill in local mode unless public access is required, restrict tunnel configuration, and disable public tunnels when finished. <br>
Risk: Interaction tracking such as habits.json may retain voice interaction behavior data. <br>
Mitigation: Disable or remove interaction tracking that is not wanted and periodically review stored workspace files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patrickgeek/voice-chat-bridge) <br>
- [Edge TTS GitHub](https://github.com/rany2/edge-tts) <br>
- [hear macOS speech recognition](https://github.com/sveinbjornt/hear) <br>
- [Cloudflare Tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and Python utility scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate MP3 voice files and local or public URLs according to the user's voice configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
