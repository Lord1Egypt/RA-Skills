## Description: <br>
Automatically integrates the Umeng Android analytics SDK into an existing Android project, including environment checks, project validation, SDK setup, build verification, and logcat-based verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Umeng analytics to Android applications with guided appkey and channel configuration, Gradle dependency changes, Android manifest updates, ProGuard rules, Application initialization, and validation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Android project files, including Gradle, manifest, ProGuard, and Application configuration. <br>
Mitigation: Run it only on a copied or version-controlled project and review all generated changes before committing. <br>
Risk: The skill can run Gradle builds and use adb/logcat during validation. <br>
Mitigation: Use it only with Android projects and connected devices or emulators that you trust. <br>
Risk: The integration can add analytics collection, network permissions, and UMConfigure logging behavior. <br>
Mitigation: Confirm that the resulting analytics behavior, permissions, appkey, channel, and logging settings meet the app's privacy and compliance requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/squall0925/umeng-analytics-integration) <br>
- [Umeng Android analytics documentation](https://developer.umeng.com/docs/119267/detail/118578) <br>
- [Android developer documentation](https://developer.android.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and generated Android project changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create backups, modify Gradle, manifest, ProGuard, and Application files, run Gradle builds, and inspect adb/logcat output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
