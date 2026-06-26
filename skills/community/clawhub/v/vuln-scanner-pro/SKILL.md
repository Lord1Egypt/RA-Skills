---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_2f568790617411f1832e5254006c9bbf
    ReservedCode1: XfhyCm/QR+rRu+L5NqIpqabWvKNxhuk0Q3OLdjgB+3wf70/KTVP8/pTy4BNmQxX+5oZ+TWw80ZDImsAxbxkyVMR2GfkBYLuBUt3SGNV01apxGp5fH93gD75Wq95BtewgiUDt8jqoMP2lD6/7AIWSKpIzNvI5tdjz7tdagf2B3GTr8dVuIn8k8a872P8=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_2f568790617411f1832e5254006c9bbf
    ReservedCode2: XfhyCm/QR+rRu+L5NqIpqabWvKNxhuk0Q3OLdjgB+3wf70/KTVP8/pTy4BNmQxX+5oZ+TWw80ZDImsAxbxkyVMR2GfkBYLuBUt3SGNV01apxGp5fH93gD75Wq95BtewgiUDt8jqoMP2lD6/7AIWSKpIzNvI5tdjz7tdagf2B3GTr8dVuIn8k8a872P8=
---

# AI 代码安全审查 (Code Security Audit)

## 概述

Code Security Audit 是一款 AI 驱动的代码安全审查技能，基于 OWASP / CWE 漏洞知识库 + 多语言安全规则引擎，自动检测代码中的安全漏洞、注入风险、不安全配置和合规性问题，生成结构化审查报告并给出可落地的修复方案。

## 适用场景

- CI/CD 流水线中代码提交前的自动安全扫描
- 存量代码的安全审计与风险评估
- 第三方依赖与开源组件的安全性分析
- 安全培训中的代码示例审查与教学

## 审查维度

| 维度 | 说明 |
|------|------|
| 注入攻击 | SQL 注入、命令注入、LDAP 注入、XPath 注入等 |
| 跨站脚本 (XSS) | 反射型 / 存储型 / DOM 型 XSS 检测 |
| 认证与授权 | 弱密码策略、会话劫持、权限提升漏洞 |
| 敏感数据暴露 | 硬编码密钥、日志泄露、明文传输 |
| 安全配置错误 | 调试模式开启、默认密码、不安全加密算法 |
| 跨站请求伪造 (CSRF) | Token 缺失、Referer 校验绕过 |
| 服务端请求伪造 (SSRF) | 未校验的用户输入 URL 请求 |
| 路径遍历 | 目录穿越、文件包含漏洞 |
| 反序列化漏洞 | 不可信数据反序列化 |
| 依赖安全 | 已知 CVE 漏洞的第三方库版本 |

## 支持的语言与规则覆盖

| 语言 | 支持版本 | 安全规则数 | 覆盖标准 |
|------|---------|-----------|---------|
| Python | 3.6+ | 120+ | Bandit + PEP + OWASP |
| JavaScript / TypeScript | ES6+ | 130+ | ESLint Security + Node.js |
| Java | 8+ | 110+ | FindSecBugs + OWASP Java |
| Go | 1.16+ | 80+ | Gosec + OWASP Go |
| PHP | 7.4+ | 90+ | PHPCS Security |
| C / C++ | C99 / C++11+ | 75+ | CERT C/C++ + MISRA |
| Ruby | 2.7+ | 60+ | Brakeman + RubySec |

## 评分体系

| 分数区间 | 风险等级 | 说明 |
|---------|---------|------|
| 9 - 10 | 安全 | 无已知漏洞，编码规范良好 |
| 7 - 8.9 | 低风险 | 少量低危问题，建议改进 |
| 5 - 6.9 | 中风险 | 存在中等风险漏洞，需尽快修复 |
| 3 - 4.9 | 高风险 | 存在严重漏洞，可能导致数据泄露 |
| 1 - 2.9 | 严重 | 多个高危漏洞，系统面临直接威胁 |

## 支付协议（AI收）

本技能采用支付宝 AI 收 HTTP 402 协议，按次计费。

| 项目 | 值 |
|------|-----|
| 单价 | ¥0.50 / 次 |
| 支付协议 | `alipay_` 短链协议 |
| 网关地址 | `http://8.145.54.67:3000` |
| 技能路径 | `/skill/security-scan` |
| 支付确认路径 | `/pay-confirm` |

### 支付流程

```
1. 客户端发起审查请求  POST /skill/security-scan
2. 服务端返回 402 Payment Required
   Header: X-Payment-Needed: true
   Header: X-Short-Link: alipay_XXXXXXXXXXXXXXXX
3. 用户完成支付宝支付
4. 客户端携带支付凭证回传  POST /pay-confirm
   Header: X-Payment-Credential: <支付凭证>
5. 服务端验证通过 → 执行安全审查 → 返回结果
```

### HTTP 请求头规范

| 头名称 | 说明 |
|--------|------|
| `X-Payment-Needed` | 服务端返回：`true` 表示需要支付 |
| `X-Short-Link` | 服务端返回：支付宝短链 URL 供用户支付 |
| `X-Payment-Credential` | 客户端回传：支付完成后的凭证字符串 |
| `X-Service-Tier` | 可选，`basic`（快速扫描）或 `deep`（深度审计） |

## 审查服务档位

### 基础档（basic = ¥0.50）
- 单文件代码扫描（最多 2000 行）
- 漏洞列表（严重度/行号/CWE编号）
- 安全评分（1-10）
- 简要修复建议
- 输出 JSON 格式审查报告

### 深度档（deep = ¥1.00 - 预留）
- 全部基础功能
- 跨文件数据流分析
- 第三方依赖 CVE 漏洞检测
- 修复代码 diff 补丁
- 合规性检查（SOC2 / ISO27001 / PCI-DSS）
- 输出 PDF 完整审计报告

## 数据底座

所有漏洞模式、安全规则、CWE 映射、不安全函数列表存储于 `references/security-scan.json`，结构如下：

```json
{
  "vulnerability_patterns": { ... },  // OWASP Top 10 + CWE Top 25 漏洞模式
  "injection_patterns": [ ... ],       // SQL注入/XSS/CSRF/SSRF/路径遍历规则
  "language_rules": { ... },           // Python / JS / Java 安全规则
  "unsafe_functions": [ ... ],         // 各语言常见不安全函数列表
  "cwe_reference": [ ... ],            // CWE 编号到漏洞描述映射
  "compliance_checks": [ ... ]         // 合规性检查规则
}
```

## 使用示例

### 请求

```bash
curl -X POST http://8.145.54.67:3000/skill/security-scan \
  -H "Content-Type: application/json" \
  -H "X-Service-Tier: basic" \
  -d '{"code": "def login(user, pw):\n  query = \"SELECT * FROM users WHERE name=\'\" + user + \"\'\"\n  cursor.execute(query)", "language": "python"}'
```

### 响应（支付后）

```json
{
  "service": "AI 代码安全审查",
  "tier": "basic",
  "language": "python",
  "security_score": 3.2,
  "risk_level": "高风险",
  "vulnerabilities_found": 3,
  "summary": "检测到 3 处安全漏洞，包括 SQL 注入、硬编码凭证、不安全哈希算法。建议立即修复。",
  "details": [
    {
      "line": 2,
      "severity": "严重",
      "cwe_id": "CWE-89",
      "title": "SQL 注入",
      "description": "用户输入直接拼接到 SQL 查询字符串，未使用参数化查询",
      "code_snippet": "query = \"SELECT * FROM users WHERE name='\" + user + \"'\"",
      "remediation": "使用参数化查询：cursor.execute('SELECT * FROM users WHERE name=?', (user,))",
      "owasp_category": "A03:2021 - Injection"
    }
  ]
}
```

## 许可

MIT License — 详见 LICENSE 文件
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
