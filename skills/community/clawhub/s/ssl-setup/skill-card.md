## Description: <br>
Configure Nginx as a reverse proxy with SSL/TLS via Let's Encrypt, security headers, HTTP/2, and gzip compression for any application on any VPS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llcsamih](https://clawhub.ai/user/llcsamih) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure production HTTPS for VPS-hosted applications by setting up Nginx reverse proxying, Let's Encrypt certificates, security headers, redirects, and renewal checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides production server changes that can disrupt live sites if commands or generated Nginx configuration are applied without review. <br>
Mitigation: Review each command before execution, back up existing Nginx site files, run nginx -t before reloads, and stop to diagnose failures instead of continuing. <br>
Risk: The hardened configuration includes an HSTS preload header that can make a domain and its subdomains HTTPS-only long term. <br>
Mitigation: Do not enable HSTS preload unless the operator has explicitly decided that the domain and all subdomains should remain HTTPS-only long term. <br>
Risk: Wildcard certificate automation can require DNS provider API tokens, and exposed tokens can permit unauthorized DNS changes. <br>
Mitigation: Use a dedicated least-privilege DNS token scoped only to the needed zone, keep it out of shared transcripts and logs, store it with restrictive file permissions, and rotate it if exposed. <br>
Risk: Certificate issuance can fail or hit rate limits when DNS is not pointed at the target server before Certbot runs. <br>
Mitigation: Verify DNS A records against the server public IP before running Certbot and stop until DNS is corrected when records do not match. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/llcsamih/ssl-setup) <br>
- [Publisher profile](https://clawhub.ai/user/llcsamih) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash and Nginx configuration code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces step-by-step server administration guidance for DNS checks, Nginx configuration, Certbot certificate issuance, renewal setup, and verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
