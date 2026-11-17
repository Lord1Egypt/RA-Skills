## Description:

Thần Cửu (Jaskies) helps agents calculate eight Thần Cửu personality indicators and compare relationship compatibility from names and birth dates using bundled Vietnamese reference material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaskies](https://clawhub.ai/user/jaskies)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to prepare Vietnamese Thần Cửu personality analyses for individuals and relationship comparisons from provided names and birth dates. The skill is suited for reflective personality reports, not identity verification, medical, legal, financial, or other high-stakes decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for full legal names and dates of birth and may include relationship context and personality inferences in reports.

Mitigation: Collect only the minimum details needed for the requested analysis, avoid unnecessary identity-document details, and get consent before analyzing another person.

Risk: The artifact instructs agents to save generated analyses persistently without clear consent, retention, or deletion controls.

Mitigation: Ask the agent not to save results unless retention is explicitly wanted, and delete knowledge/ThanCuu/ records when they are no longer needed.

Risk: One bundled reference file points to an external knowledge path for Số Đường Đời content rather than including that material in the artifact.

Mitigation: Review any generated Số Đường Đời analysis for completeness and ensure required source material is available before relying on that part of a report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaskies/skills/thancuu-jaskies)
- [GioiThieuThanCuu.md](references/GioiThieuThanCuu.md)
- [SoCamXuc.md](references/SoCamXuc.md)
- [SoDuongDoi.md](references/SoDuongDoi.md)
- [SoNgaySinh.md](references/SoNgaySinh.md)
- [SoNhanCach.md](references/SoNhanCach.md)
- [SoNoiTam.md](references/SoNoiTam.md)
- [SoTenGoi.md](references/SoTenGoi.md)
- [SoThaiDo.md](references/SoThaiDo.md)
- [SoVanMenh.md](references/SoVanMenh.md)
- [TracNghiemThanCuu.md](references/TracNghiemThanCuu.md)
- [TuongQuanGiuaCacConSo.md](references/TuongQuanGiuaCacConSo.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Vietnamese plain text or Markdown personality and relationship analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Artifact instructions say generated analyses may be saved under knowledge/ThanCuu/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
