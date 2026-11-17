## Description:

Helps assess UDI database submission obligations, required fields, timing, and potential gaps for medical devices in China, the United States, and the European Union.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Medical-device compliance teams and developers use this skill to screen which UDI database and submission fields may apply, identify timing obligations, and flag incomplete inputs for human review. It is decision support, not a legal or regulatory determination.

### Deployment Geography for Use:

Global; the described regulatory coverage is China, the United States, and the European Union.

## Known Risks and Mitigations:

Risk: The skill requests shell, file-write, and web access without a clear need in its documentation.

Mitigation: Review before installation; withhold those permissions unless their purpose, file scope, and network destinations are justified and approved.

Risk: UDI submission guidance may be incomplete or outdated, particularly for exceptional devices or changing rules.

Mitigation: Treat results as decision support and have a qualified reviewer check current official regulatory requirements before submission or launch.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/udi-db-submission-check)
- [SynomosAI knowledge site](https://SynomosAI.cn/knowledge/)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Described fields include result, obligation and warning details, rc (0 complete, 1 warnings, 2 invalid or insufficient input), and error_code; no executable is included in the supplied artifact.]

## Skill Version(s):

1.0.1 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
