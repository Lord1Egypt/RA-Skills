## Description: <br>
Connects an agent to OKKI (Xiaoman) CRM for customer lookup, follow-up records, order management, and channel-limited execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CRM operators use this skill to let an agent query OKKI CRM records, review follow-up activity, manage leads and orders, and gate CRM actions to an authorized #okki channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify CRM business records and send email through an external OKKI client. <br>
Mitigation: Require explicit human approval for create, update, delete, order, and email actions before execution. <br>
Risk: The referenced OKKI client, configuration, and token cache behavior are not included or fully described in the artifact. <br>
Mitigation: Review and trust the referenced okki_client.py and config before installation, use a least-privilege sandbox account, and restrict the #okki channel to authorized users. <br>


## Reference(s): <br>
- [OKKI CRM ClawHub release](https://clawhub.ai/cjboy007/ssa-okki-crm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with table outputs and inline shell or Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Customer and follow-up results are intended to hide internal IDs by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
