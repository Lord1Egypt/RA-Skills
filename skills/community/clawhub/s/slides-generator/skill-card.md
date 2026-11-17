## Description:

Create Hummingbot-branded PDF slides from markdown with Mermaid diagram support. Use for presentations, decks, and technical documentation with professional diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengtality](https://clawhub.ai/user/fengtality)

### License/Terms of Use:


## Use Case:

Developers, technical writers, and external users can use this skill to turn markdown presentation content into Hummingbot-branded PDF slide decks, including Mermaid diagrams and two-column slide layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use can run a remote script that may change outside this release artifact.

Mitigation: Use a reviewed local copy or fixed version of the generation script instead of fetching and executing the remote script at runtime.

Risk: The script can download and install Python or Node packages during execution.

Mitigation: Run it in an isolated environment with pinned dependencies, and require separate user confirmation before any setup changes the Python or Node environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengtality/skills/slides-generator)
- [Remote generation script referenced by the skill](https://raw.githubusercontent.com/hummingbot/skills/main/skills/slides-generator/scripts/generate_slides.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with bash commands, Mermaid code, slide outline text, and generated PDF file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate PDF slides from local markdown input; Mermaid diagrams require Mermaid CLI or fall back to code block rendering.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
