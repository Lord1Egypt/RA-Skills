---
name: workday-calendar
author: wUwproject
license: MIT
tags: ['calendar', 'workday', 'holiday', 'schedule', 'rotation', 'gongxiu', 'linxiu', 'excel-export']
version: 2.2.0
description: 智能周历系统。支持法定假日、补班日、轮休系统（跳过/不跳过法定假双模式）、特殊休息（公休/临修）、个人日程管理。
sensitive_access: false
critical_write: false
permission_weight: LOW
data_dir: ../.standardization/workday-calendar/data/
trigger: 法定假日|周历|工作日|调休|补班|节假日|假日区间|年度工日|日程|安排|空闲时间|轮休|公休|临修|排班
trigger_negative: true
external_data_dir: true
h1_position: true
meta_field_sync: true
create_permissions_md: true
---
# 智能周历系统 (Workday Calendar)

## 触发条件

**正向触发：**
- 查询或管理**法定假日**、**补班日**、**调休**安排
- 计算**年度工作日**、**工作日统计**
- 生成**周历**、**日程安排**
- 查询某天的**空闲时间**、**日程安排**
- 添加、更新、删除**日程事件**
- 说出关键词："周历"、"工作日"、"假日区间"、"日程"、"安排"
- 用户讨论日历 UI 组件设计（如"帮我画一个日历组件"），应触发 drawiodo 而非本技能
- 用户要求操作其他日历应用（如 Google Calendar、Outlook 日历），本技能仅管理本地数据

### 否定条件（不触发）
- 用户只是询问日期（如"今天几号"），无假日/工作日/日程管理意图
- 用户讨论日历 UI 组件设计（如"帮我画一个日历组件"），应触发 drawiodo 而非本技能
- 用户要求操作其他日历应用（如 Google Calendar、Outlook 日历），本技能仅管理本地数据

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

| 能力 | 说明 |
| ------ |------|
| **法定假日管理** | 区间形式存储节假日，支持 AI 批量导入 |
| **补班日管理** | 单独记录调休上班日期 |
| **周末规则可配置** | 双休/单休/单双休/自定义周几 |
| **工作日计算** | 自动计算年度总工日，含所有休息类型统计 |
| **轮休系统** | skip/add 双模式，可配置周期，跨年缓存 |
| **特殊休息** | 公休/临修，支持单日和区间，最高优先级 |
| **个人日程** | 添加/删除/更新/查询/冲突检测 |
| **排班时段** | 15 分钟粒度，支持岗位+人员多赋值 |
| **HTML 导出** | 排班周历 / 日程周历 / 排班表（周/月/日期范围） |
| **定时任务** | 自动化配置，Markdown 输出 |
| **配置中心** | Web 界面（settings.py，端口 8765） |

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
| -------- |------| ---------- |----------|
| `references/LICENSE.md` | 许可协议 | MIT 许可证完整文本 | R-26 |
| `references/antipatterns.md` | 规范指南 | 常见反模式与避坑指引 | R-18 |
| `references/changelog.md` | 版本管理 | 版本更新日志 | R-24 |
| `references/cli.md` | 命令参考 | CLI 命令完整列表 | 无 |
| `references/data_format.md` | 参考文档 | JSON 数据格式说明 | 无 |
| `references/examples.md` | 使用示例 | 各场景完整交互示例 | R-25 C-17 |
| `references/faq.md` | 常见问题 | 常见疑问与解答 | R-19, R-25 C-19 |
| `references/guide.md` | 使用指南 | Python API 使用示例 | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描说明与测试结论 | R-15, R-16 |
| `references/test-report.md` | 测试报告 | skill-function-test 测试结论 | 无 |

## 工作流程

### 首次使用 / 新年份

当某年没有法定假日数据时（`load_holiday_intervals(year)` 返回空列表），**必须主动联网查询**国务院办公厅放假安排通知：

1. **联网查询** — 输入：年份 → 搜索"国务院办公厅 20XX年 放假安排" → 输出：法定假日日期范围、补班日、假期名称
2. **组织规则模板 JSON** — 输入：查询结果 → 按 `export_rules_template` 格式组织 JSON → 输出：标准规则模板
3. **导入** — 输入：规则模板 → 调用 `import_rules_from_template()` → 输出：数据写入 JSON 文件
4. **核对** — 输入：已导入数据 → 运行 `python scripts/workday_calendar.py rules 20XX` → 输出：规则确认表
5. **计算** — 输入：确认无误的数据 → 调用 `calculate_total_workdays(20XX)` → 输出：年度工日统计

**联网查询要求：**
- 搜索关键词："国务院办公厅 20XX 年 放假安排"
- 获取：法定假日日期范围、调休上班日（补班）、假期名称
- 确认该年周末规则（通常为标准双休日六日）

**组织规则模板（`export_rules_template` 格式）：**
```json
{
  "version": "1.0",
  "year": 2027,
  "base_type": "holiday",
  "rules": {
    "weekend_config": {"weekends": [0, 6]},
    "holiday_intervals": [
      {"name": "元旦", "start": "2027-01-01", "end": "2027-01-03"}
    ],
    "compensatory_days": [
      {"date": "2027-01-04", "note": "元旦补班"}
    ],
    "rotation_configs": [],
    "special_rests": []
  }
}
```

**执行导入：**
```python
template = {上面组织好的 JSON}
import_rules_from_template(template)
```

**导入后核对：**
```bash
python scripts/workday_calendar.py rules 2027
```

⚠️ **核对步骤必须执行**：节假日日期、补班日必须与国务院通知完全一致。

### 四层数据架构

```text
底板(法定假休, 永远不变)
  └→ weekend_config(双休/单休/自定义周几)
      └→ 排班规则(轮休/公休/临修, 始终叠在 weekend_config 上)
          ├─ toggle OFF → 假休保留(不受排班影响)
          └─ toggle ON  → 排班全面覆盖(包括假休)
              └→ 个人日程(记事本, 永远最上层)
```

### 日期类型优先级
| 优先级 | 类型 | 规则 |
| -------- |------| ------ |
| 1 | **补班日** | 强制计为工作日 |
| 2 | **临修** | 强制计为休息日 |
| 3 | **公休** | 强制计为休息日 |
| 4 | **轮休** | 按配置生成的休息日 |
| 5 | **法定假日** | 强制计为休息日 |
| 6 | **周末** | 按配置的周末规则 |
| 7 | **工作日** | 其他日期 |

### 日程冲突检测
- 添加日程时自动检测时间冲突
- 更新日程时重新检测冲突，冲突则自动还原

- `scripts/workday_calendar.py` — 核心逻辑
- `scripts/settings.py` — 配置中心 Web 服务器


