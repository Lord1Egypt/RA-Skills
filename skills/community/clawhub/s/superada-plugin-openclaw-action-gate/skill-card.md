## Description: <br>
OpenClaw Action Gate is an OpenClaw runtime plugin that applies per-scope Action Gate policies to inbound and outbound Discord actions and records decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h-mascot](https://clawhub.ai/user/h-mascot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw developers and operators use this plugin to gate Discord ingress and egress by scope policy, reserve outbound actions, cancel disallowed sends, and write per-decision audit metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can send message content plus routing and session metadata to a configured external Action Gate service. <br>
Mitigation: Prefer embedded local mode unless you operate the service yourself; when serviceUrl is used, require a trusted HTTPS endpoint and account for data leaving the local runtime. <br>
Risk: The install flow described by the artifact builds from an unpinned source checkout. <br>
Mitigation: Pin the source revision or install from a reviewed artifact rather than cloning a moving branch for production use. <br>
Risk: Server security evidence marks the release suspicious pending review. <br>
Mitigation: Install only if you trust the publisher and control the configuration, and review the package before enabling it in production. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/h-mascot/superada-plugin-openclaw-action-gate) <br>
- [SuperAda Action Gate page](https://superada.ai/plugins/openclaw-action-gate/) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance, JSON, text] <br>
**Output Format:** [OpenClaw hook responses, configuration schema, decision metadata, and audit records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Disabled by default; can use embedded local mode or a configured remote Action Gate service.] <br>

## Skill Version(s): <br>
0.1.603 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
