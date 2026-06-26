## Description: <br>
Helps audit transitive skill dependency chains in agent compositions, catching risks where a direct dependency appears safe but a deeper dependency introduces vulnerability into the full chain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill to audit full skill dependency graphs for transitive dependency risk, trust decay, version pinning gaps, graph anomalies, and undeclared capability propagation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use network lookups and process provided skill identifiers or installed skill lists. <br>
Mitigation: Use it as an advisory audit aid, review any network lookup targets before execution, and avoid providing sensitive private inventory data unless the execution environment is trusted. <br>
Risk: Incomplete or inaccurate dependency metadata can produce incomplete dependency graphs. <br>
Mitigation: Confirm dependency declarations and registry metadata before relying on the chain integrity verdict for deployment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/skill-dependency-chain-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a transitive dependency inventory, trust gradient analysis, version pinning assessment, graph anomaly findings, aggregated capability surface, chain integrity verdict, and recommended actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
