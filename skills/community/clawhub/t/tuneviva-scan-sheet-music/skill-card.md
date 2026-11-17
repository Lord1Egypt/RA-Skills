## Description:

Guide a user through recognising printed sheet music from photos or a PDF in TuneViva, reviewing the notation and opening the result for practice. Use for browser-based sheet music recognition, not audio transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omercelik](https://clawhub.ai/user/omercelik)

### License/Terms of Use:

MIT-0

## Use Case:

People with printed sheet music can use this skill to guide recognition of a photo or PDF in TuneViva, check the resulting notation against the source, and open it for practice or download. It also explains how to open an existing MusicXML score without scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optical recognition can misread notes, rhythms, signatures, or staff grouping.

Mitigation: Compare the result with the original score, review flagged measures, and correct or reprocess only after improving the source image.

Risk: The practice result uses temporary browser-session storage and may not be available in another tab or on another device.

Mitigation: Keep the same tab and session while practising, and download MusicXML or PDF when a lasting copy is needed.

Risk: Microphone matching is experimental and device access depends on user permission and the recording environment.

Mitigation: Request device access from the user and describe microphone feedback as experimental rather than guaranteed.

## Reference(s):

- [TuneViva sheet music recognition](https://tuneviva.com/recognize)
- [TuneViva Learn and Open MusicXML](https://tuneviva.com/learn/)
- [ClawHub skill release](https://clawhub.ai/omercelik/skills/tuneviva-scan-sheet-music)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Plain text or Markdown browser workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of TuneViva and does not itself process or transcribe score files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
