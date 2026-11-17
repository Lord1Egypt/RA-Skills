# MCP 市场目录与评估框架 v1.0

> 大脑加强：本技能不去抓取市场数据，只提供"市场目录 + URL 模板 + 评估维度 + 决策框架"。
> 用户的 Agent 按本表提供的 URL 自行抓取，由 Audit 给出推荐结论。

## 一、四大权威市场对比（2026-07 实测可用）

| 市场 | 主 URL | 规模 | 特色 | 评分机制 | 推荐场景 |
|---|---|---|---|---|---|
| **官方 MCP Registry** | https://registry.modelcontextprotocol.io/ | 1000+ | Anthropic/MCP 官方维护 | 无（仅收录） | 权威性背书、合规场景 |
| **Glama** | https://glama.ai/mcp/servers | 10,000+ | maintainer-verified + 持续重建 | 质量分（quality + safety） | **首选**：找高质量 MCP |
| **Smithery** | https://smithery.ai | 5000+ | 提供 CLI 与托管执行 | 安装数 + stars | **次选**：找易部署的 |
| **mcp.so** | https://mcp.so | 3000+ | 简洁的目录 | stars | 快速浏览 |
| **PulseMCP** | https://pulsemcp.com | 2000+ | 中文友好 | 无 | 中文用户 |
| **MCP Toplist** | https://mcptoplist.com | 聚合 | 实时排名（跨多市场） | 综合排名 | **趋势追踪** |

### 各市场详情 API（用户授权后由 agent 调用）

```
# Glama（推荐主源）— 支持 search query
https://glama.ai/mcp/servers/@v1/servers?search={query}&limit=20
https://glama.ai/mcp/servers/{server-id}

# 官方 MCP Registry
https://registry.modelcontextprotocol.io/v0/servers
https://registry.modelcontextprotocol.io/v0/servers/{server-id}

# Smithery
https://registry.smithery.ai/v1/servers?q={query}

# MCP Toplist（聚合排名）
https://mcptoplist.com/api/toplist?category={cat}&limit=20
```

## 二、MCP 健康度六维评估（参考 OpenSSF Scorecard + npms.io）

> 不直接抓数据；提供评估框架供 Agent 按规则打分

| 维度 | 权重 | 评估指标 | 取数方式 | 阈值（10 分制） |
|:-:|:-:|---|---|---|
| **维护活跃度** | 30% | 最近 commit / release 距今天数 | GitHub API `repos/{owner}/{repo}/commits` | <30d=10 · <90d=7 · <180d=4 · ≥180d=1 |
| **社区热度** | 25% | stars / forks / contributors | GitHub API `repos/{owner}/{repo}` | ⭐≥10k=10 · ≥1k=7 · ≥100=4 · <100=1 |
| **文档质量** | 15% | README 字数 / 示例数 / 是否含 install 章节 | fetch README | 完整=10 · 基础=6 · 缺=2 |
| **安全信号** | 15% | Glama 安全分 / 是否有 CVE / 是否 signed | Glama API | A=10 · B=7 · C=3 · 无=0 |
| **依赖深度** | 10% | 一级依赖数 / 包大小 | package.json / pyproject.toml | ≤5=10 · ≤15=7 · ≤30=4 · >30=1 |
| **测试与 CI** | 5% | 有无 CI 配置 / 测试文件覆盖率 | 检查 `.github/workflows/`、`test/` | 全有=10 · 部分=5 · 无=0 |

### 综合分公式

```
MCPHealth = 维护×0.30 + 社区×0.25 + 文档×0.15 + 安全×0.15 + 依赖×0.10 + 测试×0.05
```

**判定阈值**：
- ≥8.0 → 🟢 **推荐引入**（默认 project scope，必要时升 global）
- 6.0–7.9 → 🟡 **观察评估**（在 1-2 个场景试用）
- 4.0–5.9 → 🟠 **谨慎引入**（仅供测试，不入生产）
- <4.0 → 🔴 **不建议**

## 三、推荐 MCP 候选库（精选 T0/T1，按能力维度）

> 本表为已知优秀 MCP 服务器的快速索引，避免每次都去市场查

### 🔍 搜索调研类

| MCP | 主能力 | 评分(估算) | URL | 备注 |
|---|---|:-:|---|---|
| **firecrawl** | web-search/scrape/crawl | 9 | https://github.com/firecrawl/firecrawl | 144k⭐，JS 渲染+反反爬 |
| **brave-search** | web-search | 8 | https://github.com/brave/brave-search-mcp | 隐私优先 |
| **tavily-mcp** | web-search（LLM 优化） | 9 | https://github.com/tavily-ai/tavily-mcp | 专为 AI 设计 |
| **exa-mcp** | web-search（语义） | 8 | https://github.com/exa-labs/exa-mcp-server | 语义搜索 |

### 🌐 浏览器自动化

| MCP | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **playwright** | browser-auto | 9 | https://github.com/microsoft/playwright-mcp |
| **puppeteer** | browser-auto | 8 | https://github.com/puppeteer/puppeteer-mcp |
| **browserbase** | browser-auto（云端） | 7 | https://github.com/browserbase/mcp-server |

### 💻 代码与开发

| MCP | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **github** | repo-read/pr-manage | 9 | https://github.com/github/github-mcp-server |
| **gitlab** | repo-read | 8 | https://github.com/modelcontextprotocol/servers/tree/main/src/gitlab |
| **filesystem** | file-ops | 8 | 官方 servers 仓库 |
| **codegraph** | code-analysis | 9 | 本地索引（项目已用） |

### 🗄️ 数据与存储

| MCP | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **postgres** | db-query | 8 | https://github.com/modelcontextprotocol/servers/tree/main/src/postgres |
| **sqlite** | db-query | 7 | 官方 servers |
| **s3** | file-store | 7 | AWS 官方 |

### 🔧 系统与运维

| MCP | 主能力 | 评分 | URL |
|---|---|:-:|---|
| **sequential-thinking** | reasoning | 9 | 官方 servers |
| **memory** | memory-write | 8 | 官方 servers |
| **time** | datetime | 7 | 官方 servers |

## 四、用户 Agent 抓取指引（指导"如何指导 agent"）

> 这是本技能的核心："我不动手，我教你如何让你的 agent 高效动手"

### 模板：让 agent 抓 MCP 市场数据

```
[用户对 agent 说]

请按以下步骤评估 MCP "firecrawl" 是否适合引入我的项目：

1. 调用 WebFetch 获取：
   - https://glama.ai/mcp/servers/firecrawl
   - https://github.com/firecrawl/firecrawl
2. 按下表评估（六维，每维 0-10）：
   | 维度 | 权重 | 评分依据 | 我的项目相关性 |
   |---|---|---|---|
   | 维护活跃度 | 30% | 最近 commit | ? |
   | 社区热度 | 25% | stars | ? |
   | 文档质量 | 15% | README | ? |
   | 安全信号 | 15% | Glama grade | ? |
   | 依赖深度 | 10% | package.json | ? |
   | 测试与 CI | 5% | workflows | ? |
3. 计算综合分，给出 🟢/🟡/🟠/🔴 判定
4. 如果 🟢，给我具体的 mcp.json 配置片段（按 ZCode/Claude/Cursor 格式）
5. 注明：scope=project 还是 global，理由
```

### 模板：跨市场横向对比

```
[用户对 agent 说]

我要找一个 web-search MCP，请横向对比以下候选：
- firecrawl
- tavily-mcp
- brave-search
- exa-mcp

输出对比表（含六维评分、许可证、是否免费、是否需 API Key），按综合分排序。
最后给出"互补 vs 替代"判断：如果已装 agent-reach，谁更适合补强？
```

## 五、本地 MCP 配置扫描规则

> Audit 这边只读本地，不抓市场；以下规则用于 Phase ② 能力映射

### 扫描路径（已在 config.yaml mcp_config.files 配置）

```
~/.zcode/cli/config.json         # ZCode MCP
~/.claude.json                   # Claude Code MCP  
~/.codex/config.toml             # Codex MCP
```

### 提取规则

```yaml
# 解析每个 mcp server 块
for server in mcpServers:
  name = server.key
  command = server.value.command
  args = server.value.args
  env = server.value.env  # 注意脱敏
  enabled = server.value.disabled != true
  
  # 探测类型
  type = 
    if command contains "npx": node
    if command contains "uvx": python
    if command contains "python -m": python-module
    if "url" in server.value: remote
    else: unknown
```

### 健康度本地信号

| 信号 | 检测方法 | 含义 |
|---|---|---|
| 命令存在 | `command -v <command>` | 是否能启动 |
| 模块可导入 | `python -c "import <mod>"` | Python 包是否装 |
| URL 可达 | HTTP HEAD | 远程服务是否在线 |
| 启动响应 | `<cmd> --help` 5s 超时 | 是否能正常响应 |

## 六、给推荐引擎的输入契约

```
# Phase ⑤b 推荐引擎应接收的结构
mcp_candidates:
  - name: "firecrawl"
    sources: ["glama", "github"]            # 数据来源
    health_score: 8.5                        # 六维加权
    confidence: "observed"                   # 数据状态
    capability_overlaps:
      - dimension: web-search
        current_tool: agent-reach
        current_level: 5
        candidate_level: 9
        relationship: complement             # complement/supersede/irrelevant
    install_complexity: low                  # low/medium/high
    license: "AGPL-3.0"                      # 必须显式
    evidence_urls: ["https://..."]
```

## 七、安全边界

- **永远不在 audit 内执行抓取**：URL 模板提供给 agent，由用户授权后调用
- **永远不输出 API Key**：抓取结果中 env 字段必须脱敏
- **外部信号必须 observed**：评分依据每个 URL 都要可复查
- **OpenSSF 警告**：xz-utils 事件证明高健康分 ≠ 安全，必须保留人工复核环节

## 八、维护

- 市场规模/URL 变动时更新本表
- 新增高分 MCP 时追加到第四节"候选库"
- 评估维度变更时同步 `references/recommendation-framework.md`
