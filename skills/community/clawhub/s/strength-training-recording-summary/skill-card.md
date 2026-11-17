## Description:

Create WorkoutSummary notes from strength-training recordings or transcripts, including total time, completed exercises, sets, reps, durations, and concise coach notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangxuyi](https://clawhub.ai/user/fangxuyi)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to turn local strength-training recordings or transcripts into compact WorkoutSummary notes for future reference. It is especially useful for timestamped or mixed Chinese/English trainer sessions where exercise names, durations, sets, reps, and coaching cues need to be summarized accurately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud transcription can send workout audio to the selected provider when Groq, OpenAI, or another compatible API is used.

Mitigation: Prefer an existing transcript or local Whisper for offline-only workflows, and use cloud transcription only when the user has configured and chosen that provider.

Risk: The exercise-matching helper can download and cache an external exercise dataset, and untrusted dataset URLs may broaden network exposure.

Mitigation: Use a local pinned dataset with --dataset when tight network controls are required, and avoid untrusted --dataset-url values.

Risk: Scanner evidence marked the release suspicious because of overbroad network and caching behavior in the exercise-matching helper.

Mitigation: Review the skill before installation in controlled environments and apply local-only or allowlisted-network execution policies where needed.

## Reference(s):

- [Skill page](https://clawhub.ai/fangxuyi/skills/strength-training-recording-summary)
- [Summary workflow](references/summary-workflow.md)
- [hasaneyldrm/exercises-dataset](https://github.com/hasaneyldrm/exercises-dataset)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text WorkoutSummary notes, with shell commands or setup guidance when transcription or helper tools are needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve the requested language, avoid invented workout details or medical conclusions, and save files only when the user asks or provides an output path.]

## Skill Version(s):

0.1.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
