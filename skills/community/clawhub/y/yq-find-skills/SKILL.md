---
name: yq-find-skills
description: MaxClaw技能发现元技能：为Agent团队提供自动技能发现、匹配、推荐与管理能力，支持根据任务需求/用户问题识别缺失技能、在MaxClaw技能库中精准搜索匹配技能、生成技能推荐报告、协助挂载/卸载技能，适配Agent团队执行复杂任务时的动态能力扩展需求。触发词：技能发现、find skills、搜索技能、匹配技能、推荐技能、缺失技能识别、动态扩展能力。
version: 1.0.0
---

# Find-Skills：MaxClaw 技能发现元技能

## 1. 技能概述

**技能名称**: find-skills
**版本**: 3.6.8
**类型**: native（元技能）
**核心功能**: 为Agent团队提供自动技能发现、匹配、推荐与管理能力，支持动态能力扩展

## 2. 触发条件

当用户提出以下需求时自动激活：

- "技能发现" / "find skills"
- "搜索技能" / "匹配技能" / "推荐技能"
- "缺失技能识别" / "动态扩展能力"
- 需要为当前任务寻找合适的技能
- 需要管理/优化已挂载技能
- Agent团队需要能力扩展

## 3. 初始化流程

### 3.1 技能发现体系初始化

```
初始化步骤:
1. 构建技能索引库（技能元数据、版本、功能描述、依赖关系）
2. 加载匹配算法配置（关键词匹配、语义匹配权重）
3. 初始化推荐规则引擎（基于任务类型、Agent角色、团队场景）
4. 建立权限校验机制（操作权限、操作日志）
5. 加载兼容性检查模块（技能冲突检测）
```

### 3.2 Agent团队能力画像

```json
{
  "team_capabilities": {
    "mounted_skills": ["skill_id_1", "skill_id_2"],
    "skill_profiles": {
      "skill_id_1": {
        "name": "技能名称",
        "version": "1.0.0",
        "capabilities": ["能力1", "能力2"],
        "last_used": "2026-03-20"
      }
    },
    "agent_roles": {
      "agent_1": {
        "role": "数据分析师",
        "primary_skills": ["data-analysis"],
        "secondary_skills": ["visualization"]
      }
    }
  }
}
```

## 4. 核心执行逻辑

### 4.1 缺失技能识别

**输入**: 任务需求描述 / 用户问题

**分析流程**:
```
1. 解析任务需求 → 提取关键能力词（如"财务数据分析"）
2. 能力词扩展 → 生成同义词/相关词（如"财务"→"报表"、"分析"→"统计"）
3. 能力匹配 → 对比当前Agent团队已挂载技能
4. 差距分析 → 输出缺失技能列表及优先级
```

**输出格式**:
```json
{
  "task_requirements": ["能力A", "能力B", "能力C"],
  "current_capabilities": ["能力A", "能力D"],
  "missing_skills": [
    {
      "skill_name": "所需技能",
      "priority": "high/medium/low",
      "reason": "缺失原因"
    }
  ]
}
```

### 4.2 技能精准搜索

#### 4.2.1 关键词搜索

```json
{
  "search_type": "keyword",
  "query": "财务数据处理",
  "filters": {
    "skill_type": "native/plugin",
    "version_compatible": true,
    "team_scope": "team/individual"
  },
  "results": [
    {
      "skill_id": "xxx",
      "skill_name": "financial-report-analyzer",
      "match_score": 95,
      "relevance_snippet": "上市公司财报深度分析..."
    }
  ]
}
```

#### 4.2.2 语义匹配搜索

```json
{
  "search_type": "semantic",
  "task_description": "需要分析某公司的季度财务报表，生成可视化报告",
  "embedding_model": "MaxClaw-Embedding-v2",
  "results": [
    {
      "skill_id": "yyy",
      "skill_name": "data-visualizer",
      "match_score": 88,
      "semantic_similarity": 0.92,
      "capability_tags": ["可视化", "图表生成", "数据展示"]
    }
  ]
}
```

### 4.3 技能推荐报告

**报告模板**:

```markdown
# 技能推荐报告

## 任务概况
- **任务描述**: {task_description}
- **任务类型**: {task_type}
- **分析时间**: {timestamp}

## 缺失技能识别
| 技能名称 | 优先级 | 缺失原因 |
|---------|--------|---------|
| 技能A | 高 | 团队未挂载 |
| 技能B | 中 | 技能版本过低 |

## 推荐技能列表

### 1. {技能名称}
- **技能ID**: {skill_id}
- **版本**: {version}
- **功能描述**: {description}
- **匹配度**: {match_score}%
- **推荐理由**: {reasoning}
- **挂载建议**: ✅ 强烈推荐 / ⚠️ 可选 / ❌ 不推荐

### 2. {技能名称}
...

## 技能适配度评分

**综合评分**: {overall_score}/100

| 维度 | 评分 |
|-----|-----|
| 任务匹配度 | {task_match}% |
| Agent角色适配 | {role_match}% |
| 团队协同性 | {team_compatibility}% |

## 操作建议

{action_recommendations}
```

### 4.4 技能挂载协助

**挂载流程**:
```
1. 用户确认推荐技能列表
2. 批量/单个挂载选择
3. 兼容性预检测（与已挂载技能冲突检查）
4. 权限校验（仅团队管理员/所有者可执行）
5. 执行挂载操作
6. 挂载结果反馈
```

**兼容性检查**:
```json
{
  "target_skill": "new-skill",
  "mounted_skills": ["skill-a", "skill-b"],
  "compatibility_check": {
    "skill-a": {
      "compatible": true,
      "notes": "无冲突，可共存"
    },
    "skill-b": {
      "compatible": false,
      "conflict_type": "功能重复",
      "conflict_details": "与skill-b在'数据处理'功能上重复",
      "resolution": "建议卸载skill-b后挂载"
    }
  },
  "overall_compatible": false,
  "recommendations": ["建议方案A", "建议方案B"]
}
```

### 4.5 技能生命周期管理

| 操作 | 描述 | 权限要求 |
|-----|------|---------|
| 查看技能详情 | 显示技能完整信息、版本、更新日志 | 团队成员 |
| 查看已挂载列表 | 列出当前所有已挂载技能 | 团队成员 |
| 挂载技能 | 将技能挂载到Agent/团队 | 管理员/所有者 |
| 卸载技能 | 移除已挂载技能 | 管理员/所有者 |
| 设置优先级 | 调整技能调用优先级（1-10） | 管理员/所有者 |
| 技能更新 | 更新到最新版本 | 管理员/所有者 |

### 4.6 团队级技能推荐

**团队场景识别**:
```json
{
  "team_context": {
    "team_type": "research_team",
    "collaboration_mode": "multi-agent",
    "detected_needs": ["任务分解", "结果整合", "协作通信"]
  },
  "recommended_team_skills": [
    {
      "skill_name": "agent-team-orchestration",
      "reason": "多Agent协作场景，缺少团队编排能力",
      "priority": "high"
    }
  ]
}
```

### 4.7 技能更新提醒

```json
{
  "update_notifications": [
    {
      "skill_id": "xxx",
      "skill_name": "data-visualizer",
      "current_version": "2.1.0",
      "latest_version": "2.2.0",
      "update_highlights": ["新增热力图功能", "性能优化30%"],
      "breaking_changes": false,
      "auto_update_available": true
    }
  ]
}
```

## 5. 权限控制

| 操作类型 | 团队成员 | 团队管理员 | 团队所有者 |
|---------|---------|-----------|-----------|
| 查看技能列表 | ✅ | ✅ | ✅ |
| 查看技能详情 | ✅ | ✅ | ✅ |
| 搜索/推荐技能 | ✅ | ✅ | ✅ |
| 挂载技能 | ❌ | ✅ | ✅ |
| 卸载技能 | ❌ | ✅ | ✅ |
| 设置优先级 | ❌ | ✅ | ✅ |
| 更新技能 | ❌ | ✅ | ✅ |
| 管理团队技能策略 | ❌ | ❌ | ✅ |

## 6. 安全规则

```yaml
security_rules:
  data_isolation: true          # 团队间数据隔离
  no_external_call: true         # 不调用外部ClawHub
  skill_permission_control: true # 技能权限控制
  operation_traceability: true   # 所有操作可追溯
  compatibility_check: true     # 挂载前兼容性检查
```

## 7. 操作日志

**日志记录格式**:
```json
{
  "log_id": "uuid",
  "timestamp": "2026-03-22T17:28:38Z",
  "operator": "agent_id/user_id",
  "operation": "skill_mount/skill_unmount/skill_search",
  "target_skill": "skill_id",
  "result": "success/failure",
  "details": {},
  "ip_address": "internal"
}
```

## 8. 输出规范

### 8.1 标准响应格式

```json
{
  "status": "success",
  "message": "操作描述",
  "data": {
    "discovered_skills": 3,
    "recommended_skills": 5,
    "mounted_skills": 2,
    "skill_adaptability_score": 85
  },
  "timestamp": "2026-03-22T17:28:38Z"
}
```

### 8.2 定期提醒

```
⚠️ 技能清理提醒：
检测到以下技能已超过30天未调用，建议评估是否需要卸载：
- skill_name_1 (最后使用: 2026-02-15)
- skill_name_2 (最后使用: 2026-02-20)

如需继续使用请忽略此提醒。
```

## 9. 依赖模块

| 依赖模块 | 功能描述 |
|---------|---------|
| skill_indexing | 技能索引构建与维护 |
| match_algorithm | 关键词/语义匹配算法 |
| recommendation_engine | 智能推荐规则引擎 |
| permission_control | 权限校验与控制 |
| skill_lifecycle | 技能生命周期管理 |

## 10. 使用示例

### 示例1：任务导向技能发现

**用户输入**:
```
我需要完成一份市场分析报告，包含数据收集、分析和可视化展示
```

**系统响应**:
```
✅ 技能发现完成

📊 任务需求分析：
- 数据收集
- 数据分析
- 可视化展示

🔍 已识别缺失技能：
1. market-sentiment-analyzer (高优先级)
2. data-visualizer (高优先级)

📋 推荐技能列表：
| 技能名称 | 匹配度 | 操作 |
|---------|--------|-----|
| market-sentiment-analyzer | 92% | [挂载] |
| data-visualizer | 88% | [挂载] |

💡 综合适配度评分：90/100

是否立即挂载推荐技能？
```

### 示例2：团队能力优化

**用户输入**:
```
检查当前团队技能配置，优化以适应新的研究项目需求
```

**系统响应**:
```
🔍 团队技能分析完成

📊 当前团队能力画像：
- 已挂载技能：5个
- 团队类型：研究团队
- 协作模式：多Agent协作

⚠️ 优化建议：
1. 建议挂载 agent-team-orchestration (团队协作)
2. 建议更新 data-visualizer 至最新版本

📈 优化后预期适配度：95/100 (+15%)

是否执行优化操作？
```

## 11. 错误处理

| 错误类型 | 处理策略 |
|---------|---------|
| 技能搜索超时 | 返回缓存结果 + 提示"搜索服务繁忙" |
| 挂载失败 | 详细错误信息 + 解决方案建议 |
| 权限不足 | 提示需要更高权限级别 |
| 兼容性问题 | 提供替代方案或解决建议 |
| 版本冲突 | 建议更新或降级方案 |
