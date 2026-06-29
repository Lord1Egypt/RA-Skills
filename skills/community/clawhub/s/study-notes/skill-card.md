## Description: <br>
Study Notes generates polished standalone HTML study notes and step-by-step homework solutions for academic subjects, especially STEM, with KaTeX math, worked examples, collapsible derivations and solutions, callouts, figures, and practice problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eric6286](https://clawhub.ai/user/eric6286) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, tutors, and educators use this skill to turn course PDFs, homework sets, problem images, or topic prompts into exam-ready study notes or standalone solution pages for learning and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated notes can include content, figures, or images from user-provided course files. <br>
Mitigation: Review the generated HTML before sharing it and avoid embedding sensitive, private, or restricted course material. <br>
Risk: Generated HTML may load KaTeX assets from a CDN. <br>
Mitigation: Use the generated file only in an environment where that network access is acceptable, or adapt the template to use locally hosted KaTeX assets. <br>
Risk: Optional helper setup may install Python packages. <br>
Mitigation: Run helper commands in an isolated environment and review package installation commands before execution. <br>
Risk: Study notes or homework solutions may contain educational or mathematical mistakes if not reviewed. <br>
Mitigation: Use the skill's verification workflow and helper checks, then review important solutions before relying on them. <br>


## Reference(s): <br>
- [Study Notes on ClawHub](https://clawhub.ai/eric6286/study-notes) <br>
- [Design System](references/design-system.md) <br>
- [Problem Solutions](references/problem-solutions.md) <br>
- [Workflow Orchestration](references/workflow-orchestration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Standalone HTML with embedded styling and KaTeX math, plus Markdown guidance and command snippets during the workflow.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are local files and may embed user-provided images or reference KaTeX CDN assets depending on the generated template.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
