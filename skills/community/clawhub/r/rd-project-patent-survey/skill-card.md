## Description:

研发立项调研、项目立项专利、研发前专利调研。当用户说「这个研发项目值不值得做」「立项前看看别人有哪些方案」「帮研发团队列技术路线和验证问题」时使用，交付立项专利参考表，不作查新或侵权结论。 Survey patents for an R&D project by mapping requirements to existing technical approaches, evidence and validation questions in a project decision table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

R&D teams use the skill before project approval to compare existing patent approaches against project goals and constraints, then identify evidence gaps and validation questions. Its patent reference table supports planning and does not provide novelty, infringement, or other legal conclusions.

### Deployment Geography for Use:

Global; the documented patent coverage includes China, the United States, Europe, Japan, South Korea, and WIPO.

## Known Risks and Mitigations:

Risk: Conflicting assessment instructions can lead to inconsistent or misleading guidance.

Mitigation: Review and correct the conflicting assessment instructions before relying on the skill's outputs.

Risk: Saved trial credentials may be weakly protected on shared computers.

Mitigation: Before saving a trial key on a shared computer, ensure private file permissions are enforced at creation and handle permission failures safely.

Risk: Patent search results could be mistaken for a patentability or infringement conclusion.

Mitigation: Use approved, non-confidential search terms, set a spending limit, and obtain independent review for patentability or infringement decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ip930/skills/rd-project-patent-survey)
- [PatentMax](https://ip930.com)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Search workflow](artifact/references/search-workflow.md)
- [Query syntax](artifact/references/query-syntax.md)
- [PatentMax API reference](artifact/references/api-reference.md)
- [Key setup and storage guidance](artifact/references/key-setup.md)

## Skill Output:

**Output Type(s):** [Analysis, CSV, Markdown, Guidance]

**Output Format:** [UTF-8 with BOM CSV reference table, candidate list, and concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses returned patent records as references; patent claims are not independent validation, and the output is not a legal opinion.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
