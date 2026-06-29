## Description: <br>
Push-to-talk voice input via Snarling hardware button and USB mic. Snarling records audio, plugin transcribes via OpenAI Whisper, then spawns a subagent that answers and sends the result to the Snarling display via send_notification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snarflakes](https://clawhub.ai/user/snarflakes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add push-to-talk voice input from Snarling hardware, transcribe recorded audio with OpenAI, and route the transcript into an agent turn that can reply on the display. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recorded audio is sent to OpenAI for transcription. <br>
Mitigation: Install only where users understand this data flow, configure an approved transcription endpoint, and avoid recording sensitive conversations. <br>
Risk: The transcription endpoint accepts a local WAV path that may be caller supplied. <br>
Mitigation: Restrict accepted audio paths to the expected recording directory before broad use. <br>
Risk: Speech is converted into an agent turn that can lead to tool use. <br>
Mitigation: Use a current patched OpenClaw runtime and consider confirmations or tighter tool limits for voice-originated actions. <br>
Risk: Debug or operational logs can expose sensitive transcript content if logging practices change. <br>
Mitigation: Keep debug logging opt-in, avoid logging raw transcripts in shared environments, and retain secret redaction for credentials. <br>


## Reference(s): <br>
- [OpenClaw Voice Bridge on ClawHub](https://clawhub.ai/snarflakes/skills/voice-bridge) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance] <br>
**Output Format:** [Text transcripts, JSON endpoint responses, and display notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Voice-triggered agent turns should keep display notifications brief.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
