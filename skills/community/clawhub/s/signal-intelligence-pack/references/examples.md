# 端到端用例

## 用例 1: 战略分析 — "评估全球AI芯片竞争格局"

### 统一输入

```json
{
  "primary_task": "评估全球AI芯片竞争格局，分析主要玩家的技术路线、市场份额和发展趋势",
  "primary_subject": "全球AI芯片产业",
  "canonical_time_frame": "2025-01至今",
  "goal_mode": "strategic",
  "target_variable": "AI芯片市场份额与竞争态势",
  "available_sources": ["tavily", "bailian", "web_search"]
}
```

### 判定：必须跑满5步（goal_mode=strategic）

---

### Step 1: query-planner 输出

```json
{
  "planned_queries": [
    {
      "query_id": "Q1",
      "dimension": "市场份额",
      "query": "AI芯片市场份额2025 NVIDIA AMD Intel 竞争格局",
      "intent": "获取当前主要厂商的AI芯片市场占有率数据",
      "keywords": ["AI芯片", "市场份额", "NVIDIA", "AMD", "Intel"]
    },
    {
      "query_id": "Q2",
      "dimension": "技术路线",
      "query": "NVIDIA Blackwell vs AMD MI400 vs Intel Gaudi4 技术对比 benchmark 2025",
      "intent": "对比三大厂商最新AI芯片的技术参数和性能基准",
      "keywords": ["Blackwell", "MI400", "Gaudi4", "benchmark", "技术对比"]
    },
    {
      "query_id": "Q3",
      "dimension": "新兴挑战者",
      "query": "Google TPU v6 Amazon Trainium2 Groq LPU AI芯片新进入者 2025",
      "intent": "识别除NVIDIA/AMD/Intel外的新兴AI芯片玩家",
      "keywords": ["TPU", "Trainium", "Groq", "LPU", "AI芯片挑战者"]
    },
    {
      "query_id": "Q4",
      "dimension": "地缘政治",
      "query": "美国AI芯片出口管制 CHIPS Act 2025 影响分析",
      "intent": "评估地缘政治对AI芯片供应链的影响",
      "keywords": ["出口管制", "CHIPS Act", "供应链", "地缘政治"]
    },
    {
      "query_id": "Q5",
      "dimension": "需求趋势",
      "query": "AI算力需求增长 大模型训练推理 2025 趋势预测",
      "intent": "分析AI算力需求端的增长趋势和结构变化",
      "keywords": ["算力需求", "大模型训练", "推理", "增长趋势"]
    },
    {
      "query_id": "Q6",
      "dimension": "国产替代",
      "query": "中国AI芯片国产替代 华为昇腾 寒武纪 海光 2025进展",
      "intent": "评估中国AI芯片自主化进展",
      "keywords": ["华为昇腾", "寒武纪", "海光", "国产替代"]
    }
  ],
  "counter_queries": [
    {
      "query_id": "CQ1",
      "targets_dimension": "市场份额",
      "query": "NVIDIA AI芯片市场份额下降 AMD崛起 挑战者侵蚀 2025",
      "expected_counter_type": "直接反驳"
    },
    {
      "query_id": "CQ2",
      "targets_dimension": "技术路线",
      "query": "GPU不再是AI最优架构 专用芯片ASIC NPU超越GPU 2025",
      "expected_counter_type": "因果替代"
    },
    {
      "query_id": "CQ3",
      "targets_dimension": "需求趋势",
      "query": "AI算力泡沫 过度建设 算力过剩 需求放缓 2025",
      "expected_counter_type": "条件反转"
    }
  ],
  "dimensions": [
    { "name": "市场份额", "description": "主要厂商的市场占有率", "query_count": 2 },
    { "name": "技术路线", "description": "芯片架构和性能对比", "query_count": 2 },
    { "name": "新兴挑战者", "description": "新进入AI芯片市场的玩家", "query_count": 1 },
    { "name": "地缘政治", "description": "政策对供应链的影响", "query_count": 1 },
    { "name": "需求趋势", "description": "算力需求增长预测", "query_count": 2 },
    { "name": "国产替代", "description": "中国AI芯片自主化", "query_count": 1 }
  ]
}
```

---

### Step 2: source-router 输出

```json
{
  "routed_queries": [
    { "query_id": "Q1", "query": "AI芯片市场份额2025...", "assigned_source": "tavily", "source_type": "search_engine", "priority": 1, "method": "tavily_search", "fallback_source": "web_search" },
    { "query_id": "Q2", "query": "NVIDIA Blackwell vs AMD...", "assigned_source": "tavily", "source_type": "search_engine", "priority": 1, "method": "tavily_search", "fallback_source": "bailian" },
    { "query_id": "Q3", "query": "Google TPU v6 Amazon...", "assigned_source": "tavily", "source_type": "search_engine", "priority": 2, "method": "tavily_search", "fallback_source": "web_search" },
    { "query_id": "Q4", "query": "美国AI芯片出口管制...", "assigned_source": "tavily", "source_type": "search_engine", "priority": 2, "method": "tavily_search", "fallback_source": "bailian" },
    { "query_id": "Q5", "query": "AI算力需求增长...", "assigned_source": "tavily", "source_type": "search_engine", "priority": 1, "method": "tavily_search", "fallback_source": "web_search" },
    { "query_id": "Q6", "query": "中国AI芯片国产替代...", "assigned_source": "bailian", "source_type": "search_engine", "priority": 1, "method": "bailian_search", "fallback_source": "tavily" },
    { "query_id": "CQ1", "query": "NVIDIA AI芯片市场份额下降...", "assigned_source": "tavily", "source_type": "search_engine", "priority": 2, "method": "tavily_search", "fallback_source": "web_search" },
    { "query_id": "CQ2", "query": "GPU不再是AI最优架构...", "assigned_source": "tavily", "source_type": "search_engine", "priority": 3, "method": "tavily_search", "fallback_source": "web_search" },
    { "query_id": "CQ3", "query": "AI算力泡沫...", "assigned_source": "tavily", "source_type": "search_engine", "priority": 2, "method": "tavily_search", "fallback_source": "bailian" }
  ],
  "source_coverage": {
    "total_queries": 9,
    "unique_sources_used": 2,
    "source_breakdown": { "tavily": 8, "bailian": 1 }
  }
}
```

---

### Step 3: evidence-cleaner 输出（节选）

```json
{
  "cleaned_evidence": [
    {
      "evidence_id": "E1",
      "source_query_id": "Q1",
      "content": "NVIDIA在AI加速器市场的份额约为80%，AMD约12%，Intel约1%。NVIDIA的份额较2023年的92%有所下降。",
      "source_url": "https://example.com/ai-chip-market-share-2025",
      "source_rating": "A",
      "relevance_score": 0.95,
      "is_counter": false,
      "timestamp_raw": ["2025年3月"]
    },
    {
      "evidence_id": "E2",
      "source_query_id": "Q2",
      "content": "NVIDIA Blackwell B200在MLPerf训练基准中比H100快2.2倍，AMD MI400尚未发布正式benchmark。",
      "source_url": "https://mlcommons.org/benchmarks",
      "source_rating": "S",
      "relevance_score": 0.92,
      "is_counter": false,
      "timestamp_raw": ["2025年1月"]
    },
    {
      "evidence_id": "E3",
      "source_query_id": "Q6",
      "content": "华为昇腾910B在大模型推理场景性能达到A100的80-90%，已部署至多个国产大模型训练集群。",
      "source_url": "https://example.com/huawei-ascend-review",
      "source_rating": "A",
      "relevance_score": 0.88,
      "is_counter": false,
      "timestamp_raw": ["2025年2月"]
    },
    {
      "evidence_id": "E4",
      "source_query_id": "CQ3",
      "content": "Microsoft、Meta、Google三家公司在2024年AI基础设施上的资本支出合计超过$1500亿，但AI变现收入增速未能匹配，华尔街开始质疑投资回报率。",
      "source_url": "https://example.com/ai-capex-roi-concern",
      "source_rating": "A",
      "relevance_score": 0.85,
      "is_counter": true,
      "timestamp_raw": ["2025年3月"]
    }
  ],
  "coverage_report": {
    "total_raw_results": 47,
    "after_dedup": 32,
    "after_filtering": 28,
    "dimension_coverage": {
      "市场份额": { "hits": 8, "status": "covered" },
      "技术路线": { "hits": 6, "status": "covered" },
      "新兴挑战者": { "hits": 5, "status": "covered" },
      "地缘政治": { "hits": 4, "status": "covered" },
      "需求趋势": { "hits": 3, "status": "covered" },
      "国产替代": { "hits": 2, "status": "partial" }
    }
  }
}
```

---

### Step 4: freshness-judge 输出（节选）

```json
{
  "dated_evidence": [
    { "evidence_id": "E1", "publish_date": "2025-03-15", "freshness": "fresh", "freshness_note": "在canonical_time_frame内", "canonical_alignment": "in_window" },
    { "evidence_id": "E2", "publish_date": "2025-01-22", "freshness": "fresh", "freshness_note": "在canonical_time_frame内", "canonical_alignment": "in_window" },
    { "evidence_id": "E3", "publish_date": "2025-02-10", "freshness": "fresh", "freshness_note": "在canonical_time_frame内", "canonical_alignment": "in_window" },
    { "evidence_id": "E4", "publish_date": "2025-03-20", "freshness": "fresh", "freshness_note": "在canonical_time_frame内", "canonical_alignment": "in_window" }
  ],
  "freshness_report": {
    "fresh_count": 22,
    "aging_count": 4,
    "stale_count": 1,
    "unknown_count": 1,
    "overall_freshness_score": 82
  },
  "staleness_warnings": [
    {
      "evidence_id": "E8",
      "warning": "该证据引用的AMD MI300X市场份额数据来自2024年Q2，当前MI400即将发布",
      "recommendation": "需验证AMD最新一代产品的市场接受度数据"
    }
  ]
}
```

---

### Step 5: counter-evidence-hunter 输出（节选）

```json
{
  "mainline_synthesis": "NVIDIA在AI芯片市场仍占据绝对主导地位（~80%份额），Blackwell架构维持技术领先，但AMD/Google/Amazon等挑战者正在从专用场景切入蚕食份额，同时AI算力投资回报率面临质疑。",
  "counter_evidence": [
    {
      "content": "三大超大规模云厂商合计$1500亿AI基础设施投资，但AI变现收入增速不匹配，华尔街开始质疑AI算力需求是否被高估",
      "source": "华尔街日报/摩根士丹利分析报告",
      "strength": "hard",
      "counter_type": "条件反转",
      "rebuttal_to": "AI算力需求将持续指数级增长"
    },
    {
      "content": "Google TPU v6在内部推理工作负载中成本仅为同等级NVIDIA GPU的60%，Google正通过云服务将TPU性价比优势外化",
      "source": "Google Cloud官方博客, Anyscale基准测试",
      "strength": "soft",
      "counter_type": "因果替代",
      "rebuttal_to": "GPU架构是AI训练和推理的唯一最优解"
    }
  ],
  "flip_conditions": [
    {
      "condition": "AMD MI400在2025下半年发布且MLPerf基准达到B200的70%以上，同时定价低于B200的50%",
      "probability": "medium",
      "impact_if_triggered": "NVIDIA份额可能在12个月内从80%降至70%以下，竞争格局从'一家独大'转向'双寡头'",
      "time_horizon": "2025 Q4 - 2026 Q2"
    },
    {
      "condition": "AI应用变现收入增速持续低于基础设施投入增速超过4个季度",
      "probability": "low-medium",
      "impact_if_triggered": "超大规模云厂商将削减AI芯片采购，整个市场进入'算力过剩'周期",
      "time_horizon": "2026"
    }
  ],
  "alternative_supports": [
    {
      "alternative_path": "竞争格局的核心变量不是芯片性能，而是软件生态（CUDA vs ROCm vs 自研框架）",
      "supporting_evidence": ["CUDA拥有超过400万开发者生态", "AMD ROCm开发者生态仍不到CUDA的10%", "但PyTorch 2.x的OpenXLA正在降低对CUDA的依赖"],
      "compatibility_with_mainline": "extends"
    }
  ],
  "confidence_assessment": {
    "mainline_robustness": "medium",
    "blind_spots": ["国产替代维度的证据覆盖不足（partial）", "缺乏NVIDIA下一代Rubin架构的公开信息"],
    "search_coverage": "adequate"
  }
}
```

---

### 最终增强证据底座（summary部分）

```json
{
  "metadata": {
    "generated_at": "2025-03-26T15:00:00+08:00",
    "pipeline_version": "1.0",
    "steps_completed": 5,
    "steps_degraded": [],
    "stop_reason": "full_run"
  },
  "input_snapshot": { "...": "（同输入）" },
  "pipeline_steps": { "...": "（包含全部5步输出）" },
  "summary": {
    "evidence_count": 28,
    "fresh_evidence_count": 22,
    "counter_evidence_count": 2,
    "flip_condition_count": 2,
    "mainline_robustness": "medium",
    "key_findings": [
      "NVIDIA仍主导AI芯片市场（~80%份额）但份额持续被蚕食",
      "Blackwell架构维持性能领先，但价格策略面临AMD竞争压力",
      "AI基础设施投资回报率受到华尔街质疑，可能影响需求预期",
      "TPU等专用芯片在推理场景展现出成本优势"
    ],
    "critical_gaps": [
      "国产替代维度覆盖不足，华为昇腾最新进展信息有限",
      "NVIDIA下一代Rubin架构信息缺失"
    ],
    "recommendation": "主线判断韧性为中等，建议在最终分析中特别关注AI投资回报率风险和专用芯片替代路径。国产替代维度需补充搜索后再做战略判断。"
  }
}
```

---

## 用例 2: 新闻情报 — "分析某公司突发被制裁事件的连锁影响"

### 统一输入

```json
{
  "primary_task": "分析某中国科技公司被美国列入实体清单后的连锁影响，包括供应链、业务、市场和股价",
  "primary_subject": "某中国科技公司（假设场景）",
  "canonical_time_frame": "过去72小时",
  "goal_mode": "tactical",
  "target_variable": "制裁事件的多维度连锁影响",
  "available_sources": null
}
```

### 判定：检测到高风险关键词"制裁"，必须跑满5步

---

### 各步产出衔接

**Step 1 查询规划**:
- Q1: 实体清单具体限制内容（技术/芯片/软件）
- Q2: 公司供应链依赖美国技术的环节
- Q3: 公司海外业务占比和客户分布
- Q4: 股价和债券市场反应
- Q5: 类似案例的历史对比（华为/中芯国际/大疆）
- CQ1: 公司是否有替代供应商预案
- CQ2: 制裁是否可逆或存在豁免机制

**Step 2 来源路由**:
- Q1-Q4 → tavily（时效性要求高）
- Q5 → tavily + web_fetch（需要历史对比）
- CQ1-CQ2 → tavily

**Step 3 证据清洗**:
- 获取约35条原始结果
- 去重后28条
- 关键发现：供应链维度证据最丰富，替代预案维度证据稀少

**Step 4 新鲜度判断**:
- 72小时内新闻占比85%（新鲜度得分91）
- 1条引用2023年华为制裁分析为历史参照，标注为aging
- 无stale证据

**Step 5 反证搜索**:
- 主线："制裁将导致公司业务严重受损"
- 反证1（hard）：公司此前已布局2年的"备胎计划"，关键芯片库存可支撑18个月（软反证 → 硬反证）
- 翻转条件：若公司成功通过第三方渠道绕过核心限制，短期影响可控
- 替代路径：制裁可能加速公司技术自主化，长期反而增强竞争力（参考华为案例）

**最终summary**:
- 证据28条，fresh 24条
- 关键发现：供应链冲击确定，但公司有18个月缓冲期；股价短期承压但可能超跌
- 临界缺口：缺乏公司内部应对计划的一手信息
- 建议：基于历史案例（华为）分析，短期冲击确定但长期影响高度取决于自主替代进度

---

## 用例 3: 技术调研 — "对比RAG vs Fine-tuning在企业知识管理中的适用性"

### 统一输入

```json
{
  "primary_task": "对比RAG和Fine-tuning在企业知识管理场景中的适用性，为技术选型提供依据",
  "primary_subject": "RAG vs Fine-tuning技术",
  "canonical_time_frame": "2024-2025",
  "goal_mode": "tactical",
  "target_variable": "两种技术方案在企业知识管理中的适用场景和限制",
  "available_sources": null
}
```

### 判定：goal_mode=tactical，但涉及决策依赖型评估，检测到"决策"信号 → 跑满5步

---

### 各步产出衔接

**Step 1 查询规划**:
- Q1: RAG在企业知识管理中的应用案例和效果数据
- Q2: Fine-tuning在企业知识管理中的应用案例和效果数据
- Q3: RAG vs Fine-tuning学术对比研究
- Q4: 企业知识管理场景的技术需求特征（更新频率、数据量、精度要求）
- Q5: 混合方案（RAG + Fine-tuning）的实践案例
- CQ1: RAG在特定场景下的已知局限性（幻觉、检索质量、延迟）
- CQ2: Fine-tuning在特定场景下的已知局限性（知识过时、灾难性遗忘、成本）
- CQ3: 是否存在超越RAG和Fine-tuning的第三种方案

**Step 2 来源路由**:
- Q1-Q2 → tavily（行业案例）
- Q3 → tavily（学术论文）
- Q4 → tavily（行业分析报告）
- Q5 → tavily
- CQ1-CQ3 → tavily

**Step 3 证据清洗**:
- 获取约42条原始结果
- 去重后31条
- 信源分布：S级（学术论文/官方文档）6条，A级（技术博客/行业报告）15条，B级（快讯）10条

**Step 4 新鲜度判断**:
- 2024-2025年证据占比75%
- 核心发现：RAG技术迭代较快（2024年GraphRAG、Agentic RAG等新范式出现），部分早期对比结论可能已过时
- 过时预警：2条2023年的RAG评估引用的是旧版embedding模型，结论需更新

**Step 5 反证搜索**:
- 主线倾向："RAG在企业知识管理中优于Fine-tuning"
- 反证1（soft）：Fine-tuning在需要高度领域专业术语一致性时优于RAG（如医疗、法律）
- 反证2（soft）：RAG的检索质量高度依赖embedding模型选择和文档分块策略，工程复杂度被低估
- 反证3（hard）：2024年多家企业反馈RAG在实时知识更新场景中仍存在"知识窗口"问题，无法真正替代Fine-tuning的知识内化
- 翻转条件：若企业知识更新频率极高（每日/每小时），RAG的优势将被实时性需求部分抵消
- 替代路径：RAG + Fine-tuning混合方案可能比单一方案更优；GraphRAG/Agentic RAG正在改变传统RAG的局限性

**最终summary**:
- 证据31条，fresh 23条
- 关键发现：(1) RAG在大多数知识管理场景更适用但工程复杂度高；(2) Fine-tuning在深度领域知识和术语一致性场景有优势；(3) 混合方案成为越来越多企业的选择；(4) GraphRAG等新范式可能改变传统对比结论
- 临界缺口：缺乏大规模生产环境的A/B测试数据（多数案例为概念验证阶段）
- 建议：技术选型应基于具体业务场景决定，不建议"一刀切"。对于知识更新频繁且对实时性要求高的场景，RAG更优；对于需要深度领域理解和术语一致性的场景，Fine-tuning更优；预算充足时建议评估混合方案
