## Description: <br>
Generate retro robotic speech audio using SAM (Software Automatic Mouth), the classic C64 text-to-speech synthesizer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fourthdensity](https://clawhub.ai/user/fourthdensity) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to generate one-time SAM voice messages or toggle an agent mode that speaks responses as local WAV audio. It also provides voice parameter controls for pitch, speed, mouth, throat, and phonetic input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill adds the sam-js npm dependency before audio generation can run. <br>
Mitigation: Install it only in environments where that dependency is acceptable and keep dependency review aligned with local policy. <br>
Risk: Generated WAV files are written to local paths chosen by the agent or user. <br>
Mitigation: Use temporary or intended output directories and avoid writing audio files into sensitive or shared locations. <br>
Risk: SAM mode can persist in memory/sam-mode.json and cause later responses to be spoken as audio. <br>
Mitigation: Use /sam off or reset memory/sam-mode.json when speech output is no longer desired. <br>


## Reference(s): <br>
- [ClawHub SAM TTS skill page](https://clawhub.ai/fourthdensity/sam-tts) <br>
- [fourthdensity publisher profile](https://clawhub.ai/user/fourthdensity) <br>
- [SAM JavaScript package artifact](https://registry.npmjs.org/sam-js/-/sam-js-0.3.1.tgz) <br>
- [SAM project homepage](https://github.com/discordier/sam) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Local WAV audio files with optional JSON metadata and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the sam-js dependency; generated audio is WAV, mono, 22050 Hz, 8-bit PCM.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
