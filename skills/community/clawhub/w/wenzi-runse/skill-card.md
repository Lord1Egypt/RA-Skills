## Description:

Rewrites user-provided text in a more natural voice across languages, with selectable polishing and formatting modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abcqq1234567](https://clawhub.ai/user/abcqq1234567)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users use this skill to polish or format text they provide, choosing a processing mode before the service handles the text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports no detected issues, but coverage is incomplete: one of three components was not analyzed and some referenced paths were missing.

Mitigation: Review the remaining files and referenced paths, and account for the limited scan coverage when deciding whether to install.

Risk: Text submitted for processing is sent to a cloud service.

Mitigation: Do not submit sensitive personal information.

Risk: A personal API key is stored in plaintext if the user chooses to save it locally.

Mitigation: Save a personal key only when that local storage is acceptable, and clear it when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abcqq1234567/skills/wenzi-runse)
- [Publisher profile](https://clawhub.ai/user/abcqq1234567)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Rewritten or formatted text in the input language, with a text menu for mode selection when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processing mode is selected by the user; output length and formatting follow the submitted text and selected mode.]

## Skill Version(s):

1.6.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
