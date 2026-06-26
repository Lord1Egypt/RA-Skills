---
name: buddy-gacha
description: "Buddy 抽卡体验。基于 Claude Code 原版 Buddy 系统的抽卡，让用户体验抽到什么稀有度的电子宠物。触发词：抽卡、buddy、电子宠物抽卡。"
metadata: { "openclaw": { "emoji": "🎰", "requires": { "bins": ["python3"] } } }
---

# Buddy 抽卡

基于 Claude Code 原版 Buddy 系统的抽卡体验。

## 功能

根据你的用户名（或指定名字）抽卡，看看你能抽到什么 Buddy！

- 18 种物种（duck, cat, dragon, ghost 等）
- 5 档稀有度（★ 到 ★★★★★）
- 闪光系统（1% 概率）
- 帽子系统

## 使用方式

直接运行：

```bash
python3 buddy.py [名字]
```

### 示例

```bash
# 用系统用户名抽卡
python3 buddy.py

# 用指定名字抽卡
python3 buddy.py 豪哥
python3 buddy.py 张三
```

## 稀有度概率

| 稀有度 | 概率 |
|--------|------|
| ★ 普通 | 60% |
| ★★ 优秀 | 25% |
| ★★★ 稀有 | 10% |
| ★★★★ 史诗 | 4% |
| ★★★★★ 传说 | 1% |

闪光概率：1%（独立于稀有度）

## 原理

使用 Claude Code 原版 Mulberry32 PRNG 算法，相同用户名永远抽到同一只 Buddy（确定性随机）。

## 文件

- `buddy.py` - 抽卡脚本
- `SKILL.md` - 本说明文件