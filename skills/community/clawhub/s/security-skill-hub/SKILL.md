---
name: security-skill-hub
description: |
  安全技能插座 - 统一的安全技能管理和调用平台
  
  这是一个安全技能的"插座"框架，提供统一的安全能力入口。已集成以下技能：
  
  **全网技能搜索 (ClawHub)**:
  - clawhub: 从 clawhub.com 搜索安装全网技能
  
  **信息收集类**:
  - collector-strategy: 采集策略Skill
  - skill-sample-collector: 样本采集Skill
  
  **漏洞扫描类**:
  - security-vuln-scanner: 漏洞扫描Skill
  - agent-security-code-scanner: 代码安全扫描
  
  **威胁情报类**:
  - ioc-validator: IOC验证Skill
  - security-ioc-research: IOC研究Skill
  - threat-monitoring: 威胁监控
  
  **恶意软件分析**:
  - code-malware-scanner: 恶意代码扫描
  - agent-security-skill-scanner: 技能安全扫描
  
  **防护类**:
  - agent-defender: Agent Defender安全防护
  - agent-security-network-guardian: 网络防护监控
  
  **审计类**:
  - agent-security-openclaw-audit: OpenClaw安全审计
  - agent-security-governance-audit: 治理审计
  
  **其他安全类**:
  - agent-security-password-hardening: 密码硬化检测
  - agent-security-key-manager: 密钥管理
  - security-ioc-research: IOC研究
  
  使用场景:
  - 需要调用安全能力时
  - 不知道用哪个安全技能时
  - 需要组合多个安全技能时
  - 扩展新的安全能力时
---

# 安全技能插座 (Security Skill Hub)

## 概述

这是一个统一的安全技能管理平台，提供"插座式"的安全能力调用接口。

## 架构

```
security-skill-hub/
├── SKILL.md (本文件 - 技能插座核心)
└── skills/ (已注册的安全技能列表)
```

## 已集成的技能

### 1. 全网技能搜索 (ClawHub)

| 技能名称 | 功能 | 触发关键词 |
|---------|------|-----------|
| clawhub | 从 clawhub.com 搜索安装全网技能 | 搜索技能, 安装技能, clawhub |

### 2. 性能检测类

| 技能名称 | 功能 | 触发关键词 |
|---------|------|-----------|
| ai-performance-analyzer | AI工具性能诊断/卡顿优化 | 性能, 卡顿, 优化, 诊断 |
| machine-health-explorer | 机器健康探索/僵尸进程/负载评估 | 机器健康, 僵尸进程, 负载, 升级建议 |

### 3. 问题研究类

| 技能名称 | 功能 | 触发关键词 |
|---------|------|-----------|
| claude-code-openclaw-troubleshoot | Claude Code/OpenClaw 常见问题研究 | 常见问题, 故障, 性能问题 |

### 3. 信息收集类

| 技能名称 | 功能 | 触发关键词 |
|---------|------|-----------|
| collector-strategy | 采集策略、关键词扩展 | /collector-help, 采集 |
| skill-sample-collector | 样本采集 | 样本采集 |

### 2. 漏洞扫描类

| 技能名称 | 功能 | 触发关键词 |
|---------|------|-----------|
| security-vuln-scanner | 漏洞扫描 | 漏洞, CVE, 扫描 |
| agent-security-code-scanner | 代码安全扫描 | 代码扫描, 安全审计 |

### 3. 威胁情报类

| 技能名称 | 功能 | 触发关键词 |
|---------|------|-----------|
| ioc-validator | IOC验证(域名/邮箱/hash) | IOC, 验证, 威胁情报 |
| security-ioc-research | IOC研究分析 | IOC研究, 情报分析 |
| threat-monitoring | 威胁监控 | 威胁, 监控, APT |

### 4. 恶意软件分析

| 技能名称 | 功能 | 触发关键词 |
|---------|------|-----------|
| code-malware-scanner | 恶意代码检测 | 恶意代码, 后门 |
| agent-security-skill-scanner | 技能安全扫描 | 技能扫描, 安全检测 |

### 5. 防护类

| 技能名称 | 功能 | 触发关键词 |
|---------|------|-----------|
| agent-defender | Agent安全防护 | 防护, Defender |
| agent-security-network-guardian | 网络防护监控 | 网络防护, SSH爆破 |

### 6. 审计类

| 技能名称 | 功能 | 触发关键词 |
|---------|------|-----------|
| agent-security-openclaw-audit | OpenClaw安全审计 | OpenClaw审计 |
| agent-security-governance-audit | 治理审计 | 治理, 审计 |

### 7. 其他安全类

| 技能名称 | 功能 | 触发关键词 |
|---------|------|-----------|
| agent-security-password-hardening | 密码硬化检测 | 硬编码, 密码检测 |
| agent-security-key-manager | 密钥管理 | 密钥, API Key |
| agent-security-knowledge-query | 知识查询 | 知识查询 |

## 使用方式

### 直接调用

根据需求选择对应的安全技能，使用其 SKILL.md 中定义的触发方式。

### 组合调用

当需要组合多个安全技能时，可以：
1. 先调用一个技能获取结果
2. 基于结果调用另一个技能
3. 汇总分析

### 扩展新技能

要添加新的安全技能：
1. 在 skills/ 目录下创建或导入新技能
2. 更新本文件的技能列表
3. 定义触发关键词

## 快速调用示例

```
用户: "搜索一个做PDF的技能"
→ 调用 clawhub 搜索安装

用户: "帮我验证这个域名是不是恶意"
→ 调用 ioc-validator

用户: "扫描这个项目的安全漏洞"
→ 调用 security-vuln-scanner 或 agent-security-code-scanner

用户: "检查这个技能有没有后门"
→ 调用 agent-security-skill-scanner

用户: "监控SSH暴力破解"
→ 调用 agent-security-network-guardian

用户: "检测代码中的硬编码密码"
→ 调用 agent-security-password-hardening
```

## ClawHub 全网技能搜索

当需要搜索/安装新技能时，使用 clawhub：

```bash
# 搜索技能
clawhub search "关键词"

# 安装技能
clawhub install 技能名

# 更新所有技能
clawhub update --all

# 查看已安装
clawhub list
```

### 常用搜索示例

- 安全相关: `clawhub search security`
- 浏览器自动化: `clawhub search browser`
- 深度研究: `clawhub search research`
- 漏洞扫描: `clawhub search vuln`
- 威胁情报: `clawhub search threat`

## 技能注册表

技能注册到 ~/.openclaw/workspace/skills/ 目录。

完整技能列表参考: AGENTS.md 中的安全相关技能
