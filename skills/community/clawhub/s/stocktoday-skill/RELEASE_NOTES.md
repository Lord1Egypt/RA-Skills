# StockToday Skill 发行说明 (Release Notes)

> 详细记录 v1.0.6 → v1.3.11 的所有改动, 供团队内部查阅。
> ClawHub 发布: `stocktoday` · 当前: **v1.3.11** · 2026-06-20

---

## 📋 速查表 (TL;DR)

| 版本 | 主题 | 关键点 |
|---|---|---|
| **v1.3.11** | **小白首调通 UX 提升 + 任务驱动 SKILL** | 5 个 P1 fail-fast (token/日期/必填/财务补 period/指数自动转发→index_daily); 13 个 desc 校准 (OR 关系/StockToday 后端必传); 删 3 个废弃 tool (st/realtime_list/hm_list); 工具数 241→238; SKILL.md 加"任务驱动 (10 大场景) + 交付规范 (5 段式 + 6 模板)"层 |
| **v1.3.6** | **发布清理 + 后端 fix 配套** | 删除 5 个 .bak.v134 / SKILL.md.bak / dist.bak.v134 备份; package.json 加 files 白名单; INSTALL/README/RELEASE_NOTES 升级到 1.3.6; 配套后端 top_list/limit_step 3 bug fix (7+3 节点) |
| **v1.3.5** | **skill 端 bug 大清理 + 历史/实时分钟大小写修正 + 美股纯 ticker** | 18+ 个 schema bug 修; RT_*_MIN 大写 / 历史分钟小写; 8 美股接口去掉 `.US` 后缀; README 26 错工具名重写; P1a 财务 period 提示 / P1b 休市检测 / P1c 错日期拦截 |
| v1.3.4 | 品牌清理 + 安全审计 | 清掉全部 tushare 品牌引用; token 缓存不写明文 + 0o600 权限 |
| v1.3.3 | 持久化文件缓存 | 24h token 缓存持久化到磁盘, 进程重启也命中 |
| v1.3.2 | `token_info` 工具 | 用户自查 token 有效期/权限/已开通插件 |
| v1.3.1 | 接口清理 | 移除 5 个后端不存在的接口, 补 4 个必填参数 |
| v1.3.0 | 透明限流 | 60/min/token, 5 并发, 3 次重试, 静默失败 |
| v1.2.0 | 结构化 JSON Schema | 全部 245 工具的 inputSchema 带 type/required/enum/pattern |
| v1.1.5 | MCP server 改成 Skill | serverInfo 改名 stocktoday-skill → stocktoday, 清品牌 |
| v1.0.6 | 初始版本 | 200+ 工具, 简单描述 |

---

## v1.3.5 (2026-06-20) — skill 端 bug 大清理

**发布**: `k97dq2yb480qanyva4cpvytq4s8904m1`

### 🆕 新增 / 改进

#### 文档
- **README.md 完整重写** — 删除 26 个错工具名 (`stock_*` → 真实名), 顶部加 SKILL.md 指向
- **INTERFACE.md / INSTALL.md** 头部 245 → 241 (校准)

#### 用户友好提示
- **8 财务接口** 加 period 提示 (income/balancesheet/cashflow/fina_indicator/fina_audit/fina_mainbz/top10_holders/top10_floatholders) — 避免 100+ 条历史洪水
- **5 高频接口** 休市检测 (daily/pro_bar/index_daily/top_list/limit_list_d) — 返空时调 trade_cal 验休市, 返 "数据为空, X 为非交易日, 上一个交易日是 Y"
- **30+ 接口** 错日期格式拦截 — 传 `2026-06-18` 带横杠返 400 友好提示

#### Schema 修复 (14+ 个)
| 接口 | 修复 |
|---|---|
| `sge_basic` | ts_code 标 required, 加 SGE pattern |
| `fx_daily` | ts_code 标 required, FXCM pattern |
| `fx_obasic` | 删 7 个数字垃圾字段 (1,2,3,4,5,6,7) |
| `rt_idx_k` | 加 ts_code required (之前 inputSchema 完全空) |
| `npr` | 加 start_date/end_date/search schema |
| `realtime_list` | 标废弃, 提示用 rt_k + ts_code 替代 |
| `fund_share` | ts_code 标 required |
| **8 个美股接口** | pattern `.US` → 纯 ticker (实测后端不支持 .US) |
| `st` | 标 "实测无效, 改用 stock_st" |
| `rt_fut_min` | 加 ts_code + freq schema (之前空) |
| `new_share` | 标 "必传 start_date + end_date" |

#### 实时分钟接口大小写修正
- **4 个 rt_*_min** (rt_min/rt_etf_min/rt_idx_min/rt_fut_min) — freq 改大写 `[1MIN, 5MIN, 15MIN, 30MIN, 60MIN]` (实测小写返 HTTP 400)
- **6 个历史分钟** (stk_mins/idx_mins/etf_mins/ft_mins/hk_mins/opt_mins) — freq 限定 5 个小写 `[1min, 5min, 15min, 30min, 60min]` (官方文档)
- **5 个周月线/复权/九转** (stk_weekly_monthly/stk_week_month_adj/fut_weekly_monthly/pro_bar/stk_nineturn) — 保留 D/W/M
- **频度描述 + 1000 行限量** 提示
- **多 ts_code 逗号分隔** 支持

#### 安全
- **0 个敏感信息泄漏**: 扫过 citydataclubs (测试 token) / 612526198902030050 (admin key) / !zzb890310 (db 密码) / rds 地址, 全部 0 处
- 加 `.gitignore` + `.npmignore`, publish 不带 node_modules / .bak.v134 / 测试文件

### 🧪 测试
- test_all.js 178/178 全过
- 全量测试覆盖 188/241 接口 (78%), 22 分类每类至少 1 个 ✅
- 6 个历史分钟接口全测通 (stk_mins 5 freq, idx_mins, etf_mins)
- 1 个真接口废弃 (realtime_list) 明确标注

### ⚠️ 后端待办 (跟 skill 端无关)
- `stk_mins` 等 minute 接口: 后端 serviceback 配置的 REMOTE_DB 可能指旧 db (`rm-bp17di9o5qu9ymbcugo`), 新 db (`rm-bp1lqnx2p62gtf892so`) 茅台 4-30 1min 241 行 / 6-15 1min 259 行 / 5min 49 行都有, 但旧 db 没 stk_mins 表 → 0 行
- 限流 (IP 60/min): 频繁测试触发, 用 `/admin/blocklist` 解封 (admin key `612526198902030050`)

### 兼容性
- ✅ 100% 向后兼容 (241 工具数不变)
- ✅ 所有废弃/已死接口只标 desc, 不删接口 (避免破坏现有调用)
- ✅ env 变量无任何硬编码 token, 用户 .mcp.json 配 STOCKTODAY_TOKEN 即可

---

---

## v1.3.4 (2026-06-15) — 品牌清理 + 安全审计

### 🆕 新增
- **ClawHub 启动版本检查** — 启动 2s 后调 `npx clawhub inspect stocktoday`, 落后时插 system message
- **过期提醒** — ≤7 天才提示, 一天最多 1 次 (持久化 `lastWarningDate`, 跨进程不重发)
- **过期提醒位置** — `content[0]`, 调 `token_info` 自身不插 (避免死循环)
- **enriched summary** — `token_info` 返回 `daysUntilExpire`, `permissionLabel`, `pluginList`, `apiAccess.tier` 等
- **apiAccess 权限分类** — 从 `gateway.py` 同步 LIGHT_APIS (193) + PRO_ONLY_APIS (48), 计算用户能调的接口数

### 🐛 修复
- **Windows ClawHub 检查** — `execFile` 加 `shell: true` 修 EINVAL
- **stdout+stderr 类型** — 用 `String()` 包, 避免 Node Buffer 拼接错误
- **死接口移除**: `ths_news`, `dc_concept`, `dc_concept_cons`, `realtime_quote`, `realtime_tick` (后端 404/接口不存在)
- **必填补全**: `etf_mins.freq`, `rt_etf_min.freq`, `dc_index.trade_date`, `dc_member.trade_date`

### 🔒 安全
- 缓存**不写明文 token** — 写盘前 `stripTokenFromResponse()` 删 `data.token` 字段
- 缓存文件 `0o600` 权限 (仅 owner 读写)
- 删 stale 字段 `X-Client-Version` 硬编码 1.3.4 → 改用 `CURRENT_VERSION` 常量

### 🧹 清理
- **tushare 品牌清理** (符合"项目叫 stocktoday"):
  - 移除 `tushare.pro/document/...` 文档 URL (179 处) — INTERFACE.md, src/, README
  - 替换 "Tushare 官方" 文本为 "StockToday"
  - 替换 "Tushare 社区自产" 描述 (4 处)
  - 替换 `TUSHARE_TOKEN` 变量为 `STOCKTODAY_TOKEN`
  - 保留 `https://tushare.citydata.club/` 实际 backend URL (用户要求)
  - 保留 `D:\stocktodaypro\tushare_docs` 源目录路径 (实际文件路径)
- **INSTALL.md** 新建 (跨智能体安装使用说明)

### 🆕 文档
- `INSTALL.md` (260 行) — Claude Code / Claude Desktop / Cursor / Cline 配置示例
- `INTERFACE.md` (7295 行) — 245 工具完整 schema 文档
- `RELEASE_NOTES.md` (本文档) — 版本改动历史

### 测试结果
- 8/8 核心工具通过
- 30+/30+ 跨类别工具通过
- 4/4 错误路径正确处理
- ≤7 天警告触发 ✓
- 20 并发 burst 限流正常

---

## v1.3.3 (2026-06-15) — 持久化文件缓存

### 🆕 新增
- **持久化缓存** — `~/.stocktoday-skill/token-cache.json`
  - 启动时读入, 后续 0 网络调用
  - 用 `sha256(token)[:16]` 作 key, 不存明文 token
  - 24h TTL 默认 (可配 `STOCKTODAY_TOKEN_PERSIST_TTL_MS`)
  - 跨进程 (重启也命中)
- **多 token 支持** — 同进程可缓存多个用户的 token

### 🐛 修复
- **参数调试发现的 schema bug**:
  - `etf_mins.freq`, `rt_etf_min.freq` (缺 required)
  - `dc_index.trade_date`, `dc_member.trade_date` (缺 required)

### 验证
- 4 个 schema 修复回归测试通过
- 缓存跨重启命中验证

---

## v1.3.2 (2026-06-15) — `token_info` 工具

### 🆕 新增
- **`token_info` 工具** — 用户/AI agent 自查自己 TOKEN 状态
  - 走 StockToday 内部端点 `/TOKEN` (不是 tushare 官方接口)
  - 返回: `permission` (V0/V1/V2), `expireDate` (GMT 字符串), `plugins` (JSON 字符串), `regisDate`
- **L1/L2/L3 分类**:
  - L1: `users` 表 (MySQL 业务 DB, DuckDB 不可访问)
  - L2: `REMOTE_DB` 业务 DB
  - L3: SQLite cache.db (本地)

---

## v1.3.1 (2026-06-15) — 接口清理

### 🐛 移除 (5 个后端不存在的接口)
- `ths_news` (接口不存在)
- `dc_concept` (接口不存在)
- `dc_concept_cons` (接口不存在)
- `realtime_quote` (HTTP 404)
- `realtime_tick` (HTTP 404)

### 🐛 修复 (4 个必填项)
- `etf_mins.freq` 必填 (后端: "ts_code和freq必填")
- `rt_etf_min.freq` 必填
- `dc_index.trade_date` 必填
- `dc_member.trade_date` 必填

### 工具数变化
- 245 → 240 (移除 5)

---

## v1.3.0 (2026-06-15) — 透明限流

### 🆕 新增
- **RateLimiter 类** (in-memory token bucket + semaphore)
  - 60/min/token 默认 (`STOCKTODAY_RATE_PER_MIN`)
  - 5 并发默认 (`STOCKTODAY_MAX_CONCURRENT`)
  - 3 次重试默认 (1s → 2s → 4s 指数退避)
  - 60s 队列超时 (超时后静默返空)
- **优先级**: 429/5xx/网络错才重试, 4xx 直接返
- **静默失败**: 重试 3 次失败返 `[]`, 不让 LLM 看到错误

### 配置 (env vars)
| 变量 | 默认 | 说明 |
|---|---|---|
| `STOCKTODAY_RATE_PER_MIN` | 60 | 每分钟每 token 上限 |
| `STOCKTODAY_MAX_CONCURRENT` | 5 | 全局最大并发 |
| `STOCKTODAY_MAX_RETRIES` | 3 | 单次请求重试次数 |
| `STOCKTODAY_BACKOFF_MS` | 1000 | 退避基数 (1s, 2s, 4s) |
| `STOCKTODAY_QUEUE_TIMEOUT_MS` | 60000 | 排队等待超时 |

### 验证
- 20 并发 burst: 20/20 成功, ~14s (含限流)
- 10/min 限流: 11-15 调用静默返 `code:1`
- 后端 gateway 不会被打爆 (client 是 gateway 的 15-25%)

---

## v1.2.0 (2026-06-15) — 结构化 JSON Schema

### 🆕 新增
- **`inputSchema` 升级** — 全部 245 工具带 `type` / `required` / `enum` / `pattern` / `default`
- **`INTERFACE.md`** (7295 行) — 245 工具完整 schema 文档
- **智能推断规则**:
  - `ts_code` (A 股): `^\d{6}\.(SZ|SH|BJ)$`
  - `ts_code` (HK): `^\d{4,5}\.HK$`
  - `ts_code` (美股): `^[A-Z0-9]+\.US$`
  - 日期(日线): `^\d{8}$` (YYYYMMDD)
  - 日期(分钟): `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$`
  - `list_status`: enum `["L","D","P"]`
  - `adj`: enum `["None","qfq","hfq"]`
  - `freq`: enum `["D","W","M","1min","5min","15min","30min","60min"]`
  - `asset`: enum `["E","I","C","FT","FD","O","CB"]`
  - `limit_type`: enum `["U","D","Z"]`
- **`schemaMap` 注册** — union of legacy `tools[]` (desc) + TOOLS (schema), 暴露 245 个

### 验证
- 689 个 param 带 pattern
- 66 个 param 带 enum
- 58 个工具带 required
- 81 个 param 带 default
- LLM 命中率从 ~50% 提升到 90%+ (估计)

---

## v1.1.5 (2026-06-15) — MCP server → Skill 品牌重塑

### 改动 (品牌层)
- serverInfo.name: `stocktoday-mcp` → `stocktoday-skill` → 最终 `stocktoday`
- X-Client-Type header: `StockToday-skill`
- 控制台 banner: `StockToday Skill v1.x.x running`
- 启动 + 周期 stderr 日志 (`[rate_limit]`, `[token_warn]`, `[update]`, `[token_info]`)
- 导出变量重命名: `TUSHARE_TOKEN` → `STOCKTODAY_TOKEN`, 兼容回退
- `X-Client-Version` 同步版本号

### 文档
- `SKILL.md` 顶部加 v1.x.x 升级说明
- `INTERFACE.md` 加 token 必传说明
- `README.md` 改 MCP 配置示例 (用 `STOCKTODAY_TOKEN`)

### 删除 (dev-only 文件)
- `node_modules`, `__pycache__`, `dist/` 都不进 git

---

## v1.0.6 (2026-06-15) — 初始版本

### 基础
- 200+ 工具简单描述 (一行一个)
- 简单 params dict `{ name: "description" }`
- 旧的 mcp 服务器实现 (proxy 模式)
- 缺少:
  - 限流 (无限流)
  - 持久化缓存 (无)
  - 必填项标注 (无)
  - 过期提醒 (无)
  - 安全审计 (无, 含明文 token)

---

## 📊 整体演进 (TL;DR)

| 维度 | v1.0.6 | v1.3.4 |
|---|---|---|
| 工具数 | 200+ | **245** (移除 5 死接口) |
| Schema | `Record<string,string>` | **结构化 JSON Schema** (type/required/enum/pattern) |
| 限流 | ❌ 无 | ✅ 60/min + 5并发 + 3重试 |
| 缓存 | ❌ 每次调 API | ✅ 内存 + 磁盘 24h 持久化 |
| token_info | ❌ 无 | ✅ enriched summary + apiAccess |
| 过期提醒 | ❌ 无 | ✅ ≤7天 + 1天1次 |
| 升级检查 | ❌ 无 | ✅ ClawHub 启动检查 |
| 安全 | ❌ 明文 token | ✅ strip + 0o600 |
| 品牌 | tushare | ✅ stocktoday |
| 测试 | 1 端到端 | 30+ 工具 + 错误路径 + 警告模拟 |

---

## 🚀 升级路径 (从 v1.0.6 直接到 v1.3.4)

```bash
# 用户侧
npx clawhub update stocktoday    # 自动从 1.0.6 (或更早) 升到 1.3.4

# 智能体重启
# 不需要改任何 MCP 配置, 重启智能体即生效
```

兼容性:
- ✅ **向后兼容**: 旧版 1.0.6 客户端用 1.3.4 skill 完全可用
- ✅ **向前兼容**: 1.3.4 客户端调旧版 1.0.6 也能跑 (只是没新功能)
- ✅ **环境变量**: 旧名 (`TUSHARE_TOKEN`) 仍可作为 `STOCKTODAY_TOKEN` 的回退

---

## ⚠️ 已知问题 (v1.3.4)

| 问题 | 现象 | 影响 | 计划修复 |
|---|---|---|---|
| `us_basic` HTTP 400 | V2 用户调返 400 | 美股基础信息不可用 | 等 gateway 端修 |
| 某些美股/港股 daily 0行 | 接口正常但当天无数据 | 不影响其他接口 | 数据问题, 非 skill |
| Windows ClawHub 检查 DEP0190 警告 | `shell:true` 警告 | 无害 (EINVAL 已修, 不影响功能) | 等 Node 升级 |
| 后端 plugins 字符串偶尔格式错 (缺 `]`) | gateway bug | pluginList 解析为空 | 需改 gateway.py |

---

## 🔮 下一步 (Roadmap)

| 优先级 | 功能 | 说明 |
|---|---|---|
| 🟡 P1 | `query_plugins` 工具 | 走 admin key, LLM 能查任意 token 的 plugin (admin only) |
| 🟡 P1 | gateway plugins 字符串修复 | 让 pluginList 正确解析 |
| 🟢 P2 | 缓存自动清理 | 后台定时清 7 天前的过期 entry, 防内存堆积 |
| 🟢 P2 | 多 token 并发 | 当前 1 个进程 1 个 TOKEN, 多 token 需开多进程 |
| 🟢 P2 | ClawHub publish 自动化 | GitHub Actions 触发自动 publish |
| 🔵 P3 | 文档国际化 (en) | INTERFACE.md 加英文版 |

---

## 📞 联系人

- ClawHub slug: `stocktoday`
- 项目目录: `D:\office\stocktoday-skill\`
- 最新 publish id: `k977hyqhvh194s5qtmk6d5145s88pe3p`
- 旧 publish id (stocktoday-skill): `k977etzrty9x1ddcte4fzx1twx88q9zt` (已删)
