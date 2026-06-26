# Same Idea Skill

<p align="center">
  <strong>发现知识之间的隐藏联系</strong>
</p>

<p align="center">
  <em>Find similar ideas and resonating quotes from your reading notes and knowledge base</em>
</p>

---

## 简介

当你在阅读时遇到一个想法或引用，这个技能帮你发现它与现有知识的联系。它会搜索你的 Logseq 和 Obsidian 笔记库，找到相似的概念、共鸣的引用或相关的想法，并返回带有来源（书籍、作者、人物）的匹配引用。

**核心价值：让每一次阅读都与你已有的知识产生连接，构建更有深度的个人知识网络。**

## 功能特点

- 🔍 **智能关键词提取** - 自动从输入文本中提取核心概念
- 📚 **多笔记库支持** - 同时搜索 Logseq 和 Obsidian vault
- 🎯 **相关性排序** - 按语义相似度对结果进行排名
- 📖 **来源追溯** - 始终返回带有书籍/作者信息的引用
- ⚡ **高效搜索** - 使用 ripgrep 实现快速全文检索
- 🔄 **去重过滤** - 自动合并相似内容，避免重复

## 安装

### 方法一：手动安装

```bash
# 克隆仓库
git clone https://github.com/jianghaidong/same-idea-skill.git

# 复制到 OpenClaw skills 目录
cp -r same-idea-skill ~/.openclaw/workspace/skills/same-idea

# 重启 OpenClaw 或重新加载技能
```

### 方法二：使用 clawhub 安装（推荐）

```bash
clawhub install same-idea
```

### 依赖项

- **Python 3.6+** - 运行核心搜索脚本
- **ripgrep (rg)** - 快速文本搜索（可选，但强烈推荐）

安装 ripgrep：

```bash
# macOS
brew install ripgrep

# Ubuntu/Debian
sudo apt install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC
```

## 使用方法

### 基本用法

只需向你的 agent 分享一个想法、概念或引用：

```
"真正的自由是自律的结果"
```

或

```
"复利效应不仅适用于金钱，也适用于知识和关系"
```

### 工作流程

1. **解析输入** - 从你的想法中提取关键词和核心概念
2. **搜索笔记库** - 在 Logseq 日记/页面和 Obsidian 笔记中搜索
3. **匹配与排名** - 使用语义相似度找到最佳匹配
4. **格式化输出** - 展示结果，包含来源和共鸣说明

### 示例输出

```
## 输入想法
复利效应不仅适用于金钱，也适用于知识和关系

## 共鸣发现

### 1. 知识复利
> "每天进步1%，一年后你会进步37倍"

**来源**: 《掌控习惯》 - 詹姆斯·克利尔
**共鸣点**: 强调微小积累的巨大效应，与你提到的知识复利概念一致

### 2. 关系投资
> "人际关系就像银行账户，需要持续存款"

**来源**: 《高效能人士的七个习惯》 - 史蒂芬·柯维
**共鸣点**: 将关系视为需要长期投入的资产，与复利思维相通
```

## 配置

### 笔记库路径

默认配置的笔记库位置：

```python
LOGSEQ_VAULT = "~/Library/Mobile Documents/iCloud~com~logseq~logseq/Documents"
OBSIDIAN_VAULT = "~/Library/Mobile Documents/iCloud~md~obsidian/Documents"
```

如果你的笔记库在其他位置，可以编辑 `scripts/find_similar.py` 文件中的路径变量。

### 搜索优先级

搜索会按照以下顺序进行：

1. **Logseq Journals** - 日记和即时想法
2. **Logseq Pages** - 永久笔记和概念页面
3. **Obsidian Reading Notes** - 书籍高亮和摘要
4. **Obsidian Literature Notes** - 处理过的阅读笔记

## 项目结构

```
same-idea/
├── SKILL.md              # 技能定义（OpenClaw 格式）
├── README.md             # 本文件
├── CONTRIBUTING.md       # 贡献指南
├── LICENSE               # MIT 许可证
└── scripts/
    ├── find_similar.py   # 核心搜索脚本
    └── release.sh        # 发布脚本
```

## 使用场景

- 📖 **阅读时** - 遇到一个观点，想找找自己以前记录的相似想法
- 📝 **写作时** - 寻找可以支持或对比的引用
- 💡 **思考时** - 探索一个概念在你的知识体系中的位置
- 🔄 **复习时** - 发现笔记之间的意外联系

## 技术细节

### 关键词提取算法

- 中文：提取 2 字以上的词组，过滤常用停用词
- 英文：提取 3 字以上的单词（小写）
- 自动去重，保留最多 10 个关键词

### 匹配评分

结果按以下标准评分排序：

- **关键词匹配**：每个匹配关键词 +1 分
- **引用标记**：包含 `>` 或引号 +2 分
- **来源标记**：包含书名号或作者标注 +1 分

## 常见问题

<details>
<summary><strong>Q: 搜索没有返回结果怎么办？</strong></summary>

确保你的 Logseq 或 Obsidian vault 路径配置正确。可以手动运行脚本测试：

```bash
python3 ~/.openclaw/workspace/skills/same-idea/scripts/find_similar.py "测试想法"
```
</details>

<details>
<summary><strong>Q: 如何添加自定义停用词？</strong></summary>

编辑 `scripts/find_similar.py` 文件中的 `cn_stop` 集合，添加你想要过滤的词。
</details>

<details>
<summary><strong>Q: 支持其他笔记软件吗？</strong></summary>

目前支持 Logseq 和 Obsidian。如需支持其他软件，可以修改 `find_similar.py` 中的 vault 路径和搜索逻辑。欢迎提交 PR！
</details>

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 作者

Created by [jianghaidong](https://github.com/jianghaidong)

---

<p align="center">
  <strong>让每一次阅读都成为知识的积累 ✨</strong>
</p>