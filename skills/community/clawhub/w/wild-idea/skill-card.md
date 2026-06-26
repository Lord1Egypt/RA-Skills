## Description: <br>
Generates lateral brainstorming outputs by juxtaposing concrete constraints from remote domains, random seed texts, and web-discovered topics against specific user-domain products or features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liwenyu2002](https://clawhub.ai/user/liwenyu2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, product teams, and creative workers use this skill when they are stuck on a product, design, or strategy problem and want unusual concrete idea prompts. The skill is intended to produce nail-to-counterpart brainstorming tables that pass comfort and web-verification gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local command execution through helper scripts. <br>
Mitigation: Review the scripts before running them and execute the skill in an environment where local command execution is acceptable. <br>
Risk: Tavily searches can expose search terms derived from the user's problem, and the skill involves a Tavily API key. <br>
Mitigation: Use a dedicated, revocable Tavily API key and avoid confidential project names, private strategy, or sensitive prompt details unless sending related queries to Tavily is acceptable. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/liwenyu2002/wild-idea) <br>
- [Skill specification](SKILL.md) <br>
- [ClawScan overview](CLAWSCAN.md) <br>
- [Remote-domain paradigms](references/paradigms.md) <br>
- [Seed library](references/mao-seeds.md) <br>
- [Search integration notes](references/search-integration.md) <br>
- [Tavily curl example](references/tavily-curl-example.md) <br>
- [Output example](templates/output-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables, optional helper-script JSON, shell commands, and an HTML poster template.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are expected to avoid explanatory connective text between the remote-domain nail and the user-domain counterpart.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package.json reports 5.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
