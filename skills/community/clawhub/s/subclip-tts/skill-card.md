## Description:

Generate persistent speech audio with Subclip AI using live model and voice discovery. Use for narration, voiceover, spoken dialogue, or revisiting generated speech in AI Generations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Creators use this skill in Subclip to choose or confirm a voice and generate persistent narration, voiceovers, or spoken dialogue using cloud or offline speech. Generated audio can be imported into the project for continued work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting offline and cloud speech guidance could send a script intended for offline use to a paid cloud service and incur credits.

Mitigation: Review the selected speech path before use; the security guidance says an offline fallback may send the script to a cloud service and incur credits.

Risk: The security scan was partial because several local path references could not be resolved, so not every referenced item was inspected.

Mitigation: Review unresolved local references before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prosamik/skills/subclip-tts)
- [Model selection and pricing](artifact/references/model-selection.md)

## Skill Output:

**Output Type(s):** [Audio, API Calls, Guidance]

**Output Format:** [Generated speech audio files and structured tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Speech can be generated offline or through cloud services. Persistent outputs can be imported into the project and managed using the operation ID.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
