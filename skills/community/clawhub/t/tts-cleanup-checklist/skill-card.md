## Description:

Cleans Markdown and TXT files into TTS-ready text, with optional chapter splitting, configurable cleanup levels, quality checks, and cleanup reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[booynal](https://clawhub.ai/user/booynal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and agents use this skill to prepare long-form Markdown or TXT content for natural TTS reading without summarizing or changing the original meaning. It supports single-file cleanup, batch cleanup, optional chapter splitting, configurable text normalization, and cleanup quality reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default cleanup may remove citation markers, bare URLs, and reference sections from source-sensitive documents.

Mitigation: Ask the agent to preserve citations and links, or choose a less aggressive reference_trim setting before processing, then review the cleanup report.

Risk: Cleanup report labels may be generated in Chinese by default.

Mitigation: Set the desired output and report language before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/booynal/skills/tts-cleanup-checklist)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown text with cleanup notes and optional batch summary reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Configurable cleanup mode, citation and URL trimming level, punctuation tuning, number style, English alias handling, and long sentence threshold.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
