## Description:

Exports SiYuan Note documents to Word (.docx), supporting document ID, path, or name search and optional batch export of child documents with embedded assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chimyves](https://clawhub.ai/user/chimyves)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users with SiYuan Note use this skill to export one document, a searched document, or a document subtree into Word files while returning structured JSON results for agent handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted search text or document IDs could broaden SiYuan SQL queries and expose unintended notes.

Mitigation: Prefer exact trusted document IDs or paths, avoid untrusted search terms, and review or patch SQL handling before use on sensitive notebooks.

Risk: The skill uses a private SiYuan API token to export notebook content.

Mitigation: Use the least-privileged token available, keep the token out of committed configuration, and install only for agents and prompts you trust.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chimyves/skills/siyuan-export)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration]

**Output Format:** [Word (.docx) files with JSON status results and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running SiYuan instance and a configured SiYuan API token; exported document assets are embedded in the generated .docx files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
