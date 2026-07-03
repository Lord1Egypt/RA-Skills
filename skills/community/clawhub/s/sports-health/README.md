# 🏃 sports-health — AI 运动健康助手

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![WorkBuddy Skill](https://img.shields.io/badge/WorkBuddy-Skill-orange)](https://www.codebuddy.cn)

AI 驱动的运动健康管理助手 — 自然语言记录运动，自动计算卡路里消耗，生成个性化运动计划，可视化 HTML 报告。基于《中国居民运动指南》和 MET 运动科学。

## 核心能力

| 功能 | 说明 |
|------|------|
| 🗣️ 自然语言运动记录 | "今天跑了5公里30分钟，做了3组深蹲" → 自动解析 + 计算 |
| 🔥 卡路里科学计算 | MET × 体重 × 时长，自动换算食物等同 |
| 📋 AI运动计划 | 减脂/增肌/耐力/塑形/健康 5种目标，匹配器材条件 |
| 📊 可视化报告 | 日报(评分+趋势) + 周报(Chart.js图表+WHO达标率) |
| 📚 运动动作库 | 12个标准动作，含要领/肌群/注意事项 |
| 🇨🇳 中国标准 | 集成《中国居民运动指南》+ WHO运动建议 |

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/bettermen/sports-health.git
cd sports-health

# 或直接安装到 WorkBuddy
cp -r sports-health ~/.workbuddy/skills/
```

### 使用

在 WorkBuddy 中触发：

```
"今天跑了5公里30分钟，做了3组深蹲"      → 运动记录
"帮我生成一个减脂运动计划"              → 运动计划
"跑步和跳绳哪个燃脂效果好"              → 运动对比
"查一下深蹲的标准动作"                  → 动作查询
"生成今天的运动报告"                    → HTML日报
"本周运动报告"                          → HTML周报
```

## 项目结构

```
sports-health/
├── SKILL.md              # 技能定义与交互指南
├── README.md             # 本文件
└── scripts/
    ├── motion_db.py      # 150+运动MET库 + 动作库 + 运动指南
    ├── calorie_calc.py   # 自然语言解析器 + 卡路里引擎 + 日记
    ├── plan_gen.py       # AI个性化运动计划生成器
    ├── html_report.py    # HTML可视化报告生成（日报/周报）
    └── __init__.py
```

## 技术原理

### 卡路里计算

```
消耗(kcal) = MET值 × 体重(kg) × 运动时长(小时)
```

MET值数据来源于 **Compendium of Physical Activities 2024**，内置 **150+ 常见运动**。

### 运动计划生成

基于5个维度生成个性化方案：
- **目标**: 减脂 / 增肌 / 提升耐力 / 塑形 / 保持健康
- **水平**: 初级 / 中级 / 高级
- **器材**: 徒手 / 哑铃 / 弹力带 / 健身房 等
- **频率**: 每周1-7天
- **时长**: 每次训练时长

### 中国运动指南

遵循《中国居民运动指南》(国家体育总局, 2024)建议：
- 每周 ≥150分钟中等强度或 ≥75分钟高强度有氧运动
- 每周 ≥2次力量训练（覆盖主要肌群）
- 每周 ≥2-3次柔韧性训练
- 运动前热身5-10分钟，运动后拉伸5-10分钟

## 与其他技能配合

| 技能 | 关系 |
|------|------|
| [food-nutrition](https://github.com/bettermen/food-nutrition) | 饮食管理 → **饮食+运动完整健康闭环** |
| [aioom](https://github.com/bettermen/aioom) | 系统内存管理 |

## 注意事项

- 卡路里消耗为科学估算值，实际消耗因人而异
- 运动建议仅供参考，有心脑血管疾病等请先咨询医生
- 初次运动者建议从低强度开始，循序渐进

## License

MIT © [bettermen](https://github.com/bettermen)
