## Description:

Tra cuu thong tin doanh nghiep tu masothue.com, ghi du lieu vao Google Sheet Hop dong, va tao hoac cap nhat ban ghi khach hang va co hoi trong Odoo CRM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minhduongqngai](https://clawhub.ai/user/minhduongqngai)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and operators use this skill to turn a Vietnamese tax code or masothue.com link into a contract row in Google Sheets and matching Odoo CRM customer and opportunity records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may update a Google Sheet and automatically create or update Odoo CRM records.

Mitigation: Use least-privilege Google and Odoo accounts and review the intended sheet and CRM behavior before installing or running the skill.

Risk: The security review reports persistent Odoo CRM writes with limited disclosure and no confirmation step.

Mitigation: Prefer a version that previews Odoo writes and asks permission before creating or updating CRM records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minhduongqngai/skills/taohopdong)
- [masothue.com](https://masothue.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update Google Sheets and create or update persistent Odoo CRM records when executed by an agent.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
