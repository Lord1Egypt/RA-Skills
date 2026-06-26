## Description: <br>
Save, search, list, update, and delete bookmarks and text notes in Runa. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imprakharshukla](https://clawhub.ai/user/imprakharshukla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to save links, text notes, and supported files to their Runa library, then search, list, update, archive, or delete saved items through the Runa API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user-selected links, notes, and uploaded files to Runa for storage and processing. <br>
Mitigation: Avoid saving secrets, private notes, internal links, or sensitive documents unless the user is comfortable with Runa storing and processing that content. <br>
Risk: Delete operations can permanently remove bookmarks and tags. <br>
Mitigation: Require explicit user confirmation before deleting bookmarks and review the target item before confirming. <br>
Risk: API access depends on a valid Runa API key. <br>
Mitigation: Store the API key in the configured secret location or environment variable and avoid exposing it in prompts, logs, or saved notes. <br>


## Reference(s): <br>
- [Runa API Reference](references/api.md) <br>
- [Runa ClawHub listing](https://clawhub.ai/imprakharshukla/runa) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown responses with API results and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured RUNA_API_KEY to call the Runa API; delete operations require confirmation.] <br>

## Skill Version(s): <br>
0.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
