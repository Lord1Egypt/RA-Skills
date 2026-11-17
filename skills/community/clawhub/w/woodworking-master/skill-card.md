## Description:

AI木工大师 provides Chinese-language woodworking guidance across joinery, hand tools, machines, wood selection, safety, finishing, and project planning, with optional interactive HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and woodworking learners use this skill to get practical Chinese-language guidance on joinery, tool selection, machine safety, materials, finishing, and staged project work. Agents can also generate an HTML report for supported woodworking topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report generator accepts a custom output path and can overwrite arbitrary writable local files.

Mitigation: Run the generator only with trusted arguments, prefer the default report filename, and constrain or remove the custom output option before use in shared or important workspaces.

## Reference(s):

- [Woodworking Knowledge Base](references/woodworking_knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown/text response with optional generated HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report generator supports topic listing, index generation, detail reports, and general-topic reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
