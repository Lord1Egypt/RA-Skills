## Description: <br>
Manage recipes, meal plans, and shopping lists in Tandoor Recipe Manager. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsnikhil](https://clawhub.ai/user/itsnikhil) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to manage a configured Tandoor Recipe Manager instance, including recipe search and creation, meal planning, and shopping-list updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create recipes, schedule meals, check off shopping-list items, and delete shopping-list entries in the configured Tandoor instance. <br>
Mitigation: Require user confirmation before mutation or deletion actions and verify the target item IDs and dates before execution. <br>
Risk: The skill uses a Tandoor API token and configured instance URL. <br>
Mitigation: Use the least-privileged token Tandoor supports, confirm TANDOOR_URL points to the intended instance, and avoid pasting or logging the token. <br>


## Reference(s): <br>
- [Tandoor API Quick Reference](references/API.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Tandoor API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js plus TANDOOR_URL and TANDOOR_API_TOKEN for live Tandoor API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
