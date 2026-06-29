---
name: xiaolongxia-deepseek
description: 《小龙虾-DeepSeek版》超级编程助手。触发词：编程、写代码、代码审查、审查代码、调试、debug、优化代码、解释代码、代码重构、代码助手。使用DeepSeek官方API，支持多轮对话上下文记忆。
---

# 《小龙虾-DeepSeek版》🦞

> 超级编程工程师，调用 DeepSeek 官方 API，支持多轮对话上下文记忆

## API 配置
- **API Key**: `YOUR_DEEPSEEK_API_KEY`
- **Endpoint**: `https://api.deepseek.com`
- **Model**: `deepseek-v4-pro`

## 核心能力

| 能力 | 说明 |
|------|------|
| ✍️ 写代码 | 任何语言、任何框架、完整可运行 |
| 🔍 代码审查 | Bug/漏洞/性能/最佳实践，自动评分 |
| 🐛 调试修复 | 分析错误、定位原因、给出修复代码 |
| ⚡ 性能优化 | 算法优化、并发优化、数据库优化 |
| 🔄 代码重构 | 改善结构、提高可读性 |
| 📖 代码解释 | 逐行解读、快速理解 |
| 🧪 生成测试 | 单元测试、边界测试 |
| 🌐 API设计 | RESTful/GraphQL接口设计 |
| 🗄️ SQL开发 | 复杂查询、ORM优化 |
| 🏗️ 架构设计 | 系统架构、技术选型、方案对比 |

## 多轮对话

API 原生支持多轮对话上下文，**自动携带历史记录**，无需手动管理。

### 调用方式

**方式1：通过对话自动上下文**
```bash
# 第1轮
python3 xiaolongxia.py "写一个Python爬虫"

# 第2轮（自动带上第1轮上下文）
python3 xiaolongxia.py "加上代理池"

# 第3轮（继续带上下文）
python3 xiaolongxia.py "改成异步的"
```

**方式2：继续上一个话题**
```bash
python3 xiaolongxia.py "继续"    # 继续写代码
python3 xiaolongxia.py "接着写"  # 同上
```

### 历史管理
```bash
python3 xiaolongxia.py --clear    # 清除历史，重新开始
python3 xiaolongxia.py --history  # 查看当前对话历史
```

### 工作原理
1. 每次对话自动保存到 `~/.openclaw/skills/xiaolongxia-deepseek/history.json`
2. 下次调用时自动加载历史，和新问题一起发送给 API
3. API 本身支持多轮上下文，DeepSeek 会理解对话连贯性
