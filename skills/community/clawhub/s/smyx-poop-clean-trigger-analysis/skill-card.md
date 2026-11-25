## Description:

Analyzes video of a pet's designated toilet area for defecation events and emits a cleaning trigger after the pet leaves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners use the skill to review video from a designated pet toilet area, identify a possible defecation event, and receive a cleaning trigger after the pet leaves. The trigger is an event signal; connecting it to a robot vacuum requires a compatible home automation integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Camera footage may be processed externally and expose private household imagery.

Mitigation: Submit only footage you are authorized to share, limit it to the relevant area, and review the service's processing and retention terms before uploading.

Risk: A reported access-control flaw could expose reports across users.

Mitigation: Limit access to reports and avoid submitting sensitive footage until report access controls have been verified.

Risk: The security review flags account or credential handling beyond the stated purpose and unclear export-only behavior.

Mitigation: Review requested account permissions and credential handling, protect any keys, and confirm what an operation will export before running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-poop-clean-trigger-analysis)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [API reference](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured analysis results in JSON; history report listings in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include event status, timestamps, cleaning trigger signals, and report links when available.]

## Skill Version(s):

1.0.17 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
