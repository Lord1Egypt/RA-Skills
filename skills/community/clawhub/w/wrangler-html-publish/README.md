# Wrangler HTML Publish

给支持本地终端操作的 AI Agent 使用的技能：仅明确要求 Wrangler/Cloudflare Pages 时归档并在获得公开授权后部署，不默认接管普通 HTML 生成。

## 安装

将整个 `wrangler-html-publish/` 文件夹放入你的 Agent 支持的 skills 目录，保留 `SKILL.md`、`scripts/`、`references/` 和 `tests/` 的结构。不包含作者电脑路径、账号、认证信息或运行记录。

多 Agent 用户可将本体放在 `~/.agents/skills/wrangler-html-publish/`，再由各 Agent 的 skills 目录建立软链接。安装前检查同名路径，不覆盖原有技能；Windows 不方便建立链接时可安装副本，但升级时需要同步。各工具的扫描目录以其当前文档为准，不能保证它们都默认扫描 `.agents`。

重新加载技能或新建会话后，可明确输入：

> 使用 wrangler-html-publish，把这份 HTML 保存到固定目录并发布，给我地址。

## 默认行为

- 存放目录：当前用户主目录的 `Documents/published-html/<slug>/index.html`，可自行指定其他目录。
- 仅本地：说“生成 HTML，先不要上传”；不会登录或部署。
- 首次发布：检查 Node.js/npm/Wrangler、引导登录、确认项目/分支与公开范围，保存非敏感配置。
- 后续发布：复用配置，按白名单保留旧站点页面，不把私人草稿混入快照。
- Pages 内容通常公开，不适合直接分享客户隐私或内部原文；随机 URL 不提供访问控制。

本机普通 HTML 生成不自动触发本技能，避免与默认发布流程重复上传。本技能不会擅自安装 hooks 或修改全局 settings。

## 依赖与测试

本地脚本只用 Node.js 内置模块，无 npm 依赖，不执行 Cloudflare 请求。部署需要可用的 Node.js、npm、Wrangler 和 Cloudflare 账号；登录凭证由 Wrangler 自行管理。

```sh
node --test "<技能目录>/tests/files.test.mjs"
```

离线测试验证路径与文件整理，不证明真实 Cloudflare 部署已成功。技能安装和升级不应包含运行态 config、plan、manifest、快照或缓存。
