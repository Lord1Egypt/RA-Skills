## Description:

Swarm Layer orchestrates spec-driven OpenClaw workflows with task planning, manual or ACP execution, session tracking, review gates, retries, autopilot controls, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xucheng](https://clawhub.ai/user/xucheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow operators use this skill to plan, run, review, and troubleshoot multi-step OpenClaw project workflows while keeping human review gates and reporting in the loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned external plugin installation paths may resolve to code outside the reviewed 0.5.12 release.

Mitigation: Pin installation to the reviewed 0.5.12 release or a specific audited commit, and verify provenance where possible before use.

Risk: Autopilot and watcher modes can continue dispatching workflow actions after they are started.

Mitigation: Start with status and dry-run commands, keep autopilot or watcher mode off until the workflow is understood, and review approvals instead of bulk-approving blindly.

Risk: ACP automation can run task workflows in the active project context.

Mitigation: Run the skill only in the intended project and fall back to manual execution when ACP readiness is blocked or unclear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xucheng/skills/swarm-layer)
- [OpenClaw Swarm Layer npm Package](https://www.npmjs.com/package/openclaw-swarm-layer)
- [OpenClaw Swarm Layer Documentation](https://github.com/xucheng/openclaw-swarm-layer/tree/main/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and operational status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local workflow reports such as status snapshots, run logs, review logs, spec archives, and completion summaries when the referenced plugin workflow is executed.]

## Skill Version(s):

0.5.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
