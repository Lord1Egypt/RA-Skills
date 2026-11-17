## Description:

Manage Thermomix/Cookidoo meal planning via tmx-cli for recipe search, weekly meal plans, shopping lists, favorites, and recipe details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lars147](https://clawhub.ai/user/lars147)

### License/Terms of Use:

MIT

## Use Case:

External users and AI agents use this skill to manage Cookidoo/Thermomix recipes, meal plans, favorites, and shopping lists through the bundled tmx-cli command-line tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI requires Cookidoo account access and stores session or token data locally.

Mitigation: Install only if comfortable granting Cookidoo account access, prefer the bundled reviewed file or a pinned release, and protect or delete local cookie and token files when finished.

Risk: Supplying a password through command-line flags can expose credentials through shell history or process inspection.

Mitigation: Use the interactive login flow when possible and avoid passing passwords as command-line arguments.

Risk: Meal plan, favorites, and shopping-list commands can remove or clear user data.

Mitigation: Confirm destructive actions, including plan removal and shopping-list clearing, before running the command.

## Reference(s):

- [Full Command Reference](references/commands.md)
- [tmx-cli README](README.md)
- [Cookidoo](https://cookidoo.de)
- [tmx-cli Repository](https://github.com/Lars147/tmx-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and CLI outputs in text, Markdown, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to prefer --json for parseable CLI output and to confirm destructive actions before execution.]

## Skill Version(s):

0.1.0 (source: release evidence and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
