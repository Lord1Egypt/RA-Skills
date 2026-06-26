## Description: <br>
Modifies the User-Agent string in TongDaXin's TcefWnd.dll browser component, with install discovery, dry-run preview, backup creation, and custom UA support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[libertyzero10](https://clawhub.ai/user/libertyzero10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect TongDaXin installations and prepare commands that patch the embedded browser DLL's User-Agent string. It is intended for owned installations where the user understands the operational and authorization risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill patches a trading application's browser DLL and can cause application instability or an unusable component if applied to the wrong file. <br>
Mitigation: Use dry-run first, verify the exact DLL path, close TongDaXin before patching, and keep an independent backup in addition to the generated backup. <br>
Risk: Changing the User-Agent can be used to impersonate a mobile browser or bypass website restrictions. <br>
Mitigation: Use only on owned installations and do not use the patched browser to bypass access controls or website restrictions without authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/libertyzero10/tdx-ua-patcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline PowerShell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead to filesystem changes when the user executes the generated patching commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
