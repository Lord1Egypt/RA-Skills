## Description:

Analyzes video of a pet water fountain to estimate drinking frequency, session duration, daily intake, and changes from historical baselines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet guardians use this skill to review water fountain videos, track each pet's drinking behavior, and spot changes against historical baselines. Results are estimates for health monitoring and do not provide a diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags possible credential exposure to arbitrary URLs and warns that the export-only option may still upload video for analysis.

Mitigation: Review the service destination before use, and send only video and account information you are comfortable sharing with a remote service. Do not treat export-only mode as a guarantee that video stays local.

Risk: The security review was partial because a local reference could not be resolved.

Mitigation: Review the unresolved reference and service settings before sending private video or account information.

## Reference(s):

- [API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-pet-water-fountain-intake-analysis)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured drinking-behavior report with estimates, baseline comparisons, alerts, and report links; JSON or Markdown depending on the requested detail level.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes estimated drinking frequency, session duration, and daily intake; estimates are based on video and are not direct measurements. No diagnosis or treatment advice.]

## Skill Version(s):

1.0.17 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
