# 🔍 Semantic Memory Search

**为 OpenClaw 记忆文件添加语义搜索能力**

[![ClawHub](https://img.shields.io/badge/ClawHub-semantic--memory--search-blue)](https://clawhub.com/skills/semantic-memory-search)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 痛点

OpenClaw 的记忆以纯 Markdown 文件存储。这对可移植性和人类可读性很好，但：
- ❌ 没有搜索功能
- ❌ 只能 grep（仅关键词，会漏掉语义匹配）
- ❌ 将整个文件加载到上下文（浪费 token）

你需要一种方式来问"我关于 X 做了什么决定？"并获得精确的相关片段。

---

## ✨ 功能

| 功能 | 说明 |
|------|------|
| 语义搜索 | 通过语义而非关键词找到相关记忆 |
| 混合搜索 | 稠密向量 + BM25 全文检索 + RRF 重排序 |
| 智能去重 | SHA-256 哈希，未更改文件不重新嵌入 |
| 本地运行 | 无需 API Key，完全离线 |
| 自动同步 | 文件变更时自动重新索引 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip3 install "memsearch[local]"
```

### 2. 索引记忆文件

```bash
cd ~/.openclaw/workspace/skills/semantic-memory-search/scripts
./index.sh
```

### 3. 搜索记忆

```bash
./search.sh "Discord 频道重组"
```

---

## 📊 搜索示例

| 查询 | 说明 |
|------|------|
| "我们选了什么缓存方案？" | 即使没有"缓存"关键词也能找到 |
| "Discord 频道重组" | 找到所有相关决策和过程 |
| "播客制作流程" | 找到播客相关的所有记忆 |
| "财报跟踪配置" | 找到财报系统的配置历史 |

---

## 🔧 配置

配置文件：`~/.memsearch/config.toml`

```toml
[milvus]
uri = "~/.memsearch/milvus.db"

[embedding]
provider = "local"
model = "all-MiniLM-L6-v2"

[search]
top_k = 5
```

---

## 📁 文件结构

```
semantic-memory-search/
├── SKILL.md              # 技能说明
├── README.md             # 使用文档
├── package.json          # 包信息
├── LICENSE               # MIT 许可证
├── .gitignore            # Git 忽略文件
├── scripts/
│   ├── index.sh          # 索引脚本
│   └── search.sh         # 搜索脚本
└── config/
    └── settings.json     # 配置文件
```

---

## 🔗 相关链接

- [memsearch GitHub](https://github.com/zilliztech/memsearch)
- [memsearch 文档](https://zilliztech.github.io/memsearch/)
- [Milvus](https://milvus.io/)
- [用例来源](https://github.com/AlexAnys/awesome-openclaw-usecases-zh/blob/main/usecases/semantic-memory-search.md)

---

## 📝 更新日志

### v1.0.0 (2026-03-14)
- ✅ 初始版本
- ✅ 本地 embedding 支持
- ✅ 语义搜索功能

---

## 📄 许可证

MIT License
