## Description: <br>
Monitor and manage OpenClaw API errors, model performance, retry strategies, reports, and task recovery status through a Chinese natural-language interface for the Resilience plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leijack-lo](https://clawhub.ai/user/leijack-lo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to ask for API reliability statistics, inspect model-specific failure patterns, tune retry strategies, open a local monitoring dashboard, and generate recovery reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate local plugin that registers hooks, starts a local dashboard server, and writes persistent monitoring data. <br>
Mitigation: Review and install the Resilience plugin only if those local hooks, server behavior, and persistent data paths are acceptable for the deployment environment. <br>
Risk: Session recovery requires conversation access and can affect follow-up task behavior after failures. <br>
Mitigation: Enable conversation access only when automatic session recovery is desired, and review the recovery prompt settings before use. <br>
Risk: The skill provides interface text and examples; it does not include the core tool implementation. <br>
Mitigation: Install and verify the matching plugin before relying on dashboard, statistics, retry, or recovery commands. <br>


## Reference(s): <br>
- [ClawHub Resilience Monitor listing](https://clawhub.ai/leijack-lo/skills/resilience-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/leijack-lo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces natural-language tool guidance and dashboard/report instructions; core monitoring tools and hooks are supplied by the separate Resilience plugin.] <br>

## Skill Version(s): <br>
0.3.6 (source: server release evidence and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
