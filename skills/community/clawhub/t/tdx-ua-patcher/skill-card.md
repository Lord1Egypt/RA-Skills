## Description:

通达信 TcefWnd.dll User-Agent 修改工具，用于查找通达信安装目录、检测版本信息，并修改内置浏览器组件的 UA 标识。

This skill is ready for commercial/non-commercial use.

## Publisher:

[libertyzero10](https://clawhub.ai/user/libertyzero10)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced users who administer TongDaXin installations use this skill to inspect installed TcefWnd.dll components, preview User-Agent changes, and prepare patch commands for authorized local modifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing a trading application's DLL can break the application or leave it in an unsupported state.

Mitigation: Use dry-run first, confirm the exact TcefWnd.dll path, close TongDaXin before patching, and keep the generated backup available for restore.

Risk: Using a modified User-Agent to bypass access checks may violate website rules or organizational policy.

Mitigation: Use the skill only when authorized to modify the installation and when the target site's terms and applicable policies permit the access pattern.

Risk: The script writes binary data to a DLL and accepts a custom path.

Mitigation: Review the command before execution, restrict use to the intended TongDaXin browser component, and avoid running it with unnecessary elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/libertyzero10/skills/tdx-ua-patcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with PowerShell command examples and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can preview or apply changes; applying the script may modify TcefWnd.dll and create a .backup file on the user's machine.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
