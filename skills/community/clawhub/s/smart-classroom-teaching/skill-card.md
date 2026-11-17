## Description:

Smart-Classroom Teaching helps agents plan, deliver, visualize, analyze, and review classroom teaching workflows across lesson visualization, Socratic dialogue, classroom-record analysis, personalized tutoring, teaching-resource generation, and content-safety checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers, students, and education developers use this skill to create smart-classroom teaching flows, generate lesson materials, analyze classroom records, support personalized tutoring, and optionally render teaching state in a local browser workbench.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local workbench can expose unsafe state import and rendering paths that may leak or alter classroom content.

Mitigation: Use the local server only in a trusted environment, do not leave it running while browsing untrusted sites, and avoid importing replay JSON from untrusted sources.

Risk: Classroom histories and state files can contain identifiable student data.

Mitigation: Minimize and desensitize student data before export, import, or storage, and apply the skill's privacy-desensitization workflow before handling student information.

Risk: The workbench lacks production controls for sensitive classroom data.

Mitigation: Add authentication, CORS restrictions, schema validation, and safe rendering before using it with sensitive classroom records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/smart-classroom-teaching)
- [Smart classroom task catalog](artifact/references/smart-classroom-catalog.md)
- [Smart classroom requirements](artifact/references/smart-classroom-requirements.md)
- [Smart classroom exemplars](artifact/references/smart-classroom-exemplars.md)
- [Smart classroom workbench](artifact/assets/smart-classroom-workbench.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured JSON, with optional HTML/SVG teaching-state content and local shell commands for the workbench server]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce teaching-state JSON for the browser workbench, exported lesson-history JSON, and classroom analysis or lesson-planning prose.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
