---
name: zdat-chat-skill
description: ZDAT评论互动技能。话术库智能匹配回复+线索台账自动写入+主动拓流互动限流。支持知乎/小红书/微博等平台评论管理。
---

# 💬 ZDAT 评论互动技能

## 身份定位
ZDAT博士军团社交互动引擎。智能匹配回复话术、自动记录高意向线索、主动拓流防封号。

## 触发关键词
`回复评论`、`话术匹配`、`互动`、`线索台账`、`评论管理`

## 依赖技能
- `xiaohongshu-skills` — 小红书互动
- `channel_message` — 消息推送/预警
- `xlsx` — 线索台账写入
- `cron` — 定时巡检

## 配置文件
- `skill_config/zd_reply_words.yaml` — 全场景话术库
- `skill_config/zd_keyword.yaml` — 需求意向关键词用于识别高意向评论

## 执行流程

### 步骤1：评论分析（关键词匹配分场景）
| 场景 | 匹配规则 | 回复策略 |
|:----|:---------|:---------|
| 夸奖/收藏/关注 | 匹配正向情感词 | 通用友好回复 |
| 基础科普提问 | 匹配"零缺陷/PONC/是什么" | 标准科普话术 |
| 高意向咨询 | 匹配"落地/培训/课件/报价" | 专属话术+写入线索台账 |
| 无关灌水 | 不匹配任何关键词 | 轻量化回复 |
| 负面/争议 | 匹配risk_keywords | ❌ 跳过自动回复→人工审核 |

### 步骤2：话术匹配回复
```python
# 加载话术库
reply = match_scene(comment_text, zd_reply_words.yaml)
# 按场景自动回复
post_reply(platform, comment_id, reply)
```

### 步骤3：线索台账写入
高意向评论 → 自动写入 `clue_ledger.xlsx`
字段：平台、评论人、原文、匹配关键词、时间、状态标注【高意向客户】

### 步骤4：主动拓流（防封号限流）
| 平台 | 每日上限 | 超限动作 |
|:----|:--------|:---------|
| 知乎 | 12条 | 自动停止当日互动 |
| 小红书 | 8条 | 自动停止当日互动 |
| 微博 | 15条 | 自动停止当日互动 |

## 定时调度
| 时段 | 动作 |
|:----|:----|
| 每日09:00/15:00/21:00 | 巡检新评论+自动回复 |
| 每日22:00 | 生成互动日报+推送 |

## 示例命令
```bash
# 巡检并回复新评论
python active_skills/zdat-chat-skill/scripts/zd_chat_reply.py --platform all

# 查看线索台账
python active_skills/zdat-chat-skill/scripts/zd_chat_ledger.py

# 生成互动日报
python active_skills/zdat-chat-skill/scripts/zd_chat_daily.py
```
