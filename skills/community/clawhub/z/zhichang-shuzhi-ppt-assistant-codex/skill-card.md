## Description:

Create evidence-based, management-ready workplace report presentations from personal knowledge bases, work records, project files, meeting notes, resumes, spreadsheets, images, drafts, and corporate PPT templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bz-ai](https://clawhub.ai/user/bz-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workplace presenters use this skill to turn verified personal, project, resume, meeting, spreadsheet, image, draft, and company template materials into structured Chinese-language report presentations for probation reviews, promotion defenses, project updates, year-end summaries, retrospectives, plans, and resource requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive personal, resume, company, spreadsheet, image, and work-record materials while preparing a report presentation.

Mitigation: Provide only materials needed for the PPT task and review visible slides, speaker notes, hidden objects, and document properties for sensitive personal or company information before sharing.

Risk: A workplace report can become misleading if unverified achievements, project outcomes, metrics, or business value are presented as facts.

Mitigation: Keep the skill's evidence workflow: separate facts, inferences, and suggestions; put unsupported claims in a data supplement list; and confirm the PPT strategy SPEC and outline before generating slides.

Risk: The skill is written for Chinese-language workplace reporting norms and may not fit other languages or organizational cultures without adaptation.

Mitigation: Review audience, tone, risk wording, and template requirements for the target organization before using the generated presentation externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bz-ai/skills/zhichang-shuzhi-ppt-assistant-codex)
- [Evidence, facts, and strategic SPEC](references/evidence-and-spec.md)
- [Quality and delivery checklist](references/quality-and-output.md)
- [Report page contracts](references/report-page-contracts.md)
- [Slide design and layout rules](references/slide-design.md)
- [Template page contract](references/template-contract.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, PPTX generation steps, speaker notes, evidence lists, quality checklists, and generated presentation files when requested by the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation of the PPT strategy SPEC and outline before slide generation; generated presentations should be visually reviewed page by page.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
