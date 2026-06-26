# starmemo v2.0 · OpenClaw 智能记忆系统

![Version](https://img.shields.io/badge/Version-2.0.0-blue)
![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-brightgreen)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

专为 OpenClaw 打造的**智能记忆系统**，融合结构化记忆、知识库、启发式召回与 AI 优化，让你的 AI 助手**越用越懂你**。

---

## ✨ v2.0 核心特性

| 特性 | 说明 |
|:-----|:-----|
| 📝 **结构化记忆** | 因→改→待 格式，一目了然 |
| 📚 **知识库系统** | 自动/手动提取知识点，长期积累 |
| 🔍 **启发式召回** | 智能判断何时召回，精准检索 |
| 🧠 **AI 优化** | 自动提取结构、压缩、知识抽取 |
| 🌐 **联网学习** | 知识不足时可联网补全 |
| 🇨🇳 **国内 LLM** | 支持火山方舟、通义千问、文心一言等 7 种模型 |

---

## 🆚 对比 v1.0

| 特性 | v1.0 | v2.0 |
|:-----|:-----|:-----|
| 记忆格式 | 原文+摘要 | ✅ 因→改→待 结构化 |
| 知识库 | ❌ | ✅ 自动/手动提取 |
| 索引系统 | ❌ | ✅ 自动索引更新 |
| 召回机制 | 手动搜索 | ✅ 启发式自动判断 |
| AI 处理 | 压缩摘要 | ✅ 结构化提取+知识抽取 |

---

## 📦 安装

```bash
# 通过 skillhub 安装
skillhub install starmemo

# 或手动安装
git clone https://clawhub.ai/nandujia/starmemo.git
cp -r starmemo ~/.openclaw/workspace/skills/
```

**依赖**：首次运行自动安装 `requests>=2.31.0`

---

## 🚀 快速开始

### 1. 配置 LLM

```bash
# 查看当前配置
python3 v2/cli.py config --show

# 设置模型和 API Key
python3 v2/cli.py config --llm huoshan --key YOUR_API_KEY

# 开启持久化（重启不丢失）
python3 v2/cli.py config --persist true
```

### 2. 保存记忆

```bash
# 结构化保存
python3 v2/cli.py save --cause "原因" --change "做了什么" --todo "待办"

# 文本保存（自动提取结构）
python3 v2/cli.py save --text "今天学习了 Python 装饰器，用于修改函数行为"
```

### 3. 搜索记忆

```bash
python3 v2/cli.py search "关键词"
```

### 4. 查看记忆

```bash
# 今日记忆
python3 v2/cli.py show

# 知识库
python3 v2/cli.py show --knowledge
```

---

## 📖 完整命令

| 命令 | 功能 | 示例 |
|:-----|:-----|:-----|
| `save` | 保存记忆 | `python3 v2/cli.py save --text "内容"` |
| `search` | 搜索记忆 | `python3 v2/cli.py search "关键词"` |
| `show` | 显示记忆 | `python3 v2/cli.py show` |
| `list` | 列出文件 | `python3 v2/cli.py list` |
| `config` | 配置管理 | `python3 v2/cli.py config --show` |
| `knowledge` | 知识库管理 | `python3 v2/cli.py knowledge --add "标题\|内容"` |
| `process` | 完整流程 | `python3 v2/cli.py process "文本"` |

---

## 🤖 支持的 LLM

| 厂商 | 标识 | 模型 |
|:-----|:-----|:-----|
| 火山方舟 | `huoshan` | doubao-seed-code-preview |
| 阿里通义千问 | `tongyi` | qwen-turbo |
| 百度文心一言 | `wenxin` | ernie-lite-8k |
| 深度求索 | `deepseek` | deepseek-chat |
| 智谱 AI | `zhipu` | glm-4-flash |
| 讯飞星火 | `xinghuo` | generalv3.5 |
| 腾讯混元 | `hunyuan` | hunyuan-lite |

---

## 🗂️ 存储结构

```
starmemo/
├── v2/                    # v2.0 核心代码
│   ├── cli.py             # CLI 接口
│   ├── core.py            # 核心引擎
│   ├── storage.py         # 存储层
│   ├── ai_processor.py    # AI 处理
│   └── recall.py          # 启发式召回
├── memory/                # 记忆数据
│   ├── daily/             # 每日记忆
│   ├── knowledge/         # 知识库
│   ├── archive/           # 归档
│   ├── daily-index.md     # 日期索引
│   └── knowledge-index.md # 知识索引
├── cli.py                 # v1 CLI（兼容）
├── starmemo.py            # v1 核心（兼容）
└── SKILL.md               # 技能说明
```

---

## 📝 记忆格式

### 每日记忆

```markdown
## [14:30] 学习
- **因**：用户想了解 Python 装饰器
- **改**：学习了装饰器的基本用法和常见模式
- **待**：实践装饰器项目
```

### 知识库

```markdown
# Python 装饰器

> 来源：对话提取
> 时间：2026-03-10 14:30

装饰器用于修改函数行为，常见模式包括...
```

---

## 🔄 工作流程

```
用户消息
    ↓
1. 启发式判断 → 需要召回？
    ↓ 是                    ↓ 否
2. 搜索记忆/知识库      3. AI 提取结构
    ↓                        ↓
4. 记忆足够？           保存到 daily/
    ↓ 是        ↓ 否         ↓
  直接回答    澄清提问     提取知识点到 knowledge/
                             ↓
                         更新索引
```

---

## ⚙️ 配置选项

```bash
# 查看配置
python3 v2/cli.py config --show

# 切换模型
python3 v2/cli.py config --llm tongyi --key YOUR_API_KEY

# 开启/关闭 AI 优化
python3 v2/cli.py config --ai true
python3 v2/cli.py config --ai false

# 开启/关闭联网学习
python3 v2/cli.py config --web true
python3 v2/cli.py config --web false

# 开启/关闭持久化
python3 v2/cli.py config --persist true
python3 v2/cli.py config --persist false
```

---

## 🔧 使用示例

### 在 OpenClaw 中使用

```
用户: 记住我喜欢用 TypeScript 开发

助手: (调用 CLI 保存)
python3 v2/cli.py save --cause "开发偏好" --change "喜欢用 TypeScript"
```

```
用户: 我之前说过什么技术栈？

助手: (调用 CLI 搜索)
python3 v2/cli.py search "技术栈"
```

### 知识库管理

```bash
# 添加知识点
python3 v2/cli.py knowledge --add "OpenClaw 技能系统|使用 SKILL.md 定义技能"

# 列出知识库
python3 v2/cli.py knowledge

# 搜索知识
python3 v2/cli.py search "技能"
```

---

## 🛡️ 安全与隐私

- ✅ **本地存储**：所有记忆存储在本地 `memory/` 目录
- ✅ **权限隔离**：配置文件权限 `0o600`
- ✅ **可控联网**：`config --web false` 关闭所有网络请求
- ✅ **密钥安全**：API Key 仅存储于本地配置文件

---

## 🐛 常见问题

**Q: Token 消耗过高？**
- 检查 AI 优化是否开启：`config --show`
- 关闭联网学习：`config --web false`

**Q: 记忆没有被自动保存？**
- v2.0 需要手动调用 CLI 或由 LLM 调用
- 使用 `save --text "内容"` 保存

**Q: 如何迁移 v1 数据？**
- v1 数据在 `memory_data/` 目录
- 手动复制到 `memory/daily/` 即可

---

## 📜 更新日志

### v2.0.0 (2026-03-10)
- 🎉 全新架构重构
- ✨ 结构化记忆（因→改→待）
- ✨ 知识库系统
- ✨ 启发式召回
- ✨ 自动索引

### v1.1.4
- 基础记忆保存和检索
- AI 压缩优化
- 多平台消息适配

---

## 📄 License

MIT License

---

## 🙏 致谢

- OpenClaw 团队
- memory-master 技能作者（结构化格式参考）
- 所有贡献者
