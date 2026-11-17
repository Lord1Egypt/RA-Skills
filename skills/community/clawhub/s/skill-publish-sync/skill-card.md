## Description:

Syncs locally developed agent skills to ClawHub, Tencent SkillHub, and Lenovo Open Platform with .gitignore-aware filtering, per-platform allowlists, incremental sync records, and single-skill publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to prepare, publish, and track local skills across ClawHub, Tencent SkillHub, and Lenovo Open Platform. It supports single-skill and batch-oriented workflows with platform-specific allowlists and sync status records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run mutable remote tooling and credentialed publishing workflows.

Mitigation: Pin and verify CLI versions where possible, run uploads from a constrained working copy, and confirm account identity before publishing.

Risk: Installer and upload flows may rely on curl-piped shell installers or unpinned npx execution.

Mitigation: Avoid curl-piped installers and unpinned npx commands where practical; otherwise review the fetched tooling and record the version used.

Risk: Batch Lenovo uploads can submit generated packages with weak confirmation and input handling.

Mitigation: Inspect the prepared /tmp publish directory before pushing and avoid batch uploads for untrusted skill metadata until validation and manual confirmation are added.

Risk: Public publishing can expose local configuration, credentials, or customer data if source directories are packaged directly.

Mitigation: Use the prepare-publish workflow, keep real allowlists and sync records out of committed artifacts, and verify that credentials and private data are excluded before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/skill-publish-sync)
- [Project homepage from clawdis metadata](https://github.com/cat-xierluo/legal-skills)
- [ClawHub CLI documentation](https://docs.openclaw.ai/clawhub/cli)
- [ClawHub Skill Format documentation](https://docs.openclaw.ai/clawhub/skill-format)
- [Tencent SkillHub publish tutorial](https://skillhub.cn/tutorials#publish-via-cli)
- [Lenovo Open Platform](https://open.lenovomm.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific publish status, error messages, and sync-record guidance.]

## Skill Version(s):

1.7.2 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
