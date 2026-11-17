## Description:

Connects agents to Scrollport tools for structured data, enrichment, media, connected apps, and workspace file management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrollport](https://clawhub.ai/user/scrollport)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use Scrollport when a task needs structured web or business data, verification, media, or an authorized connected app. They discover and inspect tools before paid runs, and manage workspace reference files under the user's spending and access controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial, so unresolved local references leave some evidence incomplete.

Mitigation: Review the unresolved references and complete the security review before connecting the skill to a workspace.

Risk: The skill can make paid tool calls and its file permissions include permanent deletion.

Mitigation: Check workspace spending controls and confirm the intended files and actions before running paid calls or deleting files.

## Reference(s):

- [Scrollport setup guide](https://scrollport.com/start)
- [Scrollport upload file documentation](https://scrollport.com/docs/control-tools/upload_file)
- [Scrollport Skill registry](https://scrollport.com/skills/registry.json)
- [Scrollport current Skill document](https://scrollport.com/skill)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Text, Files]

**Output Format:** [Markdown guidance and task-dependent tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected catalog tool; paid runs follow workspace spending controls, and file tools can upload or permanently delete files.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
