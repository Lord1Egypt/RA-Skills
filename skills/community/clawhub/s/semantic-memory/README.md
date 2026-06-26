# 🧠 Semantic Memory — 中文语义记忆系统

> **中文优先的三轨混合检索 | Chinese-First Hybrid Search for AI Agents**
> OpenClaw Agent 长期记忆基础设施 | v1.0.0

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-1.0-brightgreen.svg)](https://www.trychroma.com/)

---

## 一句话定位

**唯一一个为中文场景深度优化的 OpenClaw 记忆技能。**
jieba TF-IDF 中文语义 + 向量检索双轨混合，0.8秒响应，100% 命中率，开箱即用。

---

## ✨ 核心亮点

| 特性 | 说明 |
|------|------|
| 🇨🇳 **中文语义优先** | jieba 分词 + TF-IDF，向量模型做不到的中文理解 |
| 🔄 **混合三轨检索** | TF-IDF × 向量 × 关键词，加权合并评分 |
| 🤖 **Agent 自动路由** | 自动识别意图路由到对应 collection |
| ⚡ **0.8秒响应** | 预计算 TF-IDF 索引，缓存命中即查即得 |
| 🐳 **零门槛部署** | pip install 即可，无需 Docker/GPU/Qdrant |

---

## 📊 性能基准

| 测试场景 | 命中率 | 响应速度 |
|---------|--------|---------|
| 精确关键词 | **100%** | 0.8秒 |
| 语义查询（"跌倒检测ESP32"）| **100%** | 0.8秒 |
| Agent路由（"狗蛋产品规划"）| **100%** | 0.8秒 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install chromadb jieba
```

### 2. 启动 ChromaDB

```bash
# 方式一：直接启动
chroma run --path ./vector_db --host 0.0.0.0 --port 8000 &

# 方式二：用配套脚本启动
bash scripts/start_chroma.sh
```

### 3. 导入记忆文件

```bash
python3 scripts/import_memory.py
# 默认导入当前目录的 memory/*.md 到 memories collection
```

### 4. 开始检索

```bash
python3 scripts/vector_search.py "你的查询"
```

---

## 🏗️ 工作原理

```
用户查询
    │
    ▼
Agent 自动路由（关键词匹配）
    ├─ 含"狗蛋"→ projects
    ├─ 含"狗学术"→ knowledge
    └─ 含"百晓生"→ memories

    ▼
TF-IDF 预计算索引（jieba 分词）
    ├─→ 中文语义相似度（主要通道）
    │
ChromaDB 向量检索
    ├─→ 语义扩展（补充通道）
    │
关键词命中加权（source 标题匹配）
    │
    ▼
综合评分 = 0.45×向量 + 0.55×TF-IDF + boost
    │
    ▼
Top 6 结果输出
```

---

## 📁 文件结构

```
semantic-memory/
├── README.md                    # 本文件
├── SKILL.md                     # OpenClaw Skill 定义
├── scripts/
│   ├── vector_search.py        # ⭐ 核心检索脚本
│   ├── import_memory.py        # ⭐ 记忆导入脚本
│   └── start_chroma.sh         # ChromaDB 启动脚本
└── docs/
    └── benchmark.md             # 性能测试记录
```

---

## 🔧 OpenClaw 接入

在 `TOOLS.md` 中添加：

```markdown
## 向量数据库（Semantic Memory）
- 服务：ChromaDB HTTP Server，localhost:8000
- 启动：chroma run --path ./vector_db --host 0.0.0.0 --port 8000 &
- 检索：`python3 scripts/vector_search.py "关键词"`
- 缓存：`./vector_db/tfidf_cache/`
- Agent路由：含"狗蛋"→projects，含"狗学术"→knowledge，含"百晓生"→memories
```

---

## 🔧 API 用法

```python
import sys
sys.path.insert(0, 'scripts')
from vector_search import search

# 搜索记忆
results = search("跌倒检测老人", topk=6)
for r in results:
    print(f"[{r['source']}] {r['doc'][:100]}")
    print(f"  综合分: {r['combined']:.3f}")
```

---

## ⚙️ 自定义配置

### Agent 路由规则

修改 `scripts/vector_search.py`：

```python
AGENT_KEYWORDS = {
    '你的Agent': ['关键词1', '关键词2'],
}
AGENT_COLLECTION = {'你的Agent': 'projects'}
```

### 权重调整

```python
combined = 0.45 * vec_sim + 0.55 * tfidf_norm + boost
# 调高 0.55 → 更注重中文关键词精确匹配
# 调高 0.45 → 更注重语义扩展
```

### 环境变量

```bash
export CHROMA_HOST=localhost
export CHROMA_PORT=8000
export CHROMA_PATH=./vector_db
export TFIDF_CACHE=./vector_db/tfidf_cache
```

---

## 📦 技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| ChromaDB | 1.0+ | 向量数据库 |
| jieba | 0.42+ | 中文分词 |
| Python | 3.10+ | 运行环境 |

---

## ⚠️ 已知限制

1. embedding 模型为英文（all-MiniLM-L6-v2），中文语义主要靠 TF-IDF 弥补
2. ChromaDB 跨机器访问需配置 API 认证
3. 目前仅在 Linux/macOS 测试，Windows 兼容性待验证

---

## 📄 License

MIT — 署名即可，欢迎使用和二次开发。

---

*项目创建于 2026-04-12*
