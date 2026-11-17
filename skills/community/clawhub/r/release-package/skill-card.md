## Description:

Storage Manager helps agents record, search, and update item locations in Feishu Bitable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruoruochen](https://clawhub.ai/user/ruoruochen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and personal productivity users use this skill to manage item locations through a Feishu Bitable command-line workflow, including adding items, searching stored items, and updating locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary reports apparent live Feishu credentials in the bundled test.

Mitigation: Remove and rotate any embedded Feishu credentials before running tests or deploying the skill.

Risk: The skill can upload local image paths to Feishu.

Mitigation: Only provide image paths that are intended for upload, and review local file access before execution.

Risk: Item names, locations, search terms, and uploaded images are sent to Feishu.

Mitigation: Use approved Feishu workspaces, avoid sensitive inventory data unless authorized, and configure least-privilege Feishu app scopes.

Risk: The dependency declaration allows a broad requests version range.

Mitigation: Install with pinned, reviewed dependencies in production environments.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ruoruochen/skills/release-package)
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu media upload API endpoint](https://open.feishu.cn/open-apis/drive/v1/medias/upload_all)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance, configuration]

**Output Format:** [Markdown guidance with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and Feishu app credentials configured through environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
