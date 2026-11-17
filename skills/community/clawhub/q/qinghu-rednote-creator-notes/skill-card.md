## Description:

Collects a RedNote creator's published notes from a profile link using Qinghu's data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and analysts use this skill to collect a RedNote creator's published notes and review comparable accounts. Queries require a Qinghu account and may consume paid credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests installation or upgrades of qhkit and may change local Node or PATH settings.

Mitigation: Review changes before installation; preinstall and pin qhkit where possible.

Risk: Using the service requires an API token tied to a paid Qinghu account.

Mitigation: Handle the token securely and approve account configuration before use.

Risk: Queries incur credits, and larger results can increase the final charge.

Mitigation: Check the estimate and scope of the request, then obtain approval before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-rednote-creator-notes)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [Concise Markdown summary with optional tabular data file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports query credit usage; large results may be delivered as a file.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
