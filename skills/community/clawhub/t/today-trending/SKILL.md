---
name: "today-trending"
description: "获取今日微博、抖音、百度热搜排行榜 - 实时热门话题一站式查询"
metadata: { "openclaw": { "emoji": "🔥", "requires": { "bins": ["python"] } } }
---

# 今日热榜 (Today Trending)

一键拉取微博 / 抖音 / 百度 实时热搜(各 TOP 20),返回 agent 友好的 JSON。

## 用法

```bash
# 默认:三平台并发(零参数)
python ~/.openclaw/skills/today-trending/scripts/trending.py

# 单平台(2026-09-12 加)
python ~/.openclaw/skills/today-trending/scripts/trending.py --platform {weibo|douyin|baidu}

# 帮助
python ~/.openclaw/skills/today-trending/scripts/trending.py --help
```

## 输出格式(JSON schema)

```json
{
  "meta": {
    "fetched_at": "2026-09-08T17:26:09+08:00",
    "elapsed_ms": 301,
    "platforms": {"weibo": "ok", "douyin": "ok", "baidu": "ok"}
  },
  "weibo":  [{"rank": 1, "word": "...", "hot_value": 168.47, "url": "..."}, ...20 条],
  "douyin": [...20 条],
  "baidu":  [...20 条]
}
```

| 顶层 key | 说明 |
|---|---|
| `meta.fetched_at` | ISO 8601,东八区 |
| `meta.elapsed_ms` | 三平台并发耗时(ms) |
| `meta.platforms` | 各平台状态:`"ok"` 或 `"failed"` |
| `<平台>` | 该平台 TOP 20,失败时为 `[]` |

每条热搜:`rank`(1-20)、`word`(热搜词)、`hot_value`(热度,单位**万**)、`url`(搜索链接)。

## 行为约定

- 三平台并发抓取(asyncio.gather),整次 200-400ms
- stdout 纯 JSON,失败信息走 stderr
- 平台失败不阻断其它平台
- 不带 `--platform` 三平台都抓;带则单平台

## 人类可读输出模板

**拿到 JSON 后,严格按这个模板渲染**。不要 dump JSON,不要再参考其他章节字段说明。

```markdown
# 🔥 今日三平台热榜 · {YYYY-MM-DD} {HH:MM} 抓取

## {类目 1:基于当日内容灵活命名}

- 🥇 **微博#1 / 抖音#1 / 百度#1** ·「热搜词」— 一句话短评 🕯️
- 🏀 **抖音#5 / 百度#13** ·「中国女篮」— 短评 💪

## {类目 2:自命名}

- 💰 **百度#1** ·「受贿 1.48 亿 金湘军一审死缓」— 亿级大案开局 ⚡
- 🏛️ **百度#9** ·「应急管理部原部长王祥喜被双开」— 又一虎落马 🐅

## {类目 3,4,5 ...}

- ...

## 📌 一句话总结

> **核心主线 1 + 核心主线 2 + 核心主线 3。**

---

📊 **数据快照**:三平台各 20 条,共 {N} 条,跨平台共识 {X} 条,辟谣类 {Y} 条。

要哪条详情链接直接告诉我,贴完整 URL。
```

### 模板要点

- **类目不固定**,按当日内容灵活命名,2-6 字 + 1 个 emoji
- 类目 < 2 条并入相邻;> 10 条拆细
- 每条短评 10-25 字,带 1-2 个 emoji
- 一句话总结 1-3 分句,抓核心主线
- emoji 适度,移动端扫读友好,不堆砌
- 出现重大新热点(自然灾害、突发事故)可临时加新类目

### 字段填充

| 字段 | 来源 | 备注 |
|------|------|------|
| 抓取时间 | `meta.fetched_at` | `YYYY-MM-DD HH:MM` |
| 跨平台共振 | 三平台至少两个出现(同/近义) | 不强求字字一致,LLM 自判 |
| 分类 | LLM 灵活 | 不强求"反腐/财经/国际/体坛/娱乐/季节/辟谣"这套 |
| `平台#N` | `<平台>[N-1]` | N 是 1-20 |
| 一句话短评 | LLM 总结 | 10-25 字 |
| 一句话总结 | LLM 自己提炼 | 1-3 个分句 |

## Agent 工作流

1. 跑 `trending.py` 拿 JSON
2. 解析三平台数据,识别跨平台共振
3. 按当日实际内容灵活分组命名
4. 写一句话总结
5. 输出给用户,不再附带原始 JSON

要哪条详情链接直接告诉我,贴完整 URL。