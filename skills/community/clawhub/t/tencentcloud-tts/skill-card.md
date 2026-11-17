## Description:

TencentCloud TTS helps agents convert text into MP3 or WAV speech files using Tencent Cloud Text-to-Speech with configurable voice type, format, and output path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jizhouli](https://clawhub.ai/user/jizhouli)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to synthesize short text prompts into speech files through Tencent Cloud TTS, including basic setup, credential configuration, and example usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input text is sent to Tencent Cloud for speech synthesis.

Mitigation: Avoid submitting secrets, personal data, or regulated content unless Tencent Cloud processing is approved for the use case.

Risk: The output filename can overwrite local files if pointed at an existing path.

Mitigation: Restrict output filenames to a dedicated audio directory and check for existing files before writing.

Risk: Configuration helpers may print partial credential values in logs or shared terminals.

Mitigation: Use dedicated low-privilege Tencent Cloud credentials and avoid running configuration checks where logs are visible to others.

## Reference(s):

- [Tencent Cloud Text-to-Speech Documentation](https://cloud.tencent.com/document/product/1073)
- [Tencent Cloud TTS API Error Codes](https://cloud.tencent.com/document/api/1073/37996)
- [ClawHub Skill Page](https://clawhub.ai/jizhouli/skills/tencentcloud-tts)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; generated audio files are MP3 or WAV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill sends input text to Tencent Cloud TTS and writes synthesized audio to a user-specified local file path.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
