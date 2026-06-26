## Description: <br>
Use when the user wants to synthesise speech or text-to-speech (TTS) audio with Gemini through yummycli, including single-speaker narration, multi-speaker dialogue (up to 2 speakers), and listing available voices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yummysource](https://clawhub.ai/user/yummysource) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate Gemini text-to-speech WAV audio through yummycli, including narration, two-speaker dialogue, and voice discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external @yummysource/yummycli package. <br>
Mitigation: Confirm the package is trusted before installing or running commands. <br>
Risk: Speech synthesis requires a Gemini API key and sends submitted text to Gemini through the CLI. <br>
Mitigation: Use an appropriately scoped Gemini API key and avoid submitting text that should not be processed by the provider. <br>
Risk: Generated WAV files are written to the local filesystem. <br>
Mitigation: Review or specify output paths so generated audio is stored in an expected location. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is written locally as WAV files by yummycli; speak commands return JSON containing the output path.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
