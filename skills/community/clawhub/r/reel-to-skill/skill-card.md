## Description:

Download a TikTok, Instagram Reel, X video, or short-form video URL locally, extract/transcribe the audio, analyse the teaching or workflow inside it, and turn it into a concise OpenClaw skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olliewazza](https://clawhub.ai/user/olliewazza)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn short-form social videos into reusable procedural skills by downloading media, transcribing audio, and extracting repeatable workflow steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio may be uploaded to OpenAI when OPENAI_API_KEY is present.

Mitigation: Avoid sensitive or private audio unless external transcription is intended, and unset OPENAI_API_KEY for local-only operation.

Risk: The workflow downloads and stores social-video media locally.

Mitigation: Use only videos the user is allowed to download and transcribe, and choose a private per-run output directory.

Risk: The authoritative security verdict is suspicious because of broad, weakly scoped local and network handling.

Mitigation: Review the skill before installing or running it, and scan generated skill outputs before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/olliewazza/skills/reel-to-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local media, audio, transcript, and result JSON files during analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
