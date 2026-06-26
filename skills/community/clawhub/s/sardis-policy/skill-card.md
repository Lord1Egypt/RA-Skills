## Description: <br>
Natural language spending policy creation and management for Sardis agent wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EfeDurmaz16](https://clawhub.ai/user/EfeDurmaz16) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to define, create, list, and test Sardis wallet spending policies for agent payments, including limits, vendor controls, time restrictions, and approval thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent create or replace real Sardis wallet spending policies when a Sardis API key is available. <br>
Mitigation: Use a least-privilege Sardis API key and require review of the exact wallet ID, parsed rules, limits, vendors, approval thresholds, and replacement target before any POST request. <br>
Risk: High-limit, auto-approve, or unrestricted policy templates could permit unintended spending if used unattended. <br>
Mitigation: Avoid unattended use of high-limit, auto-approve, or unrestricted templates, and use dry-run policy checks before relying on a policy for payments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EfeDurmaz16/sardis-policy) <br>
- [Sardis Website](https://sardis.sh) <br>
- [Sardis Policy Documentation](https://sardis.sh/docs/policies) <br>
- [Sardis API Reference](https://api.sardis.sh/v2/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SARDIS_API_KEY, curl, and jq; examples target the Sardis API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
