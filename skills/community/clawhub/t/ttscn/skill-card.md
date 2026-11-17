## Description:

Multi-platform Chinese TTS text-to-speech via Edge/Doubao/CosyVoice/Azure/Tencent/Baidu/MiniMax/Xunfei - 8 backends, all work in China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agents use this skill to convert Chinese text into speech audio, compare supported TTS providers, choose voices, and configure provider credentials. It supports narration, voiceover, audiobook, podcast, and provider-selection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider endpoint settings can redirect API keys, source text, or voice samples to untrusted URLs.

Mitigation: Use only trusted HTTPS endpoints, and avoid setting MINIMAX_API_BASE or VOLCENGINE_TTS_ENDPOINT unless the exact endpoint has been reviewed.

Risk: Text and voice samples are sent to the selected TTS provider.

Mitigation: Use providers approved for the data being synthesized, and avoid sensitive text or voice samples unless the provider and account terms are acceptable.

Risk: Voice cloning can create unauthorized voice replicas.

Mitigation: Clone only the user's own voice or a voice they are authorized to use, and require explicit confirmation for paid MiniMax cloning.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/skills/ttscn)
- [Provider Comparison](docs/providers.md)
- [Provider Comparison Page](docs/providers.html)
- [Agent-Native Design](https://github.com/Agents365-ai/agent-native-design)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Files]

**Output Format:** [Markdown guidance with bash commands; the CLI can emit JSON envelopes and WAV or MP3 audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and ffmpeg; selected providers may require API credentials.]

## Skill Version(s):

1.3.2 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
