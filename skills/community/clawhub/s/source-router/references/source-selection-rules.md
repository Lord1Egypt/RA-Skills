# Source Selection Rules — 来源选择详细规则

本文档是 source-router 的核心参考。详细说明 5 种来源的适用场景、优先级规则和决策分支。

---

## 1. web — 互联网搜索

### 适用场景
- 时效性要求高的任务（新闻、政策变动、市场动态）
- 本地/向量库无覆盖的外部知识
- 需要多角度、多信源交叉验证
- 技术评估需要最新 benchmark 数据

### 优先触发条件
- `freshness_required = high`
- `task_type = breaking_news`
- `information_gaps` 中包含"最新""近期""当前"等关键词
- `goal_mode = investigate` 且本地无相关材料

### 预算分配建议
- 高时效：占总预算 60-80%
- 中时效：占总预算 30-50%
- 低时效：占总预算 10-30%

### 降级条件
- 搜索引擎不可用 → 降级到 `local_file` + `vector`
- 返回结果全部低质量 → 缩小搜索范围换关键词重试，最多 2 次
- GFW 封堵目标域名 → 切换备用引擎或放弃该信源

---

## 2. local_file — 本地文件系统

### 适用场景
- 已知本地有相关历史材料（缓存、报告、笔记）
- 内部知识检索（不需要联网）
- 低成本、高速度的信息获取
- 历史数据对比基准

### 优先触发条件
- `task_type = internal_knowledge`
- `freshness_required = low`
- `primary_subject` 在记忆系统中有历史记录
- `available_sources` 中 `vector` 不可用但 `local_file` 可用

### 预算分配建议
- 通常占总预算 10-20%
- 内部知识场景：占总预算 60-80%

### 搜索策略
- 优先搜索路径：`memory/` → `outbox/` → workspace 其他目录
- 文件类型优先级：`.md` > `.json` > `.txt` > `.csv`

---

## 3. vector — 向量数据库/知识库

### 适用场景
- 语义检索（模糊匹配、概念关联）
- 大量历史知识的快速召回
- "我记得之前看到过相关内容"的模糊需求
- 知识密集型任务的背景知识加载

### 优先触发条件
- `task_type = deep_research` 或 `internal_knowledge`
- `freshness_required = medium` 或 `low`
- 需要从大量历史材料中提取相关片段
- `goal_mode = analyze` 且需要背景知识

### 预算分配建议
- 深度研究：占总预算 20-30%
- 内部知识：占总预算 40-60%
- 其他：占总预算 10-20%

### 局限
- 需要预先索引，未索引的内容无法检索
- 不包含实时信息
- 语义相似 ≠ 事实相关，可能召回噪声

---

## 4. graph — 知识图谱/关系数据库

### 适用场景
- 实体关系挖掘（谁和谁有关、上下游关系、影响链条）
- 结构化推理（A→B→C 的因果链）
- 实体分析任务（人物关系、产业链、组织架构）
- 需要可视化关系网络的场景

### 优先触发条件
- `task_type = entity_analysis`
- 任务描述包含"关系""网络""链条""上下游""利益相关"
- `primary_subject` 是人名、公司名、组织名
- 需要 N 度关系查询（A 的供应商的竞争对手）

### 预算分配建议
- 实体分析：占总预算 30-40%
- 深度研究：占总预算 15-25%
- 其他：0-15%（按需）

### 搜索策略
- 从主实体出发，按关系类型分层扩展
- 优先 1 度关系，需要时扩展到 2-3 度
- 每次扩展记录已访问节点，防止循环

---

## 5. counter — 反证搜索

### 适用场景
- 任何需要质疑主线叙事的场景
- 评估型任务（政策效果、技术优劣、投资价值）
- 需要避免确认偏误的深度研究
- 数据真实性存疑时

### 触发条件（满足任一即开启）

| 条件 | 说明 |
|------|------|
| `need_counter_evidence = true` | 显式要求 |
| `task_type = evaluate` | 评估天然需要反面证据 |
| `task_type = investigate` | 调查需要多角度验证 |
| `goal_mode = compare` | 对比需要看到各方优劣势 |

### 可以跳过的条件（同时满足）

| 条件 | 说明 |
|------|------|
| `need_counter_evidence = false` | 明确不需要 |
| `budget_limit ≤ 3` | 预算极其紧张 |
| `task_type = internal_knowledge` | 纯内部检索 |

### 搜索策略
- 对主查询添加否定/质疑词缀（"质疑""争议""失败""反面""缺点""局限性"）
- 从与主流信源对立的方向搜索
- 关注学术批评、监管警告、失败案例

### 预算分配
- 开启时：占总预算 15-25%
- 通常 2-3 次搜索足够

---

## 决策分支树

```
START
├─ freshness_required = high?
│   ├─ YES → web(70%) + counter(20%) + 其他(10%)
│   └─ NO → continue
│
├─ task_type = internal_knowledge?
│   ├─ YES → local_file(50%) + vector(40%) + web(10%)
│   └─ NO → continue
│
├─ task_type = entity_analysis?
│   ├─ YES → graph(35%) + web(35%) + vector(20%) + counter(10%)
│   └─ NO → continue
│
├─ task_type = deep_research?
│   ├─ YES → web(30%) + vector(25%) + graph(20%) + counter(15%) + local(10%)
│   └─ NO → continue
│
├─ task_type = tech_evaluation?
│   ├─ YES → web(40%) + vector(25%) + counter(25%) + local(10%)
│   └─ NO → continue
│
└─ default → web(40%) + vector(25%) + local(20%) + counter(15%)
```

---

## stop_rule 规则集

### 通用模板
```
stop_rule = {
  "condition": <条件描述>,
  "max_rounds": <最大搜索轮数>
}
```

### 预设条件

| 场景 | condition | max_rounds |
|------|-----------|------------|
| 高时效新闻 | "找到3个独立权威信源确认同一事实" | 3 |
| 深度研究 | "每类来源至少覆盖2次，累计找到≥10条高置信度结果" | 5 |
| 实体分析 | "主实体关系网络 ≥5个节点，且覆盖3种以上关系类型" | 4 |
| 内部知识 | "本地命中 ≥5条相关文档，且覆盖信息缺口的80%以上" | 3 |
| 技术评估 | "找到至少2份独立benchmark/评测报告，且覆盖目标变量的正反两面" | 4 |
| 默认 | "总搜索轮数达到上限，或连续2轮无新增高价值结果" | 3 |

### 动态调整
- 搜索结果质量高（S/A级信源占比 ≥50%）→ 可提前停止
- 搜索结果质量低（C级信源占比 ≥70%）→ 换策略重试 1 次，仍低则停止并报告

---

## 搜索降级链详细规则

### 默认降级链配置

| 级别 | 搜索源 | 触发降级条件 | 优势 | 劣势 |
|------|--------|-------------|------|------|
| P1 | tavily_search | 配额耗尽/超时30s/空结果 | 英文搜索质量高，结构化输出 | 月配额1000次 |
| P2 | bailian_web_search | API错误/超时30s | 国内服务器零延迟，中文质量高 | 需要API配置 |
| P3 | web_search | 空结果/GFW封堵 | Brave API通用搜索 | GFW风险 |
| P4 | web_fetch_direct | 全部失败 | 直接URL模板访问 | 结果非结构化 |
| P5 | local_cache | 无 | 零成本 | 可能过时 |

### 降级事件记录格式

```json
{
  "degradation_log": [
    {
      "from_level": 1,
      "to_level": 2,
      "reason": "quota_exhausted",
      "timestamp": "2026-03-26T15:20:00Z",
      "query_affected": "AI芯片 市场份额 2026"
    }
  ]
}
```

### 自定义降级链

当 `available_sources` 显式提供时，降级链基于可用源重建：
- 从默认链中筛选可用源，保持原始优先级顺序
- 不可用源从链中移除，相邻级别直接衔接
- 如果可用源为空，降级到 local_cache

---

## budget_allocation 策略

### 默认总预算：10 次搜索

若未指定 `budget_limit`，默认总预算为 10 次搜索调用。

### 分配原则
1. 优先保证主来源（决策分支确定的最高优先级来源）≥50% 预算
2. counter 开启时固定分配 15-25%
3. 剩余预算在次要来源间按优先级分配
4. 单个来源最少分配 1 次（除非 decision branch 明确排除）

### 预算紧张时（≤5 次）
- 仅保留前 2 个优先级来源
- counter 仅在显式要求时保留（分配 1 次）
- stop_rule.max_rounds 降为 2
