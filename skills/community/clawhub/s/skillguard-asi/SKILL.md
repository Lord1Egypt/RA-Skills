---
name: skillguard
description: "Agent技能安全扫描器 — 上传Skill包自动检测安全漏洞（prompt注入/凭证泄露/代码执行/依赖审计等8维检测）。三平台首发，零依赖Python标准库。"
version: 1.0.0
tags: [安全, 审计, 扫描器, Agent安全, OWASP, 可执行]
category: 开发工具
---

# SkillGuard — Agent技能安全扫描器

**让Agent安装Skill前先做安全检查。** 覆盖OWASP ASI Top 10，8大检测器。

## 快速开始

```bash
python cli.py scan my-skill.zip           # 全量扫描
python cli.py scan my-skill.zip --format md  # Markdown报告
python cli.py list                        # 列出检测器
```

## 8大检测器

| 检测器 | OWASP ASI | 检测内容 |
|--------|:--:|------|
| prompt_injection | ASI-01,04 | Prompt注入/越狱/中文话术 |
| secret_exposure | ASI-02 | API Key/Token/密码泄露 |
| code_execution | ASI-03 | eval/exec/subprocess危险调用 |
| dependency_audit | ASI-06 | 依赖包安全审计 |
| permission_analysis | ASI-05 | 权限声明vs实际行为交叉验证 |
| sensitive_file_access | ASI-08 | 敏感文件+数据外泄 |
| network_whitelist | ASI-07 | URL白名单网络请求审计 |
| memory_pollution | ASI-09,10 | 记忆投毒/认知攻击 |

## TRACE五维安全评分

输出Trust(信任)/Reliability(可靠)/Authenticity(真实)/Compliance(合规)/Exposure(暴露)安全评分。

## 许可证

MIT — 免费使用、修改、分发。
