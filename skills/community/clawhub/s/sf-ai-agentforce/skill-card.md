## Description: <br>
Guides Salesforce Agentforce Builder metadata work, including Builder-managed topics and actions, Prompt Builder GenAiPromptTemplate files, GenAiFunction and GenAiPlugin metadata, Models API usage, and custom Lightning types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsouza-anush](https://clawhub.ai/user/dsouza-anush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Salesforce admins use this skill to maintain Builder-based Agentforce agents, wire topics and actions, author Prompt Builder metadata, and apply Models API or custom Lightning type guidance while avoiding code-first Agent Script, testing, and deployment-only workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied Salesforce CLI commands or metadata examples could affect the wrong org or environment. <br>
Mitigation: Confirm the target org and alias, prefer a sandbox or scratch org, and review commands before execution. <br>
Risk: Models API examples or Chatter-related patterns can expose sensitive customer or business data if copied without review. <br>
Mitigation: Minimize sensitive data sent to AI services or posted to Chatter, and apply local data-handling policy before use. <br>
Risk: Live-action previews, publication, or activation in production can trigger unintended agent behavior. <br>
Mitigation: Validate in a non-production org first and treat publish or activation commands as deliberate release actions. <br>
Risk: Incomplete Builder dependencies, draft prompt templates, or mismatched action inputs can cause publish or runtime failures. <br>
Mitigation: Deploy supporting metadata first, confirm template status, and validate action input and output contracts before activation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dsouza-anush/sf-ai-agentforce) <br>
- [Agentforce Builder Workflow](references/builder-workflow.md) <br>
- [Agentforce Metadata Reference](references/metadata-reference.md) <br>
- [GenAiPromptTemplate Reference](references/genaiprompttemplate.md) <br>
- [Agent CLI Commands Reference](references/cli-commands.md) <br>
- [Agentforce Models API](references/models-api.md) <br>
- [Custom Lightning Types for Agentforce](references/custom-lightning-types.md) <br>
- [Salesforce Agentforce Metadata Types](https://developer.salesforce.com/docs/einstein/genai/references/agents-metadata-tooling/agents-metadata.html) <br>
- [Agentforce DX Developer Guide](https://developer.salesforce.com/docs/einstein/genai/guide/agent-dx-nga-author-agent.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with XML, Apex, JSON, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; proposes Salesforce metadata and CLI actions for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata: 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
