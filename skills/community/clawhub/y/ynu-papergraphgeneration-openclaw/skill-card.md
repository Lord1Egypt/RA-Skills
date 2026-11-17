## Description:

Generates academic paper diagrams from PDF or plain-text papers, including architecture diagrams, flowcharts, motivation figures, results plots, captions, and Mermaid topology descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljk00000](https://clawhub.ai/user/ljk00000)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and paper authors use this skill to convert academic paper content into visual figure plans, generated diagrams, result charts, captions, and reusable topology descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper-derived content may be sent to the configured external image API.

Mitigation: Avoid confidential, unpublished, or proprietary papers unless the configured API and data handling terms are acceptable.

Risk: The result-chart path can execute generated Python code.

Mitigation: Review the generated code before running it and execute it in a sandbox without secrets or broad filesystem access.

Risk: The image download behavior was flagged as under-scoped by the authoritative security review.

Mitigation: Use trusted API endpoints and inspect downloaded outputs before relying on them in publications or downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljk00000/skills/ynu-papergraphgeneration-openclaw)
- [Skill instructions](artifact/skill.md)
- [Artifact README](artifact/readme.md)
- [Default image API endpoint](https://api.acedata.cloud/nano-banana/images)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with command examples, generated prompts, image files, Matplotlib code, captions, and Mermaid topology text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write extracted text and generated images or charts to an output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
