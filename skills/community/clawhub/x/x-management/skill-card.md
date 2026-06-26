## Description: <br>
Draft-first X/Twitter account management workflow for OpenClaw that helps agents read account context, draft posts, replies, quote tweets, and threads, and keep write actions behind explicit approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[princebansal](https://clawhub.ai/user/princebansal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to manage a personal X/Twitter account by gathering context, drafting social posts, and publishing only after explicit user approval through the paired X plugin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved drafts can be published publicly from the connected X/Twitter account. <br>
Mitigation: Review the exact draft text and require explicit approval before publishing. <br>
Risk: Multi-account sessions can publish from the wrong account if the accountId is ambiguous or omitted. <br>
Mitigation: Use the exact accountId for draft, approval, and publish steps, and verify non-default accounts with x_account_me before approval. <br>
Risk: The workflow requires OAuth account access through the paired plugin. <br>
Mitigation: Install only when intending to connect an X/Twitter account and reconnect if required read scopes are missing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Markdown and plain text workflow guidance with social post drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-first workflow; public posting depends on explicit approval through the paired X plugin.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata and README publish example) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
