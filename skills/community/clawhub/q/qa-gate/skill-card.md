## Description:

Final quality validation gate for any artifact before human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[corbin-breton](https://clawhub.ai/user/corbin-breton)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content authors use this skill as a final QA gate before human review or publication of documents, PRDs, skills, blog posts, and code artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes itself as read-only but also directs agents to fix critical and major issues when a gate fails.

Mitigation: Require explicit user approval before modifying reviewed artifacts; otherwise limit use to reporting findings.

Risk: The skill may create QA report files in the workspace or evidence directory.

Mitigation: Run it in an appropriate workspace and review generated reports for sensitive content before sharing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown QA gate report with a PASS, PASS WITH FIXES, or FAIL verdict and severity findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a qa-gate/YYYY-MM-DD-<artifact-slug>.md report relative to the workspace or evidence directory.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
