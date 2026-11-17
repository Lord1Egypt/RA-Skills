## Description:

Recognizes standing, sitting, lying, bending, hand-raising, running, falling, and abnormal postures for security monitoring and elderly care scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to analyze local or URL-based monitoring videos for posture recognition, abnormal posture detection, fall warnings, and history report lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release under-discloses how sensitive video, identity data, reusable tokens, and history reports are uploaded, stored, and accessed.

Mitigation: Document media and identity data handling before deployment, minimize retained data, and require explicit authorization for history report access.

Risk: The release includes configuration evidence of plaintext HTTP development endpoints.

Mitigation: Use HTTPS production endpoints, remove development endpoints from release configuration, and verify transport security before installation.

Risk: Automatic report and history lookup can expose prior analysis results if identity scoping is too broad.

Mitigation: Constrain lookup to the authenticated user or tenant, avoid exposing internal identity values, and audit report access paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-human-posture-recognition-analysis)
- [Publisher profile](https://clawhub.ai/user/smyx-sunjinhui)
- [Skill demo](https://lifeemergence.com/sample.html)
- [API documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown text or JSON analysis results, with optional output file content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fall warnings, posture counts, structured recognition data, report links, and history report tables.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
