# 分发渠道

2026-11 实测与调研。月访问和 DR 是 SimilarWeb 与 Ahrefs 的第三方估算，只用来分档，不要当精确值。

## 有真实流量的两个

### clawhub.ai

月访问 3.8M，DR 82。OpenClaw 官方 hub，也是整个生态里权威度最高的目的地。

```bash
npx clawhub login          # 设备码，必须在浏览器里输入
npx clawhub whoami         # 确认已登录
npx clawhub skill publish ./skills/<name> --slug <name> --version 0.1.0 \
  --tags "a,b,c" --changelog "..."
```

- 发布即进安全扫描队列，24 到 72 小时审核，期间不公开
- SKILL.md 的 frontmatter 必须带 `license`，否则报 `acceptLicenseTerms is required`
- 版本号必须语义化，重复版本会被拒
- 实测数据：一个零 star、零推广的新 skill，三天 89 次下载

查询下载量：

```bash
curl -s "https://clawhub.ai/api/search?q=<name>" | head -c 400
```

返回里的 `downloads` 是真实安装数。页面上显示的 Downloads 可能滞后，以 API 为准。

### skills.sh

月访问 3.7M，DR 78。Vercel 做的跨 agent 目录，同时是 `npx skills add` 这个事实标准安装命令的归属方。

**没有提交入口，没有 publish 命令。** 收录链路只有一条：安装事件（带遥测）被后端观测到。

```bash
npx skills add <owner>/<repo> --list     # 只验证布局，不产生事件
npx skills add <owner>/<repo> --skill <name> -y   # 这才是事件来源
```

前置条件全部满足才会发事件：

| 条件 | 说明 |
| --- | --- |
| 仓库公开 | 私有仓库直接跳过 |
| 文件在默认分支 | feature 分支读不到 |
| 路径是 `skills/<name>/SKILL.md` | 根目录 SKILL.md 会被提前返回 |
| name 和 description 是合法字符串 | YAML 解析失败直接丢弃 |
| `DISABLE_TELEMETRY` 不存在 | **设成 0 也算存在，等于关闭** |

验证是否被索引：

```bash
curl -s "https://www.skills.sh/api/search?q=<name>"
```

`count: 0` 就是没有。页面返回 200 不代表有内容，它是 SPA，未收录的路径也会回 200。

## 自动抓取型

这些目录爬 GitHub 公开仓库，仓库做规范就自动进，不用提交。

| 目录 | 月访问 | DR |
| --- | --- | --- |
| skillsmp.com | 931K | 61 |
| claudemarketplaces.com | 277K | 36 |
| claudepluginhub.com | 168K | 13 |
| agentskills.so | 156K | 19（抓 skills.sh） |
| claude-plugins.dev | 26K | 30 |
| tonsofskills.com | 2K | - |

抓取有延迟，通常几天到几周。取决于对方的爬虫周期，无法主动触发。

## 需要提交的

| 目录 | 月访问 | DR | 方式 |
| --- | --- | --- | --- |
| lobehub.com | 1.4M | 56 | 站内提交 repo |
| mcpmarket.com | 1.4M | 52 | 站内提交 |
| mcp.directory | 134K | 16 | 提交 repo |
| skillhub.club | 119K | 33 | 上传 SKILL.md，中文站 |
| claudeskills.info | 100K | 26 | 免费提交表单 |
| skillsdirectory.com | 79K | 20 | 提交表单 |
| aiagentsdirectory.com | 60K | 72 | 提交，$49 买 dofollow 外链 |

合计约 3.1M 月访问，但都要人工登录填表，单个转化率未知。优先级低于前两个。

## 已经失效的

**smithery.ai**：2026-10-31 关停了 MCP Proxy 和 managed identity 业务，首页只引导去 Arcade，没有提交入口了。第三方榜单上它仍然是 446K / DR 75，信息已经过期。

教训：渠道清单必须核实最新状态，第三方文章的排名数据会滞后几个月。

## 官方目录

Anthropic 的 Claude 目录（claude.ai/directory）2026-09-25 开放自助提交，要求：

- 付费 Claude 计划
- 公开 GitHub 仓库
- plugin bundle 格式（`.claude-plugin/marketplace.json`）
- 通过自动安全扫描

权威度高，但不带流量，属于品牌背书型。账号条件不满足时不必执着。

## 选不选 MCP 形态

把能力做成 MCP server 能进 Smithery 之外的 MCP 生态，但代价是要维护一个常驻服务，且用户多一步配置。skill 形态的优势是 `npx skills add` 一条命令装完，转化路径更短。本地工具类能力优先做 skill。
