## Description: <br>
Cleans Markdown or TXT content into TTS-ready text, with optional chapter splitting, configurable cleanup levels, quality checks, and cleanup reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[booynal](https://clawhub.ai/user/booynal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare Chinese-oriented Markdown or TXT source material for TTS reading while preserving meaning, removing reference noise, tuning punctuation, oralizing numbers, and optionally splitting chapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad or ambiguous input paths could cause the agent to process unintended Markdown or TXT files. <br>
Mitigation: Provide narrow input paths or globs and write cleaned output to a separate output directory. <br>
Risk: Cleanup choices may remove citations, URLs, references, language, or formatting that the user intended to preserve. <br>
Mitigation: Explicitly state preservation requirements before running cleanup, especially for citations, URLs, references, language, and formatting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/booynal/tts-cleanup-checklist) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown text with cleanup report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce per-file cleaned text and batch summary reports with quality-check results.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
