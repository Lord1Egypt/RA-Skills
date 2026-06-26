## Description: <br>
iFlytek Ultra-Realistic TTS synthesizes natural, expressive speech from text using iFlytek's ultra-realistic voice synthesis API, with multiple voices and adjustable speed, volume, pitch, and output format options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert supplied text, files, or stdin into narrated audio through iFlytek's text-to-speech service. It is suited for generating voice content, narration, and speech assets when the required iFlytek credentials and enabled voices are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected text and iFlytek API credentials to iFlytek, and the security review notes that its TLS connection deliberately disables certificate checks. <br>
Mitigation: Install only if that data transfer is acceptable, avoid sensitive or regulated text, and review or fix TLS certificate verification before use on untrusted networks. <br>
Risk: The server security verdict is suspicious, with no malware finding available from pending VirusTotal telemetry at review time. <br>
Mitigation: Review the source and current scan results before deployment, and run it only in environments that accept the documented network and credential handling risks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/xfyun-tts) <br>
- [iFlytek console](https://console.xfyun.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Files, Text] <br>
**Output Format:** [CLI output with generated audio files and a saved file path on stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports mp3, pcm, speex, and opus audio formats with voice, sample rate, speed, volume, pitch, and pronunciation options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
