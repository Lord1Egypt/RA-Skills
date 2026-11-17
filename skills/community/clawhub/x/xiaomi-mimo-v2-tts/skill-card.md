## Description:

Xiaomi-MiMo-V2-TTS synthesizes Chinese and English speech with selectable voices, emotion styles, role-play, dialects, speed control, singing mode, and wav, mp3, pcm16, or opus output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[php737](https://clawhub.ai/user/php737)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content teams use this skill to synthesize short or batched Chinese and English speech clips for agents, messaging workflows, and other audio-generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text sent for synthesis is transferred to Xiaomi's external TTS service.

Mitigation: Do not synthesize secrets, confidential business text, personal data, or regulated content unless that transfer is approved.

Risk: The skill depends on local Python packages and ffmpeg behavior for some audio formats.

Mitigation: Use a virtual environment, avoid privileged package installs, and prefer pinned dependency versions where possible.

Risk: The CLI writes audio files to caller-specified output paths or directories.

Mitigation: Review output paths before execution and keep generated files in an approved workspace location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/php737/skills/xiaomi-mimo-v2-tts)
- [Xiaomi MiMo TTS API endpoint](https://api.xiaomimimo.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration]

**Output Format:** [Audio files in wav, mp3, pcm16, or opus format, with JSON status output from the CLI script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MIMO_API_KEY; opus conversion depends on ffmpeg; batch mode writes numbered audio files to an output directory.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
