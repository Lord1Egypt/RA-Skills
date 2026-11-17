## Description:

Generate professional technical documentation from codebases - API docs, READMEs, architecture diagrams, changelogs, and onboarding guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanwyngaard](https://clawhub.ai/user/seanwyngaard)

### License/Terms of Use:


## Use Case:

Developers and technical writers use this skill to generate client-deliverable documentation from codebases, including READMEs, API documentation, architecture overviews, changelogs, and onboarding guides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads selected project files and can write generated documentation into the workspace.

Mitigation: Run it on a working branch, prefer an output directory when possible, and review generated docs or README changes before committing.

Risk: Generated documentation may be incomplete or inaccurate if project structure, APIs, or configuration are not fully captured by the scan.

Mitigation: Review generated documentation against the source code and existing project docs before publishing or sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanwyngaard/skills/technical-doc-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/seanwyngaard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation files, OpenAPI YAML, Mermaid diagrams, and summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated documentation to output/docs/ or docs/ depending on the requested documentation package.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
