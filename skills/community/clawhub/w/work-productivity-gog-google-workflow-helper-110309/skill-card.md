## Description:

Helps agent users, skill authors, maintainers, and teams create practical Gog-style Google Workspace workflows, checklists, automation outlines, code changes, analysis, and verification notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External agent users, skill authors, maintainers, and teams use this skill to turn Gog-style Google Workspace productivity requests into concrete plans, reusable workflows, checklists, automation outlines, code changes, analysis, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses broad implicit invocation keywords and may appear during unrelated Google, CLI, or productivity requests.

Mitigation: Prefer explicit invocation or narrow the trigger keywords before deployment.

Risk: Documentation-only workflow guidance can still produce incorrect plans, code suggestions, or operational advice.

Mitigation: Review generated outputs against the stated success criteria and scan any proposed code or commands before use.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/work-productivity-gog-google-workflow-helper-110309)
- [Gog skill demand signal](https://clawhub.ai/skills/gog)
- [Google Workspace CLI discussion signal](https://news.ycombinator.com/item?id=48664969)
- [LiteLLM issue summary signal](https://github.com/arielb1-sun-security/copilot-studio-test/issues/2209)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, remaining risks, and next steps when useful.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
