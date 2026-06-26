## Description: <br>
Creates, reads, edits, validates, and visually reviews PowerPoint presentations using PPTX files, Office XML, pptxgenjs, and local conversion tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
Anthropic Proprietary Terms <br>


## Use Case: <br>
Developers, analysts, and content creators use this skill to create, inspect, edit, QA, and convert PowerPoint presentations. It supports both template-based Office XML workflows and from-scratch deck generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local conversion tools and mutate Office package contents. <br>
Mitigation: Use it in a single-user or sandboxed environment and review generated or modified presentations before sharing. <br>
Risk: The security review flagged broader Office/document code and an unused browser automation dependency. <br>
Mitigation: Before broad deployment, remove or justify unused dependencies and document whether non-PPTX Office helpers are intentionally supported. <br>
Risk: The security review flagged a LibreOffice shim that compiles and preloads code from a shared temporary path. <br>
Mitigation: Replace the shared temporary shim path with a private safely created temporary directory or a vetted packaged component. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fslong520/slidepro) <br>
- [Editing Presentations](artifact/editing.md) <br>
- [PptxGenJS Tutorial](artifact/pptxgenjs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and code snippets; generated artifacts may include .pptx files, PDFs, JPEG thumbnails, and extracted text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Office and presentation tooling for conversion, thumbnailing, and visual QA workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
