## Description:

Npi Quality Gate is a Chinese-language advisory skill for manufacturing NPI gate reviews across EVT, DVT, PVT, and MP stages, using user-provided context and stage criteria to assess readiness, explain risks, and guide next steps without collecting full project records or making final release decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing quality, NPI, and product engineering teams use this skill to discuss stage-gate readiness, unresolved issue handling, and gate-risk implications for EVT, DVT, PVT, and MP reviews. It provides advisory analysis and targeted follow-up questions while leaving formal approval and sign-off to responsible humans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat advisory pass, conditional-pass, or fail wording as formal NPI release approval.

Mitigation: Require responsible humans to review any recommendation and keep final gate decisions and signatures outside the skill.

Risk: Users may paste unnecessary full project records into the chat when asking for gate-review help.

Mitigation: Limit inputs to stage-specific facts needed for the current question and avoid sharing full reports, BOMs, FMEAs, or sensitive records unless necessary.

Risk: The skill is Chinese-language and may be unsuitable for teams expecting English-language operating procedures.

Mitigation: Install it only for Chinese-language manufacturing NPI workflows or validate translations before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duding-engicool/skills/skill-npi-quality-gate)
- [Server-Resolved Source Repository](https://github.com/duding-engicool/skill-npi-quality-gate)
- [Publisher Profile](https://clawhub.ai/user/duding-engicool)
- [EVT Gate Checklist](references/gate-checklist-evt.md)
- [DVT Gate Checklist](references/gate-checklist-dvt.md)
- [PVT Gate Checklist](references/gate-checklist-pvt.md)
- [MP Gate Checklist](references/gate-checklist-mp.md)
- [NPI Gate Decision Matrix and Open-Issue Mechanism](references/decision-matrix.md)
- [Open-Issue Tracking Management](references/issue-tracking.md)
- [NPI Stage Pitfalls](references/stage-pitfalls.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Text]

**Output Format:** [Conversational text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No formal files, templates, reports, release approvals, or sign-off decisions are produced.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
