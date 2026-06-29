## Description: <br>
Integrate TapSDK v4 into Godot 4 Android games: login, anti-addiction, cloud save, leaderboard, friends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reallycsc](https://clawhub.ai/user/reallycsc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External game developers and engineers use this skill to integrate TapSDK v4 features into Godot 4 Android games, including login, anti-addiction, cloud save, leaderboard, friends, and Godot-to-Android plugin bridging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Login, friend, profile, and cloud-save features may process player data that users expect to be disclosed. <br>
Mitigation: Add clear player-facing privacy notices and request only the friend or profile scopes the game actually needs. <br>
Risk: Cloud-save payloads can contain secrets or unnecessary personal data if the game serializes too much state. <br>
Mitigation: Minimize saved fields and avoid placing secrets or unnecessary personal data in save files before upload. <br>
Risk: Cloud restore behavior can replace newer or preferred local progress. <br>
Mitigation: Compare cloud and local saves and ask for confirmation before replacing local save data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/reallycsc/taptap-godot-integration) <br>
- [TapTap Developer Portal](https://developer.taptap.cn/) <br>
- [TapTap Website](https://www.taptap.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Kotlin, GDScript, Gradle, XML, and INI code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes integration steps, Android plugin code, Godot autoload code, configuration snippets, and module-specific implementation notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
