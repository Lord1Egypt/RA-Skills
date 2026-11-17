## Description:

Audit whether the Task Execution Signal Protocol is still being followed, with low-token, exception-first checks for version drift, queue hygiene, numeric stage format, and core execution anchors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wewehg](https://clawhub.ai/user/wewehg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and governance reviewers use this skill to check whether TESP execution standards remain intact across protocol files, registry anchors, version markers, queue hygiene, archive separation, and numeric progress notation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording could invoke the skill for adjacent governance requests where TESP review is not intended.

Mitigation: Review and narrow the trigger wording if invocation should require explicit TESP requests.

Risk: A lightweight audit may miss issues that require deeper semantic review.

Mitigation: Use exception-first checks for routine governance and escalate when semantic conflicts or redesign decisions appear.

## Reference(s):

- [TESP Audit Reference](references/audit-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Short exception-first report, usually Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May stay silent in the normal case and point to a local report path when drift is detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
