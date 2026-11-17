# 漏洞评估与渗透测试报告模板

> 配套：`report generate findings.json --out report.md` 输出本模板（Markdown，--json 输出 JSON）。
> 纪律：敏感凭据自动脱敏；复现步骤用「类」表述，不给可复制注入串。
> 适用：内部漏洞评估报告；SRC / bug bounty 平台提交稿（按平台模板字段映射）。

## 报告结构

1. 目标与授权信息（目标 / 授权类型 / 授权来源 / 有效期 / 范围边界）
2. 摘要（按严重级统计发现数量）
3. 安全扫描联动（可选，`scans` 数组：工具 / 类型 / verdict / 关联报告，引用元信 / 元安 / 元审报告）
4. 发现明细（每项：标题 / 严重级 / 类别 / CWE / 端点 / 描述 / 证据 / 修复建议）
5. 复现步骤（「类」表述）
6. 修复优先级

## findings.json 输入 schema

```json
{
  "target": "<目标，如 http://127.0.0.1/dvwa>",
  "scans": [
    {
      "tool": "yotta-verify",
      "kind": "装前扫描",
      "verdict": "SAFE TO INSTALL",
      "reference": "<元信报告路径>"
    },
    {
      "tool": "yotta-security-audit",
      "kind": "深度扫描",
      "verdict": "REVIEW REQUIRED",
      "reference": "<元安报告路径>"
    }
  ],
  "findings": [
    {
      "title": "<发现标题>",
      "severity": "critical | high | medium | low | info",
      "category": "<类别，如 SQL Injection>",
      "cwe": "<CWE 编号，如 CWE-89>",
      "owasp": "<对应 OWASP 条目，如 A03 Injection>",
      "endpoint": "<端点 URL>",
      "description": "<发现描述>",
      "evidence": "<证据：请求 / 响应片段或观察记录>",
      "remediation": "<修复建议>"
    }
  ]
}
```

字段说明：

- severity 必填且取值合法，否则报错；
- 其余字段可选，但建议补齐（title / description / remediation 缺失会在报告中提示补充）；
- `scans` 可选：与元信（装前扫描）/ 元安（深度扫描）/ 元审（四阶段审查）报告互相关联，构成完整留痕链；
- 敏感键（password / token / secret / cookie 等）整值自动掩码；长 hex / base64 / URL 凭据自动脱敏。

## 生成报告

```bash
python3 scripts/yotta_security_testing.py report generate findings.json --out report.md
python3 scripts/yotta_security_testing.py report generate findings.json --json --out report.json
```

## 报告输出示例（Markdown 结构示意）

```markdown
# 漏洞评估与渗透测试报告

- 目标：http://127.0.0.1/dvwa
- 生成时间：2026-08-29T10:00:00+08:00
- 生成工具：元测 yotta-security-testing v0.3.0（Scope Guard 已启用，敏感凭据已脱敏）

## 摘要

| 严重级 | 数量 |
|---|---|
| critical | 0 |
| high | 1 |
| medium | 0 |
| low | 1 |
| info | 0 |

共 2 条发现。

## 发现 1：标识参数存在 SQL 注入候选

- 严重级：high
- 类别：SQL Injection
- CWE：CWE-89
- OWASP：A03 Injection
- 端点：/dvwa/vulnerabilities/sqli/

### 描述

标识参数插入结构闭合类字符后出现数据库错误信息差异；布尔条件类输入引起内容差异，符合注入候选特征。

### 证据

响应包含数据库错误信息类文本；对照请求结果不同。

### 修复建议

改用参数化查询 / 预编译语句；错误信息不向客户端回显。
```

## SRC / 平台提交字段映射

- 平台模板常用字段：漏洞标题 / 影响范围 / 复现步骤 / 危害等级 / 修复建议 / 附件（截图、请求记录）。
- 映射：title → 漏洞标题；severity → 危害等级（参考平台定级标准）；endpoint + description → 影响范围；
  evidence → 复现步骤证据（脱敏后）；remediation → 修复建议。
- 提交前：证据截图 / 请求记录脱敏，不包含真实用户数据、cookie、密钥。

## 脱敏与质量检查清单

- [ ] 目标 / 授权类型 / 授权来源 / 有效期齐全
- [ ] 每项发现含严重级 / 类别 / CWE / 端点 / 描述 / 证据 / 修复建议
- [ ] 敏感凭据已脱敏（口令 / token / 密钥 / 长 hex / base64 / cookie）
- [ ] 复现步骤为「类」表述，无可复制注入串
- [ ] 留痕可查（audit.log 已记录本轮操作）
- [ ] SRC 提交稿：范围 in-scope、证据脱敏、无真实用户数据
