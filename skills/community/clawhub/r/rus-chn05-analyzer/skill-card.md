## Description:

Analyzes left-wrist X-rays using the Chinese-05 RUS-CHN05 method to estimate bone age and optionally predict adult height.

This skill is ready for commercial/non-commercial use.

## Publisher:

[povoss](https://clawhub.ai/user/povoss)

### License/Terms of Use:

MIT-0

## Use Case:

An agent uses this skill to guide a bone-age assessment request, submit a wrist X-ray to the Huiling Cloud service, and present the returned estimates and report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious because it reports handling of children's medical and identifying information without a clear privacy and consent warning, along with behavior outside the stated bone-age purpose.

Mitigation: Before use, verify the recipient, purpose, retention, and guardian-consent process, and share only necessary data. Do not use the estimates as a basis for medical decisions; consult a qualified clinician.

Risk: Missing references prevented full analysis, so the scan does not establish that all referenced material or behavior is safe.

Mitigation: Review the referenced materials and verify the service behavior before installation and use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/povoss/skills/rus-chn05-analyzer)
- [API protocol](references/api-protocol.md)
- [Huiling Cloud API service](https://www.pipitu.net)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Chinese-language assessment report in text or Markdown, with structured result fields when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated bone age, scoring details, annotated-image links, and optional adult-height estimates; reports include an informational-use disclaimer.]

## Skill Version(s):

1.1.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
