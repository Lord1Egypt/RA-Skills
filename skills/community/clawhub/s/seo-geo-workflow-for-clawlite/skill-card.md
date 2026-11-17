## Description:

OpenClaw SEO-GEO Workflow guides agents through receipt-driven daily SEO and GEO content operations for ClawLite and OpenClaw marketing, including topic discovery, article production, publish QA, live deployment checks, and patrol diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run or inspect a daily SEO/GEO publishing workflow, verify receipt evidence before making publishing claims, and diagnose blockers across content production, deployment, analytics, indexing, ranking, and patrol checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow delegates important actions to local scripts and environment-specific deployment commands that were not audited in the release evidence.

Mitigation: Install only in a trusted OpenClaw workspace and verify scripts, dependencies, credentials, and deployment targets before running live deploy or main-site write paths.

Risk: The skill can trigger production-impacting publish, deploy, diagnostic, log, and messaging-session access.

Mitigation: Use skip-live-deploy modes by default, require explicit deploy evidence for production claims, and limit log or messaging-session inspection to sanitized data needed for the task.

Risk: Local staging, source publish, or build success can be mistaken for live publication.

Mitigation: Report live publication only after deploy evidence and live QA receipts are present; otherwise label results as staged, skipped, needs data, or pass with warnings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/seo-geo-workflow-for-clawlite)
- [Publisher profile](https://clawhub.ai/user/x-rayluan)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, status labels, receipt paths, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Receipt-first workflow guidance; live publishing claims require deploy evidence and live QA.]

## Skill Version(s):

0.4.3 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
