## Description:

Scaffolds and guides creation of a WeChat Mini Program backed by WeChat CloudBase using REST-style cloud functions, idempotent user and collection setup, real-time stats, subscription messages, and lifecycle pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincent-chao-lang](https://clawhub.ai/user/vincent-chao-lang)

### License/Terms of Use:

MIT

## Use Case:

Developers building a WeChat Mini Program MVP use this skill to create and adapt a CloudBase scaffold with login, database access, API routing, seed data, and optional subscription-message reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Included backend templates have authorization and quota-control weaknesses if deployed unchanged.

Mitigation: Add authorization for private group joins, validate or bound subscription grant recording, add rate limits, and create unique indexes before deployment.

Risk: Dependency versions and lockfiles may not be pinned for production use.

Mitigation: Pin dependencies, commit lockfiles, and review dependency updates before releasing an app from the scaffold.

Risk: Locale and privacy disclosures may not match the final Mini Program audience and data handling.

Mitigation: Adjust user-facing locale, category, subscription-message, login, and privacy disclosures before submission.

## Reference(s):

- [Architecture and Data Model](references/architecture.md)
- [Lifecycle Pitfalls](references/pitfalls.md)
- [ClawHub Skill Page](https://clawhub.ai/vincent-chao-lang/skills/wechat-miniprogram-cloudbase-scaffold)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate WeChat Mini Program and CloudBase scaffold files from bundled templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
