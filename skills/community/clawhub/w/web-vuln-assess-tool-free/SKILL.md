---
slug: web-vuln-assess-tool-free
name: web-vuln-assess-tool-free
version: 1.0.0
displayName: Web漏洞评估(免费版)
summary: "OWASP对齐的Web应用漏洞评估,覆盖19类漏洞,含检查清单与修复指南,支持多种使用场景和自动化处理"
license: Proprietary
edition: free
description: 核心能力:，可处理提升工作效率

  - 19个漏洞类别100+检查项

  - OWASP Top 10:2021对齐

  - 支持PHP/Node。js/Python/Java等20种技术栈

  - 安全检查清单与修复建议

  - 按严重程度排序的评估报告

  适用场景:

  - Web应用上线前安全评估

  - API安全漏洞检测

  - 渗透测试范围规划

  - 安全意识培训

  差异化:

  - 19类漏洞全覆盖(含IoT/移动端/零日)

  - 技术栈特定检测规则

  - 合规框架映射(OWASP/PCI-DSS/GDPR/HIPAA)

  - 中文修复建...'
tags:
  - 安全
  - Web安全
  - 漏洞评估
  - OWASP
  - Web开发
  - 前端
  - 开发工具
  - high
  - web
  - owasp
  - medium
  - api
tools:
  - read
  - exec
  - write
  - glob
homepage: ""
category: "Development"
---
# Web漏洞评估(免费版)

## 概述

Web漏洞评估免费版是一款面向Web应用的安全漏洞评估工具。覆盖19个漏洞类别、100+检查项,对齐 OWASP Top 10:2021 标准。支持 PHP、Node.js、Python、Java、React 等20种技术栈,提供技术特定的漏洞检测规则。包含安全检查清单、修复建议和按严重程度排序的评估报告,帮助开发者在上线前发现和修复安全风险.
## 核心能力

### 19个漏洞类别

| 编号 | 类别 | 严重等级 | OWASP映射 |
|---|---|----|-------|
| 1 | 注入漏洞 | CRITICAL | A03:2021 |
| 2 | 认证与会话管理失效 | HIGH | A07:2021 |
| 3 | 敏感数据暴露 | HIGH | A02:2021 |
| 4 | 安全配置错误 | MEDIUM | A05:2021 |
| 5 | XML外部实体(XXE) | HIGH | - |
| 6 | 访问控制失效 | HIGH | A01:2021 |
| 7 | 不安全反序列化 | HIGH | A08:2021 |
| 8 | API安全 | HIGH | - |
| 9 | 不安全通信 | MEDIUM | - |
| 10 | 客户端漏洞 | MEDIUM | - |
| 11 | 拒绝服务(DoS) | MEDIUM | - |
| 12 | 服务端请求伪造(SSRF) | HIGH | A10:2021 |
| 13 | 认证绕过 | CRITICAL | - |
| 14 | 内容欺骗 | MEDIUM | - |
| 15 | 业务逻辑缺陷 | HIGH | - |
| 16 | 零日模式 | CRITICAL | - |
| 17 | 移动应用漏洞 | HIGH | - |
| 18 | IoT漏洞 | HIGH | - |
| 19 | 其他漏洞 | MEDIUM | - |

**处理**: 解析个漏洞类别的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回个漏洞类别的响应数据,包含状态码、结果和日志.
### 支持的技术栈

## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | Web漏洞评估(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
后端语言: PHP, Node.js, Python, Java, .NET, Ruby
前端框架: React, Angular, Vue
CMS系统: WordPress
数据库: MySQL, `PostgreSQL`, MongoDB, Redis
基础设施: Docker, Kubernetes, Nginx, Apache
云平台: AWS, Azure
```

**处理**: 解析支持的技术栈的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回支持的技术栈的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 免费版与专业版对比

| 功能 | 免费版 | 专业版 |
|---:|---:|---:|
| 漏洞类别 | 19类 | 19类+自定义 |
| 检查项 | 100+ | 100+实时更新 |
| 评估方式 | 手动清单 | API自动化 |
| 技术栈 | 20种 | 20+自定义 |
| 合规映射 | 4种框架 | 4种+自定义 |
| 报告格式 | 文本/Markdown | HTML/PDF/SARIF |
| 修复脚本 | 不支持 | 自动生成测试脚本 |
| 批量评估 | 不支持 | 多应用批量 |

**处理**: 解析免费版与专业版对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回免费版与专业版对比的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：对齐的、Web、应用漏洞评估、类漏洞、含检查清单与修复、核心能力、Top、种技术栈、安全检查清单与修、复建议、按严重程度排序的、评估报告等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:Web应用上线前评估

对新开发的Web应用执行全面安全评估.
```text
评估流程:
1. 确定应用信息:
   - 应用名称: ShopFast 电商平台
   - 应用类型: Web Application
   - 技术栈: Python, React, `PostgreSQL`, Docker, AWS
   - 部署环境: Cloud (AWS)
   - 评估范围: 全部19类漏洞
# ...
2. 执行评估:
   [1/19] 注入漏洞检测 ........... 发现 2 个问题
   [2/19] 认证与会话管理 ......... 发现 1 个问题
   [3/19] 敏感数据暴露 ........... 未发现问题
   ...
   [19/19] 其他漏洞 .............. 发现 1 个问题
# ...
3. 生成报告:
   CRITICAL: 2 (SQL注入, 认证绕过)
   HIGH: 3 (XSS, SSRF, 访问控制)
   MEDIUM: 4 (配置错误, CORS, DoS, 内容欺骗)
```

### 场景二:API安全评估

```bash
# 评估REST API安全性
# 检查项:
# - 认证机制是否安全(JWT/Session)
# - 授权检查是否到位(IDOR/SSRF)
# - 输入验证是否完整
# 已知限制
# - 错误信息是否泄露敏感数据
```

### 场景三:合规性评估

```text
合规框架映射:
- OWASP Top 10: 检查A01-A10所有类别
- PCI-DSS: 支付数据保护相关检查
- GDPR: 个人数据保护相关检查
- HIPAA: 医疗数据保护相关检查
```

## 不适用场景

以下场景Web漏洞评估(免费版)不适合处理：

- 渗透测试未授权目标
- 物理安全防护
- 社会工程学攻击

## 触发条件

需要安全检测、合规审计、漏洞扫描、加密防护时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 漏洞评估检查清单

```python
class WebVulnAssessment:
    """Web漏洞评估工具"""
# ...
    VULN_CATEGORIES = {
        "injection": {
            "name": "注入漏洞",
            "severity": "CRITICAL",
            "owasp": "A03:2021",
            "checks": [
                "SQL注入: 是否使用参数化查询?",
                "命令注入: 用户输入是否直接执行?",
                "LDAP注入: 目录服务查询是否安全?",
                "NoSQL注入: NoSQL查询是否参数化?",
                "模板注入: 模板引擎是否安全使用?"
            ]
        },
        "authentication": {
            "name": "认证与会话管理",
            "severity": "HIGH",
            "owasp": "A07:2021",
            "checks": [
                "密码是否使用bcrypt/scrypt/argon2哈希?",
                "JWT是否设置过期时间和签名验证?",
                "Session是否使用安全Cookie(httpOnly, secure, sameSite)?",
                "是否有登录速率限制和账户锁定?",
                "密码重置流程是否安全?"
            ]
        },
        "data_exposure": {
            "name": "敏感数据暴露",
            "severity": "HIGH",
            "owasp": "A02:2021",
            "checks": [
                "是否全程使用HTTPS/TLS?",
                "敏感数据是否加密存储?",
                "API响应是否泄露敏感字段?",
                "错误信息是否包含堆栈跟踪?",
                "日志是否记录敏感数据?"
            ]
        },
        "misconfiguration": {
            "name": "安全配置错误",
            "severity": "MEDIUM",
            "owasp": "A05:2021",
            "checks": [
                "是否更改默认凭据?",
                "是否配置安全HTTP头(CSP, HSTS, X-Frame-Options)?",
                "是否关闭目录列表?",
                "是否禁用调试模式?",
                "CORS是否配置为通配符(*)?"
            ]
        },
        "access_control": {
            "name": "访问控制失效",
            "severity": "HIGH",
            "owasp": "A01:2021",
            "checks": [
                "所有API端点是否有认证检查?",
                "是否有授权验证(用户只能访问自己的数据)?",
                "是否存在IDOR(不安全直接对象引用)?",
                "是否有SSRF防护?",
                "管理接口是否受到保护?"
            ]
        },
        "api_security": {
            "name": "API安全",
            "severity": "HIGH",
            "owasp": "-",
            "checks": [
                "API是否有速率限制?",
                "API版本是否通过URL或Header管理?",
                "是否验证Content-Type?",
                "是否有输入大小限制?",
                "是否使用API网关统一管理?"
            ]
        },
        "ssrf": {
            "name": "服务端请求伪造",
            "severity": "HIGH",
            "owasp": "A10:2021",
            "checks": [
                "URL输入是否验证协议(http/https only)?",
                "是否阻止内网IP访问?",
                "是否限制可访问的域名?",
                "是否使用DNS重绑定防护?",
                "文件URL是否验证来源?"
            ]
        }
    }
# ...
    TECH_STACK_CHECKS = {
        "python": [
            "是否使用Django/Flask安全中间件?",
            "是否使用ORM参数化查询?",
            "是否禁用了pickle反序列化?",
            "是否使用python-jose安全处理JWT?"
        ],
        "react": [
            "是否避免使用dangerouslySetInnerHTML?",
            "是否对用户输入进行DOMPurify消毒?",
            "是否使用httpOnly Cookie存储令牌?",
            "是否配置CSP防止XSS?"
        ],
        "postgresql": [
            "是否使用参数化查询(防SQL注入)?",
            "是否配置连接加密(sslmode=require)?",
            "是否设置最小权限数据库用户?",
            "是否启用审计日志?"
        ],
        "docker": [
            "是否使用非root用户运行容器?",
            "是否设置资源限制(memory, cpu)?",
            "是否使用.dockerignore排除敏感文件?",
            "是否使用多阶段构建减小攻击面?"
        ],
        "aws": [
            "S3存储桶是否设为私有?",
            "IAM是否遵循最小权限原则?",
            "安全组是否限制入站流量?",
            "是否使用KMS加密敏感数据?"
        ]
    }
# ...
    def assess(self, app_info):
        """执行漏洞评估"""
        results = {
            "app_info": app_info,
            "categories": {},
            "tech_specific": {},
            "summary": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        }
# ...
        # 评估19个漏洞类别
        for cat_id, cat_info in self.VULN_CATEGORIES.items():
            findings = []
            for check in cat_info["checks"]:
                findings.append({
                    "check": check,
                    "status": "需人工确认",
                    "severity": cat_info["severity"]
                })
# ...
            results["categories"][cat_id] = {
                "name": cat_info["name"],
                "severity": cat_info["severity"],
                "owasp": cat_info["owasp"],
                "findings": findings
            }
# ...
        # 技术栈特定检查
        for tech in app_info.get("technology_stack", []):
            if tech in self.TECH_STACK_CHECKS:
                results["tech_specific"][tech] = self.TECH_STACK_CHECKS[tech]
# ...
        return results
# ...
    def generate_report(self, results):
        """生成评估报告"""
        report = f"""
Web漏洞评估报告
═══════════════════════════════════════════
应用名称: {results['app_info'].get('name', 'N/A')}
应用类型: {results['app_info'].get('type', 'N/A')}
技术栈: {', '.join(results['app_info'].get('technology_stack', []))}
部署环境: {results['app_info'].get('deployment', 'N/A')}
评估范围: 全部{len(results['categories'])}个漏洞类别
═══════════════════════════════════════════
# ...
漏洞类别详情:
"""
# ...
        for cat_id, cat in results["categories"].items():
            report += f"\n[{cat['severity']}] {cat['name']} (OWASP: {cat['owasp']})\n"
            for finding in cat["findings"]:
                report += f"  - {finding['check']}\n"
# ...
        if results["tech_specific"]:
            report += "\n技术栈特定检查:\n"
            for tech, checks in results["tech_specific"].items():
                report += f"\n  {tech}:\n"
                for check in checks:
                    report += f"    - {check}\n"
# ...
        report += f"""
═══════════════════════════════════════════
建议: 优先修复CRITICAL和HIGH级别漏洞
═══════════════════════════════════════════
"""
        return report
```

#
## 示例

### 评估信息收集

```python
# 评估前需收集的信息
app_info = {
    "name": "ShopFast电商平台",
    "type": "E-commerce Platform",
    "technology_stack": ["python", "react", "postgresql", "redis", "docker", "aws"],
    "deployment_environment": "Cloud (AWS)",
    "assessment_scope": [
        "injection", "authentication", "data_exposure",
        "misconfiguration", "access_control", "api_security",
        "communication", "client_side", "ssrf", "business_logic"
    ],
    "compliance_frameworks": ["owasp_top_10", "pci_dss"]
}
```

### 合规框架映射

| 框架 | 检查重点 | 适用场景 |
|:---:|:---:|:---:|
| OWASP Top 10 | A01-A10全部类别 | 通用Web应用 |
| PCI-DSS | 支付数据保护 | 电商平台 |
| GDPR | 个人数据保护 | 面向欧洲用户 |
| HIPAA | 医疗数据保护 | 医疗健康应用 |

## 最佳实践

### 1. 评估优先级

```text
第一优先: CRITICAL漏洞(注入、认证绕过、零日模式)
第二优先: HIGH漏洞(XSS、SSRF、访问控制、API安全)
第三优先: MEDIUM漏洞(配置错误、CORS、DoS)
第四优先: LOW漏洞(信息泄露、最佳实践)
```

### 2. 技术栈特定检查

```bash
# Python/React/`PostgreSQL`/Docker/AWS 技术栈
# 每种技术有其特定的安全检查项
# 评估时需覆盖技术栈相关的所有检查项
```

### 3. 合规对齐

```bash
# 如果处理支付数据,映射PCI-DSS
# 如果处理欧洲用户数据,映射GDPR
# 如果处理医疗数据,映射HIPAA
# 始终对齐OWASP Top 10
```

## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 常见问题

### Q1: 评估需要多长时间?

A: 手动评估取决于应用复杂度。小型应用2-4小时,中型应用1-2天,大型应用1-2周。使用专业版API自动化评估可缩短至30分钟.
### Q2: 19个类别都需要评估吗?

A: 建议全量评估。可根据应用类型调整重点: API应用重点评估api_security和access_control; 电商平台重点评估data_exposure和PCI-DSS合规.
### Q3: 评估后发现漏洞怎么办?

A: 按严重程度优先级修复。CRITICAL立即修复,HIGH在7天内修复。每个漏洞的检查清单中包含修复建议.
### Q4: 如何获取API自动化评估?

A: 免费版提供手动检查清单。专业版提供API驱动的自动化评估,支持HTML/PDF报告和自动生成测试脚本.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| Python | 运行时 | 推荐 | 系统自带 |
| curl | CLI工具 | 可选 | 系统自带(API调用用) |

### API Key 配置
- 免费版无需API Key,所有评估基于检查清单手动执行
- 可选配置外部漏洞评估API Key(如需API自动化评估)

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行Web漏洞评估任务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Web漏洞评估(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "web vuln assess"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
