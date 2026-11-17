## Description:

Manage Volcengine's AI-native BaaS platform, Supabase edition/AIDAP, by helping agents inspect, create, configure, and troubleshoot workspaces, branches, computes, SQL, Auth, Realtime, Edge Functions, Storage, Pages, API keys, and connection details through byted-supabase-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to manage Volcengine Supabase/AIDAP backend resources and database workflows from an agent session. It supports operational inspection, provisioning, schema changes, security checks, app integration, and deployment support for Volcengine-backed applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-privilege dataplane code can send service-role credentials to arbitrary or plaintext endpoints.

Mitigation: Install only in trusted environments, verify endpoints before use, require HTTPS, avoid unverified SUPABASE_URL values, and prefer the official CLI login or profile flow.

Risk: Workspace stop and delete operations can cause service outage or irreversible resource loss.

Mitigation: Require explicit user confirmation, restate the operational impact, and verify the target workspace or branch identifier before executing destructive commands.

Risk: External packages or demo archives may introduce supply-chain exposure.

Mitigation: Pin or review external packages and inspect demo archives before running or deploying them.

## Reference(s):

- [Volcengine Homepage](https://www.volcengine.com/)
- [Volcengine AIDAP Feature Changelog](https://www.volcengine.com/docs/87275/2105759?lang=zh)
- [Volcengine AIDAP API List](https://www.volcengine.com/docs/87275/2105871?lang=zh)
- [Volcengine Database Documentation](https://www.volcengine.com/docs/87275/2385100?lang=zh)
- [Volcengine Authentication Documentation](https://www.volcengine.com/docs/87275/2277072?lang=zh)
- [Volcengine Realtime Documentation](https://www.volcengine.com/docs/87275/2277058?lang=zh)
- [Volcengine Edge Function Documentation](https://www.volcengine.com/docs/87275/2288709?lang=zh)
- [Volcengine Storage Documentation](https://www.volcengine.com/docs/87275/2277057?lang=zh)
- [Command Reference](references/tool-reference.md)
- [Security Guide](references/security-guide.md)
- [RLS Guide](references/rls-guide.md)
- [Workflows](references/workflows.md)
- [Application Integration Guide](references/app-integration-guide.md)
- [IAM Permission Guide](references/iam-permission-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, SQL, configuration snippets, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute or propose byted-supabase-cli commands and may write supporting files when an agent has the required tool permissions.]

## Skill Version(s):

2.3.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
