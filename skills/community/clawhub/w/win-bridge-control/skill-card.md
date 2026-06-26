## Description: <br>
Bridge: Cross-OS UI automation for Windows Host <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2059247714](https://clawhub.ai/user/2059247714) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators working in WSL2 use this skill to request supervised Windows host UI actions such as screenshots, button clicks, and cursor movement through the Windows shell and Node tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad Windows desktop control from WSL, which can affect visible applications or expose sensitive on-screen information. <br>
Mitigation: Use it only in supervised, low-risk sessions, close sensitive windows first, and require explicit confirmation before clicks or changes. <br>
Risk: The workflow depends on an external npm package invoked through npx. <br>
Mitigation: Verify the package source and version before use and avoid running it in sessions with sensitive applications open. <br>
Risk: Prompt text is incorporated into a shell command. <br>
Mitigation: Keep action prompts narrow and sanitize shell metacharacters before constructing commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/2059247714/win-bridge-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WSL2 access to Windows cmd.exe and Node/npx; desktop actions should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
