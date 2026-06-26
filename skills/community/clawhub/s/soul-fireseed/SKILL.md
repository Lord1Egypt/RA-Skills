---
name: soul-fireseed
version: 2.1.0
description: "火种·灵魂 v2.0 — 人格建模与记忆沉淀技能。激活后有两种模式：①对话提取 ②记忆分析。首次提取后自动进入后台模式，可设置每周/每日自动提取。"
author: topofthesky
homepage: https://fireseed.online
repository: https://gitee.com/topofthesky/soul-fireseed
icon_emoji: 🔥
trigger:
  - 点燃火种
  - 启动火种
  - 火种启动
  - 灵魂启动
  - 火种对话
  - 火种记忆
  - 灵魂
  - 人格建模
  - 记忆沉淀
  - 思维化石
  - 数字孪生
  - 提取化石
  - 查看人格
---

# 🔥 火种·灵魂 v2.1 — AI 使用指南

> **快速激活**: 用户说 **「点燃火种」** 或 **「启动火种」** 即可激活  
> **版本**: 2.1.0 | **最后更新**: 2026-05-09

---

## 🚀 快速激活与两种模式

### 激活方式
用户说以下任意一句即可激活：
```
「点燃火种」  「启动火种」  「火种启动」  「灵魂启动」
```

### AI 激活后，立即询问用户选择模式：

```
🔥 火种·灵魂 v2.1 已激活！
请选择提取模式：

[1] 💬 对话提取 — 通过聊天实时提取你的人格特征
    适合：想边聊边了解自己

[2] 📂 记忆分析 — 分析我的已有记忆，批量提取化石
    适合：已有大量对话记录，想要快速建立人格模型

请回复 1 或 2 选择模式
```

---

## 💬 模式一：对话提取（实时聊天）

### 流程
```
用户选择模式1
  ↓
AI: "好，随便聊聊吧——说说你的想法、经历或喜好，我会自动提取特征"
  ↓
用户正常聊天 → AI 每轮对话识别特征并实时标注
  ↓
收集约5-8个特征后 → 输出人格快照卡片
  ↓
询问是否进入后台模式
```

### AI 交互示例
```
用户: "我做决定前喜欢收集大量信息"
  → 🔍 🟡 认知架构 → 决策风格: 分析型 (信心: 0.85)

用户: "最近经常熬夜赶项目"
  → 🔍 🔵 生物基座 → 作息规律: 熬夜型 (信心: 0.72)

...继续对话，收集到5个以上特征后...

🔥 火种·灵魂 人格快照
─────────────────
🔵 生物基座: 高能量·熬夜型 (72%)
🟢 自传记忆: 工程师·项目导向 (68%)
🟡 认知架构: 分析型·中等风险 (81%)
🔴 情感动力: 目标驱动·压力应对 (60%)
🟣 社会网络: — (待收集)
🟠 元认知: — (待收集)
─────────────────
✨ 人格完整度: ★★★☆☆

[🧬 生成报告] [📂 切换到记忆分析]
```

---

## 📂 模式二：记忆分析（批量提取）

### 适用场景
- 用户和 AI 已有大量历史对话记录
- 希望快速建立完整人格模型
- 不需要逐条聊，直接分析存量数据

### 流程
```
用户选择模式2
  ↓
AI 扫描已有记忆/对话记录
  ↓
按六维度批量提取特征化石
  ↓
输出批量分析结果摘要
  ↓
生成初始人格画像（完整性更高）
  ↓
询问是否进入后台模式
```

### AI 执行指令
```
模式2激活后：

1. 【扫描】检索用户历史对话中涉及以下内容的部分：
   - 工作/生活习惯 (→ 生物基座)
   - 人生经历/回忆 (→ 自传记忆)
   - 决策/判断方式 (→ 认知架构)
   - 情绪/感受表达 (→ 情感动力)
   - 人际关系描述 (→ 社会网络)
   - 自我反思/评价 (→ 元认知)

2. 【提取】对每条相关内容进行维度标注，输出结构化化石

3. 【汇总】展示提取结果摘要：
   📂 记忆分析完成！
   扫描了 N 条历史记录
   提取了 M 个特征化石
   六维度覆盖率: 5/6

4. 【建档】生成初始人格档案，询问用户是否调整
```

### 输出示例
```
📂 记忆分析报告
─────────────────
扫描范围: 最近30天的对话记录
扫描条目: 47条
提取化石: 12个
─────────────────
维度覆盖率:
  🔵 生物基座 ★★★★☆ (3个化石)
  🟢 自传记忆 ★★★☆☆ (2个化石)
  🟡 认知架构 ★★★★★ (4个化石)
  🔴 情感动力 ★★☆☆☆ (1个化石)
  🟣 社会网络 ★★☆☆☆ (1个化石)
  🟠 元认知 ★★★☆☆ (2个化石)
─────────────────
✅ 初始人格档案已建立！
[💬 切换到对话提取] [⏰ 设置自动提取]
```

---

## ⏰ 后台模式与自动提取

### 首次提取后自动进入
无论用户选择哪种模式，完成首次提取后，AI 主动询问：

```
✅ 首次人格建模完成！
是否开启「后台自动提取」？

[1] 📅 每周自动提取一次（推荐）
[2] 📅 每天自动提取一次
[3] 🔕 手动模式（不自动提取）
```

### 自动提取行为
```
根据用户选择，后续自动执行：

【每周模式】  → 每周固定时间提醒用户：
  "🔥 火种·灵魂 周报时间到了，聊聊这周发生了什么？"

【每天模式】  → 每日对话末尾自动扫描：
  "📝 正在提取今日对话特征..."
  在用户无感知的情况下完成提取

【手动模式】  → 用户可随时说：
  「提取化石」「更新人格」「分析记忆」
```

### AI 自动提取的规则
- 自动提取时**不需要每次都输出完整卡片**，只需简要提示
- 每次提取后与上一次画像做**增量对比**
- 发现显著变化（如某维度变动超过20%）时主动提醒用户
- 每月自动生成一次**演化报告**

### 用户主动触发指令
```
用户任何时候可以说：
  「提取化石」     → 立即执行一次提取（当前模式）
  「更新人格」     → 重新蒸馏生成最新人格画像
  「查看人格」     → 展示当前人格快照卡片
  「分析记忆」     → 切换到记忆分析模式
  「对话提取」     → 切换到对话提取模式
  「设置提取」     → 修改自动提取频率
  「演化报告」     → 生成人格变化轨迹报告
  「🧬 生成报告」  → 输出完整人格报告
  「📊 演化对比」  → 对比上次画像变化
  「🔍 检索化石」  → 搜索历史特征
```

> **版本**: 2.0.0  
> **最后更新**: 2026-05-09  
> **技能定位**: 人格建模与记忆沉淀（独立升级版）  
> **设计理念**: "从对话中提取思维化石，蒸馏人格模型，构建数字孪生"

---

## 📚 架构参考（以下为技术细节，供深度使用参考）

### 1.1 设计理念

火种·灵魂 v2.0 是火种技能的完全独立升级版，整合了原版本的核心能力并进行了全面优化。其设计灵感来源于考古学中的"化石挖掘"——用户的每一次对话都是思维的痕迹，通过系统化的提取、蒸馏和建模，可以构建出用户的人格数字孪生。

**核心哲学**：
- **提取即洞察**：从看似随意的对话中识别稳定的思维模式
- **蒸馏即升华**：将零散的观察提炼为结构化的人格模型
- **演化即成长**：持续追踪人格模型的动态变化

### 1.2 核心能力

| 能力模块 | 功能描述 | 技术实现 |
|---------|---------|---------|
| **化石提取引擎** | 六大维度特征提取 | 多任务学习架构 |
| **置信度校准器** | 贝叶斯更新机制 | 历史准确率追踪 |
| **隐空间映射器** | 语义相似度计算 | Sentence Transformers |
| **人格蒸馏器** | 跨会话聚合建模 | 聚类分析 + 时间序列 |
| **演化追踪器** | 人格变化轨迹 | 版本控制 + 差异分析 |

### 1.3 六维度提取框架

基于心理学大五人格理论和认知科学最新研究，火种 v2.0 采用六维度提取框架：

```
维度1: 生物物理基座 (Bio-Physical Base)
  ├─ 能量水平 (Energy Level)
  ├─ 作息规律 (Sleep Pattern)
  └─ 健康意识 (Health Awareness)

维度2: 自传体记忆 (Autobiographical Memory)
  ├─ 关键事件 (Key Events)
  ├─ 情感锚点 (Emotional Anchors)
  └─ 身份认同 (Identity Markers)

维度3: 认知架构 (Cognitive Architecture)
  ├─ 决策风格 (Decision Style)
  ├─ 风险偏好 (Risk Preference)
  └─ 学习模式 (Learning Pattern)

维度4: 情感动力学 (Affective Dynamics)
  ├─ 情绪触发 (Emotional Triggers)
  ├─ 应对机制 (Coping Mechanisms)
  └─ 情感表达 (Expression Style)

维度5: 社会网络 (Social Network)
  ├─ 关系模式 (Relationship Patterns)
  ├─ 社交偏好 (Social Preferences)
  └─ 影响力圈 (Influence Circle)

维度6: 元认知自我 (Meta-Cognitive Self)
  ├─ 自我觉察 (Self-Awareness)
  ├─ 反思能力 (Reflective Capacity)
  └─ 成长心态 (Growth Mindset)
```

---

## 二、技能架构

### 2.1 目录结构

```
skills/soul-fireseed-v2/
├── SKILL.md                          # 技能定义文件（本文件）
├── README.md                         # 使用指南和API参考
├── manifest.json                     # 技能元数据
├── config/
│   ├── defaults.json                 # 默认配置
│   ├── schema.json                   # 配置Schema
│   └── keywords.json                 # 六维度关键词库
├── lib/
│   ├── __init__.py                   # 包初始化
│   ├── extractor.py                  # 主提取引擎
│   ├── distiller.py                  # 人格蒸馏器
│   ├── embedder.py                   # 隐空间映射器
│   ├── validator.py                  # 置信度校验器
│   ├── utils.py                      # 工具函数
│   └── models/
│       ├── __init__.py
│       ├── persona_model.py          # 人格模型
│       ├── evolution_tracker.py      # 演化追踪器
│       └── similarity_engine.py      # 相似度引擎
├── templates/
│   ├── fossil-snapshot.md.j2         # 化石快照模板
│   ├── profile.md.j2                 # 用户画像报告模板
│   ├── fingerprint.json.j2           # 人格指纹模板
│   └── evolution-report.md.j2        # 演化报告模板
├── scripts/
│   ├── extract.sh                    # 快速提取脚本
│   ├── distill.sh                    # 批量蒸馏脚本
│   └── export_profile.sh             # 导出画像脚本
├── tests/
│   ├── test_extractor.py             # 提取器测试
│   ├── test_distiller.py             # 蒸馏器测试
│   ├── test_embedder.py              # 嵌入器测试
│   ├── test_validator.py             # 校验器测试
│   └── test_integration.py           # 集成测试
└── docs/
    ├── extraction_guide.md           # 提取指南
    ├── dimension_reference.md        # 维度参考手册
    └── troubleshooting.md            # 故障排除
```

### 2.2 核心数据流

```
用户输入（对话/文本）
│
▼
[Phase 1] 预处理
│  - 分词和句法分析
│  - 情感极性标注
│  - 实体识别
│
▼
[Phase 2] 并行提取（六大维度）
│  BioPhysicalExtractor      → 化石列表 (维度1)
│  AutobiographicalExtractor → 化石列表 (维度2)
│  CognitiveExtractor        → 化石列表 (维度3)
│  AffectiveExtractor        → 化石列表 (维度4)
│  SocialNetworkExtractor    → 化石列表 (维度5)
│  MetaCognitiveExtractor    → 化石列表 (维度6)
│
▼
[Phase 3] 置信度校准
│  Validator.calibrate()
│  - 历史准确率加权
│  - 一致性检查
│  - 矛盾检测
│
▼
[Phase 4] 隐空间映射
│  Embedder.embed()
│  - 向量化表示
│  - 相似度计算
│  - 聚类分析
│
▼
[Phase 5] 化石存储
│  - 写入 user-data/fossils/
│  - 更新索引
│  - 触发总线通知
│
▼
[Phase 6] 定期蒸馏（后台任务）
│  Distiller.distill()
│  - 跨会话聚合
│  - 人格模型更新
│  - 演化轨迹记录
│
▼
[输出] 化石集合 / 人格画像 / 演化报告
```

---

## 三、核心机制详解

### 3.1 化石提取引擎（`FossilExtractor`）

**设计原理**：借鉴 FirmAE 的模块化提取器架构[2](@ref)，将复杂的特征提取任务拆分为六个独立的维度提取器，每个提取器专注一个维度的特征识别。

**核心方法**：

| 方法 | 功能 | 返回值 |
|------|------|--------|
| `extract()` | 主入口，执行完整提取流程 | `List[Fossil]` |
| `_preprocess()` | 文本预处理（分词、标注） | `Dict` |
| `_parallel_extract()` | 并行调用六个维度提取器 | `Dict[int, List[Fossil]]` |
| `_validate_and_calibrate()` | 置信度校准 | `List[Fossil]` |
| `_store_fossils()` | 持久化存储 | `bool` |

**提取策略**：
- **关键词匹配**：基于维度专属关键词库进行初步筛选
- **模式识别**：使用正则表达式识别典型表达模式
- **上下文推理**：结合对话历史推断隐含特征
- **交叉验证**：多个维度提取器相互验证

### 3.2 人格蒸馏器（`FossilDistiller`）

**设计原理**：借鉴数据挖掘中的"频繁模式挖掘"思想，从大量化石中识别稳定出现的人格特征，形成结构化的人格模型。

**蒸馏流程**：

1. **化石聚合**：按维度分组，收集所有相关化石
2. **聚类分析**：使用 DBSCAN 算法识别特征簇
3. **特征提炼**：从每个簇中提取代表性特征
4. **权重计算**：基于频率、置信度、时效性计算权重
5. **模型构建**：生成六维度人格向量

**人格模型结构**：

```json
{
  "user_id": "USR-20260509-001",
  "version": "2.0",
  "dimensions": {
    "bio_physical": {
      "energy_level": 0.72,
      "sleep_regularity": 0.65,
      "health_awareness": 0.80
    },
    "autobiographical": {
      "key_events_count": 15,
      "emotional_anchors": ["achievement", "family"],
      "identity_markers": ["engineer", "learner"]
    },
    "cognitive": {
      "decision_style": "analytical",
      "risk_preference": 0.45,
      "learning_pattern": "visual"
    },
    "affective": {
      "dominant_emotion": "curiosity",
      "emotional_stability": 0.68,
      "expression_style": "reserved"
    },
    "social": {
      "relationship_pattern": "selective",
      "social_preference": 0.40,
      "influence_circle_size": 12
    },
    "meta_cognitive": {
      "self_awareness": 0.75,
      "reflective_capacity": 0.82,
      "growth_mindset": 0.88
    }
  },
  "evolution_timeline": [...],
  "last_updated": "2026-05-09T20:00:00Z"
}
```

### 3.3 隐空间映射器（`FossilEmbedder`）

**设计原理**：使用预训练的 Sentence Transformers 模型将化石文本映射到 768 维语义空间，支持语义相似度计算和聚类分析。

**核心功能**：

| 功能 | 说明 | 应用场景 |
|------|------|---------|
| **向量化** | 文本 → 768维向量 | 化石索引建立 |
| **相似度计算** | 余弦相似度 | 重复检测、关联推荐 |
| **聚类分析** | DBSCAN/K-Means | 特征簇识别 |
| **语义检索** | 向量搜索 | 快速查找相关化石 |

### 3.4 置信度校验器（`ConfidenceValidator`）

**设计原理**：基于贝叶斯更新理论，维护每个提取器的历史准确率，动态调整置信度评分。

**校准公式**：

```
校准后置信度 = 原始置信度 × 历史准确率 × 一致性系数

其中：
- 历史准确率 = 正确预测数 / 总预测数（滑动窗口：最近100次）
- 一致性系数 = 1.0 + 0.2 × (相关化石支持数 - 相关化石反对数)
```

**矛盾检测**：
- 检测同一维度内的矛盾化石（如"我喜欢冒险" vs "我讨厌风险"）
- 标记矛盾对，降低双方置信度
- 生成待确认列表，需要用户澄清

---

## 四、配置项说明

### 4.1 核心配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `extraction.max_fossils_per_dimension` | 2 | 每维度最大化石数 |
| `extraction.pending_confidence_threshold` | 0.6 | 待确认阈值 |
| `extraction.high_confidence_threshold` | 0.8 | 高置信度阈值 |
| `extraction.min_confidence` | 0.2 | 最小保留置信度 |
| `distillation.batch_size` | 50 | 蒸馏批处理大小 |
| `distillation.frequency_hours` | 24 | 自动蒸馏间隔 |
| `embedding.model_name` | "sentence-transformers/all-MiniLM-L6-v2" | 嵌入模型 |
| `validation.historical_window` | 100 | 历史准确率窗口 |
| `storage.auto_backup` | true | 自动备份 |
| `storage.backup_retention_days` | 30 | 备份保留天数 |

### 4.2 维度权重配置

初始权重均匀分布，后续由蒸馏器根据信息量动态调整：

```json
{
  "dimension_weights": {
    "1_bio_physical": 1.0,
    "2_autobiographical": 1.0,
    "3_cognitive": 1.0,
    "4_affective": 1.0,
    "5_social": 1.0,
    "6_meta_cognitive": 1.0
  }
}
```

---

## 五、依赖与接口

### 5.1 外部依赖

```txt
Python >= 3.8
sentence-transformers >= 2.2.0
scikit-learn >= 1.0.0
numpy >= 1.21.0
pandas >= 1.3.0
jinja2 >= 3.0.0
```

### 5.2 独立运行模式

火种 v2.0 设计为**完全独立技能**，不依赖其他技能：

- ✅ 无需北斗聚焦提供聚焦点
- ✅ 无需破局决策提供决策记录
- ✅ 可单独部署和运行
- ✅ 自有数据存储和索引

### 5.3 对外接口

| 接口 | 类型 | 说明 |
|------|------|------|
| `FossilExtractor.extract()` | 主入口 | 从文本提取化石 |
| `FossilExtractor.batch_extract()` | 批量 | 批量提取化石 |
| `FossilDistiller.distill()` | 蒸馏 | 生成人格模型 |
| `FossilDistiller.get_evolution()` | 查询 | 获取演化轨迹 |
| `FossilEmbedder.find_similar()` | 检索 | 语义检索化石 |
| `ConfidenceValidator.validate()` | 校验 | 验证化石可信度 |

### 5.4 数据输出

**化石文件** (`user-data/fossils/{fossil_id}.json`)：
```json
{
  "id": "FOSSIL-20260509T200000-a3b2c1",
  "dimension": 3,
  "subdimension": "决策风格",
  "content": "倾向于分析型决策，先收集信息再行动",
  "timestamp": "2026-05-09T20:00:00Z",
  "confidence": 0.85,
  "source_quote": "我觉得做决策时，我更倾向于先收集足够信息再行动",
  "tags": ["决策风格", "分析型"],
  "metadata": {...}
}
```

**人格画像** (`user-data/persona/profile_v2.json`)：
- 六维度人格向量
- 演化时间线
- 关键特征摘要

---

## 六、最佳实践

### ✅ 推荐使用方式

1. **每日对话后自动提取**
   ```bash
   ./scripts/extract.sh --auto --input today_conversation.txt
   ```

2. **每周批量蒸馏**
   ```bash
   ./scripts/distill.sh --batch --output weekly_profile.md
   ```

3. **定期查看演化报告**
   ```python
   from lib import FossilDistiller
   distiller = FossilDistiller()
   report = distiller.generate_evolution_report(days=30)
   print(report)
   ```

4. **语义检索历史化石**
   ```python
   from lib import FossilEmbedder
   embedder = FossilEmbedder()
   similar = embedder.find_similar("我对风险的看法", top_k=5)
   ```

### ❌ 避免的用法

1. **单次对话提取过多化石**（超过10个会导致噪声增加）
2. **忽略低置信度化石**（它们可能包含重要信号）
3. **不进行定期蒸馏**（人格模型会过时）
4. **手动修改化石文件**（应通过 API 操作）

---

## 七、版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| 2.1.0 | 2026-05-09 | 新增双模式（对话提取+记忆分析）+ 后台自动提取（每周/每日） |
| 2.0.1 | 2026-05-09 | 优化AI交互流程，新增「点燃火种」等激活指令 |
| 2.0.0 | 2026-05-09 | 完全独立升级版，整合所有优秀功能 |
| 1.0.0 | 2026-05-05 | 初始版本（已废弃） |

**v2.1.0 改进**：
- ✨ 两种提取模式：对话提取 + 记忆分析批量提取
- ✨ 首次提取后自动进入后台模式
- ✨ 支持每周/每日自动提取，增量对比
- ✨ 新增「提取化石」「更新人格」「设置提取」等指令
- ✨ 记忆分析模式可扫描历史对话批量产出化石

---

## 八、参考来源

- 大五人格理论 (Big Five Personality Traits)
- 认知科学中的特征提取方法
- FirmAE 模块化提取器架构[2](@ref)
- LIWC 词典分析方法[7](@ref)
- Sentence Transformers 语义嵌入技术
- DBSCAN 聚类算法
- 贝叶斯置信度更新理论

---

## 九、许可证

MIT License - FireSeed Team © 2026
