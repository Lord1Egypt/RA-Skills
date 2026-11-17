## Description:

Wiki Creator helps an agent build, update, query, and lint a local Markdown knowledge wiki from user-provided documents using full-page wiki units, two-level indexes, and explicit source citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to turn uploaded documents into a structured local wiki, incrementally update it, answer questions from the wiki first, and check wiki health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can operate outside their intended wiki boundaries.

Mitigation: Use an explicit --root in a non-sensitive location and add path containment and topic slug validation before routine use.

Risk: The wiki persists local knowledge that may include confidential documents.

Mitigation: Avoid storing confidential materials unless local persistence is acceptable, and add deletion or retention controls for managed use.

Risk: Persistent wiki content may be reused automatically in later knowledge answers.

Mitigation: Review cited wiki sources before relying on answers and keep source attribution visible in generated pages.

Risk: Raw document parsing and generated page paths require containment controls.

Mitigation: Restrict raw parsing to the wiki raw directory and scan generated pages before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neuhanli/skills/wiki-creator)
- [Query Mode](artifact/references/query-mode.md)
- [Page Authoring](artifact/references/page-authoring.md)
- [Cascade Update](artifact/references/cascade-update.md)
- [Schema Guide](artifact/references/schema-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown wiki pages, JSON index files, shell command guidance, and concise status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local filesystem state and generated wiki indexes; no vector retrieval is produced.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
