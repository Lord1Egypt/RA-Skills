## Description:

High-quality voice synthesis with 9 personas, 11 languages, and streaming using Voice.ai API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gizmogremlin](https://clawhub.ai/user/gizmogremlin)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to generate Voice.ai text-to-speech audio from text, choose curated voice personas and languages, and stream or save output files through the bundled Node.js CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech generation and the VOICE_AI_API_KEY are sent to Voice.ai.

Mitigation: Avoid sensitive text unless Voice.ai handling policies have been reviewed, and provide the API key through a managed environment variable.

Risk: Generated audio can overwrite existing local files at the selected output path.

Mitigation: Use explicit, dedicated output paths and confirm the target before running generation commands.

Risk: The bundled SDK and API specification include account-level voice update and delete operations beyond basic text-to-speech generation.

Mitigation: Expose voice update or delete actions to an agent only with explicit user approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gizmogremlin/skills/voice-ai-voices)
- [Voice.ai API Documentation](https://voice.ai/docs)
- [Voice.ai Text-to-Speech API Reference](https://voice.ai/docs/api-reference/text-to-speech/generate-speech)
- [Voice.ai Voice Library](https://voice.ai/voices)
- [Voice.ai Dashboard](https://voice.ai/dashboard)
- [Bundled API Specification](artifact/voice-ai-tts.yaml)
- [Security Notes](artifact/SECURITY.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Node.js CLI commands and generated audio files when commands run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and VOICE_AI_API_KEY; generated speech is written to the configured output path.]

## Skill Version(s):

1.1.5 (source: frontmatter, CHANGELOG.md, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
