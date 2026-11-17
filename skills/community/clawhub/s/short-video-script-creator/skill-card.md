## Description:

Creates short-video scripts from structured product, audience, benchmark, competitor, and historical-script inputs, with PDF and Word document support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, creators, and agents use this skill to assemble structured prompts and optionally generate multiple short-video scripts from product strategy, audience background, and reference documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read user-supplied strategy, product, meeting, benchmark, competitor, and historical-script documents.

Mitigation: Use only documents approved for this workflow and avoid confidential customer, strategy, product, meeting, or competitor material unless the external processing and local logging behavior is acceptable.

Risk: When model invocation is enabled, prompt contents may be sent to a hard-coded third-party model endpoint.

Mitigation: Review and replace the model endpoint and credential handling with organization-managed settings before production use.

Risk: The artifact contains an embedded API key that should be treated as compromised.

Mitigation: Remove the embedded key, rotate any associated credential, and require user-managed credentials or environment-based configuration.

Risk: The script prints parsed replacement values and saves prompts and generated scripts under the skill output directory.

Mitigation: Review local output and logging behavior, restrict file-system access where possible, and clear generated artifacts that contain sensitive source material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahsbnb/skills/short-video-script-creator)
- [Publisher profile](https://clawhub.ai/user/ahsbnb)
- [Configured third-party model endpoint](https://api2.aigcbest.top/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save a generated prompt and, when model invocation is enabled, generated scripts to the skill output directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
