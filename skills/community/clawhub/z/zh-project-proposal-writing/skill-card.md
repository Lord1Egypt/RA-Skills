## Description:

Helps agents draft, revise, diagnose, structure, and deliver Chinese project or grant proposals, including constraint matrices, proposal sections, review-style scoring, compliance checklists, and Word .docx deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drjzhou](https://clawhub.ai/user/drjzhou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help agents prepare Chinese research, grant, science-plan, and talent-project proposal materials. It supports guide interpretation, draft generation, section revision, self-checks, red-team review, and final Word document packaging while preserving explicit human verification of facts and compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command in the artifact is unpinned, which can install a moving release if used without review.

Mitigation: Install only from a trusted source and pinned reviewed version or commit, and avoid administrator privileges for the npx install command.

Risk: Generated proposal documents may contain unverified facts, budget assumptions, ethics details, attachments, or funder-rule interpretations.

Mitigation: Treat generated .docx files as drafts and require the applicant, institution, finance, ethics/data, intellectual-property, and research-management reviewers to verify facts and current rules before submission.

Risk: Proposal materials can contain sensitive, unpublished, confidential, personal, clinical, or commercial information.

Mitigation: Provide only materials needed for the task, desensitize sensitive inputs when possible, and avoid adding unsupported or confidential claims to outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drjzhou/skills/zh-project-proposal-writing)
- [README](artifact/README.md)
- [Deliverable proposal workflow](artifact/references/deliverable_proposal_workflow.md)
- [Funder rules](artifact/references/funder_rules.md)
- [Module writing guide](artifact/references/module_writing_guide.md)
- [Templates and checklists](artifact/references/templates_checklists.md)
- [Title, abstract, and story guide](artifact/references/title_abstract_story.md)
- [Knowledge boundaries](artifact/references/knowledge_boundaries.md)
- [Writing logic consensus](artifact/references/writing_logic_consensus.md)
- [Expert wisdom synthesis](artifact/references/expert_wisdom_synthesis.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, files]

**Output Format:** [Markdown, tables, structured checklists, and Word .docx documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include placeholders such as '待补充' or '需申请人核验' when required proposal facts, current funder rules, or compliance materials are not verified.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact SKILL.md states internal version 3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
