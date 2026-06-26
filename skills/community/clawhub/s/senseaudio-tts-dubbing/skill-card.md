## Description: <br>
Generates SenseAudio text-to-speech dubbing audio from user-provided copy with controls for voice, speed, pitch, volume, and output format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klilyz](https://clawhub.ai/user/klilyz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content, marketing, and operations teams use this skill to turn short-video scripts, product introductions, and promotional copy into local audio files through the SenseAudio TTS API. It also guides users through API key setup, voice selection, audio parameter tuning, and output path choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided TTS text to the SenseAudio remote service. <br>
Mitigation: Use it only after the user explicitly requests text-to-speech generation, and avoid sending sensitive or restricted text unless the user has approved that data flow. <br>
Risk: The skill requires the SENSEAUDIO_API_KEY credential. <br>
Mitigation: Keep the API key in a managed environment variable or secret store, avoid embedding it in prompts or files, and rotate it if exposure is suspected. <br>
Risk: The security scan reports that the script can silently install the requests package at runtime, which may modify the user environment and fetch unpinned code. <br>
Mitigation: Prefer installing and pinning dependencies through the normal environment setup before use, or review and remove the automatic pip-install logic for stricter supply-chain control. <br>


## Reference(s): <br>
- [SenseAudio Documentation](https://senseaudio.cn/docs) <br>
- [SenseAudio TTS API Endpoint](https://api.senseaudio.cn/v1/t2a_v2) <br>
- [ClawHub Skill Page](https://clawhub.ai/klilyz/senseaudio-tts-dubbing) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated audio files may be mp3, wav, pcm, or flac.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENSEAUDIO_API_KEY and sends requested TTS text to the SenseAudio remote service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
