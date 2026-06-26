## Description: <br>
Query Art Blocks on-chain data using artblocks-mcp GraphQL and domain-specific tools for projects, tokens, artists, sales, traits, and custom schema exploration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryley-o](https://clawhub.ai/user/ryley-o) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve and analyze Art Blocks on-chain project, token, artist, wallet, mint, release, sales, and trait data. It guides users toward domain-specific tools first and uses GraphQL tools for custom queries, schema exploration, validation, optimization, and execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom GraphQL queries can return public wallet, ownership, and sales information beyond what a narrow task needs. <br>
Mitigation: Prefer named domain tools when they answer the question, and limit custom GraphQL queries to the fields needed for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryley-o/query-artblocks-data) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code] <br>
**Output Format:** [Markdown with GraphQL query examples and tool-selection guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return public wallet, ownership, sales, project, token, and trait information from Art Blocks data sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
