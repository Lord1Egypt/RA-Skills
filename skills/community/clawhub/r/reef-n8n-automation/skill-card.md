## Description: <br>
Build, customize, test, and deliver n8n workflows using a large template library for triggers, actions, error handling, and multi-step automations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[staybased](https://clawhub.ai/user/staybased) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Automation builders, consultants, and developers use this skill to assemble client-ready n8n workflows, adapt templates to specific app integrations, configure credentials, test workflow behavior, and prepare delivery documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported n8n templates or generated workflows may contain incorrect mappings, unsafe activations, or behavior that does not match the client environment. <br>
Mitigation: Inspect each workflow before import, test nodes manually, verify error paths, and manually approve scheduled or webhook workflow activation. <br>
Risk: Workflow delivery can expose credentials or API keys if secrets are hardcoded in nodes or reused across clients. <br>
Mitigation: Store secrets in n8n credentials or environment variables, use separate client-owned credentials, and review exported workflow JSON before sharing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with workflow JSON snippets, shell commands, checklists, and delivery notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include n8n workflow architecture, import/export steps, credential checklists, test plans, and client handoff documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
