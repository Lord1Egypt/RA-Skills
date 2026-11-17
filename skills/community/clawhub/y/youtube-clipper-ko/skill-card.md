## Description:

YouTube Clipper KO helps agents turn Korean YouTube or local videos into short-form clips with Whisper transcripts, Claude Haiku segment selection, burned-in Korean subtitles, and JSON metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thedalbee](https://clawhub.ai/user/thedalbee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and content creators use this skill to prepare Korean short-form clips from long-form YouTube or local video sources. It supports human review by producing segment scores, hooks, reasons, weaknesses, transcripts, and clip metadata alongside the generated media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input media and transcript content are sent to OpenAI for transcription and Anthropic for transcript analysis.

Mitigation: Use the skill only with media approved for cloud processing, and avoid confidential, regulated, or third-party content without appropriate permission.

Risk: The install path relies on mutable dependencies and external command-line tools.

Mitigation: Run the skill in an isolated environment, pin dependency versions where possible, and review tool versions before processing production media.

Risk: Source media, extracted audio, transcripts, metadata, and generated clips may remain on disk after a run.

Mitigation: Choose an appropriate output location, restrict local access, and delete generated artifacts when they are no longer needed.

Risk: The current artifacts do not implement the advertised silence or breath removal behavior.

Mitigation: Review generated clips manually before publication and disclose or correct this limitation in release notes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thedalbee/skills/youtube-clipper-ko)
- [Clawitzer Integration Reference](https://github.com/thedalbee/clawitzer)

## Skill Output:

**Output Type(s):** [Files, JSON metadata, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated MP4 and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local output directories containing source media, transcripts, viral segment metadata, result metadata, and clips.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
