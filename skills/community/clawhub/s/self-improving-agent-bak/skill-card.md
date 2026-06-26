## Description: <br>
Captures learnings, errors, and corrections for continuous improvement and reminds agents to review prior learnings before major tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robertstarry-gif](https://clawhub.ai/user/robertstarry-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to capture useful corrections, command failures, feature requests, and project-specific lessons in persistent learning logs. It can also scaffold new reusable skills from recurring, resolved lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can store inaccurate guidance or sensitive information that later influences agent behavior. <br>
Mitigation: Require manual review before writing to .learnings, and do not store secrets, credentials, customer data, or sensitive internal details. <br>
Risk: Global or broad hooks can repeatedly inject reminders and shape future agent sessions more widely than intended. <br>
Mitigation: Prefer project-scoped hooks, narrow matchers, and review hook scripts before enabling them. <br>
Risk: Promoting learnings into future instruction files can preserve unverified or outdated behavior. <br>
Mitigation: Promote only reviewed, broadly applicable lessons and keep pending or uncertain entries out of agent instruction files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robertstarry-gif/self-improving-agent-bak) <br>
- [Hook setup guide](references/hooks-setup.md) <br>
- [OpenClaw integration](references/openclaw-integration.md) <br>
- [Entry examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, hook configuration snippets, and generated skill scaffolds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local learning logs and skill scaffold files when its scripts are enabled by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
