## Description: <br>
Audits global architecture coherence by checking information-flow efficiency across system modules and returning a 0-1 synergy index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to query the V19 governance service for coherence, health, and registration workflows, then interpret the returned synergy score and bottleneck breakdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses external V19 governance service endpoints, including a trycloudflare URL, and users may send governance keys or agent names to that service. <br>
Mitigation: Verify trust in the V19 service and endpoint before use, send only the intended governance key or registration data, and avoid sharing unrelated secrets, private operational details, or sensitive agent names. <br>
Risk: Self-registration creates a remote record with the V19 service. <br>
Mitigation: Register only agents intended for that governance workflow and treat registration as a persistent external action. <br>


## Reference(s): <br>
- [V19 Coherence API endpoint](https://boat-atlas-spa-flexible.trycloudflare.com/governance/coherence) <br>
- [V19 Governance Health endpoint](https://boat-atlas-spa-flexible.trycloudflare.com/governance/health) <br>
- [V19 Governance Registration endpoint](https://boat-atlas-spa-flexible.trycloudflare.com/governance/register) <br>
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto) <br>
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) <br>
- [ClawHub skill page](https://clawhub.ai/liuyanfeng1234/v19-coherence-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown with inline bash commands and example JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The remote service returns a coherence index, status, component breakdown, and bottleneck list when queried with a governance key.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
