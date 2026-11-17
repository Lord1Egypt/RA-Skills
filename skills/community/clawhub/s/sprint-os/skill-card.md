## Description:

Sprint OS is a 5-minute operating discipline for AI agents that runs ASSESS, PLAN, SCOPE, EXECUTE, MEASURE, ADAPT, LOG, and NEXT cycles with optional Convex-backed sprint tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[batsirai](https://clawhub.ai/user/batsirai)

### License/Terms of Use:


## Use Case:

External users, developers, and agent operators use Sprint OS to keep AI agents in short execution loops that produce shippable artifacts, measure progress, and record sprint history. It supports local Markdown sprint logs and optional Convex logging for persistent tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic sprint logging can capture sensitive project details in local logs or a remote sprint-tracking service.

Mitigation: Review log contents before enabling the workflow for sensitive projects and avoid recording secrets, private customer data, or confidential business details.

Risk: The optional Convex logging backend may allow unwanted reads or writes if deployed without authentication or access controls.

Mitigation: Enable Convex logging only after adding authentication, restricting backend access, and confirming who can read and write sprint records.

Risk: The optional Convex setup depends on external packages and deployment commands.

Mitigation: Pin and review the Convex dependency before running setup commands.

## Reference(s):

- [Sprint OS ClawHub listing](https://clawhub.ai/batsirai/skills/sprint-os)
- [README](artifact/README.md)
- [Convex Backend Setup](artifact/scripts/convex-setup.md)
- [Convex documentation](https://convex.dev)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces sprint-loop guidance, sprint-log entries, daily or weekly summaries, and optional Convex logging commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
