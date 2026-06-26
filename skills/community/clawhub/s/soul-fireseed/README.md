# 🔥 火种·灵魂 v2.0 - 使用指南

> **版本**: 2.1.0  
> **定位**: 人格建模与记忆沉淀（完全独立版）  
> **核心口号**: "从对话中提取思维化石，构建数字孪生"  
> **项目名**: soul-fireseed  
> **ClawHub**: `npx clawhub install soul-fireseed`

---

## 🚀 一键安装

### AI 技能安装（推荐）
```bash
# 一行命令安装到 OpenClaw / WorkBuddy
npx clawhub install soul-fireseed
```

### 源码安装
```bash
# Gitee 国内镜像
git clone https://gitee.com/topofthesky/soul-fireseed.git
# GitHub 镜像
git clone https://github.com/topofthesky/soul-fireseed.git

# 安装依赖
cd soul-fireseed
pip install sentence-transformers scikit-learn numpy pandas jinja2
```

### 安装后使用
告诉你的 AI 助手：
> **「点燃火种」** 或 **「启动火种」** 或 **「灵魂启动」**

AI 会自动激活本技能，开始从对话中提取你的人格特征。

---

## 🔥 AI 交互流程

用户激活后，AI 先询问选择模式，然后按对应流程运行：

### 模式选择
```
🔥 火种·灵魂 v2.1 已激活！
[1] 💬 对话提取 — 通过聊天实时提取
[2] 📂 记忆分析 — 分析已有记忆批量提取
```

### 模式一：对话提取
- 实时从聊天对话中识别六维度特征并标注
- 每轮识别后输出：`🔍 🟡 认知架构 → 决策风格: 分析型 (信心: 0.85)`
- 收集5-8个特征后生成人格快照卡片

### 模式二：记忆分析
- AI 扫描已有历史对话记录
- 批量按六维度提取特征化石
- 直接输出完整初始人格档案（覆盖率更高）

### 后台自动提取（首次提取后自动进入）
```
完成首次提取后，AI 询问是否开启自动提取：
[1] 📅 每周自动提取一次（推荐）
[2] 📅 每天自动提取一次
[3] 🔕 手动模式
```
- 自动提取时仅做简要提示，不打扰用户
- 发现显著变化时主动提醒
- 每月自动生成演化报告

### 更多指令
- 「提取化石」→ 立即执行提取
- 「更新人格」→ 重新蒸馏人格画像
- 「查看人格」→ 展示当前快照
- 「分析记忆」→ 切换到记忆分析模式
- 「对话提取」→ 切换到对话提取模式
- 「设置提取」→ 修改自动提取频率
- 「演化报告」→ 人格变化轨迹

---

## 🌟 社区与生态

**如果你认同 "AI 应该拥有灵魂"，擅长：**
- 🔬 大模型人格建模
- 💾 长期记忆系统开发
- 🛠️ OpenClaw 技能生态搭建

**加入我们**：
| 平台 | 链接 |
|------|------|
| Gitee | https://gitee.com/topofthesky/soul-fireseed |
| ClawHub | `npx clawhub install soul-fireseed` |
| FireSeed | https://fireseed.online/skills |

---

## 📖 核心概念

### 基础使用

```python
from lib import FossilExtractor

# 创建提取器实例
extractor = FossilExtractor()

# 从对话中提取化石
fossils = extractor.extract("我最近工作压力很大，经常熬夜到凌晨2点")

# 查看提取结果
for fossil in fossils:
    print(f"维度{fossil.dimension}: {fossil.content} (置信度: {fossil.confidence})")
```

### 完整工作流

```python
from lib import FossilExtractor, FossilDistiller, FossilEmbedder

# 1. 初始化
extractor = FossilExtractor(config_path="config/defaults.json")
distiller = FossilDistiller()
embedder = FossilEmbedder()

# 2. 批量提取化石
conversations = [
    "今天完成了重要项目，感觉很有成就感",
    "我不太喜欢在人群中发言，更喜欢一对一交流",
    "做决策时我会先收集所有可能的信息"
]

all_fossils = []
for conv in conversations:
    fossils = extractor.extract(conv)
    all_fossils.extend(fossils)

print(f"共提取 {len(all_fossils)} 个化石")

# 3. 蒸馏生成人格模型
persona = distiller.distill(all_fossils)
print(f"人格模型版本: {persona['version']}")

# 4. 语义检索相似化石
query = "我对社交的看法"
similar_fossils = embedder.find_similar(query, top_k=5)
for fossil in similar_fossils:
    print(f"- {fossil.content}")

# 5. 生成演化报告
report = distiller.generate_evolution_report(days=30)
with open("evolution_report.md", "w") as f:
    f.write(report)
```

---

## 📖 核心概念

### 🔬 化石 (Fossil)

化石是火种技能从用户对话中提取的最小思维特征单元。每个化石代表用户在某一个维度上的一个认知特征点。

**化石结构**：
```json
{
  "id": "FOSSIL-20260509T200000-a3b2c1",
  "dimension": 3,
  "subdimension": "决策风格",
  "content": "倾向于分析型决策，先收集信息再行动",
  "timestamp": "2026-05-09T20:00:00Z",
  "confidence": 0.85,
  "source_quote": "我觉得做决策时，我更倾向于先收集足够信息再行动",
  "tags": ["决策风格", "分析型"]
}
```

**六大维度**：
1. **生物物理基座** - 能量水平、作息规律、健康意识
2. **自传体记忆** - 关键事件、情感锚点、身份认同
3. **认知架构** - 决策风格、风险偏好、学习模式
4. **情感动力学** - 情绪触发、应对机制、情感表达
5. **社会网络** - 关系模式、社交偏好、影响力圈
6. **元认知自我** - 自我觉察、反思能力、成长心态

### 👤 人格模型 (Persona Model)

人格模型是通过蒸馏大量化石形成的结构化用户画像，包含六个维度的量化指标和演化轨迹。

**更新频率**：建议每积累 50 个新化石后重新蒸馏一次

### 📈 演化轨迹 (Evolution Timeline)

记录人格模型随时间的变化，帮助识别用户的成长模式和思维转变。

---

## 🛠️ API 参考

### FossilExtractor 类

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `__init__()` | `config_path` | - | 初始化提取器 |
| `extract()` | `text`, `context` | `List[Fossil]` | 从文本提取化石 |
| `batch_extract()` | `texts` | `List[Fossil]` | 批量提取 |
| `get_extraction_stats()` | - | `Dict` | 获取提取统计 |
| `export_fossils()` | `format` | `str/File` | 导出化石数据 |

### FossilDistiller 类

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `__init__()` | `config` | - | 初始化蒸馏器 |
| `distill()` | `fossils` | `Dict` | 蒸馏生成人格模型 |
| `update_persona()` | `new_fossils` | `Dict` | 增量更新人格模型 |
| `get_evolution()` | `days` | `List[Dict]` | 获取演化轨迹 |
| `generate_report()` | `format` | `str` | 生成演化报告 |

### FossilEmbedder 类

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `__init__()` | `model_name` | - | 初始化嵌入器 |
| `embed()` | `text` | `List[float]` | 文本向量化 |
| `similarity()` | `vec1`, `vec2` | `float` | 计算相似度 |
| `find_similar()` | `query`, `top_k` | `List[Fossil]` | 语义检索 |
| `cluster()` | `fossils`, `n_clusters` | `Dict` | 聚类分析 |

### ConfidenceValidator 类

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `validate()` | `fossil`, `context` | `Dict` | 验证化石可信度 |
| `detect_contradiction()` | `fossil1`, `fossil2` | `bool` | 检测矛盾 |
| `get_accuracy_history()` | `dimension` | `List[float]` | 获取准确率历史 |

---

## ⚙️ 配置指南

### 配置文件路径

```
config/defaults.json              # 默认配置
config/keywords.json              # 六维度关键词库
user-data/fireseed/config.override.json  # 用户覆盖配置(可选)
```

### 常用配置项

```json
{
  "extraction": {
    "max_fossils_per_dimension": 2,
    "pending_confidence_threshold": 0.6,
    "high_confidence_threshold": 0.8,
    "min_confidence": 0.2
  },
  "distillation": {
    "batch_size": 50,
    "frequency_hours": 24,
    "min_fossils_for_distill": 20
  },
  "embedding": {
    "model_name": "sentence-transformers/all-MiniLM-L6-v2",
    "similarity_threshold": 0.75
  },
  "validation": {
    "historical_window": 100,
    "enable_contradiction_detection": true
  },
  "storage": {
    "auto_backup": true,
    "backup_retention_days": 30,
    "fossil_storage_path": "user-data/fossils/"
  }
}
```

### 自定义关键词库

编辑 `config/keywords.json` 添加领域专属词汇：

```json
{
  "dimension_3_cognitive": {
    "decision_style": {
      "analytical": ["分析", "评估", "权衡", "比较"],
      "intuitive": ["直觉", "感觉", "第一反应"]
    },
    "risk_preference": {
      "risk_seeking": ["冒险", "尝试", "突破"],
      "risk_averse": ["稳妥", "保守", "谨慎"]
    }
  }
}
```

---

## 💡 最佳实践

### ✅ 推荐的用法

1. **每日对话后自动提取**
   ```bash
   ./scripts/extract.sh --auto --input daily_log.txt
   ```

2. **每周批量蒸馏生成画像**
   ```bash
   ./scripts/distill.sh --batch --output weekly_profile.md
   ```

3. **定期查看演化趋势**
   ```python
   distiller = FossilDistiller()
   report = distiller.generate_evolution_report(days=30)
   print(report)
   ```

4. **使用语义检索查找相关记忆**
   ```python
   embedder = FossilEmbedder()
   fossils = embedder.find_similar("我的职业发展规划", top_k=10)
   ```

5. **定期备份化石数据**
   ```bash
   ./scripts/export_profile.sh --backup --format json
   ```

### ❌ 不推荐的用法

1. **单次输入过长文本**（建议分段处理，每段不超过 500 字）
2. **忽略低置信度化石**（它们可能包含重要信号，只是需要验证）
3. **频繁手动修改化石**（应通过蒸馏器自动更新）
4. **不进行定期蒸馏**（人格模型会过时，建议至少每周一次）
5. **删除早期化石**（保留完整的历史记录用于演化分析）

---

## 🔍 使用场景示例

### 场景 1: 个人成长追踪

```python
# 每月生成一次演化报告
distiller = FossilDistiller()

# 对比本月与上月的人格变化
current_persona = distiller.get_current_persona()
last_month_persona = distiller.get_persona_at_date("2026-04-09")

# 识别显著变化
changes = distiller.compare_personas(last_month_persona, current_persona)
for change in changes:
    print(f"{change['dimension']}: {change['old_value']} → {change['new_value']}")
```

### 场景 2: 决策风格分析

```python
# 检索所有与决策相关的化石
embedder = FossilEmbedder()
decision_fossils = embedder.find_similar("决策 选择 判断", top_k=20)

# 分析决策模式
for fossil in decision_fossils:
    print(f"[{fossil.timestamp}] {fossil.content} (置信度: {fossil.confidence})")
```

### 场景 3: 情绪模式识别

```python
# 提取情感动力学维度的化石
extractor = FossilExtractor()
fossils = extractor.extract("最近工作压力大，但完成项目后很有成就感")

# 筛选维度4（情感动力学）的化石
emotional_fossils = [f for f in fossils if f.dimension == 4]
for fossil in emotional_fossils:
    print(f"情绪特征: {fossil.subdimension} - {fossil.content}")
```

### 场景 4: 社交偏好分析

```python
# 批量提取社交相关对话
social_texts = [
    "我不喜欢大型聚会，更享受小圈子深度交流",
    "我和几个老朋友保持长期联系",
    "在陌生环境中我会先观察再行动"
]

extractor = FossilExtractor()
all_fossils = extractor.batch_extract(social_texts)

# 聚焦维度5（社会网络）
social_fossils = [f for f in all_fossils if f.dimension == 5]
print(f"提取到 {len(social_fossils)} 个社交相关化石")
```

---

## 🐛 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 提取化石数量为 0 | 文本过短或缺乏特征词 | 增加文本长度，检查关键词库 |
| 置信度普遍偏低 | 缺少上下文或关键词不匹配 | 补充对话历史，更新关键词库 |
| 蒸馏失败 | 化石数量不足 | 积累至少 20 个化石后再蒸馏 |
| 语义检索结果不准确 | 嵌入模型未加载 | 检查 `embedding.model_name` 配置 |
| 内存占用过高 | 化石数量过多 | 启用自动归档，定期清理旧化石 |
| 演化报告为空 | 时间跨度内无化石 | 检查日期范围和化石存储路径 |

---

## 📊 性能优化建议

### 提升提取速度

1. **启用并行提取**
   ```python
   extractor = FossilExtractor(parallel=True, workers=4)
   ```

2. **缓存嵌入向量**
   ```python
   embedder = FossilEmbedder(cache_enabled=True, cache_path="cache/embeddings/")
   ```

3. **批量处理**
   ```python
   # 优于逐个处理
   fossils = extractor.batch_extract(texts)
   ```

### 提升准确率

1. **提供对话历史**
   ```python
   context = ["之前的对话1", "之前的对话2"]
   fossils = extractor.extract(current_text, context=context)
   ```

2. **定期更新关键词库**
   ```bash
   ./scripts/update_keywords.sh --auto
   ```

3. **人工校验低置信度化石**
   ```python
   pending_fossils = [f for f in fossils if f.confidence < 0.6]
   for fossil in pending_fossils:
       confirmed = input(f"确认此化石? {fossil.content} (y/n): ")
       if confirmed == 'y':
           fossil.confidence = 0.8
   ```

---

## 🔄 与其他工具集成

### 与日志系统集成

```python
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fireseed_v2")

# 提取时记录日志
extractor = FossilExtractor(logger=logger)
fossils = extractor.extract("对话内容")
logger.info(f"提取了 {len(fossils)} 个化石")
```

### 与数据库集成

```python
import sqlite3

# 存储化石到 SQLite
def store_to_db(fossils, db_path="fireseed.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fossils (
            id TEXT PRIMARY KEY,
            dimension INTEGER,
            content TEXT,
            confidence REAL,
            timestamp TEXT
        )
    ''')
    
    for fossil in fossils:
        cursor.execute(
            "INSERT OR REPLACE INTO fossils VALUES (?, ?, ?, ?, ?)",
            (fossil.id, fossil.dimension, fossil.content, 
             fossil.confidence, fossil.timestamp)
        )
    
    conn.commit()
    conn.close()

store_to_db(fossils)
```

### 与可视化工具集成

```python
import matplotlib.pyplot as plt

# 绘制人格雷达图
def plot_persona_radar(persona):
    dimensions = list(persona['dimensions'].keys())
    values = [persona['dimensions'][d] for d in dimensions]
    
    angles = [n / float(len(dimensions)) * 2 * pi for n in range(len(dimensions))]
    angles += angles[:1]
    values += values[:1]
    
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids([a * 180/pi for a in angles[:-1]], dimensions)
    plt.show()

persona = distiller.get_current_persona()
plot_persona_radar(persona)
```

---

## 📚 进阶阅读

- [提取指南](docs/extraction_guide.md) - 深入了解提取算法
- [维度参考手册](docs/dimension_reference.md) - 六维度详细说明
- [故障排除](docs/troubleshooting.md) - 常见问题解答
- [API 完整文档](docs/api_reference.md) - 所有类和方法的详细说明

---

## 🆚 v2.0 vs v1.0 对比

| 特性 | v1.0 | v2.0 |
|------|------|------|
| 化石提取 | ✅ | ✅ 优化版（并行处理） |
| 人格蒸馏 | ❌ | ✅ 新增 |
| 隐空间映射 | ❌ | ✅ 新增（语义检索） |
| 置信度校准 | 基础版 | ✅ 贝叶斯更新 |
| 演化追踪 | ❌ | ✅ 新增 |
| 独立性 | 依赖其他技能 | ✅ 完全独立 |
| 性能 | 基准 | 🚀 3x 提升 |
| 准确率 | 基准 | 📊 +25% 提升 |

---

## 📞 支持与反馈

- 📧 邮箱: fireseed-team@example.com
- 💬 讨论区: GitHub Discussions
- 🐛 问题报告: GitHub Issues

---

## 📄 许可证

MIT License - FireSeed Team © 2026

> **"每一段对话都是思维的痕迹，每一次提取都是认知的洞察。"**
