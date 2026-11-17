## Description:

Use when managing QJZD Nav links, categories, and tags from the terminal, including list, create, update, delete operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nqdy666](https://clawhub.ai/user/nqdy666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent manage QJZD Nav content from the terminal. It supports listing, creating, updating, deleting, filtering, paginating, and reordering links, categories, and tags through qjzd-nav commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delete and category reorganization commands can remove or move QJZD Nav content in ways that may be irreversible without recovery planning.

Mitigation: List objects first, confirm IDs, document recovery expectations, and use backups or a non-production environment before bulk changes.

Risk: Running the skill without an authenticated qjzd-nav session can fail or target the wrong account context.

Mitigation: Check qjzd-nav auth current before content operations, or load the companion authentication skill when auth may not be ready.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nqdy666/skills/qjzd-nav-cli-content)
- [Publisher profile](https://clawhub.ai/user/nqdy666)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented qjzd-nav command options for automation.]

## Skill Version(s):

1.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
