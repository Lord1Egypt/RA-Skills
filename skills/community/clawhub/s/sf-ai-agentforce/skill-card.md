## Description:

Supports Salesforce Agentforce Builder metadata work for Builder-managed topics and actions, Prompt Builder templates, GenAiFunction and GenAiPlugin metadata, Models API usage, and custom Lightning types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsouza-anush](https://clawhub.ai/user/dsouza-anush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Salesforce admins use this skill to maintain Builder-based Agentforce agents, register Flow, Apex, and Prompt Builder actions, author current GenAiPromptTemplate metadata, and troubleshoot publish or activation issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can lead users to update CRM records or publish AI output without enough permission, data-handling, and review safeguards.

Mitigation: Add user-mode SOQL/DML or explicit CRUD/FLS checks, minimize and classify CRM data sent to models, validate generated output, and require human approval before Chatter posts or business-record writes.

Risk: Live-action preview can execute agent actions in an org before the action behavior has been fully reviewed.

Mitigation: Use live-action preview only in an isolated test org unless the actions have been confirmed safe to execute.

Risk: Untrusted CRM record text can influence prompts or generated output.

Mitigation: Isolate untrusted record text in prompts and review model output before using it in customer-facing, operational, or write-back workflows.

## Reference(s):

- [Agentforce Builder Workflow](references/builder-workflow.md)
- [Agentforce Metadata Reference](references/metadata-reference.md)
- [GenAiPromptTemplate Reference](references/genaiprompttemplate.md)
- [Agent CLI Commands Reference](references/cli-commands.md)
- [Prompt Templates in Agentforce](references/prompt-templates.md)
- [Agentforce DX Developer Guide](https://developer.salesforce.com/docs/einstein/genai/guide/agent-dx-nga-author-agent.html)
- [Agentforce Metadata Types](https://developer.salesforce.com/docs/einstein/genai/references/agents-metadata-tooling/agents-metadata.html)
- [Salesforce AI Documentation](https://developer.salesforce.com/docs/einstein/genai/overview)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Salesforce metadata XML, Apex snippets, sf CLI commands, and configuration checklists for review before deployment.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
