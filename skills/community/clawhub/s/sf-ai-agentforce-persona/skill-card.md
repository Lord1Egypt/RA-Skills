## Description:

Designs Salesforce Agentforce agent personas using an identity and 12-dimension framework, with optional scoring, sample dialog, and Agentforce encoding outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsouza-anush](https://clawhub.ai/user/dsouza-anush)

### License/Terms of Use:

MIT-0

## Use Case:

Agent designers, conversation designers, and Salesforce Agentforce implementers use this skill to turn brand, audience, and use-case inputs into a structured agent persona. It can also produce sample dialog, scorecards, and Agentforce Builder or Agent Script persona-encoding guidance for downstream implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated persona and Agentforce instructions may not meet legal, disclosure, or brand requirements for a live customer-facing agent.

Mitigation: Review generated persona documents and Agentforce instructions with the appropriate legal, disclosure, and brand stakeholders before pasting them into a live agent.

Risk: The skill reads supplied brand or persona material and creates local Markdown outputs.

Mitigation: Provide only material approved for agent-assisted processing and inspect generated files in _local/generated/ before sharing or deploying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dsouza-anush/skills/sf-ai-agentforce-persona)
- [Agent Persona Framework](artifact/references/persona-framework.md)
- [Persona Encoding Guide](artifact/references/persona-encoding-guide.md)
- [Voice Encoding Guide](artifact/references/persona-encoding-guide-voice.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files and inline Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown artifacts under _local/generated/ for persona documents, sample dialogs, scorecards, and Agentforce encoding outputs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
