## Description:

Reads up to ten visible videos from a user-selected YouTube playlist and turns their visible durations into a daily watch-plan draft with source links and explicit missing items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users can organize a course or series playlist into a read-only daily schedule based on their available minutes, while keeping restricted or incomplete entries marked for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer may resolve to a changing CLI version and may run with the user's account privileges.

Mitigation: Review the package and version before installation, use a trusted source, and run with only the privileges needed.

Risk: The security review had incomplete coverage of one script and binary assets.

Mitigation: Review the remaining script and binary assets before installing or relying on the skill.

## Reference(s):

- [Easy WebBridge](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR v1.7.8 release](https://github.com/xxjrq/easybr/releases/tag/v1.7.8)
- [OpenCLI YouTube adapter documentation](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/youtube.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown table with a daily viewing schedule, visible duration budget, source links, and unresolved items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers at most 10 visible videos; unknown durations are left pending and excluded from a complete budget.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
