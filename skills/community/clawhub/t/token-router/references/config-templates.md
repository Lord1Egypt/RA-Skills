# 用户配置模板

## 目录
- [基础配置模板](#基础配置模板)
- [策略预设](#策略预设)
- [场景化配置示例](#场景化配置示例)
- [平台专属配置](#平台专属配置)
- [Agent工作流配置](#agent工作流配置)
- [Memory 存储结构](#memory-存储结构)

> **价格时效性声明**：本文档中的模型定价更新于 2026年6月。模型价格频繁变动，使用前请以各厂商官方文档为准。
> 推荐通过 `openrouter.ai` 统一接入多模型，可避免频繁更新各厂商 API 配置。

---

## 基础配置模板

```yaml
# token-router-config.yaml
# 大模型自动切换配置文件

version: "1.0"

# 用户画像
profile:
  strategy: balanced  # cost_first | quality_first | balanced | custom
  monthly_budget_usd: null  # 可选：月度预算上限
  primary_language: zh  # zh | en | bilingual
  preferred_providers: []  # 留空表示不限制，可填 ["anthropic", "openai", "google"]

# 模型分级映射（可自定义）
tiers:
  L0:  # 路由级 - 意图分类、简单提取
    models:
      - name: deepseek-v4-flash
        provider: deepseek
        input_price: 0.14
        output_price: 0.28
      - name: gpt-4.1-nano
        provider: openai
        input_price: 0.10
        output_price: 0.40
      - name: gemini-2.5-flash-lite
        provider: google
        input_price: 0.10
        output_price: 0.40

  L1:  # 执行级 - 摘要、翻译、简单QA
    models:
      - name: claude-haiku-4.5
        provider: anthropic
        input_price: 0.80
        output_price: 4.00
      - name: minimax-m3
        provider: minimax
        input_price: 0.60
        output_price: 2.40
      - name: gemini-3.5-flash
        provider: google
        input_price: 1.50
        output_price: 9.00

  L2:  # 推理级 - 代码生成、分析报告
    models:
      - name: claude-sonnet-4.6
        provider: anthropic
        input_price: 3.00
        output_price: 15.00
      - name: gpt-5.5
        provider: openai
        input_price: 5.00
        output_price: 30.00

  L3:  # 创造级 - 架构设计、复杂规划
    models:
      - name: claude-opus-4.8
        provider: anthropic
        input_price: 5.00
        output_price: 25.00
      - name: gpt-5.5-pro
        provider: openai
        input_price: 待定
        output_price: 待定

# 安全规则（强制升级）
safety_rules:
  - trigger: "涉及金钱交易/支付"
    min_tier: L2
    reason: "金融相关任务需要高精度"
  - trigger: "法律/医疗/合规建议"
    min_tier: L2
    recommended: L3
    reason: "专业领域需要最强模型保障"
  - trigger: "生产环境代码修改"
    min_tier: L2
    reason: "生产代码变更需要高质量保障"
  - trigger: "安全审计/漏洞分析"
    min_tier: L2
    reason: "安全相关需要深度分析能力"

# 路由方式
routing:
  default_method: direct  # direct | cascade | hybrid
  cascade:
    quality_threshold: 0.8  # 级联路由的质量阈值
    max_retries: 3          # 最大升级次数
  hybrid:
    agent_steps: auto       # auto | manual

# 成本追踪
tracking:
  enabled: true
  log_level: summary  # summary | detailed
  report_frequency: per_session  # per_session | daily | weekly
```

---

## 策略预设

### 成本优先策略

```yaml
# 适合：个人开发者、预算有限的一人公司
strategy: cost_first

# 自定义覆盖
tier_overrides:
  # 大幅提升降级阈值
  L0_threshold: 8    # 默认6，提升到8意味着更多任务走L0
  L1_threshold: 12   # 默认10
  L2_threshold: 16   # 默认15
  # L3 只给最高分任务

# 默认模型选择（优先最便宜的）
default_models:
  L0: deepseek-v4-flash   # 最便宜
  L1: minimax-m3           # 开源+1M上下文，性价比极高
  L2: claude-sonnet-4.6    # 代码质量顶级
  L3: claude-opus-4.8      # 关键时刻用最强

# 级联路由（成本优先推荐级联）
routing:
  default_method: cascade
  cascade:
    quality_threshold: 0.75  # 稍低的质量阈值，容忍更多降级
```

### 质量优先策略

```yaml
# 适合：企业级应用、客户面向场景
strategy: quality_first

tier_overrides:
  # 降低降级阈值
  L0_threshold: 5    # 只有极简任务走L0
  L1_threshold: 8
  L2_threshold: 13
  # 更多任务走L2/L3

default_models:
  L0: gpt-4.1-nano
  L1: claude-haiku-4.5
  L2: claude-sonnet-4.6
  L3: claude-opus-4.8

routing:
  default_method: direct
```

### 平衡策略（推荐）

```yaml
# 适合：大多数场景
strategy: balanced

# 使用默认阈值
# 使用默认模型推荐
# 单次路由为主
routing:
  default_method: direct
```

---

## 场景化配置示例

### 一人公司（AI编程+内容创作）

```yaml
profile:
  strategy: cost_first
  monthly_budget_usd: 50

# 场景-模型映射
scene_mapping:
  coding:
    simple_fix: L1        # 简单bug修复
    feature_dev: L2       # 新功能开发
    architecture: L3      # 架构设计
    code_review: L1       # 代码审查

  content:
    outline: L1           # 大纲生成
    draft: L2             # 初稿写作
    polish: L2            # 润色
    seo_meta: L0          # SEO标签生成

  business:
    email_reply: L0       # 邮件回复
    data_analysis: L2     # 数据分析
    contract_review: L3   # 合同审查

# 月度预算熔断
circuit_breaker:
  enabled: true
  warning_at: 80%   # 80%预算时提醒
  hard_stop_at: 100%  # 100%时强制降级到L0
```

### AI客服 Agent

```yaml
profile:
  strategy: balanced
  primary_language: zh

scene_mapping:
  customer_service:
    intent_classification: L0
    faq_match: L0          # FAQ库匹配，可能不需要模型
    simple_inquiry: L0     # 简单查询
    complaint_handling: L2 # 投诉处理需要同理心
    refund_processing: L2  # 退款涉及金钱
    product_recommendation: L1

routing:
  default_method: hybrid
  hybrid:
    steps:
      - name: intent识别
        tier: L0
        model: gemini-2.0-flash
      - name: FAQ检索
        tier: skip          # 跳过模型，直接查库
      - name: 回复生成
        tier: dynamic       # 根据意图动态选择
      - name: 质量校验
        tier: L0
      - name: 敏感词过滤
        tier: L0
```

### 数字员工（企业内部）

```yaml
profile:
  strategy: quality_first
  primary_language: zh

safety_rules:
  - trigger: "涉及员工薪资"
    min_tier: L3
  - trigger: "涉及合同条款"
    min_tier: L3
  - trigger: "对外发送邮件"
    min_tier: L2
  - trigger: "内部文档查询"
    min_tier: L0

scene_mapping:
  hr:
    resume_screening: L1
    interview_question: L2
    policy_inquiry: L0
  finance:
    invoice_extraction: L0
    report_generation: L2
    budget_planning: L3
  it:
    ticket_classification: L0
    code_fix: L2
    security_audit: L3
```

---

## 平台专属配置

### OpenClaw 配置

OpenClaw 通过 `config.yaml` 的 `models.providers` 配置多模型路由，支持 `provider/model` 引用格式。

#### 3层级联路由配置

```yaml
# OpenClaw config.yaml - 3层级联路由
agents:
  defaults:
    model:
      primary: "deepseek/deepseek-v4-flash"      # L0 默认走最便宜的
      fallback: "anthropic/claude-sonnet-4-6"     # fallback 走 L2

models:
  mode: "merge"
  providers:
    deepseek:
      baseUrl: "https://api.deepseek.com/v1"
      apiKey: "${DEEPSEEK_API_KEY}"
      api: "openai-completions"
      models:
        - id: "deepseek-v4-flash"
          name: "DeepSeek V4 Flash"
          input: ["text"]
          cost:
            input_per_mtok: 0.14
            output_per_mtok: 0.28
        - id: "deepseek-v4-pro"
          name: "DeepSeek V4 Pro"
          input: ["text"]
          cost:
            input_per_mtok: 0.27
            output_per_mtok: 1.10

    anthropic:
      apiKey: "${ANTHROPIC_API_KEY}"
      api: "anthropic-messages"
      models:
        - id: "claude-sonnet-4-6"
          name: "Claude Sonnet 4.6"
          input: ["text"]
          cost:
            input_per_mtok: 3.00
            output_per_mtok: 15.00
        - id: "claude-opus-4-6"
          name: "Claude Opus 4.6"
          input: ["text"]
          cost:
            input_per_mtok: 5.00
            output_per_mtok: 25.00

    ollama:
      baseUrl: "http://localhost:11434"
      api: "openai-completions"
      models:
        - id: "qwen3.5:27b"
          name: "Qwen 3.5 27B (本地)"
          input: ["text"]
```

#### 本地模型 + API 混合配置

```yaml
# OpenClaw 本地优先 + API 升级
agents:
  defaults:
    model:
      primary: "ollama/qwen3.5:27b"           # 默认走本地（免费）
      fallback: "deepseek/deepseek-v4-flash"  # 本地失败走 API

models:
  providers:
    ollama:
      baseUrl: "http://localhost:11434"
      api: "openai-completions"
      models:
        - id: "qwen3.5:27b"
          name: "Qwen 3.5 27B"
        - id: "deepseek-v4-flash"  # 通过 Ollama 代理
          name: "DeepSeek V4 Flash"
```

### Hermes Agent 配置

Hermes 通过 `~/.hermes/config.yaml` 配置多 Provider，对话中用 `!model` 命令动态切换。

#### 3层级联配置（$8/月最佳实践）

```yaml
# ~/.hermes/config.yaml - 3层级联
providers:
  deepseek:
    api_key: ${HERMES_DEEPSEEK_KEY}
    default_model: deepseek-v4-flash    # L0 执行层
    models:
      - name: deepseek-v4-flash
        description: "执行层 - 文件编辑、工具调用、格式化"
      - name: deepseek-v4-pro
        description: "执行层增强 - 结构化输出、中等推理"

  openrouter:
    api_key: ${HERMES_OPENROUTER_KEY}
    default_model: minimax/m2           # L1 规划层
    models:
      - name: minimax/m2
        description: "规划层 - 步骤分解、工具选择"
      - name: kimi/k2-thinking
        description: "推理层 - 复杂逻辑链、困难决策"

  anthropic:
    api_key: ${HERMES_ANTHROPIC_KEY}
    default_model: claude-sonnet-4-6    # L2 推理层
    models:
      - name: claude-sonnet-4-6
        description: "推理层 - 代码生成、分析报告"
      - name: claude-opus-4-6
        description: "L3 创造层 - 架构设计、复杂规划"

# 自动路由规则
routing:
  default: deepseek-v4-flash           # 90% 的调用走最便宜的
  rules:
    - trigger: "plan|design|architect"  # 规划类关键词
      model: minimax/m2
    - trigger: "code|implement|debug"   # 编码类
      model: claude-sonnet-4-6
    - trigger: "security|audit|review"  # 安全相关（强制升级）
      model: claude-opus-4-6
    - trigger: "translate|summarize|format"  # 简单任务
      model: deepseek-v4-flash

# Failover 配置
failover:
  deepseek-v4-flash:
    - deepseek-v4-pro
    - openrouter/deepseek-v4-flash
  claude-sonnet-4-6:
    - openrouter/anthropic/claude-sonnet-4-6
    - kimi/k2-thinking
```

#### 月成本 $8 的实际配置

```yaml
# Hermes Agent $8/月配置（VPS $6.49 + API ~$1.50）
# 参考：Moe Lueker 的实际案例

providers:
  openrouter:
    api_key: ${OPENROUTER_KEY}
    default_model: deepseek/deepseek-v4-flash
    models:
      - name: deepseek/deepseek-v4-flash     # $0.14/$0.28 - 执行层
      - name: minimax/m2                     # ~$0.30/$1.20 - 规划层
      - name: kimi/k2-thinking               # $0.60/$2.50 - 推理层

routing:
  default: deepseek/deepseek-v4-flash
  rules:
    - trigger: "plan|design|decide"
      model: minimax/m2
    - trigger: "complex|reason|think"
      model: kimi/k2-thinking
```

#### 本地零成本配置

```yaml
# Hermes Agent 零API成本配置（通过 Ollama）
providers:
  ollama:
    base_url: http://localhost:11434
    default_model: qwen3.5:27b
    models:
      - name: qwen3.5:27b          # 主力模型（需 24GB VRAM）
      - name: qwen3.5:9b           # 轻量备选（需 8GB VRAM）
      - name: gemma4:26b-moe       # MoE 高效版（需 20GB VRAM）

routing:
  default: qwen3.5:27b
  rules:
    - trigger: "quick|simple|format"
      model: qwen3.5:9b
```

---

## Agent工作流配置

### SOLO Agent 集成模板

在 Trae SOLO Agent 中，可以通过自定义智能体实现模型切换：

```yaml
# 自定义智能体配置示例
agents:
  - name: model-router
    description: "评估任务复杂度，推荐最优模型层级"
    system_prompt: |
      你是模型路由专家。根据任务复杂度推荐模型层级。
      输出格式：JSON {"tier": "L0|L1|L2|L3", "model": "模型名", "reason": "推荐理由"}
    model: gemini-2.0-flash  # 路由器本身用最便宜的模型

  - name: light-executor
    description: "执行L0/L1级别的简单任务"
    model: deepseek-v4-pro

  - name: heavy-executor
    description: "执行L2/L3级别的复杂任务"
    model: claude-sonnet-4.6
```

### 通用 Agent 框架集成

```python
# model_router.py - 通用路由器实现

class ModelRouter:
    def __init__(self, config_path="token-router-config.yaml"):
        self.config = load_config(config_path)
        self.user_profile = load_memory("user_profile")
        self.cost_tracker = CostTracker()

    def route(self, task_description, task_type=None):
        """主路由方法"""
        # 1. 评估复杂度
        complexity = self.assess_complexity(task_description)

        # 2. 确定层级
        tier = self.complexity_to_tier(complexity)

        # 3. 安全检查
        tier = self.apply_safety_rules(task_description, tier)

        # 4. 用户偏好调整
        tier = self.apply_user_preferences(tier, task_type)

        # 5. 选择具体模型
        model = self.select_model(tier)

        # 6. 记录
        self.cost_tracker.log(task_type, tier, model)

        return model

    def assess_complexity(self, task):
        """四维度复杂度评估"""
        scores = {
            "reasoning": self._score_reasoning(task),
            "output_length": self._score_output_length(task),
            "precision": self._score_precision(task),
            "context": self._score_context(task),
        }
        return sum(scores.values()), scores

    def complexity_to_tier(self, total_score):
        """分数到层级映射"""
        if total_score <= 6: return "L0"
        if total_score <= 10: return "L1"
        if total_score <= 15: return "L2"
        return "L3"
```

---

## Memory 存储结构

### 用户画像存储

```json
{
  "token_router_profile": {
    "version": "1.0",
    "strategy": "balanced",
    "monthly_budget_usd": null,
    "created_at": "2026-06-03",
    "updated_at": "2026-06-03",
    "preferences": {
      "primary_language": "zh",
      "preferred_providers": [],
      "tier_overrides": {}
    },
    "feedback_history": [
      {
        "date": "2026-06-03",
        "task_type": "code_generation",
        "recommended_tier": "L1",
        "user_action": "upgraded",
        "new_minimum": "L2"
      }
    ],
    "usage_stats": {
      "total_recommendations": 0,
      "accepted": 0,
      "upgraded": 0,
      "downgraded": 0
    }
  }
}
```

### 成本追踪存储

```json
{
  "token_router_costs": {
    "period": "2026-06",
    "daily_logs": {
      "2026-06-03": {
        "calls": {
          "L0": 15,
          "L1": 8,
          "L2": 3,
          "L3": 1
        },
        "estimated_cost_usd": 0.52,
        "comparison_all_flagship_usd": 2.85,
        "savings_percent": 81.8
      }
    },
    "monthly_summary": {
      "total_calls": 0,
      "total_cost_usd": 0,
      "comparison_all_flagship_usd": 0,
      "savings_percent": 0
    }
  }
}
```
