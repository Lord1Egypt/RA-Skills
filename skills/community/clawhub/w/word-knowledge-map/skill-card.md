## Description:

Generates Chinese-language, hand-drawn teaching-poster style English vocabulary knowledge maps from an input word using Knowledge IR, layout selection, image generation guidance, and content and visual QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuzongbao](https://clawhub.ai/user/xuzongbao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn English words or phrases into educational vocabulary maps for upper-primary and middle-school learners. It is aimed at producing concise Chinese-language learning posters with accurate word relationships, examples, and a hand-drawn classroom-poster visual style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The activation rule is broad and may trigger in casual prompts containing English words.

Mitigation: Use the skill when Chinese-language English vocabulary poster output is intended, and route unrelated English-word prompts outside this skill.

Risk: The skill is not language-configurable and is designed for Chinese-language learner-facing output.

Mitigation: Confirm the user wants Chinese-language explanations before using it in multilingual or non-Chinese workflows.

Risk: Generated vocabulary maps could mislead learners if the agent invents derivatives, usages, or word-family chains.

Mitigation: Follow the required Knowledge IR, content QA, and layout-mode constraints; leave weak word-family sections empty or use fallback layouts instead of fabricating relationships.

Risk: Visual outputs can drift into clean app-style or Soft UI layouts that do not match the intended teaching-poster style.

Mitigation: Run the visual QA checklist against the style guide and regenerate with the hand-drawn poster reference when the output fails the style lock.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuzongbao/skills/word-knowledge-map)
- [Server-resolved GitHub provenance](https://github.com/xuzongbao/word-knowledge-map/tree/main/skills/word-knowledge-map)
- [Style guide](artifact/templates/style-guide.md)
- [Layout modes](artifact/templates/layout-modes.md)
- [Knowledge schema](artifact/templates/knowledge-schema.json)
- [Infographic prompt template](artifact/templates/infographic-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown response with generated poster image and optional memory tip; internal Knowledge IR is structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for Chinese-language English vocabulary learning posters and should hide internal IR, schema, QA, and layout-mode terminology from end users.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
