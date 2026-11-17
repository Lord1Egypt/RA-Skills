## Description:

Generates standalone HTML study notes and homework solutions for academic subjects, especially STEM, with KaTeX math, structured explanations, collapsible solutions, worked examples, and practice problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric6286](https://clawhub.ai/user/eric6286)

### License/Terms of Use:

MIT-0

## Use Case:

Students, tutors, and education-focused agents use this skill to convert topics, PDFs, or homework prompts into study notes, chapter guides, or step-by-step solution pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime commands may install unpinned Python packages into the active environment.

Mitigation: Review commands before execution and run helper scripts in a virtual environment with pinned dependencies.

Risk: Generated HTML may load KaTeX JavaScript from a third-party CDN.

Mitigation: Bundle KaTeX locally or redact sensitive study and homework content before opening the HTML.

Risk: Standalone homework solution pages may embed original problem images that contain sensitive student or course material.

Mitigation: Remove or redact sensitive images before sharing generated HTML outside the intended audience.

## Reference(s):

- [Study Notes ClawHub listing](https://clawhub.ai/eric6286/skills/study-notes)
- [Publisher profile](https://clawhub.ai/user/eric6286)
- [Design System](references/design-system.md)
- [Problem Solutions Reference](references/problem-solutions.md)
- [Workflow Orchestration & Verification](references/workflow-orchestration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Standalone HTML with KaTeX math, optional TSV flashcard exports, and supporting Markdown or shell snippets during generation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be self-contained files; homework images may be base64-inlined, and KaTeX assets may be loaded from a third-party CDN unless bundled locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
