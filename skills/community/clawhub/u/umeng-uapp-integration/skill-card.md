## Description: <br>
帮助 Android 开发者集成友盟 U-APP 统计 SDK，包括依赖、权限、初始化代码、混淆规则和合规注意事项。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Squall0925](https://clawhub.ai/user/Squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add Umeng U-APP analytics to Android apps, including Gradle dependencies, manifest permissions, privacy-gated initialization, ProGuard rules, and tracking examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics SDK integration can introduce data collection before user consent or add permissions that are not needed for a specific app. <br>
Mitigation: Review generated manifest and initialization changes, keep full SDK initialization behind privacy consent, and omit optional permissions unless the app has a clear need and disclosure. <br>
Risk: Using the skill with real Umeng project identifiers or credentials can expose them to the local agent environment. <br>
Mitigation: Provide only the values needed for the current task, avoid sharing secrets when placeholders are sufficient, and review generated code before committing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Squall0925/umeng-uapp-integration) <br>
- [Umeng Android SDK integration documentation](https://developer.umeng.com/docs/119267/detail/118584) <br>
- [Umeng developer center](https://developer.umeng.com/) <br>
- [Umeng SDK download](https://devs.umeng.com/sdk) <br>
- [Umeng compliance configuration guide](https://developer.umeng.com/docs/119267/detail/182050) <br>
- [Umeng U-APP FAQ](https://developer.umeng.com/docs/119267/cate/119530) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Gradle, XML, Kotlin, Java, and ProGuard code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides project-file guidance for Android SDK integration; users should review generated changes before applying them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
