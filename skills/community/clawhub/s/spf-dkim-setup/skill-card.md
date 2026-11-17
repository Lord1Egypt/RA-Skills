## Description:

Manage Cloudflare DNS records for SPF, DKIM, DMARC, domain verification, and related email authentication setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masasdani](https://clawhub.ai/user/masasdani)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect and change Cloudflare-hosted DNS records, especially for SPF, DKIM, DMARC, and sending-domain setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly create, update, overwrite, import, batch-change, or delete live Cloudflare DNS records.

Mitigation: Use a least-privilege Cloudflare token scoped to the specific zone, back up existing records, and require review of exact record IDs, names, types, old values, new values, and impact before applying changes.

Risk: Incorrect email authentication records can break domain verification or email delivery.

Mitigation: Preview proposed SPF, DKIM, DMARC, MX, and CNAME records against provider requirements before writing them, and keep email-related CNAME records unproxied when required.

## Reference(s):

- [Cloudflare DNS API Reference](references/api.md)
- [Cloudflare API documentation](https://developers.cloudflare.com/api/)
- [Cloudflare API tokens](https://dash.cloudflare.com/profile/api-tokens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl commands and JSON DNS record examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live Cloudflare DNS API operations requiring a Cloudflare API token and zone ID.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
