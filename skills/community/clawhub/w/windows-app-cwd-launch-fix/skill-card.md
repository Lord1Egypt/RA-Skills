## Description:

Diagnose and fix Windows packaged apps that crash on launch because relative resource paths (res/xxx) resolve against the process working directory. Includes a four-step elimination method (line endings / start inheritance / file truly missing / CWD attribution), an A/B reproduction, and a self-checking hardened launcher template. Use for 'app crashes on double-click', 'PyInstaller exe crash', 'FileNotFoundError res path', 'CWD wrong', 'works in one folder but not another', '打包给客户跑不起来'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to diagnose Windows packaged applications that fail when their working directory differs from the application folder, and to create or verify a launcher that checks required files and sets the startup directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher wildcard loop may start every executable in the application folder with the user's permissions.

Mitigation: Replace the wildcard with the exact intended executable filename and verify that file exists before running the launcher.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/catsmansion/skills/windows-app-cwd-launch-fix)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with diagnostic tables and Windows batch code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a Windows .cmd launcher template and diagnostic steps.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
