# Smart Model Selector 🧠

[![ClawHub](https://img.shields.io/badge/ClawHub-smart--model--selector-blue)](https://clawhub.com/skills/smart-model-selector)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**让 AI 更聪明，从选择合适的模型开始！**

Smart Model Selector 是一个智能模型路由系统，根据你的任务内容自动选择最合适的 Qwen 模型，让每次对话都恰到好处。

---

## ✨ 特性

- 🎯 **自动选择** - 无需手动指定，AI 自动判断任务类型
- 🧠 **越用越聪明** - 记录每次对话效果，持续优化选择策略
- 💰 **成本优化** - 简单任务不用贵模型，最高可省 60%
- 📊 **透明可解释** - 告诉你为什么选这个模型
- 🔒 **本地存储** - 所有数据存在本地，保护隐私

---

## 🚀 安装

### 方式 1：通过 ClawHub（推荐）

```bash
clawhub install smart-model-selector
```

### 方式 2：手动安装

```bash
# 克隆仓库
git clone https://github.com/xuyun/smart-model-selector.git

# 复制到 skills 目录
cp -r smart-model-selector ~/.openclaw/workspace/skills/

# 启用技能
openclaw skills enable smart-model-selector
```

---

## 💬 使用

安装后自动激活，直接开始对话即可：

```
你：上海天气怎么样？
🧠 智能模型选择：默认模型（简单任务） → 使用 qwen3.5-plus

你：帮我设计一个高并发的系统架构
🧠 智能模型选择：检测到复杂推理任务 → 使用 qwen-max

你：用 Python 写个快速排序
🧠 智能模型选择：检测到代码相关任务 → 使用 qwen-coder-plus
```

### 可用命令

| 命令 | 说明 |
|------|------|
| `/model-stats` | 查看模型使用统计 |
| `/model-use <model>` | 手动指定模型 |
| `/model-rate <1-5>` | 评分反馈 |
| `/model-reset` | 重置当前任务 |
| `/model-help` | 查看帮助 |

---

## 📊 效果

### 模型分配（典型使用场景）

```
qwen3.5-plus     ████████████████████████████████  80% (简单任务)
qwen-max         ███████                           15% (复杂推理)
qwen-coder-plus  ██                                 5% (代码任务)
```

### 成本对比

| 场景 | 使用前 | 使用后 | 节省 |
|------|--------|--------|------|
| 每日对话 (100 次) | ¥20 | ¥8 | 60% |
| 月度成本 | ¥600 | ¥240 | 60% |

---

## 🎯 工作原理

### 1. 任务分析

系统分析你的任务内容，提取特征：
- 关键词匹配
- 任务长度
- 复杂度评估
- 历史相似度

### 2. 模型选择

根据分析结果选择模型：
- **代码任务** → `qwen-coder-plus`
- **复杂推理** → `qwen-max`
- **简单任务** → `qwen3.5-plus`

### 3. 反馈学习

记录每次对话效果：
- ✅ 一轮完成 → 强化选择
- ⚠️ 多轮未完成 → 调整策略
- ⭐ 用户高分 → 成功案例
- 👎 用户低分 → 优化方向

---

## 📁 项目结构

```
smart-model-selector/
├── SKILL.md                 # 技能说明
├── clawhub.yaml             # ClawHub 配置
├── README.md                # 项目说明
├── .gitignore              # Git 忽略文件
├── src/
│   └── model_selector.py   # 核心逻辑
├── hooks/
│   └── smart_model_selector.py  # Hook 入口
└── data/                   # 数据存储（自动生成）
    └── model_selection.db
```

---

## 🔧 配置

创建 `config.json` 自定义规则：

```json
{
  "default_model": "qwen3.5-plus",
  "auto_select": true,
  "show_reason": true,
  "custom_rules": [
    {
      "keywords": ["翻译", "translate"],
      "model": "qwen3.5-plus"
    }
  ]
}
```

---

## 📈 统计示例

```
/model-stats

📊 模型使用统计

总任务数：42
平均对话轮数：1.8
高质量任务比例：85%

各模型使用情况：
- qwen3.5-plus: 28 次，平均得分 88.5
- qwen-max: 10 次，平均得分 92.3
- qwen-coder-plus: 4 次，平均得分 95.0
```

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

- 💡 新功能建议
- 🐛 Bug 报告
- 📝 文档改进
- 🎨 规则优化

---

## 📄 许可证

MIT License

---

## 👤 作者

**许允** (xuyun)

---

## 🙏 致谢

- OpenClaw 社区
- ClawHub 平台
- Qwen 模型团队

---

**让 AI 更聪明，从选择合适的模型开始！🚀**

[![ClawHub](https://img.shields.io/badge/ClawHub-install-blue)](https://clawhub.com/skills/smart-model-selector)
