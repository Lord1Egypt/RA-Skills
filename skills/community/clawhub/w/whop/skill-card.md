## Description: <br>
Run and grow a Whop business with better offers, checkout flows, promo strategy, affiliates, ads, tracking, analytics, support operations, and advanced API workflows when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Whop operators, marketers, support teams, and developers use this skill to improve offers, checkout paths, attribution, affiliate programs, analytics, member operations, and advanced API or webhook workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Whop API keys, webhook secrets, payment details, customer data, or other sensitive business information could be saved into local notes. <br>
Mitigation: Keep secret values and customer or payment details out of ~/whop/; store credentials in environment variables or a normal secret manager and save only non-sensitive metadata. <br>
Risk: Advanced API, webhook, payment, or embedded app changes can affect production memberships, payments, or customer operations. <br>
Mitigation: Prefer sandbox credentials and separate sandbox notes for technical tests, verify webhook deliveries before side effects, and keep sandbox and production assets distinct. <br>
Risk: Using the wrong Whop authentication surface or missing permissions can produce incorrect access decisions or failed automation. <br>
Mitigation: Choose the narrowest valid credential for the task, keep Whop IDs and environments explicit, and re-check required permissions and approvals before production use. <br>


## Reference(s): <br>
- [Whop Skill Release](https://clawhub.ai/ivangdavila/whop) <br>
- [Whop API](https://api.whop.com/api/v1) <br>
- [Whop Documentation](https://docs.whop.com/*) <br>
- [Whop Sandbox](https://sandbox.whop.com/*) <br>
- [Whop App Install Flow](https://whop.com/apps/*/install) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local notes under ~/whop/ and optional Whop environment variables for advanced API, webhook, and embedded app workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
