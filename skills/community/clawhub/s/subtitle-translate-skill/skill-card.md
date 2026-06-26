## Description: <br>
Translate SRT subtitle files using LLM APIs with OpenAI-compatible format, supporting single-language and bilingual output while preserving timestamps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Thetail001](https://clawhub.ai/user/Thetail001) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, localization teams, and content operators use this skill to translate SRT subtitle files through an OpenAI-compatible LLM API while preserving subtitle timing. It can produce translated-only subtitles or bilingual subtitles with the translation above the original text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subtitle text is sent to the configured LLM API provider. <br>
Mitigation: Use trusted HTTPS API endpoints and do not process confidential subtitles unless the API service is controlled or trusted. <br>
Risk: API keys may be exposed through plaintext configuration files, command-line arguments, or untrusted proxy settings. <br>
Mitigation: Prefer environment variables or secure secret managers, avoid plaintext key files on shared systems, and use trusted network and proxy settings. <br>


## Reference(s): <br>
- [SRT Subtitle Format Specification](references/srt_format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated SRT subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-language or bilingual SRT output, configurable batch size, model selection, API endpoint, and progress logging.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
