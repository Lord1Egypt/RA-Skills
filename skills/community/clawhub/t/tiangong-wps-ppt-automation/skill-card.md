## Description: <br>
Automates common PowerPoint/WPS Presentation operations on Windows via COM for single-presentation actions, including reading text, notes, and outlines; exporting PDF or images; replacing text; editing slides; unifying fonts or themes; and extracting images or media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fadeloo](https://clawhub.ai/user/Fadeloo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and office automation users use this skill to inspect, export, and modify a single local PowerPoint or WPS Presentation file on Windows through scripted COM commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted slide text, speaker notes, PDFs, and images may contain sensitive presentation content. <br>
Mitigation: Treat generated text, notes, PDFs, and images as sensitive files and store or share them only in approved locations. <br>
Risk: Replace, slide editing, font, theme, and export commands can overwrite or materially change presentation outputs. <br>
Mitigation: Prefer saving modified presentations and exports to new paths, and keep the original presentation unchanged until results are reviewed. <br>
Risk: The skill depends on local Windows COM automation and pywin32 package installation. <br>
Mitigation: Install pywin32 only from trusted package sources and use the skill only on Windows systems where PowerPoint or WPS Presentation automation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fadeloo/tiangong-wps-ppt-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; generated files may be TXT, PDF, PNG images, or PPTX.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally on Windows with PowerPoint or WPS Presentation and pywin32; intended for one presentation at a time.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
