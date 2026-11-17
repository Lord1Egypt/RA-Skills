## Description:

Access Splitwise expense and group data via MCP. Use when the user asks about Splitwise expenses, groups, friends, or balances, or wants to add, edit, or delete expenses. Triggers on phrases like "add that expense to Splitwise", "split this with the vacation group", "make sure Sam is in that group", "what do I owe", or any request involving shared expenses or group management in Splitwise. Requires splitwise-mcp installed and the splitwise server registered (see Setup below).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

People using Splitwise can ask an agent to look up shared expenses, groups, friends, balances, and receipts, or to manage expenses and group membership through Splitwise. The agent can summarize account information and prepare changes for user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign security verdict has medium confidence, and Skillspector coverage was partial because references were unresolved.

Mitigation: Review unresolved references and the skill before enabling it with a Splitwise API key.

Risk: The skill uses a Splitwise API key to access account and shared-expense data.

Mitigation: Keep the API key in the configured secret environment variable and approve each proposed write after reviewing its preview.

## Reference(s):

- [Project repository](https://github.com/chrischall/splitwise-mcp)
- [splitwise-mcp on npm](https://www.npmjs.com/package/splitwise-mcp)

## Skill Output:

**Output Type(s):** [Text, Expense and group data, Confirmation previews]

**Output Format:** [Natural-language summaries and structured expense or group data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations require user confirmation; receipt retrieval can return image or PDF files.]

## Skill Version(s):

3.7.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
