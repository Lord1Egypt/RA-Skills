---
name: video_finder_feedback
description: "观影后反馈闭环：提醒用户给反馈（非强制）、根据反馈加权标签和作者、低权重标签自动清理。触发：反馈、评价、觉得怎么样、好看吗"
---

# feedback — 反馈闭环与标签加权

提醒用户给反馈（非强制），根据反馈维护带权重的标签和作者列表，低权重自动淘汰。

## 前置条件

- **称呼约定**：`{{{user}}}` 为占位符
- **依赖**：`video_finder_preferences`（读写 `preferences.json`）
- **历史文件**：`./history.md`

## 触发时机

下载完成后，隔一段时间（如下次对话或几小时后），**轻量提醒一次**：

```
{{{user}}}，对了，上次那个《xxx》看了吗？觉得怎么样可以说说，我记一下喜好～
```

- 用户给了反馈 → 走反馈处理
- 用户忽略 / "再说" / 转移话题 → **不追问**，结束

---

## 反馈处理

| 用户反馈 | 操作 |
|---|---|
| 好看/不错/喜欢 | 提取片中标签和作者，每项 **+2 权重** |
| 不好看/不喜欢 | 提取相关标签和作者，每项 **-2 权重** |
| 还行/一般 | 标签权重不变，仅记录 |
| 具体指出哪里好/不好 | 提取具体关键词，精准 +2/-2 |

## 标签加权系统

`preferences.json` 中每个 tag 带权重，替代原来的纯列表：

```json
{
  "tag_weights": {
    "amateur": 12,
    "homemade": 10,
    "natural tits": 8,
    "euro": 7,
    "blonde": 6,
    "cosplay": 5,
    "young": 5,
    "big tits": 4,
    "petite": 3,
    "outdoor": 2,
    "hospital": 1
  },
  "author_weights": {
    "CreatorName": 4,
    "AuthorName": 2
  }
}
```

### 权重规则

| 事件 | 权重变化 |
|------|---------|
| 用户喜欢某标签 | +2 |
| 用户不喜欢某标签 | -2 |
| 搜索时该标签命中（被视频包含且用户没说不喜欢） | +1（被动增益，search.md Layer 3 Step 5） |
| 每次搜索会话结束 | 全部 tag_weights 衰减 -1（自然老化） |
| 权重 ≤ 0 | **自动删除** |
| 新标签首次出现 | 初始权重 = 1 |

### 衰减与淘汰

每次搜索会话结束（或反馈处理完），先执行被动增益，再全局衰减：

```
# 被动增益（由 search.md 产出）
for tag in 本次搜索命中标签:
  tag_weights[tag] += 1

# 全局衰减
for tag in tag_weights:
  tag_weights[tag] -= 1
  if tag_weights[tag] <= 0:
    delete tag_weights[tag]        ← 权重归零或负数，清除
  if tag_weights[tag] <= 2 && tag 未在本次搜索结果中出现:
    delete tag_weights[tag]        ← 冷门低权重标签也清除
```

> 衰减机制替代了计数器：活跃标签被持续增益维持高权重，冷门标签自然衰减归零。

### 权重对搜索的影响

搜索时，`tag_weights` 替换原来的 `positive_tags`/`negative_tags`：

- Layer 1 Query Rewrite：取权重 ≥ 3 的标签参与查询扩展
- Layer 3 Result Merge：评分时用权重值代替固定加分（见 search.md）

---

## preferences.json 更新

标签加权字段替换旧的 `positive_tags` / `negative_tags`：

```json
{
  "...原有字段不变...": "...",
  "tag_weights": { "amateur": 12, "homemade": 10, ... },
  "author_weights": { "CreatorName": 4, ... }
}
```

> `exclude_tags` 保留为硬排除列表，不受权重影响。`negative_tags` / `positive_tags` 废弃，合并到 `tag_weights`。

## history.md 记录格式

```markdown
## 2026-07-06
- [Passionate sex of real amateur couple](url) — XVideos，1080p，445MB
  → 反馈：👍 不错，女优身材好（tag_weights: natural tits +2 → 10, euro +2 → 9, amateur +1 → 13）
```

