## Description:

AI-powered Xiaohongshu (RED) note imitation writing that analyzes viral post structure, style, and traffic logic, then generates original, differentiated content matching a reference tone; it requires a wsdsocial.com API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wsd-mj](https://clawhub.ai/user/wsd-mj)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and marketers use this skill to turn a reference Xiaohongshu (RED) post, product information, and selling points into new RED-style note content with requested tone, length, and emoji preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the reference post, product information, selling points, and WSD API key to wsdsocial.com.

Mitigation: Use a dedicated rotatable API key, avoid submitting secrets or regulated personal data, and use the skill only after approving wsdsocial.com for the submitted data types.

Risk: Generated imitation writing may be too close to the reference post or unsuitable for a brand's content standards.

Mitigation: Review generated notes before publication and revise for originality, accuracy, brand fit, and platform compliance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wsd-mj/skills/red-note-imitation-writing)
- [Server-resolved GitHub provenance](https://github.com/WSD-MJ/red-note-imitation-writing)
- [WSD API key setup](https://ai.wsdsocial.com/skills)
- [WSD skill API endpoint](https://ai.wsdsocial.com/api/pub/skills/red-note-imitation-writing/_tool_89)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text note content with Markdown setup guidance and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WSD_API_KEY and sends the reference post, request, product information, and selling points to wsdsocial.com.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
