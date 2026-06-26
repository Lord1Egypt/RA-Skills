## Description: <br>
Sentry.io error monitoring via sentry-cli. Use when working with Sentry releases, source maps, dSYMs, events, or issue management. Covers authentication, release workflows, deploy tracking, and debug file uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iAhmadZain](https://clawhub.ai/user/iAhmadZain) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release engineers use this skill for Sentry CLI workflows, including authentication, release creation, deploy tracking, source map uploads, debug file uploads, event testing, issue management, and CI/CD integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sentry authentication tokens can be exposed through source control, local configuration, command history, or CI logs. <br>
Mitigation: Use least-privilege Sentry tokens, store them in secret managers or protected environment variables, and keep them out of committed files and shell history. <br>
Risk: Uploaded logs, source maps, dSYMs, ProGuard mappings, and related build artifacts may contain sensitive application or user data. <br>
Mitigation: Review and redact artifacts before upload, and limit uploads to the files required for the target Sentry project and release. <br>
Risk: The direct curl-to-bash installer path executes a remote script. <br>
Mitigation: Prefer trusted package managers where practical, or verify the source and contents before using direct installation. <br>


## Reference(s): <br>
- [Sentry CLI installer](https://sentry.io/get-cli/) <br>
- [ClawHub skill page](https://clawhub.ai/iAhmadZain/sentry-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, YAML, and INI snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command examples require user-supplied Sentry organization, project, release, environment, and token values.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
