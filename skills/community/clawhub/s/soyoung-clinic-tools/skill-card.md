## Description: <br>
Soyoung clinic tools help an OpenClaw agent handle appointment booking, store lookup, doctor information, doctor schedules, project knowledge, and pricing for the Soyoung clinic chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[east5ringroad-kyle](https://clawhub.ai/user/east5ringroad-kyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and clinic workflow agents use this skill to query Soyoung clinic stores, doctors, schedules, project information, and prices, and to manage appointment workflows. It is intended for OpenClaw deployments that need to call Soyoung clinic APIs while preserving owner-only API key handling and group-chat appointment approval rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles credentials and real appointment actions. <br>
Mitigation: Install only when the agent is expected to manage Soyoung clinic data, keep the API key in direct owner chat, and review appointment actions before execution. <br>
Risk: Broad triggers may route unrelated appointment, doctor, or cosmetic-health questions to this skill. <br>
Mitigation: Review the bootstrap hook and routing rules before installation, and disable or narrow the hook when Soyoung clinic handling is not desired. <br>
Risk: The implementation can fall back to a default workspace API key when another workspace lacks one. <br>
Mitigation: Review workspace API key isolation before use and configure keys only in the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/east5ringroad-kyle/soyoung-clinic-tools) <br>
- [User guide](使用说明.md) <br>
- [API specification](references/api-spec.md) <br>
- [Changelog](CHANGELOG.md) <br>
- [Soyoung API key login](https://www.soyoung.com/loginOpenClaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-oriented text with JSON API request and response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, bash, workspace message context, and a Soyoung clinic API key for authenticated appointment and clinic-data actions.] <br>

## Skill Version(s): <br>
2.2.2 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
