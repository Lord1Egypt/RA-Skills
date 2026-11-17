## Description:

OpenClaw Skill Publisher helps agents publish, update, generalize, and distribute OpenClaw skill packages through ClawHub and Gitee.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruyuechina](https://clawhub.ai/user/ruyuechina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to prepare, publish, update, and distribute OpenClaw skills across ClawHub and Gitee, including token-based publishing workflows and release-version management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing commands can make repositories or skill releases public unintentionally.

Mitigation: Verify the target account, repository visibility, slug, version, and changelog before running publish or repository-creation commands.

Risk: Token-based login and API examples can expose credentials if tokens are pasted into shared transcripts, shell history, or published skill content.

Mitigation: Use a controlled publishing environment, keep tokens out of shared logs and source files, and scan all content for secrets before upload.

Risk: Global package installs and string-built shell commands can execute unexpected tooling or malformed commands.

Mitigation: Prefer pinned or local tool installs and structured command invocation, and review each generated command before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruyuechina/skills/ruyue-skill-publisher)
- [Publisher profile](https://clawhub.ai/user/ruyuechina)
- [ClawHub](https://clawhub.ai)
- [Gitee personal access tokens](https://gitee.com/profile/personal_access_tokens)
- [Gitee OpenClaw skills repository](https://gitee.com/ruyueteam/openclaw-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command templates for ClawHub and Gitee publishing; users must substitute local paths, slugs, versions, repository names, and tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
