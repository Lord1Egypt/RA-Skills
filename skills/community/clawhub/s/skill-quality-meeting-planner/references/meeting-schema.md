# 会议方案JSON数据结构规范

## 概览
本文档定义了 `generate_meeting_doc.py` 脚本所需的JSON输入数据结构。智能体在完成数据解析、大纲确认后，需按此结构组织数据并写入JSON文件，作为脚本输入。

## 数据结构定义

```json
{
  "meeting_title": "string - 会议名称，如'第12周质量周会'",
  "meeting_date": "string - 会议日期，如'2024-03-18'",
  "meeting_time": "string - 会议时间段，如'14:00-15:30'",
  "meeting_location": "string - 会议地点或线上链接",
  "organizer": "string - 会议组织者/主持人",
  "record_keeper": "string - 记录人，可为空字符串",
  "attendees": ["string - 参会人员姓名或角色列表"],
  "meeting_objectives": ["string - 会议目标列表，每个目标一句话描述"],
  "agenda_items": [
    {
      "topic": "string - 议题名称",
      "presenter": "string - 汇报/负责人",
      "time_allocation": "string - 时间安排，如'15分钟'",
      "background": "string - 背景说明，描述问题来源和现状",
      "key_data": ["string - 关键数据点列表，如'缺陷数: 5个P1'"],
      "discussion_points": ["string - 需要讨论的要点列表"],
      "expected_outcome": "string - 期望达成的结论或决策"
    }
  ],
  "preparation_requirements": ["string - 会前准备要求列表"],
  "total_duration": "string - 会议总时长，如'90分钟'",
  "notes": "string - 备注信息，可为空字符串"
}
```

## 字段说明

### 必填字段
| 字段 | 类型 | 说明 |
|------|------|------|
| meeting_title | string | 会议名称 |
| meeting_date | string | 会议日期 |
| meeting_time | string | 会议时间段 |
| meeting_location | string | 会议地点 |
| organizer | string | 组织者 |
| attendees | array[string] | 参会人员，至少1人 |
| meeting_objectives | array[string] | 会议目标，至少1项 |
| agenda_items | array[object] | 议程议题，至少1项 |

### 议题(agenda_items)子字段
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| topic | string | 是 | 议题名称 |
| presenter | string | 是 | 负责人，未知时填"待确认" |
| time_allocation | string | 是 | 时间安排 |
| background | string | 是 | 背景说明 |
| key_data | array[string] | 否 | 关键数据，无数据时为空数组 |
| discussion_points | array[string] | 是 | 讨论要点，至少1项 |
| expected_outcome | string | 是 | 期望产出 |

### 可选字段
| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| record_keeper | string | "" | 记录人 |
| preparation_requirements | array[string] | [] | 会前准备要求 |
| total_duration | string | "90分钟" | 总时长 |
| notes | string | "" | 备注 |

## 完整示例

```json
{
  "meeting_title": "第12周质量周会",
  "meeting_date": "2024-03-18",
  "meeting_time": "14:00-15:30",
  "meeting_location": "3楼会议室A",
  "organizer": "张三",
  "record_keeper": "李四",
  "attendees": ["张三", "李四", "王五", "赵六"],
  "meeting_objectives": [
    "回顾本周质量数据，识别关键风险",
    "讨论P1缺陷根因及改进措施",
    "对齐下周测试计划与资源分配"
  ],
  "agenda_items": [
    {
      "topic": "本周质量数据总览",
      "presenter": "张三",
      "time_allocation": "15分钟",
      "background": "本周测试通过率从95%下降至88%，需整体回顾质量趋势",
      "key_data": [
        "测试通过率: 88%(上周95%)",
        "新增缺陷: 23个",
        "P1缺陷: 5个",
        "P2缺陷: 8个"
      ],
      "discussion_points": [
        "通过率下降的主要原因是什么",
        "是否存在系统性质量问题"
      ],
      "expected_outcome": "明确通过率下降的Top3原因"
    },
    {
      "topic": "P1接口超时缺陷分析",
      "presenter": "王五",
      "time_allocation": "20分钟",
      "background": "本周5个P1缺陷中有3个为接口超时问题，集中在支付模块",
      "key_data": [
        "接口超时P1: 3个",
        "涉及模块: 支付、订单",
        "平均响应时间: 8.5s(阈值2s)"
      ],
      "discussion_points": [
        "接口超时的根因分析",
        "是否需要增加性能测试覆盖",
        "修复计划与时间节点"
      ],
      "expected_outcome": "确定修复方案和责任人，明确完成时间"
    }
  ],
  "preparation_requirements": [
    "各模块负责人提前整理本周缺陷数据",
    "支付模块团队准备接口性能测试报告",
    "测试团队准备通过率趋势图"
  ],
  "total_duration": "90分钟",
  "notes": ""
}
```

## 验证规则
1. `meeting_title`、`meeting_date`、`meeting_time`、`meeting_location`、`organizer` 不可为空字符串
2. `attendees` 数组至少包含1个元素
3. `meeting_objectives` 数组至少包含1个元素
4. `agenda_items` 数组至少包含1个元素
5. 每个 agenda_item 的 `topic`、`presenter`、`time_allocation`、`background`、`expected_outcome` 不可为空
6. 每个 agenda_item 的 `discussion_points` 至少包含1个元素
7. `key_data` 和 `preparation_requirements` 可为空数组
