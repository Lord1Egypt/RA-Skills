# Scholar Search Skills

学术论文搜索与下载工具

## 功能特性

- 📚 从 arXiv、ICLR、ICML、NeurIPS 等来源搜索论文
- 🔍 关键词相关性打分（模糊匹配 + TF-IDF 余弦相似度）
- 📥 批量下载论文 PDF
- 📝 自动生成结构化摘要
- 📖 支持 BibTeX 引用格式
- 🔗 引用追踪（Google Scholar）

## 触发条件

当用户提出以下需求时触发：
- "帮我搜索关于 XXX 的论文"
- "查找 XXX 相关的学术文献"
- "搜索 XXX 主题的研究论文"

## 安装

```bash
# 方式1: 使用 clawhub
npx clawhub install scholar-search-skills

# 方式2: 手动安装
git clone https://github.com/<your-username>/scholar-search-skills.git
cd scholar-search-skills
# 复制到 OpenClaw skills 目录
```

## 使用方法

### 1. 基本搜索

告诉助手你的研究主题，例如：
- "帮我搜索 LLM 安全相关的论文"
- "查找 prompt injection 防御的文献"

### 2. 关键词相关性打分

```bash
pip install scikit-learn rapidfuzz

# 单一论文
python3 scripts/score_papers.py \
    --keywords "agent,LLM,security" \
    --title "论文标题" \
    --abstract "论文摘要"

# 批量打分
python3 scripts/score_papers.py \
    --keywords "agent,LLM,security" \
    --papers paper_list.csv \
    --output results.json
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `core-papers/` | 核心文献 PDF |
| `cited-papers/` | 引用文献 PDF |
| `PAPER_LIST.md` | 论文清单 |
| `PAPER_SUMMARIES.md` | 结构化摘要 |
| `references.bib` | BibTeX 引用 |

## 依赖

- Python 3.8+
- scikit-learn
- rapidfuzz

## 工作流

```
1. 确认基本信息 (主题/关键词/筛选条件)
       ↓
2. 搜索论文 (arxiv-search / web_fetch)
       ↓
3. 下载 PDF
       ↓
4. 关键词相关性打分
       ↓
5. 生成摘要 + BibTeX
```

## 目录结构

```
scholar-search-skills/
├── SKILL.md                      # Skill 定义文件
├── scripts/
│   └── score_papers.py           # 关键词打分脚本
├── references/
│   ├── bibtex_template.md        # BibTeX 模板
│   └── summary_template.md       # 摘要模板
└── README.md                     # 本文件
```

## License

MIT License

## 作者

Your Name <your@email.com>
