## Description:

Relive helps an agent create and operate an AI digital persona from chat logs, images, and optional audio or video materials to mimic a person's personality, voice, and appearance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joonaskahnwald](https://clawhub.ai/user/joonaskahnwald)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Relive to initialize a character workspace, import chat logs, build a persona profile, retrieve conversation context, and produce text, voice, or video persona replies. It should be used only with explicit rights and consent for the person's chats, voice, and likeness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes highly sensitive identity data, including private chats, voice samples, and likeness references.

Mitigation: Use it only with explicit rights and consent for the person's chats, voice, and likeness, and avoid deceptive, forged, or impersonation use.

Risk: The upload flow accepts a file path and may read unintended local files if pointed at the wrong location.

Mitigation: Run the skill in an isolated workspace and pass only the intended chat-log files to the upload command.

Risk: Uploaded chats, generated profiles, conversation history, indexes, and media outputs are persisted in plaintext storage directories.

Mitigation: Limit access to the workspace, remove stored character data when it is no longer needed, and avoid placing unrelated secrets or API keys in the runtime environment.

Risk: Voice and video modes can send prompts, images, or generated content to configured external model providers.

Mitigation: Review provider configuration before use, disclose external processing where required, and configure only the API keys needed for the selected output mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joonaskahnwald/skills/relive)
- [Relive README](artifact/README.md)
- [Relive skill instructions](artifact/SKILL.md)
- [CosyVoice repository](https://github.com/FunAudioLLM/CosyVoice.git)
- [Volc Engine inference endpoint documentation](https://www.volcengine.com/docs/82379/1099522)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, files]

**Output Format:** [JSON command files, Markdown profiles and chat exports, plain text replies, and optional WAV or MP4 artifact paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores character source data, generated profiles, runtime conversation logs, retrieval indexes, and generated media under per-character storage directories.]

## Skill Version(s):

0.1.0 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
