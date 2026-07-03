# TRL评估Skill集成方案

> **版本**：v1.0 | **日期**：2026-06-19 | **作者**：OPC产品管理组 | **状态**：正式发布
> **关联Skill**：opc-trl-assessment（Skill #61）
> **关联文档**：技术说明书_v1.0、成熟度评估_v1.0

---

## 一、集成目标

将已开发的TRL评估Skill（#61 opc-trl-assessment）集成到5角色Agent编排中，使评估师角色具备自动化的TRL定级能力，实现：

1. 评估师在标准化报告阶段自动调用TRL评估
2. TRL评估结果自动注入评估报告JSON Schema
3. 所长和经理人可直接消费TRL评估结论进行后续决策

---

## 二、集成架构

### 2.1 TRL评估在5角色编排中的位置

```
用户输入 → 所长意图识别 → 任务路由
  │
  ├─→ 猎手工作流 ──→ 移交标准包(JSON) ──→ 经理人接收
  │                                          │
  │                              Gate 0 评审（所长）
  │                                          │
  │                                     经理人建档
  │                                          │
  │                              ┌───────────┴───────────┐
  │                              │  委托评估师            │
  │                              │  ┌─────────────────┐  │
  │                              │  │ TRL评估Skill调用 │  │  ← 新增
  │                              │  │ (opc-trl-assessment)│
  │                              │  └────────┬────────┘  │
  │                              │           │             │
  │                              │  四层尽调  │  TRL定级    │
  │                              │  风险评估  │  差距分析   │
  │                              │           │             │
  │                              └───────────┴───────────┘
  │                                          │
  │                              Gate 1 评审（所长+评估师）
  │                                          │
  │                                     经理人整合
  │                                          │
  │                              创意师介入（按需）
  │                                          │
  │                              Gate 2 评审（所长+评估师）
  │                                          │
  │                                     转化方案设计
  │                                          │
  │                              Gate 3 评审（所长）
  │                                          │
  │                                     交付闭环
```

### 2.2 触发条件

| 触发场景 | 触发方式 | 调用方 |
|----------|---------|--------|
| Gate 0 通过后，经理人委托评估 | 自动触发 | 经理人工作流 |
| 用户直接请求"评估这个项目" | 意图识别触发 | 所长编排引擎 |
| 评估师主动要求TRL定级 | 手动触发 | 评估师Agent |
| 项目阶段变更（如完成中试） | 事件触发 | 经理人工作流 |

### 2.3 调用链路

```
经理人工作流(#63)
  → 委托评估师
    → 评估师Agent
      → TRL评估Skill(#61)
        → Step 1: 成果信息收集（交互式问答）
        → Step 2: 证据链完整性检查
        → Step 3: TRL定级判定
        → Step 4: 差距分析
        → Step 5: 转化路径建议
        → Step 6: 风险概率估算
        → Step 7: 评估报告生成
      ← 返回 TRL评估结果(JSON)
    ← 评估师整合进评估报告
  ← 经理人消费评估报告
```

---

## 三、输入输出接口

### 3.1 TRL评估Skill输入（评估师→Skill）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TRLAssessmentInput",
  "type": "object",
  "required": ["tech_name", "tech_domain", "current_stage", "evidence_list", "target_trl"],
  "properties": {
    "tech_name": {
      "type": "string",
      "description": "技术成果名称"
    },
    "tech_domain": {
      "type": "string",
      "description": "技术领域"
    },
    "current_stage": {
      "type": "string",
      "enum": ["concept", "lab_validation", "component_validation", "environment_validation", "prototype_demo", "operation_validation", "test_complete", "commercial"],
      "description": "当前阶段（来自猎手移交包或经理人项目档案）"
    },
    "evidence_list": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["type", "description", "credibility"],
        "properties": {
          "type": {
            "type": "string",
            "enum": ["A_official", "B_third_party", "C_academic", "D_commercial", "E_internal", "F_self_claim"],
            "description": "证据类型：A类官方文件/B类第三方报告/C类学术发表/D类商业文件/E类内部文件/F类自我声明"
          },
          "description": {
            "type": "string",
            "description": "证据描述"
          },
          "credibility": {
            "type": "string",
            "enum": ["high", "medium", "low"],
            "description": "可信度"
          }
        }
      },
      "description": "已有证据清单"
    },
    "target_trl": {
      "type": "integer",
      "minimum": 1,
      "maximum": 9,
      "description": "目标TRL等级"
    },
    "industry_special": {
      "type": "string",
      "description": "行业特殊要求（如：航空需适航认证、药品需NMPA注册等）"
    },
    "resource_info": {
      "type": "object",
      "properties": {
        "team_size": { "type": "integer" },
        "invested_capital": { "type": "number" },
        "planned_investment": { "type": "number" },
        "timeline_months": { "type": "integer" }
      }
    }
  }
}
```

### 3.2 TRL评估Skill输出（Skill→评估师）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TRLAssessmentOutput",
  "type": "object",
  "required": ["assessment_id", "trl_result", "evidence_evaluation", "gap_analysis", "conversion_path", "risk_estimation"],
  "properties": {
    "assessment_id": {
      "type": "string",
      "pattern": "^TRL-\\d{8}-\\d{3}$",
      "description": "评估编号"
    },
    "assessment_date": {
      "type": "string",
      "format": "date"
    },
    "trl_result": {
      "type": "object",
      "required": ["current_trl", "trl_name", "evidence", "confidence"],
      "properties": {
        "current_trl": { "type": "integer", "minimum": 1, "maximum": 9 },
        "trl_name": { "type": "string" },
        "evidence": {
          "type": "array",
          "items": { "type": "string" }
        },
        "confidence": { "type": "string", "enum": ["high", "medium", "low"] },
        "key_gaps": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "evidence_evaluation": {
      "type": "object",
      "properties": {
        "completeness": { "type": "string", "enum": ["complete", "partial", "insufficient"] },
        "missing_items": {
          "type": "array",
          "items": { "type": "string" }
        },
        "quality_assessment": { "type": "string" }
      }
    },
    "gap_analysis": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "from_trl": { "type": "integer" },
          "to_trl": { "type": "integer" },
          "gap_description": { "type": "string" },
          "required_evidence": { "type": "array", "items": { "type": "string" } },
          "estimated_duration_months": { "type": "integer" },
          "estimated_investment": { "type": "number" },
          "key_bottleneck": { "type": "string" }
        }
      }
    },
    "conversion_path": {
      "type": "object",
      "properties": {
        "recommended_mode": { "type": "string", "enum": ["concept_validation", "pilot_base", "industry_incubation", "direct_commercialization"] },
        "typical_partners": { "type": "array", "items": { "type": "string" } },
        "funding_requirement": { "type": "string" },
        "key_actions": { "type": "array", "items": { "type": "string" } }
      }
    },
    "risk_estimation": {
      "type": "object",
      "properties": {
        "composite_success_rate": { "type": "number", "description": "复合成功率(0-1)" },
        "risk_level": { "type": "string", "enum": ["极高风险", "高风险", "中高风险", "中等风险", "较低风险"] },
        "major_risks": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "risk": { "type": "string" },
              "probability": { "type": "string" },
              "impact": { "type": "string" },
              "mitigation": { "type": "string" }
            }
          }
        }
      }
    }
  }
}
```

### 3.3 评估师→经理人的输出增强

评估师原有的 `EvaluationReport` JSON Schema 新增 `trl_assessment_detail` 字段，直接嵌入TRL评估Skill的完整输出：

```json
{
  "trl_assessment": {
    // 保留原有简版字段（current_trl, evidence, confidence, key_gaps）
  },
  "trl_assessment_detail": {
    // 新增：TRL评估Skill完整输出（TRLAssessmentOutput）
    "assessment_id": "TRL-20260619-001",
    "evidence_evaluation": { ... },
    "gap_analysis": [ ... ],
    "conversion_path": { ... },
    "risk_estimation": { ... }
  }
}
```

---

## 四、编排规则

### 4.1 所长编排引擎更新

所长编排引擎（Skill #65）需新增以下路由规则：

```python
# 所长意图识别新增规则
if intent == "evaluate_project" or intent == "assess_technology":
    route_to("evaluator", task="trl_assessment", skill="opc-trl-assessment")

# Gate 0 通过后自动触发
if gate_0_result == "pass":
    route_to("manager", task="setup_project")
    route_to("evaluator", task="full_evaluation", include_skill="opc-trl-assessment")
```

### 4.2 评估师工作流更新

评估师在"标准化报告"阶段自动调用TRL评估Skill：

```
评估师工作流（更新后）：
  1. 接收经理人委托
  2. 解析移交标准包 → 提取项目信息
  3. 调用 TRL评估Skill(#61)
     - 输入：从移交包提取的tech_name, tech_domain, current_stage, evidence_list等
     - 输出：TRLAssessmentOutput
  4. 执行四层尽调（L1-L4）
  5. 整合TRL评估结果 + 尽调结果 → 生成完整评估报告
  6. 输出 EvaluationReport(JSON) → 经理人
```

### 4.3 经理人工作流更新

经理人接收到评估报告后，自动解析 `trl_assessment_detail`：

```
经理人工作流（更新后）：
  1. 接收移交标准包 → 建立项目档案
  2. 委托评估师 → 等待评估报告
  3. 解析评估报告中的 trl_assessment_detail
     - current_trl → 项目分级（A/B/C/D）
     - gap_analysis → 转化方案设计依据
     - conversion_path → 转化模式选择
     - risk_estimation → 风险登记册更新
  4. 基于TRL结论制定项目计划
  5. 提交 Gate 1 评审
```

---

## 五、错误处理与兜底

### 5.1 TRL评估Skill调用失败

| 错误场景 | 处理策略 |
|----------|---------|
| Skill超时（>60s） | 降级为评估师手动TRL定级，标注"自动评估不可用" |
| 证据不足无法定级 | 输出TRL范围（如TRL 3-4），标注置信度"低" |
| 输入数据缺失 | 从项目档案自动补全，仍缺失则暂停并请求人工补充 |
| 结果与四层尽调冲突 | 以就低原则为准，标注冲突点，所长最终裁决 |

### 5.2 置信度降级规则

| 置信度 | Gate评审影响 |
|--------|-------------|
| high | 正常流程 |
| medium | Gate评审需额外确认TRL结论 |
| low | 必须人工专家介入确认TRL，否则Gate不通过 |

---

## 六、集成验收标准

| # | 验收项 | 标准 | 状态 |
|---|--------|------|------|
| 1 | TRL评估Skill可被评估师调用 | 输入技术描述，输出TRL定级+证据+置信度 | ✅ 已验证 |
| 2 | 评估报告包含TRL详细评估 | EvaluationReport含trl_assessment_detail | ⬜ 待验证 |
| 3 | 经理人可消费TRL结论 | 项目分级和计划基于TRL结果 | ⬜ 待验证 |
| 4 | 纳米涂层案例端到端跑通 | 5阶段全流程数据传递无断裂 | ⬜ 待验证 |
| 5 | Gate评审含TRL判断 | Gate 1/2评审结果含TRL置信度 | ⬜ 待验证 |

---

*本集成方案将随TRL评估Skill和编排引擎的迭代持续更新。*
