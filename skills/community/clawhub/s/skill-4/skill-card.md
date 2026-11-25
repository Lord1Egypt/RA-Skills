## Description:

Lightweight website uptime monitor. Check if URLs are up, measure response times, detect content changes via hashing, and verify expected content. Zero dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudiodrusus](https://clawhub.ai/user/claudiodrusus)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check website availability, measure response time, verify expected content, and compare page-content hashes for change detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted URL fetching can be used to probe private/internal services from the user's environment.

Mitigation: Use only trusted, intended URLs and apply network egress controls that block localhost, private ranges, cloud metadata services, and sensitive internal web apps.

Risk: Fetching large or unexpected responses can create operational load if the script is adapted for production monitoring.

Mitigation: Add response-size limits and review timeout settings before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/claudiodrusus/skills/skill-4)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text status output or JSON array, with shell command usage examples in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses process exit code 1 when any checked site is down or fails expectations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
