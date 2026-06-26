## Description: <br>
Agent identity management with TAP protocol verification and reputation tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EfeDurmaz16](https://clawhub.ai/user/EfeDurmaz16) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register AI agents, retrieve verified identity records, submit or query reputation data, and generate shareable identity cards for marketplace, compliance, and transaction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create payment-linked identity and reputation records without clear confirmation or rollback guidance. <br>
Mitigation: Require manual approval before registering agents, assigning payment or refund capabilities, or submitting reputation comments and transaction IDs. <br>
Risk: The skill depends on a Sardis API key that may allow sensitive identity or reputation operations. <br>
Mitigation: Use a least-privilege Sardis API key and test outside production before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EfeDurmaz16/sardis-identity) <br>
- [EfeDurmaz16 Publisher Profile](https://clawhub.ai/user/EfeDurmaz16) <br>
- [Sardis Homepage](https://sardis.sh) <br>
- [Sardis Identity Documentation](https://sardis.sh/docs/identity) <br>
- [Sardis TAP Protocol Documentation](https://sardis.sh/docs/tap) <br>
- [Sardis API Reference](https://api.sardis.sh/v2/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces curl and jq command patterns for Sardis identity, verification, reputation, and identity card workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
