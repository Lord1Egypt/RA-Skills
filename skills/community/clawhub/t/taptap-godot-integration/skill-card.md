## Description:

Integrate TapSDK v4 into Godot 4 Android games: login, anti-addiction, cloud save, leaderboard, friends. Invoke when adding TapTap features to a Godot Android project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reallycsc](https://clawhub.ai/user/reallycsc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add TapSDK v4 login, anti-addiction, cloud save, leaderboard, friends, and update integration patterns to Godot 4 Android games.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anti-addiction checks may fail open if sample control flow is copied without review.

Mitigation: Require fail-closed anti-addiction handling before game entry and test denial, timeout, and network-error paths.

Risk: Cloud-save snippets may upload sensitive or unnecessary game-state data.

Mitigation: Minimize saved fields, document what is synchronized, and validate serialization before enabling cloud save.

Risk: Avatar loading and update-launch behavior can expose users to unbounded remote content or external app/browser launches.

Mitigation: Validate avatar URL schemes and image sizes, and remove or gate external update launches behind explicit user action.

## Reference(s):

- [TapTap Developer Portal](https://developer.taptap.cn/)
- [TapTap](https://www.taptap.cn/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Gradle, INI, XML, Kotlin, and GDScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation snippets and integration guidance for adaptation before use.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
