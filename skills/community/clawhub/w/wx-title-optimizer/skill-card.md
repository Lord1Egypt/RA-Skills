## Description:

Optimizes WeChat public-account article headlines from a topic, draft title, or article text by producing five scored title options with brief rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spiderzhcl](https://clawhub.ai/user/spiderzhcl)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and publishing teams use this skill to score a draft WeChat headline, identify its main issue, and compare five concise alternative titles. It is intended for headline ideation and selection, not for automated publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad headline and title-rewriting requests may activate the skill outside a WeChat public-account context.

Mitigation: Confirm that the user wants WeChat-style public-account headline optimization before applying the scoring rubric and output format.

Risk: Generated headline recommendations can still be misleading, overly promotional, or unsuitable for platform policy despite the skill's constraints.

Mitigation: Review the recommended titles for content accuracy, platform compliance, and sensitive wording before use.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/spiderzhcl/skill-wx-title-optimizer/tree/main/wx-title-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with headline scores, five title options, rationale, and first-choice and second-choice recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Titles are constrained to no more than 20 Chinese characters and should avoid clickbait, sensitive terms, and content mismatch.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
