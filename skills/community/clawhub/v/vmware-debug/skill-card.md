## Description: <br>
Vmware Debug helps agents troubleshoot VMware/vSphere incidents by correlating collected events, ranking root-cause hypotheses, and recommending next checks without making changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to investigate VMware/vSphere errors, alarms, log dumps, slow or failed VMs, and disconnected hosts. It supports diagnosis and handoff planning while leaving remediation to separate approval-gated tools or skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the third-party vmware-debug package installed with uv or uvx. <br>
Mitigation: Review and pin a trusted package or source before installation, and run it in a controlled local environment. <br>
Risk: Troubleshooting logs and event bundles can contain secrets or sensitive infrastructure details. <br>
Mitigation: Sanitize inputs and avoid feeding sensitive bundles to the package unless the local environment and package source are trusted. <br>
Risk: Diagnostic hypotheses and next-check recommendations may be incomplete or incorrect. <br>
Mitigation: Review the evidence before acting and route remediation through separate approval-gated tools or skills. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zw008/skills/vmware-debug) <br>
- [Capabilities](references/capabilities.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Unified Event Envelope](references/event-envelope.md) <br>
- [Symptom Routing](references/routing.md) <br>
- [Setup Guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostic recommendations; MCP or CLI output may include JSON timelines, ranked hypotheses, and next checks.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
