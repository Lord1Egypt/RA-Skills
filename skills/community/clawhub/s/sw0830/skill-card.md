## Description:

Uploads PDD promotion spreadsheets and optional operation logs, then uses a paid API over the Alipay A2M HTTP 402 flow to return promotion diagnostics and rendered reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw0830](https://clawhub.ai/user/sw0830)

### License/Terms of Use:

MIT-0

## Use Case:

External PDD advertisers and campaign operators use this skill to submit single-product daily promotion exports, complete the paid Alipay flow, and receive diagnostic reports. Agents use it to collect required files and parameters, invoke the shell workflow, and render the paid service response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business promotion spreadsheets and optional operation logs are uploaded to an external paid service.

Mitigation: Use the skill only for explicit PDD promotion-analysis requests and only when the user accepts sending those files to aituiguangbao.com.

Risk: The skill stores a persistent API key and generated reports under ~/.pdd_skill.

Mitigation: Avoid shared machines unless filesystem permissions are restricted to the current user, and reset the stored key when access should be revoked.

Risk: Reports are rendered locally from server-provided content.

Mitigation: Review generated reports before opening or sharing them, especially HTML reports from untrusted or unexpected service responses.

Risk: Payment-Proof handling outside the payment tool flow could expose or invalidate paid access.

Mitigation: Follow the generated Alipay payment commands exactly and do not manually pass Payment-Proof values outside the payment tool flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sw0830/skills/sw0830)
- [Publisher profile](https://clawhub.ai/user/sw0830)
- [Paid analysis service](https://aituiguangbao.com)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, guidance]

**Output Format:** [Markdown/text guidance with shell commands; rendered reports as HTML, Markdown, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads .xls, .xlsx, or .csv promotion tables and optional operation logs to a paid external service; local credentials and reports are stored under ~/.pdd_skill.]

## Skill Version(s):

3.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
