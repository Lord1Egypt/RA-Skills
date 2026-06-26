## Description: <br>
Agent Script DSL for deterministic Salesforce Agentforce agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsouza-anush](https://clawhub.ai/user/dsouza-anush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Salesforce engineers use this skill to author, review, validate, preview, publish, and activate deterministic Agentforce Agent Script authoring bundles. It is intended for .agent files, finite-state topic flows, slot filling, instruction resolution, and Salesforce CLI-based Agent Script workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes automatic validation behavior that can use a local Salesforce login and default org to query Salesforce configuration. <br>
Mitigation: Review the validator before enabling hooks, set the intended validation org explicitly, use a sandbox or least-privileged org, and avoid relying on a production default org. <br>
Risk: Salesforce trace files, OAuth secrets, org aliases, and publish or activate commands can expose sensitive operational material. <br>
Mitigation: Treat these artifacts and commands as sensitive, review them before sharing or execution, and keep publish or activation steps tied to an explicitly chosen target org. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dsouza-anush/sf-ai-agentscript) <br>
- [Agent Script documentation](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html) <br>
- [Agentforce DX guide](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx.html) <br>
- [Salesforce CLI agent commands](https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/cli_reference_agent_commands_unified.htm) <br>
- [Activation checklist](references/activation-checklist.md) <br>
- [Agent user setup](references/agent-user-setup.md) <br>
- [Syntax reference](references/syntax-reference.md) <br>
- [Validator rule catalog](references/validator-rule-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Agent Script, YAML, XML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to .agent authoring bundles and Salesforce metadata; validation can involve Salesforce CLI commands against a selected org.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
