## Description:

Reviews structured medical record data and candidate surgery or procedure codes to return matched coding rules, record evidence, and an audit conclusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External users, medical coding reviewers, and healthcare workflow developers use this skill to audit surgery and procedure coding candidates against rule-library guidance and supporting medical-record evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical records and bearer credentials can be sent to configurable guideline and LLM endpoints.

Mitigation: Use only approved HTTPS endpoints, avoid caller-supplied base URLs, and use --no-llm when records cannot leave the host.

Risk: Inputs may contain real patient identifiers or other sensitive health information.

Mitigation: Redact names, identity numbers, phone numbers, detailed addresses, and other identifiers before invoking the skill.

Risk: The --save-prepared option can write plaintext prepared record text to local storage.

Mitigation: Do not enable --save-prepared unless local plaintext retention is explicitly approved and protected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-surgery-review)
- [Internal medical LLM endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [analysis, json, guidance]

**Output Format:** [JSON object with final_decision and reasoning fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision values are limited to pass, fail, or manual review; reasoning is concise and user-facing.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
