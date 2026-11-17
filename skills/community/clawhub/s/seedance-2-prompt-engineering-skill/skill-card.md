## Description:

Generate precise, timecoded Seedance 2.0 prompts integrating multimodal inputs with asset mapping for controlled 4-15s video creation and editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dandysuper](https://clawhub.ai/user/dandysuper)

### License/Terms of Use:


## Use Case:

Developers, creators, and production teams use this skill to turn rough video concepts and reference assets into structured Seedance 2.0 prompts with mode selection, asset mapping, timeline beats, negative constraints, and generation settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may involve user-selected media references for use with an external video-generation platform.

Mitigation: Review platform terms and avoid using sensitive, private, or unauthorized media as references.

Risk: Prompts that imitate recognizable franchises, characters, brands, logos, or realistic face references may be rejected or create rights or privacy concerns.

Mitigation: Use original names and designs, strip brand identifiers, and include negative constraints for logos, trademarks, recognizable likenesses, and franchise terms.

Risk: Long or multimodal requests can exceed Seedance input limits or lose control when assets are not mapped clearly.

Mitigation: Respect documented file, duration, and size limits; declare mode first; map each @asset role; use timecoded beats and segment handoff notes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dandysuper/skills/seedance-2-prompt-engineering-skill)
- [Seedance 2.0 Prompt Recipes](artifact/references/recipes.md)
- [Modes and Interaction Notes](artifact/references/modes-and-recipes.md)
- [Camera Language & Visual Styles Vocabulary](artifact/references/camera-and-styles.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown prompt drafts with mode, asset mapping, final prompt, negative constraints, and generation settings; helper scripts emit shell output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timecoded video beats, @asset role mappings, IP-safety constraints, and workspace scaffold commands.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
