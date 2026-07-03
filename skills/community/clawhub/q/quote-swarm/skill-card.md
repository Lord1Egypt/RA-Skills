## Description: <br>
Quote Swarm is a smart-home quotation workflow for parsing floor plans, identifying devices, generating quotes, and packaging delivery artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaoshung1981888](https://clawhub.ai/user/gaoshung1981888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Smart-home consultants, installers, and sales teams use this skill to convert DXF, PDF, image, or panorama inputs into room and device analysis, point and wiring plans, an HTML quote, and a device list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create persistent files under ~/.workbuddy/tasks and ~/WorkBuddy/quotes despite declaring only file-read and network permissions. <br>
Mitigation: Install only if those writes are acceptable, invoke the skill explicitly by name, and review generated paths and files before relying on them. <br>
Risk: Customer floorplans, images, or panorama inputs may be handled by external processing tools or network services. <br>
Mitigation: Avoid sensitive customer material unless you control where outputs and network processing go. <br>
Risk: Generated quotes, device counts, and wiring plans may not match final onsite conditions. <br>
Mitigation: Treat the quote as preliminary, verify device quantities onsite, and review wiring plans against field conditions before contract or delivery. <br>


## Reference(s): <br>
- [Quote Swarm on ClawHub](https://clawhub.ai/gaoshung1981888/quote-swarm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated HTML, PNG, and JSON file specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create task files under ~/.workbuddy/tasks and quote artifacts under ~/WorkBuddy/quotes when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
