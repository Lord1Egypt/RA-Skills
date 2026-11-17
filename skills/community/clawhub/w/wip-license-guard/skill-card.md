## Description:

Wip License Guard enforces repository license compliance by checking copyright headers, dual-license blocks, LICENSE files, CLA files, and README license sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to audit repository license requirements before release and to generate or repair license files, CLA files, and README license sections when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool can create or rewrite legal/license files and README sections across multiple repositories.

Mitigation: Run audit or --dry-run first, avoid broad parent directories with --fix, and review generated LICENSE, CLA.md, .license-guard.json, and README diffs before committing.

Risk: The tool applies WIP Computer-style license governance, which may not match every repository's intended license policy.

Mitigation: Install and run it only for repositories that intentionally use this governance model, and confirm configuration values before applying fixes.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/parkertoddbrooks/skills/wip-license-guard)
- [AI DevOps Toolbox repository](https://github.com/wipcomputer/wip-ai-devops-toolbox)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown and CLI-oriented text with optional generated configuration and license files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write .license-guard.json, LICENSE, CLA.md, and README license sections when init or fix modes are used.]

## Skill Version(s):

1.9.72 (source: server release metadata; artifact package.json reports 1.9.68)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
