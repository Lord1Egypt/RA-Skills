## Description:

Helps developers integrate the Umeng U-APP Analytics SDK into Android projects, including dependencies, permissions, initialization, privacy compliance, ProGuard rules, tracking examples, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Android developers use this skill to add Umeng U-APP analytics to an Android app and configure SDK dependencies, permissions, initialization after privacy consent, ProGuard rules, event tracking, and integration checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analytics SDK integration may collect device identifiers and optional location-related data.

Mitigation: Review requested permissions, dependency versions, privacy-policy text, and the consent-before-initialization flow before release.

Risk: Generated Android integration snippets may need adjustment for the target app's package name, build system, SDK versions, and release settings.

Mitigation: Verify generated changes against Umeng's official documentation, test initialization and event reporting, and disable debug mode before production release.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/squall0925/skills/umeng-uapp-integration)
- [Umeng Android SDK integration documentation](https://developer.umeng.com/docs/119267/detail/118584)
- [Umeng Developer Center](https://developer.umeng.com/)
- [Umeng SDK download](https://devs.umeng.com/sdk)
- [Umeng compliance configuration guide](https://developer.umeng.com/docs/119267/detail/182050)
- [Umeng U-APP FAQ](https://developer.umeng.com/docs/119267/cate/119530)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Gradle, XML, Kotlin or Java, and ProGuard code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Android file checks, integration steps, privacy-compliance notes, troubleshooting guidance, and official reference links.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
