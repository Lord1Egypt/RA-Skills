## Description: <br>
Interpret VoiceTrust results for owner verification on voice/audio inputs, including trust labels, command-gating decisions, and minimal handling rules for voice messages alongside STT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kunyancai](https://clawhub.ai/user/kunyancai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use VoiceTrust to interpret local owner voice-verification results and decide whether voice-command execution should proceed. It supports STT-plus-voice-trust workflows by explaining trust labels, failure reasons, and command-gating outputs without replacing transcript handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Owner enrollment samples and derived voiceprints are sensitive local biometric data. <br>
Mitigation: Keep runtime/data/owners and runtime/data/voiceprints private, protect them with local filesystem permissions, and exclude them from publishing, sharing, and cloud backup sync. <br>
Risk: Setup may download model assets before local verification can run. <br>
Mitigation: Run the downloader only when you accept the documented mirror flow, and rely on the built-in SHA-256 verification before using downloaded assets. <br>
Risk: Voice verification can be inconclusive or degraded by short, noisy, silent, or low-speech audio. <br>
Mitigation: Use the skill's decision field and threshold guidance for command execution, keep STT handling separate, and treat degraded results as low trust or unavailable rather than proof of owner identity. <br>


## Reference(s): <br>
- [VoiceTrust ClawHub page](https://clawhub.ai/kunyancai/voicetrust) <br>
- [VoiceTrust Quickstart](references/quickstart.md) <br>
- [VoiceTrust Runtime README](runtime/README.md) <br>
- [SpeechBrain ECAPA VoxCeleb model](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON result interpretation and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interprets VoiceTrust result fields such as trust_label, decision, confidence, identity_score, speech_duration, vad_status, and decision_reasons.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
