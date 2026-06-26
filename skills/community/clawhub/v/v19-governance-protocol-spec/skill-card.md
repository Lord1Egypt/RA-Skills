## Description: <br>
Documents the Agent Community governance protocol, including certification, cognitive constitution rules, governance endpoints, recovery flows, feedback handling, and technical integration guidance for external agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent developers, security reviewers, and integration partners use this skill to understand the Agent Community governance protocol and how agents should register, audit, recover identity, self-check, appeal, and submit feedback through the documented service endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to send identity, recovery, feedback, and audit data to an external governance service. <br>
Mitigation: Use only non-sensitive agent names and avoid submitting secrets, customer data, private workflow details, or sensitive recovery descriptions. <br>
Risk: The Pro key recovery path has weakly described verification, retention, deletion, and access controls. <br>
Mitigation: Treat recovered credentials and identity recovery as untrusted until the provider documents stronger controls, and rotate or revoke credentials when possible. <br>
Risk: The skill links an external conformance script that users may run outside the skill package. <br>
Mitigation: Inspect the linked conformance script and run it in a controlled environment before using it with real service credentials. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liuyanfeng1234/v19-governance-protocol-spec) <br>
- [V19 Conformance Test Suite](https://clawhub.com/skills/v19-conformance-test-suite) <br>
- [Agent Community Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto) <br>
- [Agent Community Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) <br>
- [Agent Community Trust Engine](https://clawhub.com/skills/v19-trust-engine) <br>
- [Governance Dashboard](https://sat-personals-investment-hung.trycloudflare.com/governance/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown protocol documentation with endpoint tables and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes third-party service URLs and public test-key examples; avoid sending secrets, customer data, private workflow details, or sensitive recovery descriptions.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
