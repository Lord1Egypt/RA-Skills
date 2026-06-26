## Description: <br>
Todozi Eisenhower matrix API client and LangChain tools for creating, listing, searching, updating, completing, and deleting matrices, tasks, goals, notes, bulk operations, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bgengs](https://clawhub.ai/user/bgengs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to connect agents to a Todozi account for managing Eisenhower-matrix tasks, goals, notes, matrices, bulk operations, and webhooks through an async SDK or LangChain tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify a user's Todozi account, including creating, updating, completing, and deleting tasks, goals, notes, matrices, and webhooks. <br>
Mitigation: Install only when account access is intended, use a Todozi API key appropriate for this skill, and require clear approval for deletes, bulk changes, completions, and webhook changes. <br>
Risk: A custom TODOZI_BASE endpoint could direct API-key-authenticated requests to an untrusted service. <br>
Mitigation: Leave TODOZI_BASE at the default Todozi API unless the replacement endpoint is trusted. <br>
Risk: Webhook configuration can send Todozi event data to external URLs. <br>
Mitigation: Configure webhooks only for HTTPS URLs that the user controls or trusts. <br>


## Reference(s): <br>
- [Todozi API Reference](references/api_reference.md) <br>
- [Todozi API](https://todozi.com/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/bgengs/todozi) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Configuration instructions, Text] <br>
**Output Format:** [Python SDK objects, LangChain tool results, JSON-compatible API responses, and Markdown guidance with code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Todozi API key. Treat deletes, bulk changes, completions, webhook configuration, and custom TODOZI_BASE endpoints as user-approved actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
