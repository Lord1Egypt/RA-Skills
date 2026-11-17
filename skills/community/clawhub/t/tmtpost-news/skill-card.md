## Description:

获取7x24 财经科技新闻资讯和深度报道，聚焦财经、科技、商业、创投等领域的资讯报道和深度分析。支持热门文章、最新文章、最新快讯查询。当用户需要搜索财经、科技、商业、创投等领域热点资讯和深度报道时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[taimeiti](https://clawhub.ai/user/taimeiti)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve TMTPost financial, technology, business, startup, and venture-capital news through the bundled CLI workflow. It supports hot articles, latest articles, and brief news when the user asks for current TMTPost coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and update flow can download, install, update, and run local native executables, and the security summary reports weak source verification.

Mitigation: Review the skill before installing, use it only when the TMTPost CLI distribution is trusted, and confirm downloaded binaries and checksum sources before execution.

Risk: The security guidance flags the Windows installer path because of a placeholder download URL and remote execution flow.

Mitigation: Avoid the Windows installer path until the placeholder URL and remote execution flow are fixed.

Risk: The skill requires an API key that should be treated as a secret.

Mitigation: Enter API keys only through the documented CLI command, do not expose them in prompts or logs, and clear or rotate the key if it may have been disclosed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/taimeiti/skills/tmtpost-news)
- [API Key Setup Guide](references/env-setup-guide.md)
- [Manual Update Guide](references/update-guide.md)
- [TMTPost API Key Page](https://www.tmtpost.com/exchange/appkey/skills)
- [TMTPost CLI Download Base](https://pack.tmtpost.net/tmtpost-news)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown news summaries with links and inline shell commands for setup or troubleshooting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [News output is grouped by requested article type when multiple categories are requested; setup output may include JSON status from helper scripts.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
