## Description:

一个支持通过命令行查询菜谱和报菜名的菜谱查询工具，适用于烹饪爱好者和开发者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Cooking enthusiasts and developers use this skill to retrieve available dish names and request recipe details through a command-line agent workflow backed by the XiaoBenYang API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an API key and persists it in a local .env file.

Mitigation: Use a scoped key, keep .env out of source control and shared archives, and rotate the key if the workspace is exposed.

Risk: Environment variables or .env contents can affect the API endpoint and credential used by the skill.

Mitigation: Run the skill only in a trusted workspace and inspect XBY_APIKEY and endpoint-related settings before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/recipe-query)
- [XiaoBenYang API key portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value before API-backed recipe queries can run.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
