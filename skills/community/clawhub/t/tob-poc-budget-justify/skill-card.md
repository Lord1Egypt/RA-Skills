## Description:

Generates a Chinese-language ToB POC budget justification report from customer, industry, POC goal, budget, and decision-maker inputs, covering scope, resource estimates, success criteria, and budget rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[william202404](https://clawhub.ai/user/william202404)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and pre-sales teams use this skill to structure POC budget discussions when a customer has unclear budget, scope, timeline, or success criteria. It produces a report that frames POC goals, bounded scope, estimated effort, acceptance criteria, and budget justification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown reports generated from untrusted inputs may contain unsafe raw HTML, remote images, or links when rendered in a viewer.

Mitigation: Render output with raw HTML disabled and consider blocking remote images or links in Markdown viewers, consistent with the server security guidance.

Risk: POC budget and resource estimates may be treated as definitive commercial advice even though the artifact describes them as reference estimates.

Mitigation: Review the generated report against the specific project context, customer constraints, and approval process before using it in commercial discussions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/william202404/skills/tob-poc-budget-justify)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language CLI output; users should review project-specific estimates and assumptions before sharing externally.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
