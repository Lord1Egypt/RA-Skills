## Description: <br>
Guides Expo and React Native application provisioning and scaffolding using MVC-Lite separation, RTL-first styling, typed state access, API client setup, and observability patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yahongie2014](https://clawhub.ai/user/yahongie2014) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and mobile engineers use this skill to create or extend Expo and React Native apps with consistent screen, component, navigation, API, localization, logging, and verification patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scaffolding may include bearer-token API clients, local token storage, Firebase, Sentry, and request logging patterns that can expose sensitive data if accepted without review. <br>
Mitigation: Review generated code before use, keep real secrets out of committed .env files, use secure token storage, and verify logger and Sentry sanitization before deployment. <br>
Risk: Installation and setup guidance may add or update npm or bun dependencies in a mobile project. <br>
Mitigation: Verify package names, versions, lockfile changes, and dependency trust before running install commands or committing generated changes. <br>


## Reference(s): <br>
- [React Native Clean Pattern ClawHub listing](https://clawhub.ai/yahongie2014/react-native-clean-pattern) <br>
- [Coder 79 ClawHub profile](https://clawhub.ai/user/yahongie2014) <br>
- [Coder 79 website](https://coder79.me) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing implementation guidance and scaffolding patterns; generated app code should be reviewed before execution or deployment.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
