---
name: 生产隐患排查技能
slug: hazard-inspection
displayName: 生产隐患排查技能
description: 生产现场隐患排查与整改跟踪；用于日常安全检查、隐患录入、统计分析、整改任务管理及合规性评估；帮助企业建立隐患闭环管理机制
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 生产现场隐患排查技能

## 任务目标

本 Skill 用于生产现场安全隐患的全面管理，涵盖隐患排查、记录、分析与整改全流程。

- **能力包含**: 多维度隐患录入、清单式排查、记录持久化、统计分析、整改任务跟踪
- **触发条件**: 日常安全巡检、隐患上报、整改跟踪、定期安全报告生成

## 前置准备

- 依赖说明: 无外部依赖，纯 Python 标准库实现
- 数据文件存放于 `./inspection_data/` 目录，脚本会自动创建

## 操作步骤

### 一、隐患信息录入

使用 `create_inspection.py` 录入新隐患：

```bash
python scripts/create_inspection.py \
  --location "A区-3号生产线" \
  --category "电气安全" \
  --description "配电箱门损坏，存触电风险" \
  --severity "high" \
  --inspector "张工"
```

参数说明:
- `--location`: 隐患位置（必填）
- `--category`: 隐患类别，从清单模板中选择
- `--description`: 隐患描述（必填）
- `--severity`: 严重等级（low/medium/high/critical）
- `--inspector`: 检查人姓名

### 二、查询隐患记录

使用 `list_inspections.py` 查询已有记录：

```bash
# 查询所有记录
python scripts/list_inspections.py

# 按条件筛选
python scripts/list_inspections.py --severity high --category "电气安全"
```

### 三、排查结果分析

使用 `analyze_inspections.py` 生成统计分析报告：

```bash
# 生成完整分析报告
python scripts/analyze_inspections.py

# 输出隐患类型分布
python scripts/analyze_inspections.py --type distribution

# 输出时间趋势
python scripts/analyze_inspections.py --type trend
```

### 四、整改任务管理

使用 `manage_remediation.py` 创建和跟踪整改任务：

```bash
# 为隐患创建整改任务
python scripts/manage_remediation.py create \
  --inspection-id <隐患ID> \
  --assignee "李班长" \
  --deadline "2025-02-01"

# 查看整改进度
python scripts/manage_remediation.py list

# 更新整改状态
python scripts/manage_remediation.py update \
  --task-id <任务ID> \
  --status in_progress
```

### 五、使用排查清单

执行隐患排查前，读取 `references/inspection_checklist.md` 获取标准检查项：

- 按清单逐项检查，记录发现的隐患
- 清单涵盖：电气安全、机械防护、消防设施、危化品管理、个人防护等 8 大类
- 根据实际检查对象选择对应检查类别

## 使用示例

### 示例 1：日常巡检

- **场景**: 安全员对 B 区仓库进行月度巡检
- **操作**: 先读取清单模板，对照检查并记录隐患，调用 create_inspection.py 录入
- **要点**: location 精确到具体设备位号，category 严格匹配清单分类

### 示例 2：隐患整改跟踪

- **场景**: 发现配电箱隐患后，需要安排维修并跟踪
- **操作**: 录入隐患后立即创建整改任务，设置责任人和截止日期
- **要点**: 整改任务需关联隐患 ID，形成完整闭环

### 示例 3：月度安全报告

- **场景**: 汇总本月隐患数据，生成管理层报告
- **操作**: 调用 analyze_inspections.py 生成统计，按类型/区域/严重等级分类呈现
- **要点**: 重点关注 high/critical 级别隐患的整改完成率

## 资源索引

- 脚本: [scripts/create_inspection.py](scripts/create_inspection.py) - 创建隐患记录（参数: location/category/description/severity/inspector）
- 脚本: [scripts/list_inspections.py](scripts/list_inspections.py) - 查询隐患列表（参数: severity/category/inspector）
- 脚本: [scripts/analyze_inspections.py](scripts/analyze_inspections.py) - 统计分析（参数: type=distribution|trend|summary）
- 脚本: [scripts/manage_remediation.py](scripts/manage_remediation.py) - 整改任务管理（参数: action=create|list|update）
- 参考: [references/inspection_checklist.md](references/inspection_checklist.md) - 隐患排查清单模板（检查前必读）

## 注意事项

- 录入隐患时严重等级必须准确，影响后续整改优先级
- 整改任务完成后需将任务状态更新为 completed
- 数据文件存放于 `./inspection_data/` 目录，定期备份

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 10/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互；已声明安全注意事项 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **48/50** | 通过 |
