## Description: <br>
Visual Bug Hunter helps agents inspect GUI and web app screenshots, test UI interactions, locate visual defects in project code, and propose minimal fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yitao2027](https://clawhub.ai/user/yitao2027) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to diagnose visual UI bugs such as overlapping elements, disabled controls, broken layouts, and repeated rendering in GUI or web applications. It is intended to produce focused bug reports, minimal code fixes, and screenshot-based verification notes for user-reviewed changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshot review and GUI interaction can expose sensitive information or trigger real actions in an open application. <br>
Mitigation: Close sensitive windows, use test data, and avoid production workflows that can cause real transactions or irreversible changes. <br>
Risk: Generated fixes or bug reports may be incomplete or incorrect for the actual application behavior. <br>
Mitigation: Review generated diffs and verification conclusions before accepting changes. <br>
Risk: The README mentions an optional CLI/PyPI project that is separate from this instruction-only ClawHub skill. <br>
Mitigation: Vet the optional external package separately before installing or running it outside the skill workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yitao2027/visual-bug-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON bug reports, minimal code diffs, shell commands, and verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include screenshot evidence paths, code locations, severity labels, and before/after verification conclusions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
