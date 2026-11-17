# ReadGZH — AI 打不开公众号文章怎么办？

ReadGZH 将用户提供的公开微信公众号文章链接转换为正文和 Markdown，适合交给 AI 总结、翻译或比较，也适合接入不想自行维护抓取环境的 Agent。

偶尔使用：打开 [ReadGZH](https://readgzh.site/?utm_source=clawhub&utm_medium=referral&utm_campaign=readgzh_intent_202609&utm_content=readme_quickstart)，粘贴文章链接，将生成页面交给能访问网页的 AI；否则复制正文。

持续接入：按 [SKILL.md](SKILL.md) 选择 API Key MCP 或 OAuth MCP。安装 Skill 本身不会自动完成服务器连接或账号授权。

新文章抓取每篇 3 积分，缓存读取 0 积分。注册用户每日可领 30 积分；匿名每 IP 每日 10 积分。积分不是文章数量；最新规则见 [定价页](https://readgzh.site/pricing)。

缓存搜索不等于全微信搜索，不提供完整公众号历史或自动订阅。文章需公开可访问且有权使用；转换内容可能进入共享缓存，敏感内容不适用。不能保证删除或受限文章的提取成功。

完整操作、连接地址和失败处理见 [SKILL.md](SKILL.md)。[最新 OpenAPI](https://readgzh.site/.well-known/openapi.yaml) 是接口规格的官方入口。

ReadGZH retrieves public WeChat articles for AI via its website, remote MCP, or REST API. Fresh reads cost 3 credits; cached reads cost 0. Free credits require daily claiming for registered users. Shared caching, client compatibility, and access restrictions apply.

This Skill package is licensed under MIT-0. The license does not grant rights to third-party article content or waive the cloud service's usage terms.
