---
name: persona-design
description: X 账号人设设计与声音校准：定位账号身份、提炼价值观与话题半径、建立声音标尺、划定边界与一致性检查
source:
  type: original
  repo: skills-repo/x-persona-operator
  path: skills/persona-design/SKILL.md
  version: 1.0.0
  updated: 2026-10-09
metadata:
  author: hope
  category: 社交媒体运营
  platform: X (Twitter)
  difficulty: 进阶
  version: 1.0.0
  created: 2026-10-09
tags:
  - persona
  - 人设
  - 声音校准
  - 品牌定位
  - voice
---

# Persona Design — 人设设计与声音校准

> 人设不是事后贴标签，是每条内容的滤镜。本技能帮你把"这个账号是谁"定清楚：身份、声音、边界、一致性检查，让 AI 产出的每条推文都"像同一个人发的"。

## 能力

- **身份定位**：区分真人放大 / 品牌人格 / 虚构 IP 三类，选对设定路径
- **声音标尺**：语气、自称、用词、句式、Emoji、争议话题、链接习惯——可复用的"声音指纹"
- **话题半径**：定垂直深度与跨界主线，避免"什么都聊"的杂货铺
- **边界划定**：敏感话题、不实信息、商业标注、负面互动 SOP
- **一致性检查**：每条发布前对照标尺，确认"换成别人发认不出是本号"

## 使用方式

在 Claude Code 中用 `/persona-design` 调用，或在对话中描述账号定位诉求。

```
/persona-design 帮我把"独立 AI 开发者"的人设定下来，偏犀利实用
/persona-design 给这个账号做一张声音标尺，受众是创业者和投资人
/persona-design 这个账号能不能聊加密货币？帮我划边界
```

## 工作流

1. **定身份**：走 persona-playbook 决策树 Q1（真人 / 品牌 / 角色）→ 选设定路径
2. **填标尺**：按 [../../references/persona-playbook.md](../../references/persona-playbook.md) §2 的维度表，落定"本账号设定"列
3. **划半径与边界**：Q3 信息增益 + §3 边界清单，写入运营笔记
4. **回归校验**：用一致性检查清单（§4）对历史内容抽样，找出漂移点

## 产出物

- 一份**人设卡**（身份 + 声音标尺 + 话题半径 + 边界 + 签名动作）
- 一份**一致性检查清单**，供 content-engine / engagement-ops 复用

## 适用场景

- 从零搭建一个新 X 账号的人设
- 账号运营一段时间后人设漂移，需要重新校准
- 多账号矩阵中区分不同账号的声音，避免串味

## 限制

- 人设定位、敏感话题立场、是否下场争论——最终由账号主拍板；本技能出方法论与检查，不做品牌 / 立场决策
- 声音标尺需随账号成长迭代，不是一锤定音
- 不虚构事实、不冒充真人；虚构 IP 须明确声明是角色号

## 与其它技能协作

- 用已定人设去写推文 → [../content-engine/SKILL.md](../content-engine/SKILL.md)
- 用已定人设去设计增长 → [../growth-tactics/SKILL.md](../growth-tactics/SKILL.md)
- 用已定人设去回应社区 → [../engagement-ops/SKILL.md](../engagement-ops/SKILL.md)
