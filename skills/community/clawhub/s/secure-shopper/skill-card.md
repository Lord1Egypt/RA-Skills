## Description:

Asynchronous shopping research and checkout using secure-autofill with results recorded to workspace artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moodykong](https://clawhub.ai/user/moodykong)

### License/Terms of Use:


## Use Case:

External users and shopping agents use this skill to research products across configured shopping sites, compare candidates, record results, and proceed to checkout only after explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can browse authenticated shopping sites and move into checkout flows.

Mitigation: Require explicit accept or deny decisions and a separate checkout confirmation before placing any order, and use secure-autofill rather than exposing secrets in chat.

Risk: The skill stores location context and shopping request details in persistent workspace artifact files.

Mitigation: Prefer a ZIP code over a full address and review generated shopping artifact files after use.

Risk: The status helper can rewrite caller-chosen JSON files outside the intended shopping artifact directory.

Mitigation: Fix the helper to restrict writes to the secure_shopping artifact directory or avoid the raw --file helper until it is constrained.

## Reference(s):

- [Secure Shopper ClawHub page](https://clawhub.ai/moodykong/skills/secure-shopper)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON workspace artifacts and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records shopping task state and candidates to persistent JSON artifacts; checkout remains gated by explicit user confirmation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
