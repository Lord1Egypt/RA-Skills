# SKILL VETTING REPORT 模板

check --report 生成的报告遵循本结构；人工审查也可直接套用。

```markdown
# SKILL VETTING REPORT

- 技能: <名称>
- 路径: <目录>
- 来源: <平台 / github:owner/repo>
- 审查时间: <ISO 8601>
- 审查者: <人名/角色>
- 文件数: <N>

## 结论

- 风险等级: <LOW / MEDIUM / HIGH / CRITICAL>
- 结论: <SAFE TO INSTALL / REVIEW REQUIRED / INSTALL WITH CAUTION / DO NOT INSTALL>
- 决策记录: <一句决策理由>
- 安全健康度评分: <0-100>

## 威胁捕获模型视图（8 类）

| 检测点 | verdict | 命中 |
|---|---|---|
| 供应链风险 | <safe / suspicious / danger / n/a> | N |
| 命令执行风险 | <safe / suspicious / danger / n/a> | N |
| 网络请求与数据外传 | <safe / suspicious / danger / n/a> | N |
| 文件操作与敏感路径访问 | <safe / suspicious / danger / n/a> | N |
| Prompt 注入风险 | <safe / suspicious / danger / n/a> | N |
| 远程脚本下载执行 | <safe / suspicious / danger / n/a> | N |
| 可疑编码·混淆 | <safe / suspicious / danger / n/a> | N |
| 其他安全风险 | <safe / suspicious / danger / n/a> | N |

## 行为项（13 项）

观察到：<行为项清单 / 未观察到明显系统行为>

## 汇总

| 级别 | 数量 |
|---|---|
| CRITICAL | N |
| HIGH | N |
| MEDIUM | N |
| LOW | N |
| INFO | N |

## 发现

逐条：级别 · 规则 · 位置 · 描述

## 决策记录

- [ ] 已人工复核发现项
- [ ] 已确认来源可信度
- [ ] 已确认权限范围最小化
- [ ] 审查结论与理由已记录（时间戳/审查者）
```
