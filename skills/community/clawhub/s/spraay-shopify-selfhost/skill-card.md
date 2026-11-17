## Description:

Deploy and self-host the open-source Spraay Shopify app (batch USDC payouts on Base) for a merchant's store. Use this skill whenever a user wants to install, deploy, set up, self-host, or troubleshoot the Spraay Shopify app (github.com/plagtech/spraay-shopify) - including creating the custom app in the Shopify Dev Dashboard, deploying to Railway, configuring environment variables, setting up the Supabase/Postgres database, fixing 502 errors or OAuth redirect issues, or connecting a custom domain. Also use when a Shopify merchant asks how to add crypto payouts, USDC payments, or affiliate crypto payments to their store admin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Shopify merchants use this skill to deploy and troubleshoot a self-hosted Spraay Shopify app for batch USDC payouts. It guides setup of the Shopify app, hosting, database, credentials, and a small test payout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployed application receives Shopify and database credentials, so deploying an unreviewed revision could expose them.

Mitigation: Deploy from the documented pinned commit or a newer release you have reviewed; use a restricted database role and rotate credentials after an unreviewed deployment.

Risk: The documented reset and force-push sequence can overwrite existing branch work.

Mitigation: Use it only on a fresh fork; preserve existing work or deploy from a separate branch.

Risk: A payout can send funds to the listed recipients and incurs a protocol fee.

Mitigation: Check recipients, amounts, fees, and wallet prompts, then confirm a small test payout before processing real payroll.

## Reference(s):

- [Spraay Shopify application repository (referenced by the skill)](https://github.com/plagtech/spraay-shopify)
- [Spraay protocol documentation](https://docs.spraay.app)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
