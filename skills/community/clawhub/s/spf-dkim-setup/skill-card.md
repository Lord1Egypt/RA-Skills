## Description: <br>
Manage Cloudflare DNS records for SPF, DKIM, DMARC, domain verification, and related DNS changes through the Cloudflare API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[masasdani](https://clawhub.ai/user/masasdani) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and modify Cloudflare-hosted DNS records, especially when setting up email authentication and sending-domain verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real DNS changes on a Cloudflare-hosted domain, including SPF, DKIM, DMARC, MX, CNAME, import, batch, update, and delete operations. <br>
Mitigation: Use a least-privilege Cloudflare token scoped to the intended zone and review the record name, type, old value, and new value before applying changes. <br>
Risk: Incorrect DNS changes can break websites, email delivery, domain verification, or email authentication. <br>
Mitigation: Confirm email-related CNAME records are not proxied, merge SPF directives into existing SPF records when needed, and verify DNS records after changes. <br>


## Reference(s): <br>
- [Cloudflare DNS API Reference](references/api.md) <br>
- [Cloudflare API Documentation](https://developers.cloudflare.com/api/) <br>
- [ClawHub Skill Page](https://clawhub.ai/masasdani/spf-dkim-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Cloudflare DNS API requests and record values for user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
