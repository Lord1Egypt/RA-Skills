## Description: <br>
Convert text to speech using MiniMax Speech 2.6 Turbo via WaveSpeed AI with voice presets, emotion controls, language support, and configurable audio output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure WaveSpeed AI MiniMax Speech 2.6 Turbo text-to-speech requests, choose voices and audio settings, and handle generated audio URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text is processed by WaveSpeed AI as an external service. <br>
Mitigation: Do not submit secrets, credentials, regulated data, confidential scripts, or other sensitive text unless the applicable data-sharing policy permits it. <br>
Risk: The skill uses a WaveSpeed API key for billable requests. <br>
Mitigation: Store WAVESPEED_API_KEY in an environment variable or secret manager, avoid hardcoding it, and monitor usage according to account policy. <br>
Risk: JavaScript examples depend on the wavespeed client package. <br>
Mitigation: Verify the official wavespeed client package before running examples and validate request parameters against the documented options. <br>


## Reference(s): <br>
- [WaveSpeed AI API Keys](https://wavespeed.ai/accesskey) <br>
- [ClawHub Skill Page](https://clawhub.ai/chengzeyi/wavespeed-minimax-speech-26) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers text, voice, emotion, speed, pitch, audio format, sample rate, bitrate, channel, and language boost settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
