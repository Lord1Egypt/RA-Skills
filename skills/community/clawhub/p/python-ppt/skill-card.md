## Description: <br>
Generate dark-themed, technology-style PPTX presentations in 16:9 format using python-pptx helpers for slides, layouts, fonts, colors, and reusable presentation components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mr1008611](https://clawhub.ai/user/mr1008611) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate local Python scripts that assemble PowerPoint decks from user-provided topics, outlines, and content. It is suited for creating dark technology-style presentations with cover, section, content, comparison, architecture, card, table, and summary slides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python scripts may be executed locally to create the presentation file. <br>
Mitigation: Keep generated scripts limited to the included ppt_lib.py helpers and the intended PPTX output path before execution. <br>
Risk: Presentation content may include sensitive user-provided material. <br>
Mitigation: Avoid using sensitive deck content in untrusted environments. <br>
Risk: Dependency changes in python-pptx could affect rendering or behavior. <br>
Mitigation: Pin python-pptx in controlled environments. <br>


## Reference(s): <br>
- [Python PPT Generator on ClawHub](https://clawhub.ai/mr1008611/python-ppt) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python code and generated PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local .pptx files through python-pptx helper functions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
