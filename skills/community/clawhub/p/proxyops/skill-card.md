## Description: <br>
ProxyOps is a local-first proxy inventory, routing planner, and health tracking skill for organizing proxy assets, tracking health and expiry, and selecting fit-for-purpose proxies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ProjectSnowWork](https://clawhub.ai/user/ProjectSnowWork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use ProxyOps to maintain a local proxy inventory, compare providers and regions, track status and expiry, and choose proxies that fit a task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proxy inventory details are stored locally and may include sensitive operational metadata. <br>
Mitigation: Keep proxy passwords, tokens, and account secrets out of labels and notes, and delete the local JSON files when the inventory is no longer needed. <br>


## Reference(s): <br>
- [Proxy Philosophy](references/philosophy.md) <br>
- [ClawHub ProxyOps listing](https://clawhub.ai/ProjectSnowWork/proxyops) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown with Python command examples and local JSON inventory updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores proxy inventory, sessions, and stats in local JSON files under ~/.openclaw/workspace/memory/proxy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
