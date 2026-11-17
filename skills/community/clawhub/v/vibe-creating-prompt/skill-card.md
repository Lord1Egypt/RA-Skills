## Description:

Judges whether a user's input suits the Vibe Creating style of video-prompt writing, and when it does, distills single-scene prompts, multi-shot descriptions, emotional imagery, or mixed input into prompts that are easier for a video model to generate from while preserving any user-specified dialogue, voiceover, music, sound effects, and other hard constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alisa0808](https://clawhub.ai/user/alisa0808)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent users use this skill to judge whether a rough video idea, story, feeling, or over-specified prompt should be rewritten in a more visual, emotionally coherent text-to-video style. It helps produce concise prompt text or a minimal clarifying question while preserving explicit sound, dialogue, structure, and other hard constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may demote or translate technical camera parameters when the user has not explicitly asked to keep them.

Mitigation: Ask the agent to preserve specific camera parameters, shot structure, or rhythm beats when those details are required.

Risk: Mixed-language prompts may be rewritten in an unintended output language.

Mitigation: State the desired output language before asking for the rewrite.

## Reference(s):

- [Server-resolved GitHub import source](https://github.com/Alisa0808/vibe-creating-skill/tree/main/skills/vibe-creating-prompt)
- [ClawHub skill page](https://clawhub.ai/alisa0808/skills/vibe-creating-prompt)
- [Atlas Cloud](https://www.atlascloud.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with concise sections for judgment, action, result, and optional notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces rewritten video prompts, pass-through decisions, limited cleanups, or clarifying questions; preserves explicit hard constraints and may demote undeclared low-value camera parameters.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
