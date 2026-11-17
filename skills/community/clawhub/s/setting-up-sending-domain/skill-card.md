## Description:

Use when adding or verifying a Mailtrap sending domain, resolving DNS propagation issues, following registrar or DNS provider steps, completing compliance after verification, or configuring click tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailtrap](https://clawhub.ai/user/mailtrap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email operations teams use this skill to guide Mailtrap sending-domain setup, automate domain creation and DNS publication, troubleshoot propagation, and complete verification and compliance before sending from a custom domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated setup can make Mailtrap account or DNS changes.

Mitigation: Use scoped API tokens where possible and review proposed Mailtrap API actions and DNS records before publishing them.

Risk: Incorrect, incomplete, or proxied verification records can block domain verification or affect email authentication.

Mitigation: Copy the complete Mailtrap UI or API record set exactly, confirm public DNS with lookup tools before retrying verification, and keep verification records DNS-only when proxying would interfere.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mailtrap/skills/setting-up-sending-domain)
- [Mailtrap sending domain setup](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain.md)
- [Mailtrap sending domain setup for Cloudflare](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/cloudflare.md)
- [Mailtrap sending domain setup for AWS Route 53](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/aws-route-53.md)
- [Mailtrap sending domain setup for Google Cloud DNS](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/google-cloud-dns.md)
- [Mailtrap sending domain setup for Squarespace](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/squarespace.md)
- [Mailtrap sending domain setup for GoDaddy](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/godaddy.md)
- [Mailtrap sending domain setup for Namecheap](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/namecheap.md)
- [Mailtrap sending domain setup for DigitalOcean](https://docs.mailtrap.io/email-api-smtp/setup/sending-domain/digitalocean.md)
- [Cloudflare API](https://developers.cloudflare.com/api/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with inline API endpoint examples and DNS verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include account-specific API paths, DNS record checks, and provider-specific DNS setup steps; review records before publication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
