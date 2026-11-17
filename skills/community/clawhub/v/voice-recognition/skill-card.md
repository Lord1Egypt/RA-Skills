## Description:

Local speech-to-text with OpenAI Whisper CLI. Supports Chinese, English, 100+ languages with translation and summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gykdly](https://clawhub.ai/user/gykdly)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to run local Whisper speech-to-text on audio files, translate speech to English, and generate brief transcript summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext transcripts are saved beside the audio file, which can expose sensitive speech content on shared or synced folders.

Mitigation: Run the skill only on intended local audio files, review where transcript files are written, and move or delete plaintext transcripts according to data handling needs.

Risk: The quick alias persists a local script path in ~/.zshrc and may continue to invoke an unintended script if paths change.

Mitigation: Confirm the script path before adding the alias and remove or update the alias when the installation path changes.

Risk: The skill executes the local Whisper CLI and depends on local model downloads and supported audio formats.

Mitigation: Install Whisper from a trusted source, verify the command path before use, and test with non-sensitive audio before processing important recordings.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and plaintext transcript output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates plaintext .txt transcript files beside the input audio when Whisper runs; supported audio formats include MP3, M4A, WAV, OGG, FLAC, and WebM.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
