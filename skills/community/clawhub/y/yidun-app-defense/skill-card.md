## Description: <br>
YiDunAppDefense helps agents configure and run YiDun app hardening for Android, iOS, and HarmonyOS packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xautzbl](https://clawhub.ai/user/xautzbl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to configure YiDun AppKey credentials and harden Android, iOS, and HarmonyOS mobile app packages through guided shell workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs an external YiDun hardening tool. <br>
Mitigation: Install only when you trust YiDun, verify the tool through a trusted vendor channel where possible, and pin or disable updates for reproducible release builds. <br>
Risk: The workflow handles sensitive app packages and YiDun AppKey or signing credentials. <br>
Mitigation: Use it only for packages you are authorized to submit, avoid sharing secrets in chat or shell history, and review permissions on ~/.yidun-defense/config.ini after configuration. <br>
Risk: Automated hardening can change release artifacts in ways that affect signing, size, installability, or store acceptance. <br>
Mitigation: Test protected artifacts before release and keep original packages, logs, and configuration for audit and rollback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xautzbl/yidun-app-defense) <br>
- [YiDun official documentation](https://support.dun.163.com/) <br>
- [YiDun console](https://dun.163.com/dashboard) <br>
- [Usage guide](docs/GUIDE.md) <br>
- [Platform support](docs/PLATFORM_SUPPORT.md) <br>
- [Command reference](docs/YIDUN_COMMAND.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated protected app package files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Java and curl; uses local configuration under ~/.yidun-defense and may produce logs under /tmp or ~/.yidun-defense/Log.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
