## Description:

Converts story synopses or single-scene descriptions into scored, bilingual text-to-image prompts for storyboard and image generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ggke](https://clawhub.ai/user/ggke)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to turn story outlines or single-scene descriptions into coherent prompt sets with shot language, composition guidance, negative prompts, scoring, and bilingual output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically produces polished bilingual image prompts without a confirmation step, so style, language preference, or negative-prompt choices may not match the user's intent.

Mitigation: Review generated prompts before using them with an image model and adjust style, language, and negative-prompt terms as needed.

## Reference(s):

- [Story to Prompts Skill Page](https://clawhub.ai/ggke/skills/story-to-prompts)
- [Composition Patterns Reference](references/composition-patterns.md)
- [Shot Types Reference](references/shot-types.md)
- [Style Parameters Reference](references/style-params.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with bilingual prompt sections, negative prompts, and quality scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Multi-scene mode produces one section per image; single-scene mode produces one final prompt set.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
