## Description:

Manage recipes, meal plans, and shopping lists in Tandoor Recipe Manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsnikhil](https://clawhub.ai/user/itsnikhil)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search Tandoor recipes, inspect recipe details, plan meals, create recipes, and manage shopping-list entries through command-line actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Tandoor API token could be sent over a non-HTTPS URL.

Mitigation: Set TANDOOR_URL to an HTTPS endpoint except for tightly controlled local testing.

Risk: The skill can create recipes, add meal-plan entries, and modify or delete shopping-list items.

Mitigation: Use the narrowest Tandoor API token available and review requested write actions before execution.

## Reference(s):

- [Tandoor API Quick Reference](references/API.md)
- [ClawHub skill page](https://clawhub.ai/itsnikhil/skills/tandoor-recipes)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text and JSON from command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, TANDOOR_URL, and TANDOOR_API_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
