## Description: <br>
Manage Cloudflare Workers, KV, D1, R2, and secrets using the Wrangler CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asleep123](https://clawhub.ai/user/Asleep123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to operate Cloudflare Workers and related resources with Wrangler, including deployments, secrets, KV namespaces, D1 databases, R2 buckets, queues, and live logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wrangler delete, rollback, bulk, migration, and SQL commands can affect production Cloudflare resources or data. <br>
Mitigation: Verify the Cloudflare account, environment, resource names, and production impact before execution, and back up data before destructive or database operations. <br>
Risk: Secret-management commands can expose sensitive values if plaintext secrets enter shell history, logs, or committed files. <br>
Mitigation: Use interactive or stdin-based secret entry carefully, avoid logging secret values, and keep secret files out of version control. <br>


## Reference(s): <br>
- [ClawHub Wrangler skill page](https://clawhub.ai/Asleep123/wrangler) <br>
- [Wrangler documentation](https://developers.cloudflare.com/workers/wrangler/) <br>
- [Cloudflare Workers documentation](https://developers.cloudflare.com/workers/) <br>
- [Cloudflare D1 documentation](https://developers.cloudflare.com/d1/) <br>
- [Cloudflare R2 documentation](https://developers.cloudflare.com/r2/) <br>
- [Cloudflare KV documentation](https://developers.cloudflare.com/kv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
