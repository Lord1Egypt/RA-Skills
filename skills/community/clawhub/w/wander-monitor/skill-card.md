## Description: <br>
Guides use of Wander to monitor GitHub Actions without polling after pushes, including CI notifications, workflow watching, smart-push, foreground/background/detached modes, wrappers, and edge cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ERerGB](https://clawhub.ai/user/ERerGB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to start and manage Wander-based GitHub Actions monitoring after pushes, receive completion notifications, and inspect failed workflow runs without manually refreshing GitHub Actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to start background local CI-monitor scripts after pushes, which can run repository-local wrappers or a local Wander checkout without a fresh confirmation step. <br>
Mitigation: Install only from a trusted Wander checkout, inspect repo-local watch wrappers before running them, and have the agent confirm the exact command before starting background monitoring. <br>
Risk: Monitoring the wrong workflow or branch can produce misleading CI status. <br>
Mitigation: Confirm the workflow file, branch filters, and any .workflows.yml registry entry before relying on reported status. <br>


## Reference(s): <br>
- [Wander README](https://github.com/ERerGB/wander) <br>
- [Wander EDGE_CASES.md](https://github.com/ERerGB/wander/blob/main/EDGE_CASES.md) <br>
- [Wander COFFEE_BREAK.md](https://github.com/ERerGB/wander/blob/main/COFFEE_BREAK.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that start Wander background monitors, configure workflow registries, or inspect GitHub Actions failures.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
