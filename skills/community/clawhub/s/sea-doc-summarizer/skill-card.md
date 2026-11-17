## Description:

Summarize documents in EN/CN/BM/ID with cross-language support. Optimized for Southeast Asian languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wms2537](https://clawhub.ai/user/wms2537)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to summarize English, Chinese, Bahasa Malaysia, and Bahasa Indonesia documents, optionally translating summaries across those languages. It also extracts named entities such as people, organizations, amounts, dates, deadlines, and locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs a real paid billing charge before use.

Mitigation: Confirm that users explicitly approve each charge and understand the $0.005 USDT per-call price before the billing endpoint is invoked.

Risk: A submitted user_id could bill the wrong account if identity binding is weak.

Mitigation: Validate that the requesting user is authorized to charge the submitted user_id before using the skill in an agent workflow.

Risk: Document text may contain sensitive or regulated information, and the evidence does not provide a privacy disclosure for external billing or processing.

Mitigation: Review the publisher's and billing provider's privacy handling before sending confidential documents or account identifiers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wms2537/skills/sea-doc-summarizer)
- [Skill billing endpoint](https://sea-doc-summarizer.swmengappdev.workers.dev/charge)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, shell commands]

**Output Format:** [JSON summary with key points, extracted entities, detected source language, and word-count metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs the agent to charge SkillPay before summarization and then produce summaries in brief, detailed, or action-item styles.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
