# 统一输入输出Schema

## 1. 统一最小输入 Schema

```json
{
  "$schema": "UnifiedInput",
  "type": "object",
  "required": ["primary_task", "primary_subject", "canonical_time_frame", "goal_mode"],
  "properties": {
    "primary_task": {
      "type": "string",
      "description": "用户的原始任务描述，完整保留原始意图"
    },
    "primary_subject": {
      "type": "string",
      "description": "任务核心对象/实体（如'全球AI芯片产业'、'OpenAI公司'、'RAG技术'）"
    },
    "canonical_time_frame": {
      "type": "string",
      "description": "相关时间窗口（如'2025-01至今'、'过去30天'、'2024全年'）"
    },
    "goal_mode": {
      "type": "string",
      "enum": ["strategic", "tactical", "informational"],
      "description": "strategic=战略级深度分析, tactical=战术级快速评估, informational=信息整理"
    },
    "target_variable": {
      "type": ["string", "null"],
      "description": "需要判断/预测的目标变量（如'AI芯片市场份额'、'公司股价趋势'），可为空"
    },
    "available_sources": {
      "type": ["array", "null"],
      "items": { "type": "string" },
      "description": "可用的搜索来源/工具列表（如['tavily', 'web_search', 'bailian']），为空则自动检测"
    }
  }
}
```

---

## 2. Step 1 中间输出: query-planner

```json
{
  "$schema": "Step1Output",
  "type": "object",
  "properties": {
    "planned_queries": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "query_id": "string — 唯一标识 (Q1, Q2, ...)",
          "dimension": "string — 所属维度名称",
          "query": "string — 搜索查询文本",
          "intent": "string — 搜索意图描述",
          "keywords": ["string — 核心关键词"]
        }
      },
      "minItems": 3,
      "description": "正向查询，≥3条"
    },
    "counter_queries": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "query_id": "string — 唯一标识 (CQ1, CQ2, ...)",
          "targets_dimension": "string — 反证针对的维度",
          "query": "string — 反向搜索查询",
          "expected_counter_type": "string — 预期反证类型"
        }
      },
      "minItems": 2,
      "description": "反证查询，≥2条"
    },
    "dimensions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": "string — 维度名称",
          "description": "string — 维度说明",
          "query_count": "number — 该维度下的查询数"
        }
      },
      "description": "拆解的维度列表"
    }
  }
}
```

---

## 3. Step 2 中间输出: source-router

```json
{
  "$schema": "Step2Output",
  "type": "object",
  "properties": {
    "routed_queries": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "query_id": "string — 关联Step1的query_id",
          "query": "string — 原始查询",
          "assigned_source": "string — 分配的来源",
          "source_type": "string — 来源类型 (search_engine | api | rss | direct_fetch | database)",
          "priority": "number — 优先级 (1=最高)",
          "method": "string — 执行方式描述",
          "fallback_source": "string — 降级备选来源"
        }
      }
    },
    "source_coverage": {
      "type": "object",
      "properties": {
        "total_queries": "number",
        "unique_sources_used": "number",
        "source_breakdown": {
          "type": "object",
          "additionalProperties": "number",
          "description": "来源 → 分配查询数"
        }
      }
    }
  }
}
```

---

## 4. Step 3 中间输出: evidence-cleaner

```json
{
  "$schema": "Step3Output",
  "type": "object",
  "properties": {
    "cleaned_evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "evidence_id": "string — 唯一标识 (E1, E2, ...)",
          "source_query_id": "string — 来源查询ID",
          "content": "string — 核心信息摘要",
          "source_url": "string — 来源URL",
          "source_rating": "string — 信源评级 (S | A | B | C)",
          "relevance_score": "number — 相关性评分 (0-1)",
          "is_counter": "boolean — 是否为反证查询的结果",
          "timestamp_raw": ["string | null — 原始时间戳文本"]
        }
      }
    },
    "coverage_report": {
      "type": "object",
      "properties": {
        "total_raw_results": "number",
        "after_dedup": "number",
        "after_filtering": "number",
        "dimension_coverage": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "properties": {
              "hits": "number",
              "status": "string — covered | partial | zero_hit"
            }
          }
        }
      }
    }
  }
}
```

---

## 5. Step 4 中间输出: freshness-judge

```json
{
  "$schema": "Step4Output",
  "type": "object",
  "properties": {
    "dated_evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "evidence_id": "string — 关联Step3的evidence_id",
          "publish_date": "string | null — ISO 8601格式",
          "freshness": "string — fresh | aging | stale | unknown",
          "freshness_note": "string — 新鲜度说明",
          "canonical_alignment": "string — in_window | outside_window | no_timestamp"
        }
      }
    },
    "freshness_report": {
      "type": "object",
      "properties": {
        "fresh_count": "number",
        "aging_count": "number",
        "stale_count": "number",
        "unknown_count": "number",
        "overall_freshness_score": "number — 0-100"
      }
    },
    "staleness_warnings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "evidence_id": "string",
          "warning": "string — 过时原因描述",
          "recommendation": "string — 建议操作（如'需验证该结论是否仍然成立'）"
        }
      },
      "description": "仅包含 aging 和 stale 级别的预警"
    }
  }
}
```

---

## 6. Step 5 中间输出: counter-evidence-hunter

```json
{
  "$schema": "Step5Output",
  "type": "object",
  "properties": {
    "mainline_synthesis": {
      "type": "string",
      "description": "从全部证据中归纳的主线叙事摘要（1-3句话）"
    },
    "counter_evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "content": "string — 反证内容",
          "source": "string — 来源",
          "strength": "string — hard | soft | noise",
          "counter_type": "string — 反证类型",
          "rebuttal_to": "string — 反驳主线中的哪个子命题"
        }
      }
    },
    "flip_conditions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "condition": "string — 翻转条件",
          "probability": "string — low | medium | high",
          "impact_if_triggered": "string — 触发后影响",
          "time_horizon": "string — 预估时间"
        }
      }
    },
    "alternative_supports": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "alternative_path": "string — 替代解释",
          "supporting_evidence": ["string — 支撑证据"],
          "compatibility_with_mainline": "string — contradicts | qualifies | extends"
        }
      }
    },
    "confidence_assessment": {
      "type": "object",
      "properties": {
        "overall_score": "number — 0-100 综合置信度评分",
        "dimensions": {
          "type": "object",
          "properties": {
            "source_quality": {
              "type": "object",
              "properties": {
                "score": "number — 0-100",
                "rationale": "string — 评分理由"
              }
            },
            "coverage_completeness": {
              "type": "object",
              "properties": {
                "score": "number — 0-100",
                "rationale": "string — 评分理由"
              }
            },
            "freshness_adequacy": {
              "type": "object",
              "properties": {
                "score": "number — 0-100",
                "rationale": "string — 评分理由"
              }
            },
            "counter_evidence_sufficiency": {
              "type": "object",
              "properties": {
                "score": "number — 0-100",
                "rationale": "string — 评分理由"
              }
            },
            "consistency": {
              "type": "object",
              "properties": {
                "score": "number — 0-100",
                "rationale": "string — 评分理由"
              }
            }
          }
        },
        "scoring_formula": "string — source_quality*0.25 + coverage*0.20 + freshness*0.20 + counter*0.20 + consistency*0.15",
        "score_thresholds": {
          "type": "object",
          "properties": {
            "high_confidence": "string — 80-100: 可直接进入下游分析",
            "medium_confidence": "string — 60-79: 关注扣分维度，选择性补搜",
            "low_confidence": "string — 40-59: 强烈建议回溯补充后重跑",
            "unusable": "string — 0-39: 放弃当前证据底座，重新规划搜索"
          }
        },
        "mainline_robustness": "string — high | medium | low",
        "blind_spots": ["string — 搜索盲区"],
        "search_coverage": "string — adequate | limited"
      }
    }
  }
}
```

---

## 7. 统一最终输出 Schema (Enhanced Evidence Base)

```json
{
  "$schema": "EnhancedEvidenceBase",
  "type": "object",
  "required": ["metadata", "input_snapshot", "pipeline_steps", "summary"],
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "generated_at": "string — ISO 8601生成时间",
        "pipeline_version": "string — 管线版本号",
        "steps_completed": "number — 完成步骤数 (3/4/5)",
        "steps_degraded": ["string — 降级执行的步骤"],
        "stop_reason": "string — 停止原因 (full_run | stopped_after_clean | stopped_after_freshness)"
      }
    },
    "input_snapshot": {
      "$ref": "UnifiedInput",
      "description": "原始输入的快照"
    },
    "pipeline_steps": {
      "type": "object",
      "properties": {
        "step1_query_planning": { "$ref": "Step1Output" },
        "step2_source_routing": { "$ref": "Step2Output" },
        "step3_evidence_cleaning": { "$ref": "Step3Output" },
        "step4_freshness_judging": { "$ref": "Step4Output", "description": "仅在steps_completed≥4时存在" },
        "step5_counter_evidence": { "$ref": "Step5Output", "description": "仅在steps_completed=5时存在" }
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "evidence_count": "number — 总证据条数",
        "fresh_evidence_count": "number — 新鲜证据数",
        "counter_evidence_count": "number — 反证条数",
        "flip_condition_count": "number — 翻转条件数",
        "mainline_robustness": "string — high | medium | low | unknown",
        "key_findings": ["string — 3-5条核心发现摘要"],
        "critical_gaps": ["string — 关键信息缺口"],
        "recommendation": "string — 对下游分析模块的建议"
      }
    },
    "pipeline_metadata": {
      "pipeline_version": "2.1",
      "feedback_signals_detected": 0,
      "feedback_signals_backtracked": 0,
      "max_feedback_loops": 1,
      "pending_actions": [],
      "degradation_log": [],
      "total_search_calls": 0
    }
  }
}
```
