## Description:

This skill helps operators build and run a local WeChat Official Account publishing workflow covering environment setup, source gathering, article drafting, image preparation, draft submission, optional final publication, scheduling, archiving, and security boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[16miku](https://clawhub.ai/user/16miku)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and developers use this skill to reproduce a local workflow for preparing WeChat Official Account articles, publishing them to draft, optionally submitting them for publication, and archiving results. It is aimed at reusable handoff and scheduled operations while keeping secrets outside the package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback publishing script can submit live content automatically.

Mitigation: Default production runs to draft-only and require an explicit confirmation or mode check before formal publication.

Risk: Crafted Markdown image paths may cause unintended local files to be uploaded.

Mitigation: Constrain image paths to the article directory, allowlist expected image filenames and extensions, and validate real image format before upload.

Risk: Publishing logs can expose sensitive token prefixes or operational details.

Mitigation: Remove token-prefix logging and store logs in protected, account-isolated directories.

Risk: Scheduled jobs can mix credentials, logs, or outputs across accounts.

Mitigation: Run automation under a least-privilege account with one isolated working directory, environment file, log, and result archive per WeChat account.

Risk: External dependencies and local scripts may change behavior over time.

Mitigation: Review and pin external dependencies before use, and inspect the publishing script before installation or scheduled execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/16miku/skills/wechat-auto-publishing)
- [README](artifact/README.md)
- [Runbook](artifact/runbook.md)
- [Environment and Configuration](artifact/references/environment-and-config.md)
- [Publishing](artifact/references/publishing.md)
- [Image Strategy](artifact/references/image-strategy.md)
- [Scheduling and Alerting](artifact/references/scheduling-and-alerting.md)
- [Security Boundary](artifact/references/security-boundary.md)
- [baoyu-skills dependency repository](https://github.com/jimliu/baoyu-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, configuration templates, JavaScript publishing script, cron examples, and JSON result artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workflow instructions and templates; successful publishing runs may produce draft media IDs, publish IDs, article URLs, logs, and archived result JSON.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
