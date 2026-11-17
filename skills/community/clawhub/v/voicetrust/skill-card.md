## Description:

Interpret VoiceTrust results for owner verification on voice/audio inputs. Use when you need the meaning of VoiceTrust fields, trust labels, command-gating decisions, or the minimal rule for handling voice messages alongside STT. For first-time setup or environment bootstrap, read `references/quickstart.md`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kunyancai](https://clawhub.ai/user/kunyancai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use VoiceTrust to interpret local voice owner-verification results, combine them with STT output, and gate command execution based on trust labels and decision fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime stores local biometric voiceprint data for enrolled speakers.

Mitigation: Keep the runtime and owner profile directories private, use a simple fixed speaker ID such as `owner`, and do not publish enrollment data.

Risk: `allow_command` can be produced from voice similarity and should not be the only authorization signal for sensitive actions.

Mitigation: Require a separate confirmation factor before destructive, financial, administrative, or privacy-sensitive commands.

Risk: Downloaded model assets may be incomplete or altered.

Mitigation: Use the bundled model preparation flow and review SHA256 verification output before enrollment or verification.

Risk: Voice similarity checks can be affected by spoofing, short speech, low speech ratio, or unclear audio.

Mitigation: Treat low or rejected decisions as inconclusive for identity, ask for text confirmation or a longer clearer voice sample, and keep non-command content separate from command execution.

## Reference(s):

- [VoiceTrust Quickstart](references/quickstart.md)
- [VoiceTrust ClawHub Skill Page](https://clawhub.ai/kunyancai/skills/voicetrust)
- [SpeechBrain ECAPA VoxCeleb Model](https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, text]

**Output Format:** [Markdown guidance with shell command examples and JSON runtime result fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime JSON may include speaker_match, audio_quality, overall_trust, confidence, identity_score, trust_label, decision, decision_reasons, speaker_id, speech_duration, speech_ratio, vad_status, failure_reason, and raw_scores.speaker_similarity.]

## Skill Version(s):

0.4.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
