## Description:

Reviews structured medical records and candidate diagnoses to report diagnosis-coding rule matches, supporting record evidence, and an audit conclusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare coding reviewers and developers use this skill to audit supplied diagnosis codes against medical-record evidence and diagnosis audit rules. Its output is coding-audit assistance and not medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical-record content and bearer credentials can be sent to an LLM endpoint.

Mitigation: Use only approved healthcare endpoints and keep LLM use disabled unless that endpoint and data flow are authorized.

Risk: Untrusted callers can select the LLM base URL.

Mitigation: Do not allow untrusted callers to set --base or payload.base; restrict execution to approved endpoint configuration.

Risk: Prepared record text can be persisted when requested.

Mitigation: Avoid --save-prepared for PHI and pass only authorized, de-identified patient data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-diagnosis-review)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object with final_decision and reasoning fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [final_decision is one of: 通过, 不通过, 待人工复核.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
