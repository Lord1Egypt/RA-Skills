## Description:

Translates SRT subtitle files with OpenAI-compatible LLM APIs while preserving timestamps and supporting single-language or bilingual output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thetail001](https://clawhub.ai/user/thetail001)

### License/Terms of Use:


## Use Case:

Developers and subtitle localization workflows use this skill to validate SRT files, list available OpenAI-compatible models, and translate subtitle text to another language while preserving timing. It can produce translated-only subtitles or bilingual subtitles with translated text above the original.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subtitle content is sent to the configured API provider.

Mitigation: Use the skill only with subtitle content you are allowed to transmit, and choose a trusted provider and endpoint for the data sensitivity involved.

Risk: Bearer API keys may be exposed through command-line history, plaintext configuration, logs, or untrusted proxy settings.

Mitigation: Prefer environment variables or a secret manager, use trusted HTTPS endpoints, avoid untrusted proxies, restrict key scope when possible, and rotate any key that may have been exposed.

## Reference(s):

- [SRT Subtitle Format Specification](references/srt_format.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; executed scripts produce SRT subtitle files and console status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Translation runs in configurable batches, defaults to 50 subtitle entries per batch, and can generate single-language or bilingual SRT output.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
