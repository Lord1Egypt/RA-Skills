## Description:

Student AI Agent automates an academic project workflow from assignment analysis through code, report, presentation, speaker notes, and Q&A preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18001469998ly-ops](https://clawhub.ai/user/18001469998ly-ops)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to turn assignment requirements into a structured academic project workflow with generated code, reports, slides, speaker notes, and Q&A preparation. Users should review outputs against applicable academic integrity policies before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create submission-style academic work that may be inappropriate under course or institutional rules.

Mitigation: Use it only where academic policy allows, disclose assistance when required, and review all generated work before submission.

Risk: The workflow may install dependencies, write files, and run generated code without clear safety controls.

Mitigation: Run dependency installs in an isolated environment, require confirmation before file writes or code execution, and inspect generated Python before running it.

Risk: The bundled runner should not be treated as proof that generated work was completed, validated, or correct.

Mitigation: Verify generated code, reports, slides, and Q&A materials independently before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18001469998ly-ops/skills/student-ai-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [JSON, Markdown, Python code, shell commands, .docx reports, and .pptx slides]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates project output folders and generated coursework materials when executed.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
