## Description: <br>
Manage Thermomix/Cookidoo meal planning via tmx-cli, including recipe search, weekly meal plan management, shopping list generation, favorites, and recipe details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lars147](https://clawhub.ai/user/Lars147) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use this skill to manage Cookidoo meal planning from a terminal-oriented workflow. It helps agents search recipes, inspect recipe details, maintain weekly plans and favorites, and generate or export shopping lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify a user's Cookidoo account, including meal plans, shopping lists, and favorites. <br>
Mitigation: Confirm plan, favorites, and shopping-list changes before execution, especially remove, move, clear, and generated-list actions. <br>
Risk: The skill handles Cookidoo passwords and session cookies in ways that can leak account access. <br>
Mitigation: Prefer interactive login over password-based flows, avoid sharing or committing the skill directory, and delete local cookie or token files when the integration is no longer needed. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [Cookidoo skill page](https://clawhub.ai/Lars147/tmx-cli) <br>
- [Publisher profile](https://clawhub.ai/user/Lars147) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON-producing CLI invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can direct use of --json for programmatic parsing and may produce shopping-list exports in Markdown or JSON.] <br>

## Skill Version(s): <br>
0.1.0 (source: pyproject.toml and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
