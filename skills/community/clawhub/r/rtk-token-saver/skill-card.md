## Description: <br>
Use rtk to reduce token usage from common shell, git, search, file-reading, test, build, and lint commands while preserving raw-output fallbacks when exact output is required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to choose compact RTK command wrappers for noisy shell, repository, git, test, build, lint, package manager, log, Docker, Kubernetes, and AWS output. It also guides when to rerun native commands for exact output, complete logs, structured data, or sensitive material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RTK may hide details needed for correctness when exact bytes, complete logs, full JSON, or machine-readable output are required. <br>
Mitigation: Use native commands with the narrowest useful scope whenever exact or complete output is required. <br>
Risk: Command output can expose sensitive values, especially in logs or broad environment inspection. <br>
Mitigation: Avoid reading secrets and keep command scope targeted; use native raw commands only when the exact output is necessary. <br>
Risk: The skill depends on an RTK CLI available in the agent environment. <br>
Mitigation: Verify RTK with `which rtk`, `rtk --version`, and `rtk gain`; if unavailable, do not install it silently and fall back to native commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/clarezoe/rtk-token-saver) <br>
- [Publisher profile](https://clawhub.ai/user/clarezoe) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advises compact RTK command use when sufficient and native-command fallbacks when exact output is required.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
