## Description: <br>
DNS record management on Volcengine networking services. Use when users need zone record query/update, traffic routing changes, or DNS propagation troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to query, update, and troubleshoot Volcengine DNS records with scoped changes and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect DNS record changes can disrupt websites, APIs, email, or other production services. <br>
Mitigation: Review every proposed DNS change, confirm the domain zone and record values, keep rollback values, and verify propagation after changes. <br>
Risk: Blind overwrites or broad changes can replace valid existing DNS records. <br>
Mitigation: Query existing records first, diff against the intended change, and scope add, update, or delete operations to the confirmed record. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/volcengine-network-dns) <br>
- [references/sources.md](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with command and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes existing-record checks, scoped DNS change steps, rollback values, and propagation validation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
