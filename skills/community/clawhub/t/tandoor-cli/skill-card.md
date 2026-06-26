## Description: <br>
Manage recipes, meal plans, and shopping lists on a Tandoor Recipe Manager instance via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dcenatiempo](https://clawhub.ai/user/dcenatiempo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage recipes, meal plans, shopping lists, food categories, cook logs, and household administration through a configured Tandoor Recipe Manager CLI. It supports agent-assisted querying and user-approved changes to a user's own Tandoor instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive Tandoor credentials can expose private recipe, shopping, and household data or allow unwanted changes. <br>
Mitigation: Start with a read-only, short-lived OAuth token, store it securely, rotate it regularly, and revoke it when the agent task is complete. <br>
Risk: Write, destructive, bulk, and administrative commands can modify or delete Tandoor data. <br>
Mitigation: Require explicit user approval before mutations, explain the affected data before destructive or bulk operations, and avoid --force unless the user explicitly requests it. <br>
Risk: The skill depends on an external tandoor-cli npm package that runs with the permissions of the configured token. <br>
Mitigation: Review the npm package and source repository before granting write access, pin the package version to the skill version, and avoid admin or space-owner tokens unless needed. <br>


## Reference(s): <br>
- [Setup Guide](references/SETUP.md) <br>
- [Security Guidelines](SECURITY.md) <br>
- [tandoor-cli npm package](https://www.npmjs.com/package/tandoor-cli) <br>
- [tandoor-cli source repository](https://github.com/dcenatiempo/tandoor-cli) <br>
- [Tandoor Recipe Manager](https://tandoor.dev) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands, configuration examples, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output may be text, slim JSON, or raw API JSON depending on the selected --format option.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
