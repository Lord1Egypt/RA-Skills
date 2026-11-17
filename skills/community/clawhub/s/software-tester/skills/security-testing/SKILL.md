---
name: security-testing
description: 安全测试：以攻击者视角对应用/接口做 OWASP API Security Top 10 验证（注入、越权 BOLA/BFLA、鉴权失效、速率限制等），输出风险报告
source:
  type: original
  repo: skills-repo/software-tester
  path: skills/security-testing/SKILL.md
  version: 1.0.0
  updated: 2026-08-12
metadata:
  category: 安全测试
  platform: 安全
  difficulty: 进阶
---

# 安全测试

> 对应用/接口做安全验证，聚焦 OWASP API Security Top 10 与常见漏洞，以「攻击者视角」构造用例，输出风险报告。

> 来源说明：skill-radar 三源搜索（skills.sh / GitHub）最佳社区技能为 mukul975/...@testing-api-security-with-owasp-top-10（454 安装，< 500 软线且无 ≥1K 选项），故本子技能内容由组织基于自有 [references/security-testing.md](../../references/security-testing.md) 原创（original），未改编低安装量社区技能。

## 能力

- **OWASP API Top 10 映射**：BOLA/BFLA 越权、注入、鉴权失效、过量请求、SSRF、批量分配等
- **越权验证**：用多组身份 token 交叉访问（自己/他人/匿名/越权角色）
- **注入用例**：SQL / NoSQL / 命令 / LDAP / XSS 反射等价类
- **风险报告**：按严重级（高/中/低）列证据与修复建议

## 使用方式

```
/security-testing 测一下这个接口的越权
/security-testing 对登录接口做注入测试
/security-testing 上线前安全自查，按 OWASP API Top 10 走一遍
```

## 工作流

1. 确认授权范围（只测你有权测试的系统）
2. 对照下方 OWASP API Top 10 检查清单逐条构造用例
3. 复用 [scripts/test_matrix.py](../../scripts/test_matrix.py) 生成「安全」列，补越权/注入专项
4. 执行并断言：未拦截=漏洞，错误体泄露敏感信息=配置缺陷
5. 输出风险报告（见 [references/reporting.md](../../references/reporting.md)）

## OWASP API Top 10 速查（独立可用）

1. **BOLA 越权对象**：A 的 token 访问/修改 B 的资源 → 应 403
2. **BFLA 越权功能**：普通用户调管理员接口 → 应 403
3. **注入**：`' OR '1'='1` / `{"$gt":""}` / `; cat /etc/passwd` → 应被拦截或转义
4. **鉴权失效**：无/过期/篡改签名 token → 应 401/拒绝
5. **过量请求**：高频请求 → 应触发 429
6. **安全配置错误**：暴露堆栈/版本/调试端点 → 应隐藏
7. **库存泄露**：响应含密码/token/SSN → 应裁剪
8. **未受限资源消耗**：超大 payload/深分页 → 应限流或拒绝
9. **SSRF**：服务端请求内网/元数据地址 → 应被禁
10. **批量分配**：多传 `isAdmin` 等未授权字段 → 应忽略

## 适用场景

- 接口/应用上线前安全自查
- 鉴权/授权模型、输入处理、速率限制验证

## 限制

- 不等于完整渗透测试；深度逻辑漏洞/链式利用需专业安全团队
- 不替代 SCA/DAST 工具，仅做接口层攻击面验证
- 完整方法论见整库 [references/security-testing.md](../../references/security-testing.md)
