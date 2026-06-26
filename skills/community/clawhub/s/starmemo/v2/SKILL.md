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

## 工作流

```
用户消息
    ↓
1. 启发式判断 → 需要召回？
    ↓ 是                    ↓ 否
2. 搜索记忆/知识库      3. AI提取结构
    ↓                        ↓
4. 记忆足够？               保存到 daily/
    ↓ 是        ↓ 否         ↓
  直接回答    澄清提问     提取知识点到 knowledge/
                             ↓
                         更新索引
```

---

## CLI 命令

### 保存记忆

```bash
# 结构化保存
python3 {baseDir}/v2/cli.py save --cause "原因" --change "做了什么" --todo "待办"

# 文本保存（自动提取结构）
python3 {baseDir}/v2/cli.py save --text "今天学习了Python装饰器，用于修改函数行为"

# 从 stdin 读取
echo "内容" | python3 {baseDir}/v2/cli.py save
```

### 搜索记忆

```bash
python3 {baseDir}/v2/cli.py search "关键词"
```

### 查看记忆

```bash
# 今日记忆
python3 {baseDir}/v2/cli.py show

# 知识库
python3 {baseDir}/v2/cli.py show --knowledge
```

### 知识库管理

```bash
# 添加知识
python3 {baseDir}/v2/cli.py knowledge --add "标题|内容"

# 列出知识
python3 {baseDir}/v2/cli.py knowledge
```

### 配置管理

```bash
# 查看配置
python3 {baseDir}/v2/cli.py config --show

# 设置模型
python3 {baseDir}/v2/cli.py config --llm huoshan --key YOUR_API_KEY

# 开启联网
python3 {baseDir}/v2/cli.py config --web true

# 开启持久化
python3 {baseDir}/v2/cli.py config --persist true
```

---

## 存储结构

```
memory/
├── daily/                  # 每日记忆（结构化）
│   └── 2026-03-10.md
├── knowledge/              # 知识库
│   └── Python装饰器.md
├── archive/                # 归档
├── daily-index.md          # 日期索引
└── knowledge-index.md      # 知识索引
```

---

## 记忆格式

```markdown
## [14:30] 学习
- **因**：用户想了解Python装饰器
- **改**：学习了装饰器的基本用法和常见模式
- **待**：实践装饰器项目
```

---

## 触发时机

**主动保存当：**
- 用户分享重要信息（偏好、决策）
- 完成有价值的任务
- 学习新知识/技能
- 用户说"记住"、"保存"

**主动召回当：**
- 用户说"之前"、"上次"、"那个"
- 用户问"我说过什么"
- 需要回顾历史决策

---

## 支持的 LLM

| 厂商 | 标识 |
|:-----|:-----|
| 火山方舟 | huoshan |
| 通义千问 | tongyi |
| 文心一言 | wenxin |
| DeepSeek | deepseek |
| 智谱 AI | zhipu |
| 讯飞星火 | xinghuo |
| 腾讯混元 | hunyuan |

---

## 示例

**用户**: "记住我喜欢用 TypeScript 开发"

**助手执行**:
```bash
python3 {baseDir}/v2/cli.py save --cause "用户开发偏好" --change "喜欢用 TypeScript 开发"
```

**用户**: "我之前说过什么技术栈？"

**助手执行**:
```bash
python3 {baseDir}/v2/cli.py search "技术栈"
```

---

## 当前配置

- 模型：火山方舟 (doubao-seed-code-preview-251028)
- AI优化：✅ 开启
- 联网学习：✅ 开启
- 持久化：✅ 开启
