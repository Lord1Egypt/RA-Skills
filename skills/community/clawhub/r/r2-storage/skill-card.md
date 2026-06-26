## Description: <br>
Cloudflare R2 Storage management - setup, upload, download, sync via rclone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junwatu](https://clawhub.ai/user/junwatu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Cloudflare R2 access with rclone and perform upload, download, list, sync, and delete operations from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reveal Cloudflare R2 access keys through credential-display commands. <br>
Mitigation: Do not run credential-display commands in shared or logged environments, and redact credential output before storing or sharing logs. <br>
Risk: The setup flow can install rclone by piping a remote script to sudo. <br>
Mitigation: Verify the rclone installer independently or install rclone from a trusted package source before running setup. <br>
Risk: Delete, purge, and sync --delete operations can remove cloud data with limited safeguards. <br>
Mitigation: Use least-privilege R2 tokens, review target paths and buckets before execution, and reserve purge or sync --delete for explicitly confirmed maintenance tasks. <br>


## Reference(s): <br>
- [R2 Storage on ClawHub](https://clawhub.ai/junwatu/r2-storage) <br>
- [Cloudflare dashboard](https://dash.cloudflare.com) <br>
- [rclone installer](https://rclone.org/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires rclone and R2_CONFIG credentials; commands operate on Cloudflare R2 buckets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
