## Description:

Provides a Chinese academic paper-reading workflow for user-supplied PDFs or screenshots, including full-text translation, structured explanation, figure interpretation, detailed Q&A, and optional standardized summaries for PPT preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaosu-yj](https://clawhub.ai/user/xiaosu-yj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and students use this skill to turn a supplied academic paper or paper screenshot into a Chinese full-text translation, figure-linked explanation, terminology clarification, detailed Q&A, and optional presentation-ready summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may process an entire supplied paper by default, including copyrighted, confidential, or otherwise restricted content.

Mitigation: Provide only documents the user is allowed to process, and explicitly request a limited section when full-paper processing is not appropriate.

Risk: Translations, figure explanations, or logic-chain summaries can misread evidence or overstate causal conclusions from the original paper.

Mitigation: Review important outputs against the source paper, preserve reported data and uncertainty, and avoid treating correlation or author interpretation as settled fact.

Risk: The skill is optimized for Chinese academic explanation, which may not match users who need another output language or a narrower scholarly task.

Mitigation: Specify the desired output language, section scope, and deliverable format before invoking the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaosu-yj/skills/xiaosu-paper-reader)
- [Quality checklist](references/checklist.md)
- [Academic paper reading guide](references/paper-guide.md)
- [Terminology glossary](references/terms.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured Chinese prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include full-paper translations, figure-by-figure explanations, terminology clarification, detailed Q&A, and optional standardized summaries for PPT preparation.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
