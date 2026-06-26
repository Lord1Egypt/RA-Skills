# Source Router — 完整用例

本文档提供 3 个端到端示例，展示从输入到输出的完整路由决策过程。

---

## 用例 1：实时新闻场景

**任务**：追踪某科技公司突发制裁事件的最新进展和影响

### 输入

```json
{
  "task_type": "breaking_news",
  "primary_subject": "某科技公司被美国制裁",
  "goal_mode": "investigate",
  "freshness_required": "high",
  "available_sources": ["web", "local_file", "vector", "counter"],
  "need_counter_evidence": true,
  "information_gaps": ["制裁具体条款", "公司股价影响", "供应链影响", "公司应对措施"],
  "budget_limit": 10
}
```

### 输出

```json
{
  "task_id": "SR-d4f2a8c7",
  "task_type": "breaking_news",
  "primary_subject": "某科技公司被美国制裁",
  "selected_sources": [
    {
      "source": "web",
      "priority": 1,
      "rationale": "breaking_news + freshness=high → web绝对优先，需要实时信源",
      "search_hints": [
        "某科技公司 制裁 最新进展 今天",
        "某科技公司 制裁 条款 具体内容 BIS实体清单",
        "某科技公司 股价 影响 盘前盘后",
        "某科技公司 供应链 上下游 合作伙伴 影响",
        "某科技公司 制裁 官方回应 声明"
      ]
    },
    {
      "source": "counter",
      "priority": 2,
      "rationale": "investigate模式 + 显式要求反证 → 必须开启反证搜索",
      "search_hints": [
        "某科技公司 制裁 影响 高估 低估 质疑",
        "美国制裁 实际效果 历史案例 争议"
      ]
    },
    {
      "source": "local_file",
      "priority": 3,
      "rationale": "检查是否有该公司的历史资料和之前的制裁记录作为背景",
      "search_hints": [
        "memory/*某科技公司*",
        "outbox/*制裁*"
      ]
    },
    {
      "source": "vector",
      "priority": 4,
      "rationale": "检索历史知识库中的相关背景，补充行业基准",
      "search_hints": [
        "该公司 历史 制裁 背景",
        "半导体供应链 制裁 历史"
      ]
    }
  ],
  "search_order": ["web", "counter", "local_file", "vector"],
  "counter_search_enabled": true,
  "counter_trigger": "task_type=breaking_news + need_counter_evidence=true + goal_mode=investigate",
  "stop_rule": {
    "condition": "找到3个独立权威信源确认同一事实，或信息缺口100%覆盖",
    "max_rounds": 3
  },
  "budget_allocation": {
    "total_budget": 10,
    "web": 6,
    "counter": 2,
    "local_file": 1,
    "vector": 1
  }
}
```

### 决策路径
```
freshness=high → web优先(70%)
task_type=breaking_news → confirm web+counter
need_counter_evidence=true → counter开启
information_gaps有4个缺口 → web需要5-6次覆盖
剩余预算 → local(1) + vector(1) 补充背景
```

---

## 用例 2：内部知识场景

**任务**：从内部知识库中提取某个已完成项目的经验教训

### 输入

```json
{
  "task_type": "internal_knowledge",
  "primary_subject": "公众号爆款文章生产SOP执行记录",
  "goal_mode": "analyze",
  "freshness_required": "low",
  "available_sources": ["local_file", "vector"],
  "need_counter_evidence": false,
  "information_gaps": ["SOP执行次数", "质量评分趋势", "熔断原因", "改进措施"],
  "budget_limit": 6
}
```

### 输出

```json
{
  "task_id": "SR-e7b3c1d5",
  "task_type": "internal_knowledge",
  "primary_subject": "公众号爆款文章生产SOP执行记录",
  "selected_sources": [
    {
      "source": "vector",
      "priority": 1,
      "rationale": "内部知识 + freshness=low → 向量库优先，语义检索SOP执行记录",
      "search_hints": [
        "SOP-006 执行记录 质量评分",
        "公众号文章 爆款 生产流程 经验教训",
        "熔断 质量不达标 原因分析"
      ]
    },
    {
      "source": "local_file",
      "priority": 2,
      "rationale": "直接读取已知路径的AAR复盘文件和SOP文档",
      "search_hints": [
        "memory/aar/*SOP006*",
        "memory/quality_evaluation*",
        "01_core/memory/sop006*"
      ]
    }
  ],
  "search_order": ["vector", "local_file"],
  "counter_search_enabled": false,
  "counter_trigger": null,
  "stop_rule": {
    "condition": "本地命中≥5条相关文档，且覆盖信息缺口的80%以上",
    "max_rounds": 3
  },
  "budget_allocation": {
    "total_budget": 6,
    "vector": 4,
    "local_file": 2
  }
}
```

### 决策路径
```
task_type=internal_knowledge → 本地优先
freshness=low → 确认无需web
need_counter_evidence=false → counter跳过
available_sources=[local_file, vector] → 仅用这两个
vector语义检索 → 4次覆盖4个缺口
local_file精确读取 → 2次补充
```

---

## 用例 3：实体关系场景

**任务**：分析某个跨国企业的全球供应链关系网络

### 输入

```json
{
  "task_type": "entity_analysis",
  "primary_subject": "Apple全球供应链",
  "goal_mode": "analyze",
  "freshness_required": "medium",
  "available_sources": ["web", "vector", "graph", "counter"],
  "need_counter_evidence": true,
  "information_gaps": ["核心供应商列表", "地理分布", "替代供应商", "地缘政治风险"],
  "budget_limit": 12
}
```

### 输出

```json
{
  "task_id": "SR-f9a6d2e8",
  "task_type": "entity_analysis",
  "primary_subject": "Apple全球供应链",
  "selected_sources": [
    {
      "source": "graph",
      "priority": 1,
      "rationale": "entity_analysis → 知识图谱优先，挖掘Apple与供应商的关系网络",
      "search_hints": [
        "Apple 核心供应商 1度关系",
        "Apple 供应商 地理分布 中国 台湾 韩国 日本",
        "Apple 供应链 替代供应商 2度关系",
        "Apple 供应商 地缘政治风险 制裁 关系"
      ]
    },
    {
      "source": "web",
      "priority": 2,
      "rationale": "freshness=medium → 需要补充最新供应商变动和地缘政治动态",
      "search_hints": [
        "Apple 供应商名单 2024 2025 最新",
        "Apple 供应链 中国转移 印度越南 进展",
        "Apple 供应商 地缘政治风险 关税"
      ]
    },
    {
      "source": "vector",
      "priority": 3,
      "rationale": "检索历史知识库中的供应链分析报告",
      "search_hints": [
        "Apple 供应链 分析 报告",
        "半导体供应链 关系网络"
      ]
    },
    {
      "source": "counter",
      "priority": 4,
      "rationale": "analyze模式 + 显式要求反证 → 验证供应链稳定性叙事",
      "search_hints": [
        "Apple 供应链 脆弱性 单点故障 风险",
        "Apple 供应商转移 成功失败案例 质疑"
      ]
    }
  ],
  "search_order": ["graph", "web", "vector", "counter"],
  "counter_search_enabled": true,
  "counter_trigger": "need_counter_evidence=true + task_type=entity_analysis",
  "stop_rule": {
    "condition": "主实体关系网络≥5个核心节点，且覆盖3种以上关系类型（供应/竞争/地缘）",
    "max_rounds": 4
  },
  "budget_allocation": {
    "total_budget": 12,
    "graph": 4,
    "web": 3,
    "vector": 3,
    "counter": 2
  }
}
```

### 决策路径
```
task_type=entity_analysis → graph优先(35%) + web补充(35%)
freshness=medium → graph+web混合策略
need_counter_evidence=true → counter开启
4个信息缺口 → graph(4次)覆盖关系+web(3次)覆盖最新动态
vector(3次)补充历史 → counter(2次)验证
```

---

## 用例速查表

| 用例 | 场景 | 主来源 | counter | 总预算 | stop_rule |
|------|------|--------|---------|--------|-----------|
| 1 | 实时新闻(制裁) | web(60%) | ✅ (20%) | 10 | 3权威信源确认 |
| 2 | 内部知识(SOP) | vector(67%) | ❌ | 6 | 5文档+80%覆盖 |
| 3 | 实体关系(供应链) | graph(33%)+web(25%) | ✅ (17%) | 12 | 5节点+3种关系 |
