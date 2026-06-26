---
name: starmemo
version: 2.0.0
description: "智能记忆系统 v2.0 - 结构化记忆 + 知识库 + 启发式召回 + AI优化"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["python3"] },
      },
  }
---

# starmemo v2.0 - 智能记忆系统

## 核心特性

| 特性 | 说明 |
|:-----|:-----|
| 📝 **结构化记忆** | 因→改→待 格式，一目了然 |
| 📚 **知识库** | 自动提取知识点，长期积累 |
| 🔍 **启发式召回** | 智能判断何时召回，精准检索 |
| 🧠 **AI优化** | 结构化提取、压缩、知识抽取 |
| 🌐 **联网学习** | 知识不足时可联网补全 |
| 🇨🇳 **国内LLM** | 火山、通义、文心、DeepSeek等 |

---

## CLI 命令

```bash
# 保存记忆
python3 {baseDir}/v2/cli.py save --cause "原因" --change "做了什么" --todo "待办"

# 保存文本（自动提取结构）
python3 {baseDir}/v2/cli.py save --text "内容"

# 搜索
python3 {baseDir}/v2/cli.py search "关键词"

# 今日记忆
python3 {baseDir}/v2/cli.py show

# 知识库
python3 {baseDir}/v2/cli.py knowledge

# 配置
python3 {baseDir}/v2/cli.py config --show
```

---

## 触发时机

**主动保存当：**
- 用户分享重要信息
- 完成有价值的任务
- 学习新知识
- 用户说"记住"

**主动召回当：**
- 用户说"之前"、"上次"、"那个"
- 需要回顾历史

---

## 当前配置

- 模型：火山方舟
- AI优化：✅ 开启
- 联网学习：✅ 开启
- 持久化：✅ 开启
