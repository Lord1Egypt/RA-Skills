## Description:

Guides the design, deployment, validation, and troubleshooting of Volcengine TLS LogCollector ingestion on Linux hosts and Kubernetes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to plan, configure, and verify LogCollector collection from Linux hosts or Kubernetes into Volcengine TLS, including resource bindings, parsing, and ingestion checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials or Kubernetes access could expose or change production logging resources.

Mitigation: Use only authorized access; keep access keys out of chat, command history, and manifests, and confirm the target before making changes.

Risk: Host or Kubernetes installation could alter services, workloads, or cluster permissions.

Mitigation: Verify official installer URLs and versions, use vendor-supported checksum or signature checks where available, and review generated resources before installing.

Risk: A dry-run may not catch service-side rejection or incorrect log parsing.

Mitigation: Review every dry-run before a live write, validate parsing with representative samples, and check heartbeat, binding, and actual ingestion afterward.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/volc-sdk-team/skills/volcengine-tls-logcollector)
- [Volcengine CLI homepage](https://github.com/volcengine-tls/ve-tls-cli)
- [Volcengine LogCollector host installation guide](https://www.volcengine.com/docs/6470/72007)
- [Volcengine LogCollector DaemonSet guide](https://www.volcengine.com/docs/6470/109796)
- [Volcengine LogCollector CRD guide](https://www.volcengine.com/docs/6470/1158004)
- [Configuration validation](references/config-validation.md)
- [TLS resource configuration](references/tls-resources.md)
- [Collection verification](references/verification.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports selected targets, dry-run and live-write status, validation results, and ingestion checks.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
