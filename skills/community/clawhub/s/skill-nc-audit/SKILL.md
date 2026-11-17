---
name: 内审不符合项判定技能
slug: nc-audit
displayName: 内审不符合项判定技能
description: 管理体系内审不符合项判定与验证工具；适用于内审员需要录入不符合项、基于ISO条款辅助判定性质、跟踪验证状态或生成审核结论报告的场景
version: 1.1.0
category: quality
author: org-jaxjwo0r
---
# 内审不符合项判定与验证

## 任务目标
- 本Skill用于:管理体系内审过程中不符合项(NON-CONFORMANCE)的全生命周期管理
- 能力包含:不符合项录入/分类/规则判定/验证跟踪/结论生成
- 触发条件:审核现场记录不符合项/审核结束后汇总分析/不符合项整改验证

## 前置准备
- 依赖说明:Python标准库(json/argparse/datetime)，无需额外安装
- 数据文件:脚本自动创建`assets/nc_data.json`存储所有不符合项

## 操作步骤

### 1. 录入不符合项
使用`add_nc.py`录入新的不符合项:
```bash
python scripts/add_nc.py \
  --title "检测设备未按周期校准" \
  --clause "7.1.5" \
  --description "生产部门三台量具超出校准有效期" \
  --evidence "现场检查记录" "设备台账" \
  --category minor
```

### 2. 查询不符合项
```bash
# 列出所有不符合项
python scripts/list_nc.py

# 按状态筛选
python scripts/list_nc.py --status open

# 按条款筛选
python scripts/list_nc.py --clause "7.1"

# 按类别筛选
python scripts/list_nc.py --category major
```

### 3. 规则辅助判定
使用`evaluate_nc.py`基于预设规则判定不符合项性质:
```bash
# 判定单条记录
python scripts/evaluate_nc.py --nc-id NC-20240115-001

# 批量判定(读取描述文本)
python scripts/evaluate_nc.py --input "文件未按程序执行" --clause "8.1"
```
判定依据参考[references/iso_clauses.md](references/iso_clauses.md)

### 4. 验证跟踪
使用`verify_nc.py`更新不符合项验证状态:
```bash
# 记录验证人开始处理
python scripts/verify_nc.py --nc-id NC-20240115-001 --status in_progress

# 完成验证
python scripts/verify_nc.py \
  --nc-id NC-20240115-001 \
  --status verified \
  --verifier "张审核员" \
  --result "纠正措施已实施，有效"
```

### 5. 生成审核结论
使用`generate_report.py`生成汇总报告:
```bash
# 生成完整报告
python scripts/generate_report.py --audit-id AUDIT-2024-Q1

# 仅输出统计
python scripts/generate_report.py --audit-id AUDIT-2024-Q1 --stats-only
```

## 判定规则说明

| 类别 | 定义 | 判定依据 |
|------|------|----------|
| major | 严重不符合 | 体系文件缺失/未执行;影响产品/服务符合性;重复发生 |
| minor | 轻微不符合 | 个别偏差;不影响整体体系有效性;可立即纠正 |
| observation | 观察项 | 改进机会;潜在风险;良好实践 |

## 不符合项状态流转
```
open -> in_progress -> verified -> closed
```

## 使用示例

### 示例1:审核现场录入
- 场景:内审首次会议后，审核员在车间发现检测设备超期未校准
- 预期产出:创建不符合项记录，生成唯一ID
- 关键要点:准确引用ISO条款，收集至少2项证据

### 示例2:不符合项判定
- 场景:同一问题在多个部门发现，需判定是否为严重不符合
- 预期产出:系统返回判定结果和建议
- 关键要点:提供充分的描述信息供规则引擎分析

### 示例3:整改验证
- 场景:被审核部门提交纠正措施，审核员验证有效性
- 预期产出:更新验证状态，记录验证结果
- 关键要点:验证结果需明确说明是否有效关闭

### 示例4:审核结论生成
- 场景:末次会议前，汇总本次审核所有不符合项
- 预期产出:包含统计图表、分布分析、改进建议的报告
- 关键要点:指定审核ID关联所有相关不符合项

## 资源索引

### 脚本
- [scripts/add_nc.py](scripts/add_nc.py) - 录入不符合项(参数:--title/--clause/--description/--evidence/--category)
- [scripts/list_nc.py](scripts/list_nc.py) - 查询不符合项(参数:--status/--clause/--category/--audit-id)
- [scripts/evaluate_nc.py](scripts/evaluate_nc.py) - 规则判定(参数:--nc-id/--input/--clause)
- [scripts/verify_nc.py](scripts/verify_nc.py) - 验证跟踪(参数:--nc-id/--status/--verifier/--result)
- [scripts/generate_report.py](scripts/generate_report.py) - 生成报告(参数:--audit-id/--stats-only)

### 参考
- [references/iso_clauses.md](references/iso_clauses.md) - ISO标准条款定义与判定要点

### 资产
- [assets/nc_data.json](assets/nc_data.json) - 不符合项数据存储(自动创建)

## 注意事项
- 证据建议至少2项，支持直接引用审核证据
- 条款编号需与ISO标准一致，参考文档提供常用条款
- 验证状态必须按流转顺序推进(open→in_progress→verified→closed)
- 生成报告前确保相关不符合项已关联同一审核ID

## TRACE 测评

| 维度 | 评分 | 说明 |
|------|------|------|
| T — 可信任度 | 9/10 | 纯文档/脚本技能，无外部依赖风险，支持中文交互 |
| R — 可靠性 | 9/10 | 有异常处理说明; 输出格式明确 |
| A — 适用性 | 9/10 | 有适用范围声明; 触发条件明确 |
| C — 规范性 | 10/10 | frontmatter 完整; 文档结构清晰; 内容充分 |
| E — 有效性 | 10/10 | 输出明确; 含使用示例; 文档详尽 |
| **总分** | **47/50** | 通过 |
