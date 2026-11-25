## Description:

Analyzes a pet facial image or video, matches the animal to its vaccination record, and returns a due or overdue reminder based on the configured cycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet hospital, boarding, and insurance staff can use it to check whether a matched pet's recorded vaccinations are due. It reports database comparisons and does not provide veterinary advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates this release suspicious with high confidence because credential handling, remote processing, and file or account changes exceed the stated reminder purpose; the scan was partial and the evidence is incomplete.

Mitigation: Avoid installing until credential routing, account and file changes, media transfer, and report export behavior are clarified.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured reminder results in text or JSON; historical report lists can include Markdown tables and report links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single pet media analysis or a historical report list; detail can be basic, standard, or JSON.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
