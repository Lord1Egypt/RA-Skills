# 用户画像数据结构 - 详细Schema定义

## 整体画像结构

```json
{
  "profile_id": "user_001",
  "version": "2.0",
  "created_at": "2026-03-20T00:00:00",
  "updated_at": "2026-04-01T15:00:00",
  
  // 核心画像字段
  "profile": {
    "demographics": { ... },
    "profession": { ... },
    "values": { ... },
    "habits": { ... },
    "preferences": { ... }
  },
  
  // 元数据
  "metadata": {
    "confidence_summary": { ... },
    "contradictions": [ ... ],
    "quiz_pending": [ ... ],
    "update_history": [ ... ]
  }
}
```

## 核心字段详细定义

### 人口统计信息 (demographics)

```json
{
  "demographics": {
    "age": {
      "value": 42,
      "confidence": 0.95,
      "evidence": [
        {"source": "explicit_statement", "timestamp": "2026-04-01", "excerpt": "我42岁"},
        {"source": "context_inference", "timestamp": "2026-03-28", "excerpt": "提到孩子年龄推算"}
      ],
      "last_verified": "2026-04-01",
      "contradictions": []
    },
    "family_role": {
      "value": "husband_father",
      "confidence": 0.98,
      "evidence": [
        {"source": "explicit_statement", "timestamp": "2026-04-01", "excerpt": "老婆在国企，儿子6年级"}
      ],
      "details": {
        "partner": {"relation": "wife", "work": "state_enterprise"},
        "children": [
          {"relation": "son", "age": "6th_grade", "activity": "soccer"},
          {"relation": "daughter", "age": "3rd_grade", "activity": "piano"}
        ],
        "parents": {"status": "healthy", "age_range": "60s"}
      }
    }
  }
}
```

### 职业信息 (profession)

```json
{
  "profession": {
    "current_role": {
      "value": "product_manager",
      "display": "产品经理",
      "confidence": 0.96,
      "evidence": [
        {"source": "explicit_statement", "timestamp": "2026-03-15", "excerpt": "我是产品经理"}
      ],
      "details": {
        "industry": "internet",
        "experience_years": 12,
        "specialties": ["项目管理", "产品设计", "团队协作"],
        "employment_status": "employed", // employed/self_employed/seeking
        "entrepreneurial_interest": true
      }
    },
    "career_focus": {
      "value": ["ai_tech", "content_creation", "product_management"],
      "confidence": 0.85,
      "evidence": [
        {"source": "explicit_statement", "timestamp": "2026-04-01", "excerpt": "重心：AI创业、自媒体、产品管理"}
      ],
      "priority_order": [1, 2, 3] // 优先级排序
    }
  }
}
```

### 价值观体系 (values)

```json
{
  "values": {
    "core_values": {
      "value": ["family", "creation", "financial_independence"],
      "display": ["家庭", "创造", "财务独立"],
      "confidence": 0.88,
      "evidence": [
        {"source": "explicit_statement", "timestamp": "2026-04-01", "excerpt": "核心价值观：家庭、创造、财务独立"}
      ],
      "hierarchy": { // 价值优先级
        "family": 10,
        "creation": 9,
        "financial_independence": 8
      }
    },
    "work_principles": {
      "value": ["quality_first", "long_term", "efficiency"],
      "confidence": 0.82,
      "evidence": [
        {"source": "behavior_pattern", "timestamp": "2026-03-25", "excerpt": "反复强调工作质量"}
      ]
    }
  }
}
```

### 习惯模式 (habits)

```json
{
  "habits": {
    "work_pattern": {
      "value": "project_based",
      "confidence": 0.78,
      "evidence": [
        {"source": "behavior_pattern", "timestamp": "2026-03-20", "excerpt": "按项目周期安排工作"}
      ],
      "details": {
        "typical_hours": ["09:00-12:00", "14:00-18:00", "20:00-22:00"],
        "focus_pattern": "morning_peak", // morning_peak/evening_peak/biphasic
        "break_tendency": "afternoon_slump"
      }
    },
    "health_habits": {
      "value": "sleep_insufficient_exercise_low",
      "confidence": 0.85,
      "evidence": [
        {"source": "explicit_statement", "timestamp": "2026-04-01", "excerpt": "睡眠不足，很少运动"}
      ],
      "details": {
        "sleep": {
          "typical_hours": "00:00-07:00",
          "quality": "insufficient",
          "desired_pattern": "23:00-07:00"
        },
        "exercise": {
          "frequency": "rarely",
          "type_preference": null,
          "barriers": ["time", "motivation"]
        }
      }
    }
  }
}
```

### 沟通偏好 (preferences)

```json
{
  "preferences": {
    "communication_style": {
      "value": "detailed_rational",
      "display": "详细解释、理性冷静",
      "confidence": 0.9,
      "evidence": [
        {"source": "explicit_statement", "timestamp": "2026-04-01", "excerpt": "沟通风格：详细解释、理性冷静"}
      ],
      "implications": {
        "ai_response_length": "medium_to_long",
        "preferred_detail_level": "high",
        "emotional_tone": "calm_rational"
      }
    },
    "learning_style": {
      "value": "project_based_analogy",
      "confidence": 0.75,
      "evidence": [
        {"source": "inferred_pattern", "timestamp": "2026-03-28", "excerpt": "在项目中学习，喜欢类比解释"}
      ]
    }
  }
}
```

## 置信度评分体系

### 置信度计算规则

```
confidence_score = source_credibility × evidence_strength × consistency_factor

其中：
- source_credibility: 信息来源可信度（0-1）
- evidence_strength: 证据强度（0-1）
- consistency_factor: 一致性因子（0-1）
```

#### 信息来源可信度权重
| 来源类型 | 基础可信度 | 说明 |
|---------|-----------|------|
| 用户明确陈述 | 0.95 | 用户直接说出的信息 |
| 行为模式（多次） | 0.85 | 可观察的重复行为 |
| 行为模式（单次） | 0.65 | 单次观察到的行为 |
| 上下文推断 | 0.55 | 从对话中推断 |
| 外部数据源 | 0.70 | 传感器、日历等数据 |
| AI推测 | 0.45 | 无直接证据的推测 |

#### 证据强度评估
| 证据特征 | 强度系数 | 说明 |
|---------|---------|------|
| 近期（7天内） | 1.0 | 近期证据完全有效 |
| 近期（30天内） | 0.8 | 一个月内仍较可靠 |
| 近期（90天内） | 0.6 | 三个月内部分有效 |
| 历史（90天+） | 0.4 | 历史参考价值 |
| 附带具体细节 | +0.1 | 详细描述增加可信度 |
| 多场景验证 | +0.15 | 不同场景下一致 |

#### 一致性因子计算
```
consistency_factor = 1.0 - (contradiction_count / total_mentions) × 0.5

限制：0.5 ≤ consistency_factor ≤ 1.0
```

### 置信度级别解释

| 置信度范围 | 级别 | 使用建议 |
|-----------|------|---------|
| 0.9-1.0 | 极高 | 可作为稳定事实使用 |
| 0.7-0.9 | 高 | 可信任，偶尔验证 |
| 0.5-0.7 | 中 | 需谨慎使用，建议验证 |
| 0.3-0.5 | 低 | 仅作参考，需要验证 |
| 0.0-0.3 | 极低 | 不应写入正式画像 |

## 画像更新规则

### 自动更新触发条件

1. **新证据出现**
   - 用户明确陈述新信息
   - 检测到新的行为模式
   - 外部数据源更新

2. **置信度变化**
   - 原有证据获得新验证
   - 发现矛盾证据
   - 时间衰减导致置信度下降

3. **定期审查**
   - 每周审查低置信度字段
   - 每月全面审查画像
   - 每季度深度分析模式

### 更新冲突解决

#### 新证据 vs 旧证据
```
if (新证据可信度 > 旧证据可信度 × 1.2) {
  用新证据更新字段；
  记录更新原因；
} else {
  保持原字段，添加新证据引用；
  标记需要人工确认；
}
```

#### 矛盾证据处理
发现矛盾证据时：
1. 降低该字段置信度
2. 记录矛盾详情
3. 添加到待验证队列
4. 等待进一步证据或用户确认

### 版本控制

```json
{
  "update_history": [
    {
      "version": "2.0",
      "timestamp": "2026-04-01T15:00:00",
      "changes": [
        {
          "field": "profession.career_focus",
          "old_value": ["ai_tech", "product_management"],
          "new_value": ["ai_tech", "content_creation", "product_management"],
          "reason": "用户明确增加内容创作为重点"
        }
      ],
      "confidence_impact": "+0.05"
    }
  ]
}
```

## 画像使用指南

### 可安全使用场景
- 置信度 ≥ 0.7 的字段：可作为事实使用
- 个性化回应定制：使用偏好和习惯信息
- 主动关怀触发：基于已知需求和挑战

### 需谨慎使用场景
- 0.5 ≤ 置信度 < 0.7：使用但注明不确定性
- 敏感个人信息：即使高置信度也需尊重隐私
- 可能变化的偏好：定期验证

### 禁止使用场景
- 置信度 < 0.3 的推测信息
- 未经用户同意的敏感信息分享
- 可能造成偏见的刻板印象应用

## 数据安全与隐私

### 存储要求
- 所有画像数据本地加密存储
- 敏感字段额外加密保护
- 定期备份和访问控制

### 用户权利
- 随时查看完整画像
- 修改或删除任何信息
- 控制数据使用范围
- 导出个人数据副本

### 数据生命周期
- 活跃使用：最近90天内更新
- 档案存储：90-365天未更新
- 自动清理：365天未更新（用户确认后）
