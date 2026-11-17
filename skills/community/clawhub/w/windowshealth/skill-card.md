## Description:

Windows-health helps agents diagnose Windows storage and performance issues, classify cleanup candidates, and produce evidence-based PowerShell reports with confirmation gates before deletion or migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiaoyifu1203](https://clawhub.ai/user/jiaoyifu1203)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to investigate Windows disk pressure, startup/performance issues, large-file candidates, duplicate candidates, and safe cleanup or archive plans. It is designed to produce readable diagnostics and candidate commands before any state-changing action is authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect local system metadata such as disk usage, running processes, startup entries, Recent Items, and large-file candidates.

Mitigation: Use it only where that local diagnostic scope is acceptable, and review report contents before sharing them outside the machine or organization.

Risk: Cleanup, archive, duplicate-removal, or startup-management actions can change system state if executed.

Mitigation: Require exact paths, action type, recovery notes, and explicit confirmation before any deletion, migration, symbolic link, cloud-local removal, or startup change.

Risk: The provided PowerShell scan invocation uses ExecutionPolicy Bypass.

Mitigation: In managed environments, prefer removing ExecutionPolicy Bypass and running scripts under the organization's normal PowerShell policy controls.

Risk: Administrator-level Windows cleanup paths such as WinSxS or DISM can have irreversible consequences.

Mitigation: Use Microsoft-guided analysis first, keep administrator-level actions separate from routine cleanup, and require separate confirmation for irreversible options.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiaoyifu1203/skills/windowshealth)
- [Microsoft authoritative baseline](references/microsoft-authoritative.md)
- [Safety and platform boundaries](references/safety-and-platforms.md)
- [PowerShell scan commands](references/scan-commands.md)
- [Report, execution, and rollback](references/report-and-execution.md)
- [cleanmgr command documentation](https://learn.microsoft.com/zh-cn/windows-server/administration/windows-commands/cleanmgr)
- [Storage Sense documentation](https://learn.microsoft.com/zh-cn/windows/configuration/storage/storage-sense)
- [Clean up the WinSxS folder](https://learn.microsoft.com/zh-cn/windows-hardware/manufacture/desktop/clean-up-the-winsxs-folder)
- [Clean boot support guidance](https://support.microsoft.com/help/929135)
- [Startup apps support guidance](https://support.microsoft.com/windows/9115d841-735e-488d-e749-9ba301d441e6)
- [Monitor Windows client performance](https://learn.microsoft.com/zh-cn/training/modules/monitor-troubleshoot-windows-client-performance/4-monitor-windows-client-performance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with PowerShell command blocks and action classifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-first diagnostics; state-changing actions require explicit per-path confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
