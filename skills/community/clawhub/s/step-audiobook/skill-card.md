## Description:

Use when your agent needs to build, maintain, or run a local audiobook workflow for voice-library management, Step official voice sync, clone voice analysis, LLM casting, replayable TTS requests, segment synthesis, and final audiobook export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[praanmichael](https://clawhub.ai/user/praanmichael)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and audiobook producers use this skill to turn story text and voice-library inputs into structured scripts, casting plans, replayable TTS request manifests, synthesized segments, and final audiobook exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Story text, role and casting data, and selected voice audio may be sent to StepFun or to a user-configured compatible endpoint.

Mitigation: Use a limited STEP_API_KEY, review .env and base_url settings before running, and run first in an isolated workspace when validating the skill.

Risk: Paid voice cloning can incur billing when intentionally enabled.

Mitigation: Keep clone_selected_voices.py in dry-run until cloning is intended, and require explicit confirmation before running a real clone.

Risk: Force-style operations can overwrite generated segments or final audio outputs.

Mitigation: Review run paths and existing artifacts before using --force, and keep source text, structured scripts, and request manifests available for reruns.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/praanmichael/skills/step-audiobook)
- [Audiobook Workflows](references/workflows.en.md)
- [Audiobook Voice Library](references/voice-library.en.md)
- [Audiobook Script Format](references/script-format.en.md)
- [Audiobook Casting](references/casting.en.md)
- [Audiobook Synthesis](references/synthesis.en.md)
- [Audiobook Editing Guide](references/editing.en.md)
- [Security And External Access](references/security.en.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, YAML, Audio files]

**Output Format:** [Markdown guidance with shell commands, plus JSON/YAML workflow artifacts and final audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes intermediate artifacts under configured workspace paths; requires STEP_API_KEY, ffmpeg, and ffprobe.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
