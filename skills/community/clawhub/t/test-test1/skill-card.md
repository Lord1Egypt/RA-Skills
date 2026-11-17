## Description:

从 test 页面获取数据并导入到 test01。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shandongwill](https://clawhub.ai/user/shandongwill)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or operations engineers use this skill to automate moving table data from a PCS page into an EBP system through an Excel export/import workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes unattended data import automation over plaintext HTTP.

Mitigation: Use only in a controlled test or low-risk environment unless endpoints are moved to HTTPS and imports require explicit approval.

Risk: Automated imports may create incorrect, duplicate, or hard-to-rollback records.

Mitigation: Validate exported row counts and content, add monitoring and logging, prove idempotency, and prepare a rollback plan before enabling scheduled runs.

Risk: Browser selectors and page structure changes can break the automation or target the wrong controls.

Mitigation: Review and test selectors against the live PCS and EBP pages before deployment and after page updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shandongwill/skills/test-test1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe Excel export/import artifacts and scheduled automation steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
