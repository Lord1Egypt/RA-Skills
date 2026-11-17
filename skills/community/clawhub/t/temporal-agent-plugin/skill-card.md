## Description:

Provides temporal awareness for AI agents, including timing prediction, progress monitoring, and social timing understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmzuo1976](https://clawhub.ai/user/xmzuo1976)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add temporal awareness to AI agents, including duration prediction, progress estimation, delay/anomaly detection, conversation timing, and multi-agent clock synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an undeclared archive-decoding utility that can extract ZIP contents to disk unsafely.

Mitigation: Remove or sandbox artifact/process_base64_zip.py before use, and do not run it on untrusted archives.

Risk: Dependencies are listed without pinned versions, which can make installation less reproducible.

Mitigation: Pin and review dependency versions before deploying the skill in a production or shared agent environment.

Risk: The security verdict is suspicious and the skill has not been cleared as low-risk by the available evidence.

Mitigation: Review and scan the skill before installation, then deploy it in a least-privilege environment appropriate for agent code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xmzuo1976/skills/temporal-agent-plugin)
- [Community feedback post 10347](https://clawd.org.cn/forum/post?id=10347)
- [Community feedback post 10455](https://clawd.org.cn/forum/post.html?id=10455)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated time-context strings, predicted durations, progress estimates, anomaly flags, and REST API responses when used through the provided code.]

## Skill Version(s):

2.1.0 (source: server release metadata and release notes, released 2026-04-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
