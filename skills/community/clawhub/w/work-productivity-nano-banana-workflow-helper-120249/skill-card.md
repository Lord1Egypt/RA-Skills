## Description:

Helps AI-agent users and skill authors turn Nano Banana Pro-style workflow requests into practical plans, checklists, analysis, code changes, or implementation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to structure Nano Banana Pro-style productivity requests into concrete workflows, artifacts, implementation plans, code changes, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic activation rules may route unrelated editing, image, bug-fix, or productivity requests into this workflow.

Mitigation: Review activation behavior before installing, narrow triggers to explicit Nano Banana Pro workflow requests, or invoke the skill manually.

Risk: The skill can produce code, shell commands, configuration, or workflow changes that may affect user projects if applied without review.

Mitigation: Review generated artifacts and commands, then test changes against the stated success criteria before deployment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-nano-banana-workflow-helper-120249)
- [Nano Banana Pro Demand Signal](https://clawhub.ai/skills/nano-banana-pro)
- [Nano PDF Demand Signal](https://clawhub.ai/skills/nano-pdf)
- [Looking into the Past with Nano Banana Pro](https://jacob.gold/posts/looking-into-the-past-with-nano-banana-pro/)
- [Ask HN: Recommend a Local LLM Setup](https://news.ycombinator.com/item?id=48855960)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional code blocks, checklists, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, and follow-up risks.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
