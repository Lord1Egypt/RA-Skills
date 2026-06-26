## Description: <br>
Windows UI Controller is a Windows-only skill that guides agents in using pywinauto to inspect application controls, click buttons, type text, and verify UI operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alimjan8800](https://clawhub.ai/user/alimjan8800) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automate Windows desktop applications with pywinauto, especially for UI inspection, repeated clicks, text entry, and workflow testing. It is intended for Windows 10/11 environments with Python available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad live Windows application clicking and typing, including messaging apps. <br>
Mitigation: Use it first in test applications or test accounts and require explicit confirmation before any click, type, send, delete, purchase, or administrator-elevated action. <br>
Risk: Desktop automation could expose sensitive workflows or private data if pointed at finance, administrator, password-manager, or private-chat contexts. <br>
Mitigation: Avoid using the skill in sensitive applications and limit automation to intended, low-risk windows. <br>
Risk: Installing desktop automation dependencies from untrusted sources can introduce supply-chain risk. <br>
Mitigation: Prefer official PyPI or GitHub package sources for pywinauto and related dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alimjan8800/windows-ui-controller) <br>
- [pywinauto documentation](https://pywinauto.readthedocs.io/) <br>
- [pywinauto GitHub repository](https://github.com/pywinauto/pywinauto) <br>
- [pywinauto PyPI package files](https://pypi.org/project/pywinauto/#files) <br>
- [Microsoft UI Automation overview](https://docs.microsoft.com/windows/win32/winauto/uiautooverview) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only; requires Python and pywinauto.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
