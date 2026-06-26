## Description: <br>
Guides an agent to build professional resumes for Reactive Resume by asking clarifying questions, avoiding hallucinated details, and producing valid import-ready JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amruthpillai](https://clawhub.ai/user/amruthpillai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and resume authors use this skill to gather resume details conversationally and generate Reactive Resume JSON that can be imported into rxresu.me. It is also useful when users need guidance on resume section structure, ordering, and concise content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume generation can collect personal contact details, career history, private links, and reference information. <br>
Mitigation: Only provide information intended for the final resume JSON, and omit or redact sensitive details such as exact addresses, private links, phone numbers, or reference contact information unless needed. <br>
Risk: Generated resume content may be misleading if the agent fills gaps from assumptions. <br>
Mitigation: Ask clarifying questions for missing facts and include only information explicitly provided by the user. <br>


## Reference(s): <br>
- [Reactive Resume](https://rxresu.me) <br>
- [Reactive Resume JSON Schema](https://rxresu.me/schema.json) <br>
- [Reactive Resume Schema Reference](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Guidance] <br>
**Output Format:** [Conversational guidance and complete Reactive Resume JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated resume content should include only user-provided facts and conform to the Reactive Resume schema.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
