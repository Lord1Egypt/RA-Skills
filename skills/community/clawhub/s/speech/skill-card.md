## Description:

Use when the user asks for text-to-speech narration or voiceover, accessibility reads, audio prompts, or batch speech generation via the OpenAI Audio API; run the bundled CLI (`scripts/text_to_speech.py`) with built-in voices and require `OPENAI_API_KEY` for live calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and content teams use this skill to generate narration, voiceover, IVR prompts, accessibility reads, and batch speech audio from text with consistent voice, pacing, and output settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send provided text to the OpenAI Audio API during live speech generation.

Mitigation: Use it only with text approved for that API workflow, keep OPENAI_API_KEY local, and use dry-run mode when checking commands without a live call.

Risk: The security evidence flags guidance that may encourage disabling Codex approval controls.

Mitigation: Prefer approving the specific speech command instead of broadly disabling approval prompts or network safeguards.

Risk: The security evidence flags a batch output path weakness.

Mitigation: Treat batch JSONL as trusted input, avoid --force on untrusted batches, and review per-job output paths before running.

## Reference(s):

- [CLI Reference](references/cli.md)
- [Audio Speech API Quick Reference](references/audio-api.md)
- [Voice Directions](references/voice-directions.md)
- [Prompting Best Practices](references/prompting.md)
- [Sample Prompts](references/sample-prompts.md)
- [Narration / Explainer Defaults](references/narration.md)
- [Product Demo Voiceover Defaults](references/voiceover.md)
- [IVR / Phone Prompt Defaults](references/ivr.md)
- [Accessibility Read Defaults](references/accessibility.md)
- [Codex Network Approvals / Sandbox Notes](references/codex-network.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY and network access for live OpenAI Audio API calls; dry-run mode avoids live calls.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
