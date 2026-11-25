## Description:

Manage Volcengine's Supabase-compatible AIDAP platform through its byted-supabase-cli, including workspaces, database operations, authentication, storage, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use the skill to create, inspect, and manage Volcengine Supabase or AIDAP resources and to get operational guidance for those services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports serious credential transport and authorization weaknesses.

Mitigation: Follow the security guidance and avoid installation until these issues are addressed.

Risk: The security review reports weaknesses in the database-operation guidance.

Mitigation: Review and resolve the database-operation guidance before using the skill.

Risk: Two referenced guides were only partially inspected, so the scan does not establish that the remaining material is safe.

Mitigation: Complete review of the partially inspected material before installation.

## Reference(s):

- [Volcengine Database documentation](https://www.volcengine.com/docs/87275/2385100?lang=zh)
- [Volcengine Authentication documentation](https://www.volcengine.com/docs/87275/2277072?lang=zh)
- [Volcengine Realtime documentation](https://www.volcengine.com/docs/87275/2277058?lang=zh)
- [Volcengine Edge Function documentation](https://www.volcengine.com/docs/87275/2288709?lang=zh)
- [Volcengine release notes](https://www.volcengine.com/docs/87275/2105759?lang=zh)
- [Security guide](artifact/references/security-guide.md)
- [Row level security guide](artifact/references/rls-guide.md)
- [CLI tool reference](artifact/references/tool-reference.md)
- [Application integration guide](artifact/references/app-integration-guide.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, SQL, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with command, SQL, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational results, configuration guidance, and generated TypeScript types.]

## Skill Version(s):

2.3.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
