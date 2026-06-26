# TG 爬虫 — 架构与模块说明

> 供小黑在调度时了解爬虫内部模块，非日常使用文档。

## 模块概览

| 模块 | 文件 | 职责 |
|------|------|------|
| 主入口 | `main.py` | CLI 参数解析 + 4 种模式调度 |
| 配置加载 | `config_loader.py` | YAML 解析 + 动态追加 + identifier 转换 |
| 频道发现 | `channel_discoverer.py` | TG API (SearchRequest) + 搜索 Bot (xbso1/jisou) 三路发现 |
| 关键词过滤 | `keyword_filter.py` | OR/AND 模式匹配 |
| 消息监控 | `monitor.py` | 事件监听 + 媒体下载 + Flood wait 重试 |
| 数据库 | `database.py` | SQLite 异步存储 + 去重 |
| 去重引擎 | `deduplicator.py` | LRU 内存缓存 + DB 唯一键双层去重 |

## 运行流程 (hybrid 模式)

```
main.py (parse args)
  ├─ 加载 .env → api_id, api_hash, phone
  ├─ 创建 Telethon client (session)
  ├─ client.start() → 登录验证
  │
  ├─ Stage 1: ChannelDiscoverer.discover(keywords)
  │   ├─ _discover_via_tg_search(kw)     → SearchRequest API
  │   └─ _discover_via_search_bot(bot,kw) → xbso1 & jisou Bot
  │   → 去重合并 → 追加到 targets.yaml
  │
  ├─ Stage 2: Backfill
  │   ├─ load_targets() → get_target_identifiers()
  │   ├─ KeywordFilter 初始化
  │   └─ 对每个 identifier:
  │       ├─ client.get_entity(id)
  │       ├─ client.iter_messages(entity, limit=N)
  │       ├─ keyword_filter.match(text)
  │       └─ db.save_message()  ← 自动去重
  │
  └─ Stage 3: Summary
      └─ db.get_stats() → 输出统计
```

## Flood Wait 处理

TG API 严格限速，触发 FloodWaitError 后：

1. 等待 `error.seconds + 2` 秒后重试
2. 如果重试仍失败，跳过该目标继续下一个
3. Flood wait 是全局的（同 session + 同 IP），所有后续请求都会受影响

**缓解策略：**
- 搜索 Bot 调用间隔 3 秒
- 频道回溯间隔 1.5 秒
- 加入频道间隔 2-4 秒（随机）
- 关键字搜索间隔 1.5 秒

## 数据库模型

```sql
messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  msg_id INTEGER NOT NULL,       -- TG 消息 ID
  chat_id INTEGER NOT NULL,      -- 来源频道 ID
  chat_title TEXT,               -- 频道名称
  chat_username TEXT,            -- 频道 username
  sender_id INTEGER,             -- 发送者 ID
  sender_username TEXT,          -- 发送者 username
  sender_name TEXT,              -- 发送者名字
  text TEXT,                     -- 消息文本 (max 10000 chars)
  media_type TEXT,               -- photo/video/audio/image/document
  media_path TEXT,               -- 媒体文件本地路径
  msg_date TIMESTAMP,            -- 消息发送时间
  collected_at TIMESTAMP,        -- 采集时间
  matched_keywords TEXT,         -- JSON array of matched keywords
  UNIQUE(chat_id, msg_id)        -- 去重约束
)
```

## 常见问题

**Q: Session 文件在哪？**
A: 运行目录下，默认文件名 `tg_crawler.session`。

**Q: 怎么换 TG 账号？**
A: 删除 session 文件 + 修改 `.env` 中的 TG_API_ID/TG_API_HASH/TG_PHONE。

**Q: 私密群组怎么加入？**
A: targets.yaml 中配置 `invite_link` 字段，monitor 模式启动时会自动加入。注意邀请链接可能过期。

**Q: 中文关键词匹配不准？**
A: 当前是简单的子串匹配 (`if keyword in text`)，不支持分词。对中文关键词建议使用短词或组合词。

**Q: 为什么搜快消品牌搜不到任何频道？**
A: 快消/零售行业的 TG 黑灰产不在破解/外挂频道，而在羊毛优惠线报频道。需要先搜「优惠券/薅羊毛/线报」等生态关键词发现羊毛频道，再回溯品牌名。详见 SKILL.md > 行业适配策略。

## 行业适配架构

### 双轨扫描模型

```
舆情扫描请求
├─ 判断目标行业
│   ├─ 🎮 游戏/App → TG 关键词 = 产品名 + 外挂/辅助/破解
│   ├─ 🥛 快消/零售 → TG 关键词 = 优惠券/薅羊毛/线报/漏洞单
│   ├─ 💰 金融 → TG 关键词 = 套利/路子/代刷
│   └─ ⚙️ 其他 → web_search 优先，TG 可选
│
├─ TG 轨道
│   ├─ discover → backfill（两步法）
│   └─ 失败降级 → web_fetch t.me/s 应急扫描
│
└─ 备用轨道（TG 不可用时）
    ├─ web_search 多关键词组合
    ├─ 社交媒体直搜（微博/知乎/黑猫投诉）
    └─ web_fetch 目标页面
```
