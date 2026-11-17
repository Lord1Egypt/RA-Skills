## Description:

Run a practical two-worker orchestration workflow with Xiaoma as the execution worker and Xiaoniu as the QA worker for medium or large tasks that benefit from execute-then-review delegation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyangwjy](https://clawhub.ai/user/wangyangwjy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to delegate substantial work to a local execution agent, route acceptance checks to a separate QA agent, and keep the main chat responsive while the workflow runs asynchronously.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can persistently broaden local agent access and session visibility beyond the two named workers.

Mitigation: Install in a local or isolated OpenClaw profile, review any cross-agent configuration changes before applying them, keep a recoverable backup, and tighten allow policies and session visibility after validation.

Risk: The bootstrap helper can mutate local OpenClaw configuration and restart the gateway when auto-fix mode is used.

Mitigation: Use auto-fix only when configuration mutation and restart side effects are acceptable, and follow the documented rollback path if the environment should return to its prior state.

Risk: Worker dispatch or QA routing may fail in environments where xiaoma, xiaoniu, or cross-agent routing are not ready.

Mitigation: Run the documented readiness checks and smoke tests before relying on the workflow, retry with smaller packets on dispatch failure, and fall back to main-session execution or acceptance when needed.

## Reference(s):

- [Workhorse Duo Skill Page](https://clawhub.ai/wangyangwjy/skills/workhorse-duo)
- [Session Setup and Operations](references/session-setup-and-operations.md)
- [Workhorse Duo Local Bootstrap](references/local-bootstrap.md)
- [Published Bootstrap Helper](references/published-bootstrap-helper.md)
- [Async Reporting Rule](references/async-reporting.md)
- [Review Routing Rules](references/review-routing-rules.md)
- [Risk and Rollback](references/risk-and-rollback.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and task packet templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces orchestration instructions, bootstrap checks, QA routing rules, and fallback guidance for local OpenClaw agent workflows.]

## Skill Version(s):

2.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
