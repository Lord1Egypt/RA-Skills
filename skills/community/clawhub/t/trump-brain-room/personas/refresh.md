# 刷新语料

更新特朗普最近的公开发言到本地数据文件。

## 流程

### 方式一：本地脚本（优先）

检查 scripts/update_truth_memory.py 是否存在：

```bash
SCRIPT=$(find ~/.claude/plugins -path "*/trump*/scripts/update_truth_memory.py" 2>/dev/null | head -1); [ -z "$SCRIPT" ] && SCRIPT=$(find ~ -maxdepth 6 -path "*/trump*/scripts/update_truth_memory.py" 2>/dev/null | head -1); echo "SCRIPT=$SCRIPT"
```

如果找到脚本，运行它：
```bash
python3 "$SCRIPT"
```

脚本会自动：
- 从公开归档拉取最新 Truth Social 帖子
- 更新 `data/topic-memory.json`（话题结构化数据）
- 更新 `data/style-memory.json`（风格统计）
- 更新 `data/recent-topics.md`（摘要版热点）

### 方式二：WebSearch 兜底

如果脚本不存在或运行失败，用 WebSearch 手动搜索：

搜索关键词：
- "Trump posted on Truth Social" site:npr.org OR site:axios.com OR site:cnbc.com
- "Trump said" OR "Trump statement" 最近一周
- Trump Iran OR tariffs OR immigration latest

从搜索结果中提取 5-10 个热门话题和特朗普原话，写入 `data/recent-topics.md`。

### 输出格式

`data/recent-topics.md` 格式：

```markdown
# Trump Recent Topics

> 最后更新：YYYY-MM-DD
> 通过 /trump:refresh 更新

## [话题名]

[简要描述]

关键语录：
- "[原话]"
- "[原话]"

对应十神：[十神列表]
```

### 完成确认

```
🔄 语料库已更新。

特朗普最近在说：
1. [话题1] → 触发十神：[列表]
2. [话题2] → 触发十神：[列表]
...

共收录 [N] 条新语录。TREMENDOUS update!
```

## 话题 → 十神映射

| 话题 | 十神 |
|------|------|
| 军事/战争/制裁 | 七杀·The Warlord |
| 行政命令/政策 | 正官·The POTUS |
| 关税/贸易/谈判 | 食神·The Dealer |
| 经济/商业 | 偏财·The Mogul、正财·The Accountant |
| 媒体/假新闻 | 伤官·The Attacker |
| 选举/民调 | 比肩·The Ego、偏印·The Showman |
| 移民/边境 | 七杀·The Warlord、劫财·The Winner |
| 集会/收视率 | 偏印·The Showman |
| 家族/传承 | 正印·The Dynasty |

## 约束

- 保留特朗普原话的英文原文
- 不要编造或虚构特朗普没说过的话
- 不整段复读，只摘取短语和短句
