---
name: Security Audit Pro
slug: security-audit-pro
description: 企业级全方位安全审计技能，覆盖代码静态分析、依赖漏洞扫描、容器镜像安全、云配置合规、密钥泄露检测、网络端口审计、权限审查。支持OWASP Top 10 / CIS Benchmark / SOC2 / ISO27001合规检查，自动生成修复优先级报告。
version: 1.0.0
author: ai-gaoqian
tags:
  - security
  - audit
  - vulnerability
  - compliance
  - owasp
  - cis-benchmark
  - devsecops
  - secret-scanning
metadata:
  openclaw:
    requires:
      - security-scanner
      - trivy
      - npm-audit
---

# Security Audit Pro

企业级全方位安全审计技能，覆盖代码、依赖、容器、云配置、密钥、网络、权限七大安全维度，支持多种合规标准，自动生成按风险等级排序的修复优先级报告。

## 触发条件

- "安全审计这个项目"
- "扫描依赖漏洞"
- "检查AWS/Azure/GCP配置合规"
- "检测代码中的密钥泄露"
- "容器镜像安全扫描"
- "是否符合SOC2合规要求"
- "端口安全检测"

## 审计维度

| 维度 | 检查内容 | 覆盖标准 |
|------|---------|---------|
| 代码安全 | SQL注入、XSS、SSRF、路径遍历、硬编码密钥、不安全函数 | OWASP Top 10 |
| 依赖安全 | npm audit / pip audit / gem audit漏洞扫描，供应链攻击检测 | CVE / NVD |
| 容器安全 | 镜像层漏洞、非root运行、特权模式、敏感挂载 | CIS Docker Benchmark |
| 云配置 | IAM过度授权、S3公开桶、安全组0.0.0.0/0、密钥轮转 | CIS AWS/Azure/GCP |
| 密钥检测 | 正则+熵检测API Key/Token/私钥/证书，Git历史扫描 | 自定义规则 |
| 网络审计 | 开放端口、监听服务、防火墙规则、DNS泄漏、TLS版本 | NIST SP 800-53 |
| 权限审查 | 文件权限、SUID/SGID、sudo配置、SSH authorized_keys | CIS Benchmark |

## 合规标准

- **OWASP Top 10** (2021): 注入/认证失效/敏感数据泄露/XXE/访问控制失效/安全配置错误/XSS/反序列化/已知漏洞/日志监控不足
- **CIS Benchmark**: Level 1（基本安全）和Level 2（深度防御）
- **SOC2**: 安全性/可用性/处理完整性/机密性/隐私性
- **ISO 27001**: 信息安全管理体系ISMS

## 输出格式

```
🔒 安全审计报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
审计目标: [项目/目录/API端点]
审计时间: [时间戳] | 覆盖维度: [N]/7
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 严重 (0day利用): [N] 个
   - [漏洞详情 + CVE编号 + 修复建议]

🟠 高危 (<=24h修复): [N] 个
   - [漏洞详情 + 修复建议]

🟡 中危 (<=7天修复): [N] 个

🟢 低危/建议: [N] 个

📊 合规评分: [0-100] | 通过: [标准列表] | 未通过: [标准列表]
📋 修复优先级: [按时间线排列]
```

## 注意事项

- 扫描结果基于静态分析，不模拟真实攻击
- 误报（false positive）标注为「可能」，建议人工确认
- 合规检查仅提供技术层面评估，不替代正式审计
- 密钥检测到泄露后建议立即轮转并撤销旧凭据
