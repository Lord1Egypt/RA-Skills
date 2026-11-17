## Description:

Requirements Traceability and Test Case Validation skill for PRD analysis, requirement coverage, coverage gap detection, multi-repo testing, acceptance testing, traceability matrix, LLM testing, Agentic AI, and RAG testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[start-fish](https://clawhub.ai/user/start-fish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, release managers, and product teams use this skill to compare PRDs, acceptance criteria, tests, code changes, and AI workflow evidence before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect broad project materials during traceability review.

Mitigation: Provide only the PRDs, repositories, diffs, tests, configs, prompt files, model files, and release scope that are relevant to the review.

Risk: Coverage or release acceptance conclusions can be misleading when implementation, tests, or execution evidence is incomplete.

Mitigation: Require the report to mark missing evidence, open questions, and partial or blocked requirements instead of treating them as covered.

Risk: AI workflow requirements can be under-reviewed if prompts, model services, RAG inputs, observability, fallback, or safety controls are omitted.

Mitigation: Include relevant AI workflow artifacts and review fallback, observability, and safety checks before relying on the acceptance recommendation.

## Reference(s):

- [Traceability Validation Playbook](references/traceability-validation-playbook.md)
- [ClawHub skill listing](https://clawhub.ai/start-fish/skills/tracemap-ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with traceability tables, coverage summaries, defect details, evidence checklists, and open questions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include release acceptance recommendations, requirement-test-code matrices, AI workflow validation matrices, and gap classifications.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact package metadata reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
