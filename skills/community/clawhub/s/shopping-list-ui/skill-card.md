## Description:

Web UI for the shopping-list skill that adds a /shopping page to Second Brain with categorized viewing, inline editing, and CRUD actions over the shared shopping-list data files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajeenkya](https://clawhub.ai/user/ajeenkya)

### License/Terms of Use:


## Use Case:

Developers and Second Brain users use this skill to add a shopping-list web interface that can view, add, edit, check off, and delete items while sharing data with the conversational shopping-list skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies Second Brain app source and shares the existing shopping-list data file between chat and the web UI, where items can be edited or deleted.

Mitigation: Confirm the app and data-file changes before installation, and back up skills/shopping-list/data/active.json if the shopping-list data matters.

## Reference(s):

- [Shopping List UI ClawHub Skill Page](https://clawhub.ai/ajeenkya/skills/shopping-list-ui)

## Skill Output:

**Output Type(s):** [Code, Files, Configuration, Guidance]

**Output Format:** [Markdown instructions describing app file additions, source modifications, and shared data-file behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running Second Brain Next.js portal and the shopping-list skill data files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
