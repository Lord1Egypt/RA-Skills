# 诸葛亮 · AI 推演军师 (zhuge-skill) v1.0.9

> **别再每次决策都烧 token。** 用结构化推演 + 晶体复用，把 90% 的决策留在 CPU 里跑，只在必要时调 LLM。
>
> 整合 **API-Football / The Odds API / Understat xG** 等 5 大数据源 · 6 维爻位 + 64 卦决策 · 经验自学习 · **DeepSeek / Kimi / 通义 / 智谱 / Claude / GPT / Gemini** 等 12 家 LLM 任选

---

## ⚡ 为什么比纯 LLM Agent 更省钱

大多数 AI agent 每做一次决策就烧一次 LLM（几 k ~ 几万 token）。诸葛亮的架构让你**大幅降低**这个成本：

| 决策路径 | token 消耗 | 备注 |
|---|---|---|
| 纯 LLM agent 做决策 | **~3000–10000 token/次** | 每次都要把上下文塞进 prompt |
| 诸葛亮：数据源 → 爻位 → 卦象 → 决策 | **0 token** | 纯 CPU 数值计算 |
| 诸葛亮：命中历史晶体 | **0 token** | 直接复用结构化模式，跳过 LLM |
| 诸葛亮：LLM 润色孔明评语（可选） | **~200–500 token** | 只在**你需要时**调，且可以关掉 |

**实际场景**：批量预测 50 场比赛
- 纯 LLM agent：~250,000 token（约 ¥15–50，看模型）
- 诸葛亮（不调 LLM）：**~0 token**（约 ¥0）
- 诸葛亮（每场写评语）：~15,000 token（约 ¥1–3）

**这才是 zhuge-skill 的核心价值**——不是因为易经玄学，是因为**结构化推演能做的事就不该花 token 做**。

---

## 你能让我做什么

我是一个能分析数据 + 推演决策 + 持续自学习的 AI 助手。当前主要场景是**足球比赛预测**，但底层是通用的 64 卦推演引擎，可扩展到任何决策场景。

### 核心能力

| 能力 | 命令 | 说明 |
|------|------|------|
| 单场预测 | `python start.py predict "Napoli vs Lazio"` | 拉数据 → 6 维爻位 → 卦象 → 决策 |
| 批量预测 | `python scripts/batch.py "A vs B" "C vs D"` | 一次跑多场 |
| 结果回传 | `python scripts/backfill.py` | 比赛后回填实际结果，更新命中率 |
| 命中率统计 | `python scripts/stats.py` | 看历史表现 |
| **经验结晶** | `python scripts/crystallize.py` | 提炼成功模式为「晶体」（**本地**操作） |
| **共同进化** | `python scripts/sync.py pull` | 从公共池**只拉取**匿名晶体（单向消费，HTTP GET，不携带本地数据） |
| 权重校准 | `python scripts/calibrate.py` | 用回传数据自动调爻位权重 |
| 战报 | `python scripts/report.py --llm` | LLM 写古风周报/月报 |
| 守护模式 | `python scripts/backfill.py --loop 30` | 每 30 分钟自动回传 |

### 调用示例

**给 Agent 的提示词：**
> "用诸葛亮 skill 预测明天的 Napoli vs Lazio"

Agent 应该调用：
```bash
python start.py predict "Napoli vs Lazio" --league serie-a
```

**输出要点：**
- 6 维爻位评分（攻防/士气/伤停/主客场/交锋/赔率）
- 卦象（64 卦之一）+ 阳爻数
- 孔明评语（可选 LLM 增强）
- 推荐：1X2 + 大小球
- **晶体匹配**：如果触发历史晶体，显示历史命中率

### 自学习闭环

```
预测 → 写经验库 → 等结果 → backfill 回传 → stats 看准确率
                                            ↓
共同进化 ← sync 拉公共晶体（只入） ← crystallize 本地结晶 ← calibrate 校准权重
```

---

## 🔐 环境变量清单（完整透明）

Skill 运行需要以下环境变量。**均为可选**——未填写时对应功能会**优雅降级**而不是崩溃。

### 数据源（足球预测场景必需）

| 变量 | 用途 | 获取地址 | 不填的后果 |
|---|---|---|---|
| `API_FOOTBALL_KEY` | 获取联赛/球队/比赛数据 | https://dashboard.api-football.com/ | 无数据，预测退化为 demo 模式 |
| `THE_ODDS_API_KEY` | 获取博彩赔率 | https://the-odds-api.com/ | 6 维爻位中的「赔率维度」缺失 |

### LLM 供应商（任选一个即可）

Skill 支持 12 个供应商。**只需配置其中一个**，其他留空：

| 变量 | 供应商 | 用途 |
|---|---|---|
| `DEEPSEEK_API_KEY` | DeepSeek | 孔明评语生成（**推荐，便宜**） |
| `OPENAI_API_KEY` + `OPENAI_API_BASE` | OpenAI / 任何 OpenAI-compat | 同上 |
| `ANTHROPIC_API_KEY` | Anthropic Claude | 同上 |
| `GEMINI_API_KEY` | Google Gemini | 同上 |
| `KIMI_API_KEY` | Moonshot Kimi | 同上 |
| `QWEN_API_KEY` | 阿里通义 | 同上 |
| `ZHIPU_API_KEY` | 智谱 GLM | 同上 |
| `DOUBAO_API_KEY` | 字节豆包 | 同上 |
| `YI_API_KEY` | 01.AI | 同上 |
| `BAICHUAN_API_KEY` | 百川 | 同上 |
| `MINIMAX_API_KEY` | MiniMax | 同上 |
| `CLAUDE_RELAY_KEY` + `CLAUDE_RELAY_BASE` | 第三方中转 | ⚠️ 见下方 §LLM 中转风险 |

**未配置任何 LLM** 时：跳过"孔明评语"步骤，其它功能正常。

---

## 🛡️ 安全与隐私（v1.0.1 透明度升级）

### 数据流向

| 脚本 | 行为 | 是否向外发数据 |
|---|---|---|
| `start.py predict` | 本地推演 | ❌ 否（除非调 LLM 生成评语，见下方） |
| `scripts/predict.py` | 本地推演 | ❌ 否 |
| `scripts/backfill.py` | 从数据源 API 拉结果 | ↓ 仅拉入，不外发 |
| `scripts/stats.py` | 本地统计 | ❌ 否 |
| `scripts/calibrate.py` | 本地调参 | ❌ 否 |
| `scripts/crystallize.py` | 本地提炼"晶体" | ❌ 否（只写本地 `data/crystals_local.jsonl`） |
| `scripts/sync.py pull` | 从公共 URL 拉匿名晶体（只 GET） | ↓ 仅拉入，**不外发** |
| `scripts/share.py` | 生成本地 md/json 到 `exports/` | ❌ 否（纯本地文件，不联网） |
| `scripts/report.py --llm` | 调 LLM 写周报 | ↗ prompt 送 LLM 供应商 |

### LLM 调用（所有涉及 LLM 的操作）

任何调用 LLM 的脚本（`predict --llm` / `report --llm`）会把以下内容发送到**你配置的 LLM 供应商**：
- 比赛名称、球队名、卦象结果、爻位分数
- **不含**任何用户个人信息、API key、赔率原始值

### ⚠️ LLM 中转风险（最重要）

Skill 支持一个叫 `relay` 的中转模式（`CLAUDE_RELAY_BASE=https://apiport.cc.cd` 等）。**启用中转意味着**：

- 你的 prompt / 模型响应 / API key 会经过**第三方中转服务器**
- 中转方**理论上能看到**你的所有对话内容
- 中转 key 和官方 key 是**两个不同账户**

**生产环境强烈建议**：直连官方 API（设置 `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` 指向官方端点），**不要用 relay**。

Relay 仅适用于：
- 中国大陆访问不了官方 API 时的临时方案
- 你**完全信任**该中转服务提供方

### 晶体拉取（`sync.py`）与本地导出（`share.py`）

**v1.0.1 的架构事实**：本 skill 的代码里**没有任何一行把本地数据发到网络**。

- `scripts/sync.py` 只有两个子命令：`pull`（HTTP GET 从公共 URL 拉）和 `status`（本地查看）。**`push` 函数已从代码中移除**，不是"默认关闭"——是根本没写。
- `scripts/share.py` 只把你本地的预测记录渲染成 `exports/predictions_*.md|json` 文件，供你自己手动分享，**不联网**。

**公共晶体池**（作为 `sync.py pull` 的来源）：
- URL：`https://raw.githubusercontent.com/yangfei222666-9/zhuge-crystals/main/crystals.jsonl`
- 可通过 `ZHUGE_REMOTE_CRYSTAL_URL` 环境变量改为你自己的 fork
- 这是一个**公开只读** URL，`curl` 就能看到内容，完全透明
- 贡献流程（给社区加晶体）是 GitHub Pull Request，**不是 skill 自动上传**

详见 [PRIVACY.md](./PRIVACY.md) 的架构级隐私合约。

### 本地写入权限

- `start.py` 带 wizard 模式会交互提示后**可选写入 `.env`**（`wizard.write_env`）
  - 你会看到确认提示，**必须回复 yes** 才写
  - 默认写到 skill 自身目录的 `.env`，不污染系统级 env
- 会创建：`data/experience.jsonl` / `data/crystals_local.jsonl` / `data/crystals_shared.jsonl`（均在 skill 目录下）
- **不会**修改其它 skill、不会修改系统 PATH、不会安装全局依赖

### 如何审计（2 分钟）

打开这三个文件，grep 关键词确认行为：

```bash
# 1. 确认 sync.py 没有任何上传逻辑（应只看到 docstring 里 "没有 push" 的字样）
grep -n "requests.post\|push\|upload\|POST" scripts/sync.py

# 2. 确认 share.py 不联网（应无匹配）
grep -n "requests\|urlopen\|http" scripts/share.py

# 3. 确认全仓库没有隐藏的上传端点
grep -rn "requests.post\|urlopen.*POST\|upload" scripts/ core/
#    应只看到 core/llm.py 里调你自己配置的 LLM 供应商（不含本地数据库）

# 4. 确认 wizard 写 .env 需要用户确认
grep -n "write_env\|\.env" core/wizard.py
```

---

### 文件结构

- `start.py` — 一键入口（带欢迎动画 + wizard）
- `core/` — 核心算法（卦象/爻位/LLM 适配/孔明/结晶）
- `adapters/` — 数据源（API-Football/The Odds API/Understat）
- `scripts/` — 入口脚本
- `data/` — 64 卦表 + 种子经验库 + 晶体池

### 兼容性

✓ Hermes Agent / OpenClaw / Claude Code / Cursor / 任何 Python 环境
✓ 12 LLM 供应商（豆包/Kimi/通义/智谱/Yi/百川/MiniMax/DeepSeek/OpenAI/Claude/Gemini/中转）
✓ 三种配置方式：环境变量 / `.env` / 命令行参数
✓ 网络降级：任何外部 API 失败都不阻塞核心流程

---

## 更新日志

### v1.0.4 (2026-04-17) — UX + 工具批
- `scripts/predict.py` 预测输出显示晶体复用次数 + 首见年龄 + 信任标签
- `scripts/crystallize.py --dry-run` 预览结晶结果不写入
- `scripts/stats.py --crystals` 晶体排行 + stale 监控
- `scripts/error_log.py --resolve <id>` + priority / status 字段（生命周期对齐 self-improving-agent 方法论）
- 晶体 schema v2：新增 `first_seen` / `last_seen` / `recurrence_count`，`match_crystal` 命中回写 `crystals_local.jsonl`
- 新增 `scripts/error_log.py`：JSONL 错误日志，接入 `backfill` 守护循环 / `fetch_actual_result` / `core/llm.py` 三个 except 点
- 新增 `README.en.md` 英文版（为国际用户 / Show HN 准备）
- 新增 `CHANGELOG.md` 独立文件
- README 加 📬 反馈与联系 段（邮箱优先，微信 yf529486 辅）
- README 加跨 Agent 接入片段（Claude Code / Cursor / OpenClaw / Hermes / 纯 Python 各一个可复制示例）

### v1.0.3 (2026-04-17) — 视觉素材升级
- 新增 `assets/demo.png` — 诸葛亮推演引擎实录截图（启动动画 + 6 维爻位实时评分）
- README 顶部嵌入演示截图，一眼看清 skill 的"一句话预测闭环"
- 无代码变更

### v1.0.2 (2026-04-17) — 文档一致性修正
- 修复 SKILL.md 与 PRIVACY.md 自相矛盾点：原 §晶体共享 节仍沿用 v1.0.0 "有上传功能、默认关闭"的旧描述，与 v1.0.1 的代码事实（`push` 已移除）不一致，已重写为 §晶体拉取 与本地导出，对齐代码
- 数据流向表：`sync.py` 改为 `pull`（只 GET），`share.py` 标为纯本地导出
- 自学习闭环图修正：`sync 推/拉` → `sync 拉公共晶体（只入）`
- 审计 grep 命令扩展到 4 条，加入"全仓库扫上传端点"一项
- 代码层面零变更，仅文档修正

### v1.0.1 (2026-04-17) — 透明度升级
- 新增 §环境变量清单（12 个 LLM + 2 个数据源，每个用途/获取地址/降级行为说明）
- 新增 §安全与隐私（数据流向表 + 每个脚本是否向外发数据）
- 明确 LLM 中转风险（relay 模式数据流向第三方）
- **架构级隐私合约**：`sync.py` 的 `push` 函数从代码中移除，固化为单向消费架构（只 pull 不 push）
- `sync.py` 子命令简化为 `pull`（从公开 URL 只读拉取）和 `status`（本地查看）
- `share.py` 明确为本地导出工具（生成 `exports/*.md|json`），不联网
- 新增 [PRIVACY.md](./PRIVACY.md)：详细列出网络调用清单、作者数据可见度矩阵、fork 者脱敏白名单
- 新增 §如何审计（4 行 grep 命令自查）

### v1.0.0 (2026-04-17) — Initial release on ClawHub
- 5-source data fusion + 64-hexagram reasoning + experience crystallization
- 12+ LLM provider support
- Guardian mode + crystal pool (pull-only from v1.0.1)
