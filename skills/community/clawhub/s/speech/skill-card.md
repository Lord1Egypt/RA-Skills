## Description: <br>
Use when the user asks for text-to-speech narration or voiceover, accessibility reads, audio prompts, or batch speech generation via the OpenAI Audio API; run the bundled CLI (`scripts/text_to_speech.py`) with built-in voices and require `OPENAI_API_KEY` for live calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and content teams use this skill to generate single or batch text-to-speech clips for narration, product demos, IVR prompts, accessibility reads, and audio prompts using the OpenAI Audio API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech generation is sent to OpenAI. <br>
Mitigation: Avoid highly sensitive scripts unless that data flow is acceptable for the intended deployment. <br>
Risk: Live generation uses a local OpenAI API key and account quota. <br>
Mitigation: Require `OPENAI_API_KEY` to be set locally, never ask users to paste the key in chat, and use dry runs when checking command shape. <br>
Risk: Relaxing network approvals globally can increase exposure in untrusted repositories. <br>
Mitigation: Apply any network-approval relaxation only in trusted workspaces and prefer the current environment defaults when unsure. <br>
Risk: Generated voices may be mistaken for human speech. <br>
Mitigation: Provide a clear disclosure to end users that the voice is AI-generated. <br>


## Reference(s): <br>
- [CLI reference](references/cli.md) <br>
- [Audio Speech API quick reference](references/audio-api.md) <br>
- [Voice direction patterns](references/voice-directions.md) <br>
- [Instruction prompting best practices](references/prompting.md) <br>
- [Sample prompts](references/sample-prompts.md) <br>
- [Narration defaults](references/narration.md) <br>
- [Voiceover defaults](references/voiceover.md) <br>
- [IVR prompt defaults](references/ivr.md) <br>
- [Accessibility read defaults](references/accessibility.md) <br>
- [Codex network approvals and sandbox notes](references/codex-network.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce mp3, wav, opus, aac, flac, or pcm audio files through the bundled CLI.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
