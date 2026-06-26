# Skill Combo - 技能组合器

> 让技能组合产生 1+1>2 的效果

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.ai/skills/skill-combo)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 Skill 定位

**多技能协同引擎** - 允许同时启用多个技能，让它们相互协作、优势互补，完成复杂任务

---

## ⚡ 快速开始

### 安装

```bash
clawhub install skill-combo
```

### 触发词

- `/combo` - 标准触发
- `/skill+` - 快捷触发
- `技能组合` - 中文触发

### 组合语法

**方式 1：加号连接**
```
/thinking+heart
```

**方式 2：逗号分隔**
```
/combo thinking,heart
```

**方式 3：空格分隔**
```
/combo thinking heart
```

---

## 📝 使用示例

### 示例 1：分析 + 提醒

```
/thinking+heart 帮我分析一下这个项目，30 分钟后提醒我进度
```

### 示例 2：分析 + 话术

```
/thinking+pua 老板让我加班，我怎么回复比较好？
```

### 示例 3：三技能组合

```
/combo thinking,heart,pua 我要去相亲，帮我分析注意事项，见面前提醒，教我怎么聊天
```

---

## 🏗️ 核心功能

### 1. 技能加载

自动识别和加载多个技能：
- thinking-skill - 深度思考
- temp-heartbeat - 临时心跳
- pua-skill - 沟通话术
- 以及所有已安装的技能

### 2. 能力映射

分析每个技能的能力，确定分工：
- 谁负责分析
- 谁负责提醒
- 谁负责优化

### 3. 执行编排

协调多个技能的执行顺序：
- 顺序执行
- 并行执行
- 条件执行

### 4. 结果整合

将多个技能的输出整合成统一结果：
- 分层展示
- 融合展示
- 摘要展示

---

## 🎯 适用场景

| 场景 | 推荐组合 | 说明 |
|------|----------|------|
| **复杂任务** | thinking+ 执行技能 | 先分析后执行 |
| **定时任务** | thinking+heart | 分析 + 定时提醒 |
| **沟通场景** | thinking+pua | 分析 + 话术优化 |
| **学习场景** | thinking+search | 分析 + 搜索 |

---

## 🚀 版本记录

### v1.0.0 (2026-04-04)
- ✅ 初始版本发布
- ✅ 技能组合加载
- ✅ 能力映射
- ✅ 执行编排
- ✅ 结果整合

---

## 📄 许可证

MIT License

---

**Skill Combo · 让技能组合产生 1+1>2 的效果**
