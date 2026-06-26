---
name: tg-crawler
description: "Telegram 频道/群组舆情采集工具 v3.12。支持四种模式：hybrid（发现+回溯）、discover（仅频道发现）、backfill（仅消息回溯）、monitor（实时监控）。内置数据保留策略，自动清理过期数据，防止磁盘膨胀。"
user-invocable: true
allowed-tools:
  - exec
  - read
  - write
  - fabric_call
  - fabric_exec
  - web_search
  - web_fetch
  - process
license: internal
---

## 版本历史

> 每次迭代更新此表，按时间倒序。

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| **v3.12** | 2026-06-05 | 🔧 第五轮 Review 修复 (3 项)。P0: get_entity 短 FloodWait 重试后不回溯 (B16)、resume 误跳过 rate_limited/partial 频道 (B18)。P1: dry-run 过滤说明从 "backfill" 修正为 "discover" 关键词 (B17)。重构 _backfill_channels: get_entity 提取为重试包装器，移除笨重的内嵌 retry 逻辑 |
| **v3.11** | 2026-06-05 | 🚀 实战 Review 修复 (10 项)。P0: YAML 追加改用 dump 全量重写 (B13)、get_entity FloodWait + ChannelPrivateError 专用 catch (B14)、run_hybrid discover 后 load_targets 失败兜底 (B15)。P1: YAML 写入后校验 + 失败回滚 (D10)、追加前 .bak 备份 (D11)、asyncio disconnect 先于 loop.close (D12)。P2: targets_common.yaml 自动修复脚本、短 FloodWait 分级处理 |
| **v3.10** | 2026-06-05 | 🚀 三轮 Code Review 全面修复 (13 项)。P0: title 二次过滤/discover 阶段2.5 用生态词、`_parse_channel_from_link` UnboundLocalError、`run_backfill` 缺 rules→TypeError。P1: FloodWaitError 全局覆盖、`save_message` 原子去重 (INSERT OR IGNORE)、media_files 同事务写入。P2: `iter_messages` FloodWait 保底、`--purge-after-export` VACUUM、VACUUM<10MB 跳过。P3: `--skip-discover`/`--match-mode word|regex`/YAML 追加保留注释/monitor progress 写入/rstrip 清理 |
| **v3.9** | 2026-06-05 | 🧹 数据保留策略。新增 `--retention-days`（默认 90 天自动清理）、`--no-vacuum`、`--purge-after-export`。新增 `media_files` 表追踪媒体文件。每次运行结束后自动清理过期消息、媒体文件和断点记录。新增 `run_retention_cleanup()` 统一入口 |
| **v3.8** | 2026-06-04 | 🔧 backfill 发送者信息获取修复。新增 `--fetch-sender` 参数，通过 SenderCache（内存缓存） + 批量延迟策略安全获取发送者名称和用户名，避免 Flood Wait。新增 `database.update_senders_batch()` 延迟补充机制 |
| **v3.7** | 2026-06-03 | 🔒 failover 安全加固。failover 必须用专属 `code_acc{N}.txt`，禁止共用验证码；不可恢复错误（2FA/密码/AuthKey）不触发 failover；连接失败后自动 disconnect |
| **v3.6** | 2026-06-03 | P2: dry-run 模式。新增 `--dry-run`，不连接 TG 打印执行计划 |
| **v3.5** | 2026-06-03 | P3: 账号自动 failover。新增 `--failover` 参数，主账号 Flood Wait/凭证缺失时自动尝试后续账号 |
| **v3.4** | 2026-06-03 | P2: 数据库导出 CLI。新增 `--export`/`--export-format`/`--since`/`--until`/`--chats` 参数，支持 csv/json/markdown 三种格式导出 |
| **v3.3** | 2026-06-03 | P1: 搜索 Bot 结果 title 二次过滤。利用回溯阶段 `get_entity` 获取真实 title，不匹配的跳过 `iter_messages` |
| **v3.2** | 2026-06-03 | P1: hybrid 断点续传。新增 `channel_progress` 表 + `--no-resume` 参数 |
| **v3.1** | 2026-06-03 | P1: backfill 新频道相关性过滤。hybrid stage2 跳过 title/username 与关键词不匹配的新频道 |
| **v3.0** | 2026-06-03 | P0: discover/backfill 关键词分离、6 行业 targets 分文件、三账号代理隔离、SOCKS5 认证 |
| **v2.0** | 2026-06-03 | 三账号支持、TG Web 应急扫描、行业适配策略、羊毛频道预置、实战经验库 |
| **v1.0** | 2026-06-02 | Skill 化，四模式，71 频道，单账号 |
| **原型** | 2026-05-20 | 初始原型，66 外挂频道，backfill + monitor |

# TG 爬虫 Skill

基于 Telethon 的 TG 频道/群组消息采集与舆情监控工具。

## 触发条件

当用户提到以下任一意图时触发：
- "扫描TG"/"搜一下 TG"/"TG 上有没有 XX 外挂"
- "回溯 TG 消息"/"爬一下XX频道的消息"
- "发现XX相关的TG频道"/"找一下XX的TG群"
- "监控 TG 频道"
- 更广义的舆情扫描任务中需要 TG 数据源时

## ⚠️ 核心规则：行业适配（必读）

**TG 上不同行业的黑灰产分布在完全不同的频道生态中，搜索关键词必须根据目标行业调整。**

| 行业 | TG 搜索关键词 | 禁止用 |
|------|-------------|--------|
| 🎮 游戏 | 游戏名、外挂、辅助、破解 | 优惠券、漏洞单 |
| 🥛 快消/零售 | 优惠券、薅羊毛、漏洞、线报、Bug价、0元购 | 外挂、破解 |
| 💰 金融 | 套利、路子、代刷、水钱 | 优惠券、外挂 |
| 📱 App | 破解版、Mod、去广告、解锁 | 优惠券 |
| 💬 社交 | 交友、引流、号商、脚本、代聊 | 外挂 |
| ✈️ 航司 | 里程、积分、代订、机票诈骗、退改签 | 外挂 |
| 🚗 汽车 | 车贷、二手车、违章代办、改表 | 优惠券、外挂 |

**两步法通用模式：**

```bash
# 第1步：搜生态关键词 → 发现频道（用 discover 关键词）
# 第2步：在频道中搜品牌名 → 回溯消息（用 backfill 关键词）
python3 main.py --mode hybrid \
  --keywords "生态词1,生态词2" \
  --backfill-keywords "品牌名1,品牌名2" \
  --targets <行业profile> \
  --env ../config/.env
```

各行业两步法完整命令示例 → `references/industry-playbook.md`。

> 🛑 **何时放弃 TG 渠道**：目标行业是快消/传统零售/餐饮/医疗且 discover 阶段返回 0 频道 → 切到 `web_search`（微博/知乎/黑猫投诉）。

## 运行模式

| 模式 | 命令 | 说明 |
|------|------|------|
| **hybrid** | `--mode hybrid --keywords "词"` | 发现 + 回溯（推荐） |
| **discover** | `--mode discover --keywords "词"` | 仅发现频道 |
| **backfill** | `--mode backfill --limit 500` | 对已有频道回溯 |
| **monitor** | `--mode monitor` | 7×24 实时监听 |
| **export** | `--export results.csv` | 导出数据（不连 TG） |

## 参数速查

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--mode` | hybrid / discover / backfill / monitor | — |
| `--keywords` | discover 搜索关键词，逗号分隔 | — |
| `--backfill-keywords` | backfill 专属关键词，不传回退 `--keywords` | — |
| `--targets` | 配置文件路径 或 行业 profile (gaming/retail/social/airline/auto/all) | `../config/targets.yaml` |
| `--backfill-limit` | 单频道回溯消息条数 | 500 |
| `--account` | TG 账号 1/2/3 | 1 |
| `--failover` | 失败后尝试后续 N 个备用账号 | 0 |
| `--no-bots` | 禁用搜索 Bot | false |
| `--no-backfill-filter` | 禁用新频道相关性过滤 | false |
| `--no-resume` | 禁用断点续传 | false |
| `--fetch-sender` | 🆕 获取发送者用户名/名称（缓存+批量延迟防Flood Wait） | false |
| `--sender-batch-size` | 🆕 每批获取发送者数量 | 15 |
| `--sender-batch-delay` | 🆕 批次间延迟秒数 | 3.0 |
| `--dry-run` | 试运行：不连 TG，打印参数和频道数 | false |
| `--retention-days` | 🆕 数据保留天数，自动清理过期消息/媒体/断点记录 | 90 |
| `--no-vacuum` | 🆕 禁用清理后的 VACUUM 空间回收 | false |
| `--purge-after-export` | 🆕 导出完成后清空数据库和媒体文件（需确认） | false |
| `--skip-discover` | 🆕 hybrid 模式下跳过频道发现，仅回溯已有频道 | false |
| `--match-mode` | 🆕 匹配模式: substring(子串)/word(词边界)/regex | substring |
| `--export` | 导出文件路径（跳过采集） | — |
| `--export-format` | csv / json / markdown | csv |
| `--since` / `--until` | 导出时间范围 YYYY-MM-DD | — |
| `--chats` | 导出限定频道 (逗号分隔 username) | — |
| `--db` | 数据库路径 | `../data/crawler.db` |
| `--session` | Telethon session 名 | `tg_crawler` |
| `--password` | 2FA 密码 | — |
| `--log-level` | DEBUG / INFO / WARNING / ERROR | INFO |

## 配置文件

### .env（凭证 + 代理）

```ini
# 账号 1
TG1_API_ID=xxx
TG1_API_HASH=xxx
TG1_PHONE=+86xxx
TG1_PASSWORD=          # 2FA（可选）

# 账号 2
TG2_API_ID=xxx
TG2_API_HASH=xxx
TG2_PHONE=+86xxx

# 账号 3
TG3_API_ID=xxx
TG3_API_HASH=xxx
TG3_PHONE=+86xxx

# SOCKS5 代理（可选，每账号可独立）
# TG1_PROXY_HOST=45.xx.xx.1
# TG1_PROXY_PORT=1080
# TG2_PROXY_HOST=45.xx.xx.2
# TG2_PROXY_PORT=1080
```

- **代理优先级：** `TG{account}_PROXY_HOST` > `PROXY_HOST`（全局回退）
- 账号 1 支持向后兼容 `TG_API_ID` / `TG_API_HASH` / `TG_PHONE`
- Session 自动区分：`tg_crawler.session` / `tg_crawler_acc2.session` / `tg_crawler_acc3.session`
- 🆕 **发送者信息获取：** `FETCH_SENDER_INFO=true` 启用 / CLI `--fetch-sender` 临时启用（v3.8 新增，通过 SenderCache + 批量延迟策略防 Flood Wait）

### targets.yaml（频道列表）

放在 `config/`，格式参考 `references/targets-format.md`。按行业分文件：
- `targets_gaming.yaml` — 76 个游戏外挂频道
- `targets_retail.yaml` — 5 个羊毛频道
- `targets_common.yaml` — 118 个自动发现的跨行业频道
- `targets_social.yaml` / `targets_airline.yaml` / `targets_auto.yaml` — 空模板

## 验证码

```bash
# 命令行传入
python3 main.py --code "12345" --mode hybrid --keywords "游戏名"

# 文件读取（非交互环境）
python3 main.py --code-file /path/to/code.txt --mode hybrid --keywords "游戏名"

# 交互式输入（默认）
python3 main.py --mode hybrid --keywords "游戏名"
```

## 注意事项

1. **Flood Wait**：TG API 严格限速，单次避免过大 `--backfill-limit`
2. **Session 文件**：首次运行后生成，必须在 `scripts/` 目录下运行 `main.py`
3. **2FA**：账号开启二次验证需传 `--password`
4. **web_fetch 应急**：Flood Wait 阻塞时可用 `web_fetch https://t.me/s/{channel}?q={关键词}` 应急（限 ~20 条）
5. **私密群组**：需 `invite_link`，否则无法加入

## 数据保留策略（v3.9+）

| 机制 | 默认值 | 说明 |
|------|--------|------|
| 消息保留 | 90 天 | `--retention-days N` 调整，超期消息自动删除 |
| 媒体文件 | 关联删除 | 消息删除时关联的图片/视频同步清理 |
| 断点记录 | 同步清理 | `channel_progress` 的超期记录一并清理 |
| VACUUM | 自动执行 | 清理后自动回收磁盘空间，`--no-vacuum` 禁用 |
| 彻底清空 | 手动触发 | `--export results.csv --purge-after-export` 导出后清库 |

**设计原则**：
- 舆情数据的时效性天然有限（超过 90 天的历史消息情报价值极低）
- 自动清理避免 SQLite 数据库和 `data/media/` 无限膨胀
- 每次采集运行结束后执行清理，不影响采集性能

## 已知限制

| 限制 | 应对 |
|------|------|
| Flood Wait 全阻塞 | 换账号/等冷却/`--failover` 自动切；短FloodWait(<60s)自动重试 |
| web_fetch 只能 ~20 条 | 应急用，不是 backfill 替代 |
| 频道发现仅限公开频道 | 私密群需手动提供 `invite_link` |
| CPS 推广频道信息密度低 | 采样分析，不必全量回溯 |
| 子串匹配误报 | 用 `keyword_rules.match_mode=word` 减少误报 |
| discover 重复搜索 | 用 `--skip-discover` 跳过发现阶段 |
| YAML 追加丢失注释 | v3.11 起用 dump 全量重写，注释不再保留（优先保证文件正确性） |

## 相关文档

- 行业两步法详细命令 + 羊毛频道预置列表 → `references/industry-playbook.md`
- 代理池自建方案（VPS 对比 + Dante 脚本） → `references/proxy-pool-setup.md`
- targets 格式说明 → `references/targets-format.md`
- 完整架构设计 → `references/tg-crawler-architecture.md`
- 爬虫源码 → `scripts/`
