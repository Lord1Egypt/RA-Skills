## Description:

Helps AI-agent users, skill authors, maintainers, and teams create, improve, and validate Proactive Agent-style productivity workflows using concise plans, checklists, implementation support, and verification notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn Proactive Agent-style productivity requests into practical workflows, checklists, implementation changes, and validation notes. It is suited for debugging, hardening setup and safety, improving reliability, or creating adjacent workflow skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the workflow helper to influence unrelated productivity-style requests.

Mitigation: Prefer explicit invocation or tighter trigger wording when deploying the skill in environments where unrelated tasks should not be shaped by this workflow.

Risk: The skill can produce plans, code support, checklists, and decision guidance that may be incomplete or mismatched to the user's context.

Mitigation: Review outputs against the stated success criteria and verify any code, configuration, or safety changes before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-proactive-agent-workflow-helper-100317)
- [Requirement plan](artifact/references/requirement-plan.md)
- [Proactive Agent demand signal](https://clawhub.ai/skills/proactive-agent)
- [Self-Improving + Proactive Agent demand signal](https://clawhub.ai/skills/self-improving)
- [ontology demand signal](https://clawhub.ai/skills/ontology)
- [GitHub issue demand signal](https://github.com/szmidtpiotr/ai-gm/issues/1541)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise prose, checklists, code blocks, shell commands, and verification notes as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, remaining risks, and follow-up work when helpful.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
