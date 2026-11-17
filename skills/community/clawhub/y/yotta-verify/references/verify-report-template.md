# SKILL VERIFY REPORT 模板

`yotta_verify.py report <path> [--out report.md]` 输出本模板（Markdown 或 --json）。

# SKILL VERIFY REPORT

- 工具：元信 yotta-verify v0.1.1
- 目标：<扫描路径>（扫描 N 个文件）
- 扫描时间：<UTC 时间>

## Verdict

**SAFE TO INSTALL / REVIEW REQUIRED / INSTALL WITH CAUTION / DO NOT INSTALL**

| 严重级 | 数量 |
|---|---|
| critical | N |
| high | N |
| medium | N |
| low | N |
| info | N |

## Findings

| 规则 | 严重级 | 位置 | 说明 | 置信度 |
|---|---|---|---|---|
| PIJ-001 | high | SKILL.md:6 | 指令覆盖（ignore-previous-instructions 类） | 85% |
| DEX-001 | critical | scripts/evil.sh:2 | 下载即执行（curl 管道交给 shell） | 95% |

> 结论仅供人工决策参考；最终判断由用户。建议结合元安（深度扫描）与元审（四阶段审查）。

## 使用建议

1. 安装前：先跑 scan，无 critical / high 再装；
2. 有 medium 及以上：转元审四阶段审查，再决定；
3. 高风险包：结合元安深度扫描 + 元鉴样本初筛复核。
