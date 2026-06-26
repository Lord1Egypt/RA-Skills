## Description: <br>
Voice Clone helps agents generate local speech audio from text using Edge TTS, OpenAI, ElevenLabs, or Coqui with selectable voices, language, rate, pitch, and tone controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, builders, and end users use this skill to turn Chinese or English text into natural speech audio, choose from preset voices, and route synthesis through local or third-party TTS engines. It is suited for agent workflows that need generated narration, previews, or batch text-to-speech output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audio script can run an unsafe shell command when opening a user-chosen output filename. <br>
Mitigation: Review or patch the script before installing; remove the automatic xdg-open os.system call or replace it with a non-shell subprocess call, and avoid unusual or untrusted output filenames until fixed. <br>
Risk: OpenAI and ElevenLabs modes send text and voice-related material to third-party services. <br>
Mitigation: Use those engines only for text and voice material that is acceptable to share with the selected provider, and keep API keys in environment variables rather than hardcoding them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/voice-clone-tts-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Audio files, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Local audio files with terminal status text and markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audio is saved under ~/.cache/voice-clone/ by default or to a user-specified output path; OpenAI and ElevenLabs modes require API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
