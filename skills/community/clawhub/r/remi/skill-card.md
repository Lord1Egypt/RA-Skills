## Description: <br>
Manage Apple Reminders via CLI with section support and iCloud sync. Use when the user asks to create, list, complete, search, or organize reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattheworiordan](https://clawhub.ai/user/mattheworiordan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage Apple Reminders from a command line, including lists, reminders, sections, due dates, completion, search, and diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminders access can read and change reminders, including destructive changes that may sync through iCloud. <br>
Mitigation: Install only from a trusted remi CLI source, confirm destructive targets before running commands, and prefer ID-based targeting when available. <br>
Risk: Title-based matching can affect the wrong reminder when names are ambiguous. <br>
Mitigation: Use exact list and reminder targets, inspect JSON output before follow-up actions, and use --id <prefix> when ambiguity is possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mattheworiordan/remi) <br>
- [npm package @mattheworiordan/remi](https://www.npmjs.com/package/@mattheworiordan/remi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with bash command examples and JSON response expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Use --json for programmatic calls; requires macOS 13+ with Reminders access and the remi CLI on PATH or via npx.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
