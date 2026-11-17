## Description:

YiDunAppDefense helps agents configure and run YiDun application protection for Android, iOS, and HarmonyOS app packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xautzbl](https://clawhub.ai/user/xautzbl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to configure YiDun AppKey credentials and protect Android APK/AAB, iOS IPA/xcarchive, and HarmonyOS HAP/APP packages through agent-guided commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow downloads and runs remote YiDun Java tooling that is not pinned by hash or signature verification.

Mitigation: Review the skill before installation, run it in a constrained environment, and pin or independently verify the downloaded vendor tool when possible.

Risk: Application packages and related metadata may be sent to YiDun during protection.

Mitigation: Use the skill only for applications approved for third-party processing and confirm that the YiDun service terms match the intended release workflow.

Risk: AppKey and optional signing credentials are stored in ~/.yidun-defense/config.ini and may be exposed through command history or CI logs.

Mitigation: Prefer hidden interactive AppKey entry, keep the config file restricted to the owner, avoid storing signing passwords unless necessary, and rotate any AppKey that may have been logged.

Risk: Local logs and temporary files can contain operational details about protected builds.

Mitigation: Review and clean local YiDun logs and temporary files before sharing build environments or diagnostic output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xautzbl/skills/yidun-app-defense)
- [YiDun official documentation](https://support.dun.163.com/)
- [YiDun application protection command documentation](https://support.dun.163.com/documents/15588074449563648?docId=989347548106215424)
- [YiDun console](https://dun.163.com/dashboard)
- [Platform support guide](docs/PLATFORM_SUPPORT.md)
- [Skill API documentation](docs/API.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown responses with shell commands, configuration snippets, status text, output paths, and troubleshooting guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked YiDun tooling may produce protected application package files and local logs outside the skill directory.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
