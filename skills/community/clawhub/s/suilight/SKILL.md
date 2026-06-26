---
name: suilight
description: SuiLight知识沙龙 - 多智能体知识协作平台。拥有100位虚拟思想家，覆盖26个领域(科学、哲学、社会科学等)，支持跨域讨论、知识沉淀、共识追踪和知识图谱可视化。当用户需要(1)组织多角度知识讨论、(2)创建虚拟思想家角色、(3)构建知识胶囊系统、(4)实现知识图谱、(5)部署Streamlit应用时使用此skill。基于Python Streamlit构建。
---

# SuiLight 知识沙龙

## 概述

SuiLight是26个领域的多智能体知识协作平台，拥有100位虚拟思想家，支持跨域讨论和知识沉淀。

## 特性

- **26个领域**: 科学、哲学、社会科学全覆盖
- **100位虚拟思想家**: 多角度分析问题
- **知识图谱**: 可视化知识关联
- **共识追踪**: 追踪观点演变
- **知识胶囊**: 结构化知识沉淀

## 技术栈

- **后端**: Python 3.9+
- **前端**: Streamlit
- **API**: FastAPI
- **存储**: JSON + 文件系统

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/wanyview1/SuiLight.git
cd SuiLight

# 安装依赖
pip install -r requirements.txt

# 启动UI
streamlit run ui/streamlit_app.py

# 启动API
python api/main.py
```

服务启动: http://localhost:8501

## 核心模块

### 1. 知识胶囊系统

```python
from suilight.capsule import KnowledgeCapsule

# 创建知识胶囊
capsule = KnowledgeCapsule(
    title="量子纠缠原理",
    domain="物理学",
    content="量子纠缠是量子力学中...",
    tags=["量子力学", "纠缠", "非局域性"],
    confidence=0.9
)
capsule.save()
```

### 2. 虚拟思想家

```python
from suilight.thinker import VirtualThinker

# 创建虚拟思想家
thinker = VirtualThinker(
    name="Einstein",
    domain="物理学",
    style="直觉+数学",
    expertise=["相对论", "量子力学"]
)

# 发起讨论
response = thinker.discuss(
    topic="量子意识假说",
    context="神经科学与量子物理的交叉领域"
)
```

### 3. 跨域讨论

```python
from suilight.saloon import KnowledgeSaloon

saloon = KnowledgeSalon()

# 多领域讨论
result = saloon.cross_domain_discussion(
    topic="意识的本体论地位",
    domains=["哲学", "神经科学", "物理学", "计算机科学"],
    thinkers_per_domain=3,
    rounds=3
)
```

### 4. 知识图谱

```python
from suilight.graph import KnowledgeGraph

graph = KnowledgeGraph()
graph.add_node("量子纠缠", domain="物理学")
graph.add_node("非局域性", domain="物理学")
graph.add_edge("量子纠缠", "非局域性", weight=0.9)
graph.visualize()
```

## API端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/domains` | GET | 获取26个领域列表 |
| `/api/thinker` | GET | 获取虚拟思想家 |
| `/api/discuss` | POST | 发起跨域讨论 |
| `/api/capsule` | GET/POST | 知识胶囊CRUD |
| `/api/graph` | GET | 知识图谱数据 |
| `/api/consensus` | GET | 共识追踪数据 |

## 目录结构

```
suilight/
├── api/                # FastAPI后端
│   ├── main.py         # API入口
│   ├── capsule.py      # 胶囊API
│   └── thinker.py      # 思想家API
├── ui/                 # Streamlit前端
│   └── streamlit_app.py
├── tests/              # 测试
├── docs/               # 文档
│   ├── PLATFORM_DESIGN.md
│   ├── CAPSULE_SYSTEM.md
│   └── ROADMAP.md
└── demo_capsule.py     # 演示脚本
```

## 26个领域

| 类别 | 领域 |
|------|------|
| 自然科学 | 物理学、化学、生物学、数学、天文学、地质学 |
| 计算机科学 | AI/ML、数据科学、网络安全、量子计算 |
| 哲学 | 形而上学、认识论、伦理学、美学 |
| 社会科学 | 心理学、社会学、经济学、政治学 |
| 人文学 | 历史学、语言学、文学、艺术 |
| 工程 | 生物工程、材料科学、环境科学 |

## 部署

### Streamlit Cloud

```bash
# 安装streamlit CLI
pip install streamlit

# 部署
streamlit deploy
```

### Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "ui/streamlit_app.py"]
```

## 资源

- **GitHub**: https://github.com/wanyview1/SuiLight
- **ClawHub**: https://clawhub.com
- **文档**: docs/PLATFORM_DESIGN.md

---

*Built with ❤️ by KAI*