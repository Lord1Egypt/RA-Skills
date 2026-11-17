## Description:

Windows UI Controller helps agents use pywinauto to scan, click, type in, and verify actions in Windows applications such as WeChat, QQ, NetEase Cloud Music, and Baidu Netdisk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alimjan8800](https://clawhub.ai/user/alimjan8800)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to learn and generate Windows desktop automation flows with pywinauto, including window discovery, control scanning, clicks, text input, waits, and post-action verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables real Windows desktop automation, including messaging and cloud-storage apps.

Mitigation: Use it only under intentional user direction, verify the target window and control before clicks or typing, and confirm results after each action.

Risk: Broad desktop control can affect sensitive applications if the agent targets the wrong window.

Mitigation: Avoid sensitive apps unless explicitly directed, run under a standard user account, and require explicit confirmation for sensitive actions.

Risk: The workflow depends on pywinauto and related Windows automation packages.

Mitigation: Pin or review the pywinauto dependency before installation and install only in an environment where Windows UI automation is intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alimjan8800/skills/windows-ui-controller)
- [Publisher Profile](https://clawhub.ai/user/alimjan8800)
- [pywinauto Documentation](https://pywinauto.readthedocs.io/)
- [pywinauto GitHub Repository](https://github.com/pywinauto/pywinauto)
- [pywinauto Releases](https://github.com/pywinauto/pywinauto/releases)
- [pywinauto PyPI Files](https://pypi.org/project/pywinauto/#files)
- [Microsoft UI Automation Overview](https://docs.microsoft.com/windows/win32/winauto/uiautooverview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only guidance for pywinauto-based UI automation; examples emphasize scanning and verifying each step.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
