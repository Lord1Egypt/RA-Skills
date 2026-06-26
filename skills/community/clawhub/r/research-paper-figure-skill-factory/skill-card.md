## Description: <br>
A research-paper figure Skill Factory for generating reusable specialized paper-figure-making skills from lawful corpus evidence, then using those generated skills for concrete target papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, authors, and agent-skill developers use this skill to build evidence-backed, reusable figure-making skills for specific scientific paper figure classes, then use those generated skills to plan, compare, render, review, and integrate figures for target papers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may search the web, download open PDFs, and write local corpus or manifest files. <br>
Mitigation: Use only lawful sources or user-authorized documents, and scope corpus paths to materials intended for processing. <br>
Risk: Generated specialized skills may contain incomplete figure taxonomy, workflow, or prompt guidance if the evidence corpus is limited. <br>
Mitigation: Review evidence maps, taxonomy claims, and generated skill tests before installing or reusing a generated skill. <br>
Risk: Private PDFs or broad local folders may be processed if the user points the agent at them. <br>
Mitigation: Avoid private documents and broad directories unless processing those materials is intentional and authorized. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/c-narcissus/research-paper-figure-skill-factory) <br>
- [Publisher profile](https://clawhub.ai/user/c-narcissus) <br>
- [README](README.md) <br>
- [Skill documentation](docs/README.md) <br>
- [Master workflow](references/master-workflow.md) <br>
- [Generated specialized skill output spec](references/generated-specialized-skill-output-spec.md) <br>
- [Generated skill multi-candidate policy](references/generated-skill-multi-candidate-policy.md) <br>
- [Visual-first decision board protocol](references/visual-first-decision-board-protocol.md) <br>
- [Prompt generation and rendering policy](references/prompt-generation-and-rendering-policy.md) <br>
- [Strict text/image turn separation policy](references/strict-text-image-turn-separation-policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured state footers, skill-package files, JSON/CSV templates, and image-generation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires image-generation capability for rendering; text and image outputs are separated into distinct response modes.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, metadata.json, changelog, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
