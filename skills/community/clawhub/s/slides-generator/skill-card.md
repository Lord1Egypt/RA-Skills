## Description: <br>
Create Hummingbot-branded PDF slides from markdown with Mermaid diagram support for presentations, decks, and technical documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengtality](https://clawhub.ai/user/fengtality) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, technical writers, and presentation authors use this skill to turn structured markdown into Hummingbot-branded PDF slide decks with optional Mermaid diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented workflow runs mutable remote shell code. <br>
Mitigation: Run the bundled local script or a pinned, checksummed copy instead of using the curl-to-bash command. <br>
Risk: The script may install unpinned Python or npm packages on the user's machine. <br>
Mitigation: Use a project directory, virtual environment, or container before running package-manager installs. <br>
Risk: The workflow writes generated PDF files to user-selected paths. <br>
Mitigation: Choose a non-sensitive output directory and review write permissions before generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengtality/slides-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires markdown input and an output PDF path; Mermaid diagrams require Mermaid CLI or npx availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
