## Description:

Text-to-Speech using SiliconFlow API (CosyVoice2). Supports multiple voices, languages, and dialects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creators use this skill to generate speech audio files from text through the SiliconFlow CosyVoice2 API, with selectable voices, speed, and output formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses broad local command execution to call curl and write output files.

Mitigation: Review the generated command and output path before running the skill, and execute it in a workspace where file writes are expected.

Risk: The SiliconFlow API key can be exposed through command-line process arguments during the curl call.

Mitigation: Use a limited SiliconFlow API key where possible and avoid running on shared systems where other users can inspect process arguments.

Risk: Input text is sent to the SiliconFlow API service.

Mitigation: Do not submit confidential or regulated text unless SiliconFlow data handling is acceptable for the intended use case.

Risk: Unpinned installation may pick up a different release than the reviewed artifact.

Mitigation: Prefer a version-pinned installer or otherwise verify the release hash before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilei0311/skills/siliconflow-tts-gen)
- [SiliconFlow API endpoint](https://api.siliconflow.cn/v1)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [Audio file in mp3, opus, wav, or pcm format with JSON status metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a SiliconFlow API key and sends input text to api.siliconflow.cn.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
