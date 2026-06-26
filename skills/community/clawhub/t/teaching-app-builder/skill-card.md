## Description: <br>
Teaching App Builder turns teaching text, concepts, lectures, or knowledge points into a self-contained interactive HTML teaching app that can be opened locally in a browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junwugit](https://clawhub.ai/user/junwugit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, instructional designers, and developers use this skill to convert source teaching material into a single-file interactive web lesson with charts, diagrams, formulas, quizzes, tabs, steppers, and visual explanations while preserving the original content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated pages may load JavaScript or CSS from external CDNs when opened in a browser. <br>
Mitigation: Review the generated HTML and CDN URLs before use, keep library selections minimal, and replace CDN links with trusted local copies when network exposure is not acceptable. <br>
Risk: Rendering untrusted Markdown through marked or innerHTML can introduce unsafe HTML into the generated page. <br>
Mitigation: Avoid rendering untrusted Markdown with the provided pattern unless it is sanitized, and inspect generated HTML before sharing or opening it in sensitive environments. <br>
Risk: Teaching content can become misleading if the agent adds facts, data, or citations that were not present in the source material. <br>
Mitigation: Review the generated lesson against the original teaching material and require uncertain or missing facts to remain clearly marked rather than invented. <br>


## Reference(s): <br>
- [Teaching App Builder source](artifact/SKILL.md) <br>
- [CDN catalog](artifact/references/cdn-catalog.md) <br>
- [Color schemes](artifact/references/color-schemes.md) <br>
- [Teaching interaction components](artifact/references/components.md) <br>
- [Library snippets](artifact/references/libraries.md) <br>
- [Single-file HTML skeleton](artifact/references/skeleton.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Guidance] <br>
**Output Format:** [Single self-contained HTML file with a brief Markdown delivery note] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML may reference selected external CDN libraries; default output is written to the current working directory unless the user specifies a path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
