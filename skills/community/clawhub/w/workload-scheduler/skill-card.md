## Description:

Selects appropriate workload templates from the pool based on available system capacity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to select workload templates that fit available CPU and memory capacity and produce a JSON scheduling plan for resource optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local capacity reports and workload templates may contain sensitive operational details.

Mitigation: Confirm that reading the capacity report and /etc/compute/templates JSON files is appropriate, and keep template contents limited to non-sensitive scheduling specifications.

Risk: Unreviewed or inaccurate workload templates can produce unsuitable scheduling recommendations.

Mitigation: Restrict template write access to trusted administrators and review generated schedules before using them to drive operational changes.

Risk: The source documentation is primarily in Chinese, which may reduce reviewer understanding for non-Chinese readers.

Mitigation: Provide translated documentation or require review by someone who can accurately read the source documentation before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Schedule output includes timestamp, capacity values, selected task metadata, total scheduled count, and completion status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
