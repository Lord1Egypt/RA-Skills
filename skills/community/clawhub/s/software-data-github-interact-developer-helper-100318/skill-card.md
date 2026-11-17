## Description:

Helps agent users, skill authors, maintainers, and teams plan and execute GitHub-style development workflows for bug fixes, setup hardening, reliability improvements, and adjacent skill creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI-agent users, skill authors, maintainers, and teams use this skill to turn GitHub-style development requests into practical workflows, artifacts, checklists, analysis, code changes, shell commands, configuration guidance, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may trigger on generic GitHub, CLI, API, or issue-related prompts and lead an agent toward repository edits or remote GitHub actions without enough user intent.

Mitigation: Confirm the target repository, requested outcome, allowed file edits, and any permitted remote GitHub interaction before taking downstream actions.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/software-data-github-interact-developer-helper-100318)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include assumptions, limits, verification notes, and remaining risks when relevant.]

## Skill Version(s):

0.20260729.110214 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
