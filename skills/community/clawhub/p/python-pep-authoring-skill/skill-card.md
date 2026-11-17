## Description:

Draft, review, edit, or prepare Python Enhancement Proposals using the official python/peps repository rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoqyu](https://clawhub.ai/user/zhaoqyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to draft, review, revise, and prepare Python Enhancement Proposals in line with the official python/peps repository workflow, metadata, formatting, and validation expectations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact names bundled reference files that are not present, which can leave detailed PEP process or formatting claims under-sourced.

Mitigation: Use a live python/peps checkout or the official PEP links when making detailed claims, and prefer local repository files when available.

Risk: Repository validation commands may run in untrusted checkouts.

Mitigation: Review commands before execution and run validation only in a trusted or disposable checkout.

## Reference(s):

- [Server-resolved source repository](https://github.com/zhaoqyu/python-pep-authoring-skill)
- [Official python/peps repository](https://github.com/python/peps)
- [PEP index](https://peps.python.org/)
- [PEP 1](https://peps.python.org/pep-0001/)
- [PEP 12](https://peps.python.org/pep-0012/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown responses with review findings, draft or revision text, and validation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file and line references for PEP reviews and commands to run in a local python/peps checkout.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
