## Description:

Rewrites Chinese AI-generated text into a more natural human voice for novels, articles, copywriting, and other drafts, with flash, pro, and pro_plus processing tiers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abcqq1234567](https://clawhub.ai/user/abcqq1234567)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writers use this skill to send Chinese drafts of at least 300 characters to a cloud text-polishing service and receive rewritten text with a less AI-like style. It supports light, medium, and heavy processing modes selected by user intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft text is sent to the documented cloud API for processing.

Mitigation: Do not submit sensitive, personal, confidential, or proprietary drafts unless the user accepts that transfer.

Risk: A bound personal API key is stored locally in plaintext.

Mitigation: Use the built-in shared key for casual use, save a personal key only after explicit confirmation, and clear it when no longer needed.

Risk: The rewritten output may alter nuance, tone, punctuation, or meaning.

Mitigation: Review the returned text before publishing, especially for factual, legal, commercial, or sensitive writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abcqq1234567/skills/runse-skill)
- [Documented cloud processing API endpoint](https://1257707270-955niawhww.ap-shanghai.tencentscf.com/bailian/chat)
- [Documented cloud model list endpoint](https://1257707270-955niawhww.ap-shanghai.tencentscf.com/v1/models)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON from the helper script and user-facing rewritten Chinese text or status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires input text of at least 300 characters; longer drafts may need segmented processing.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter says 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
