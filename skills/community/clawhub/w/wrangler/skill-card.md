## Description:

Manage Cloudflare Workers, KV, D1, R2, and secrets using the Wrangler CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asleep123](https://clawhub.ai/user/asleep123)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate Cloudflare Workers and related services with Wrangler, including deployments, secrets, KV namespaces, D1 databases, R2 buckets, queues, logs, and configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wrangler commands can change or delete live Cloudflare resources.

Mitigation: Verify the active Cloudflare account and target environment before running deployment, rollback, delete, or data mutation commands.

Risk: D1, R2, and KV operations may affect important application data.

Mitigation: Back up important D1, R2, and KV data before destructive operations.

Risk: Secret files and secret values may expose sensitive material.

Mitigation: Handle secret files as sensitive material and avoid exposing secret values in logs, prompts, or shared files.

Risk: Unexpected Wrangler versions may change CLI behavior.

Mitigation: Prefer a pinned, project-local Wrangler dependency for repeatable command behavior.

## Reference(s):

- [Wrangler Docs](https://developers.cloudflare.com/workers/wrangler/)
- [Workers Docs](https://developers.cloudflare.com/workers/)
- [D1 Docs](https://developers.cloudflare.com/d1/)
- [R2 Docs](https://developers.cloudflare.com/r2/)
- [KV Docs](https://developers.cloudflare.com/kv/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JSONC, and TOML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
