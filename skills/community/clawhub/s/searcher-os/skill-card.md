## Description: <br>
Manage deal pipeline, search on-market deals, track brokers, run SBA loan calculations, manage tasks, and review CIM analyses in Searcher OS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joshthacker](https://clawhub.ai/user/joshthacker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Acquisition entrepreneurs and deal teams use this skill to manage Searcher OS deal workflows, including pipeline review, broker tracking, inbox triage, CIM analysis lookup, SBA loan calculations, and task updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad API-key access to sensitive acquisition, broker, inbox, pipeline, and CIM-related data. <br>
Mitigation: Use only with trusted Searcher OS accounts, prefer a dedicated revocable API key, and limit exposure of confidential deal data to appropriate users. <br>
Risk: Some account-changing actions can update pipeline records, dismiss deals, ignore emails, or change tasks without explicit confirmation. <br>
Mitigation: Instruct the agent to ask before write actions, review the live tool list, and use the Searcher OS confirmation flow where available. <br>


## Reference(s): <br>
- [Searcher OS homepage](https://searcheros.ai) <br>
- [Searcher OS agent API base URL](https://searcheros.ai/api/agent) <br>
- [ClawHub skill page](https://clawhub.ai/joshthacker/searcher-os) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls, configuration] <br>
**Output Format:** [Markdown guidance with JSON API request and response patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SEARCHER_OS_API_KEY and Searcher OS confirmation flows for selected write actions.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
