## Description:

Analyzes fixed-camera video and optional audio in dementia care settings for behavioral signs of confusion or disorientation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Care providers and family caregivers can submit footage from dementia care settings for analysis of behaviors associated with confusion or disorientation. The skill returns structured observations and orientation-support information for care follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious and reports unclear consent for processing identifiable care footage or audio.

Mitigation: Before submitting identifiable media, confirm consent and understand where it is processed and how long it is retained.

Risk: ClawScan reports unclear account, identity, and credential handling, including broad credential-bearing network requests.

Mitigation: Review the security findings and skill configuration before installation, and verify what identity details or credentials are sent.

Risk: The security analysis is partial because a referenced local path was missing.

Mitigation: Review the missing referenced material before deployment; the available scan does not establish that it is safe.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-dementia-confusion-orientation-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance, Markdown]

**Output Format:** [Structured analysis report; JSON or text, with Markdown tables for history results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Behavioral observations and orientation-support information; not a medical diagnosis.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
