## Description:

A headless creative production studio that helps AI agents generate images, edit photos, create video clips, produce audio, and assemble polished media output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohnen](https://clawhub.ai/user/cohnen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creative operators, and marketing teams use this skill to turn briefs into image, video, voiceover, music, sound effect, and Remotion-based production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local execution and file access while referenced scripts and templates are missing from the package.

Mitigation: Review the package before installation and use it only in a sandboxed project directory until the missing files are included and command permissions are narrowed.

Risk: Media generation commands may use provider API keys and local project files.

Mitigation: Use non-sensitive inputs and provider API keys you are comfortable using for media generation; avoid private repositories, credentials, and broad home-directory access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cohnen/skills/test-creative-studio)
- [Publisher Profile](https://clawhub.ai/user/cohnen)
- [Getshell Homepage](https://getshell.ai)
- [Freepik API Keys](https://www.freepik.com/api/keys)
- [fal.ai API Keys](https://fal.ai/dashboard/keys)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)
- [OpenRouter API Keys](https://openrouter.ai/keys)
- [ElevenLabs API Keys](https://elevenlabs.io/app/settings/api-keys)
- [OpenRouter Image Models](https://openrouter.ai/collections/image-models)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, JSON]

**Output Format:** [Markdown guidance with shell command examples, JSON command output, and generated media or project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may require provider API keys and local tools such as curl and jq.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
