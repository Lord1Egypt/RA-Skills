# 质量月报数据格式规范

## 目录
- [概览](#概览)
- [数据结构](#数据结构)
- [字段说明](#字段说明)
- [PDCA格式说明](#pdca格式说明)
- [多月数据格式](#多月数据格式)
- [完整示例](#完整示例)
- [验证规则](#验证规则)

## 概览
本规范定义了质量月报输入数据的 JSON 格式，确保脚本能够正确解析和计算质量指标，支持 PDCA 总结和多月对比分析。

## 数据结构

```json
{
  "month": <字符串>,
  "test_cases": {
    "total": <整数>,
    "passed": <整数>,
    "failed": <整数>,
    "skipped": <整数>
  },
  "defects": {
    "total": <整数>,
    "by_severity": {
      "critical": <整数>,
      "high": <整数>,
      "medium": <整数>,
      "low": <整数>
    }
  },
  "work_summary": [
    {
      "task": <字符串>,
      "status": <字符串>,
      "description": <字符串>
    }
  ],
  "temporary_works": [
    {
      "task": <字符串>,
      "status": <字符串>,
      "description": <字符串>
    }
  ],
  "pdca_items": [
    {
      "title": <字符串>,
      "status": <字符串>,
      "plan": <字符串>,
      "do": <字符串>,
      "check": <字符串>,
      "act": <字符串>
    }
  ],
  "risks": [
    {
      "description": <字符串>,
      "level": <字符串>
    }
  ],
  "next_month_plan": [
    <字符串>
  ]
}
```

## 字段说明

### month（月份标识）
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| month | 字符串 | 是 | 月份标识，格式建议：YYYY-MM（如 2024-01） |

### test_cases（测试用例统计）
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| total | 整数 | 是 | 测试用例总数 |
| passed | 整数 | 是 | 通过的用例数 |
| failed | 整数 | 否 | 失败的用例数（默认：total - passed） |
| skipped | 整数 | 否 | 跳过的用例数（默认：0） |

### defects（缺陷统计）
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| total | 整数 | 是 | 缺陷总数 |
| by_severity | 对象 | 否 | 按严重级别分类的缺陷数 |
| by_severity.critical | 整数 | 否 | 严重缺陷数 |
| by_severity.high | 整数 | 否 | 高危缺陷数 |
| by_severity.medium | 整数 | 否 | 中危缺陷数 |
| by_severity.low | 整数 | 否 | 低危缺陷数 |

### work_summary（工作总结）
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task | 字符串 | 是 | 任务名称 |
| status | 字符串 | 是 | 任务状态（已完成/进行中/待处理） |
| description | 字符串 | 否 | 任务描述 |

### temporary_works（临时工作）
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task | 字符串 | 是 | 临时工作名称 |
| status | 字符串 | 是 | 任务状态（已完成/进行中/待处理） |
| description | 字符串 | 否 | 任务描述 |

### risks（风险列表）
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| description | 字符串 | 是 | 风险描述 |
| level | 字符串 | 否 | 风险级别（高/中/低） |

### next_month_plan（下月计划）
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| - | 字符串 | 是 | 计划事项 |

## PDCA格式说明

### pdca_items（PDCA总结）
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | 字符串 | 是 | PDCA 项目标题 |
| status | 字符串 | 是 | 项目状态（已完成/进行中/待处理） |
| plan | 字符串 | 否 | 计划阶段内容 |
| do | 字符串 | 否 | 执行阶段内容 |
| check | 字符串 | 否 | 检查阶段内容 |
| act | 字符串 | 否 | 改进阶段内容 |

**PDCA 使用场景**：
- 临时安排的工作需要进行 PDCA 总结
- 专项质量改进项目
- 流程优化活动
- 问题根因分析与解决

## 多月数据格式

用于连续性对比分析时，每个月的数据应保存为独立的 JSON 文件：

```
2024-01.json
2024-02.json
2024-03.json
```

调用脚本时，使用 `--previous-data` 参数传入历史文件（逗号分隔）：
```bash
python scripts/metrics_calculator.py \
  --input 2024-03.json \
  --previous-data "2024-01.json,2024-02.json"
```

## 完整示例

```json
{
  "month": "2024-03",
  "test_cases": {
    "total": 500,
    "passed": 470,
    "failed": 20,
    "skipped": 10
  },
  "defects": {
    "total": 15,
    "by_severity": {
      "critical": 1,
      "high": 3,
      "medium": 8,
      "low": 3
    }
  },
  "work_summary": [
    {
      "task": "用户中心模块测试",
      "status": "已完成",
      "description": "完成用户中心模块的所有功能测试，覆盖正常和异常场景"
    },
    {
      "task": "支付接口压力测试",
      "status": "进行中",
      "description": "执行支付接口的压力测试，验证系统并发能力"
    }
  ],
  "temporary_works": [
    {
      "task": "线上问题紧急排查",
      "status": "已完成",
      "description": "协助开发团队排查线上支付异常问题"
    }
  ],
  "pdca_items": [
    {
      "title": "测试环境稳定性提升",
      "status": "已完成",
      "plan": "分析测试环境不稳定的原因，制定优化方案",
      "do": "升级测试服务器硬件，优化测试数据清理策略",
      "check": "测试环境故障次数从每月8次降低到2次，稳定性提升75%",
      "act": "将优化措施固化为标准流程，定期监控环境状态"
    },
    {
      "title": "自动化测试覆盖率提升",
      "status": "进行中",
      "plan": "分析核心模块的自动化测试覆盖率，识别覆盖盲区",
      "do": "补充自动化测试用例，覆盖回归测试场景",
      "check": "自动化覆盖率从60%提升到75%，待进一步验证",
      "act": "持续优化自动化用例，目标是达到85%覆盖率"
    }
  ],
  "risks": [
    {
      "description": "第三方支付接口在高峰期响应不稳定",
      "level": "中"
    }
  ],
  "next_month_plan": [
    "完成支付接口压力测试",
    "推进自动化测试覆盖率提升到85%",
    "准备下版本发布的回归测试计划"
  ]
}
```

## 验证规则

1. **必填字段检查**
   - `month` 必须存在
   - `test_cases.total` 和 `test_cases.passed` 必须存在
   - `defects.total` 必须存在
   - `work_summary` 至少包含一条记录

2. **数值范围检查**
   - `total` >= 0
   - `passed` >= 0
   - `passed` <= `total`
   - `total_defects` >= 0

3. **状态值检查**
   - `work_summary[].status` 应为：已完成/进行中/待处理
   - `temporary_works[].status` 应为：已完成/进行中/待处理
   - `pdca_items[].status` 应为：已完成/进行中/待处理
   - `risks[].level` 应为：高/中/低

4. **数据一致性检查**
   - `passed + failed + skipped = total`（如果 failed 和 skipped 都存在）

5. **多月数据检查**
   - 每个月份的 `month` 字段应唯一
   - 按时间顺序排列数据文件，确保趋势分析正确
