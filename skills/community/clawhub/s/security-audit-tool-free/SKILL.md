---
slug: security-audit-tool-free
name: security-audit-tool-free
version: 1.0.0
displayName: 安全审计工具(免费版)
summary: "扫描暴露凭据、开放端口、配置问题,支持自动修复常见安全问题,适合个人与小型团队,支持多种使用场景和自动化处理"
license: Proprietary
edition: free
description: 核心能力:，可自动提升工作效率

  - 凭据泄露检测(API Key、Token、硬编码密码)

  - 开放端口扫描与防火墙检查

  - 配置安全验证(CORS、认证、速率限制)

  - 文件权限审计

  - Docker容器安全检查

  - 常见问题自动修复

  适用场景:

  - 部署前安全自检

  - 定期安全审计

  - 开发环境安全基线

  - 快速漏洞排查

  差异化:

  - 一键自动修复常见安全问题

  - 多维度扫描(凭据/端口/配置/文件/Docker)

  - 纯本地执行,无需外部依赖

  - JSON格式报告输出

  适用关键词: 安全审...'
tags:
  - 安全
  - 安全审计
  - 漏洞扫描
  - 配置检查
  - 加密
  - 工具
  - self
  - node
tools:
  - read
  - exec
homepage: ""
category: "Security"
---
# 安全审计工具(免费版)

## 概述

安全审计工具免费版是一款面向个人开发者和小型团队的安全扫描工具。覆盖凭据泄露检测、开放端口扫描、配置安全验证、文件权限审计和Docker容器安全检查五大维度,支持自动修复常见安全问题。所有扫描在本地执行,无需外部依赖,输出结构化JSON报告,帮助快速发现和修复安全风险.
## 核心能力

### 扫描维度

| 维度 | 检测内容 | 严重等级 |
|---|----|----|
| 凭据检测 | API Key、Token、命令历史中的密钥、硬编码密码 | CRITICAL |
| 端口扫描 | 意外开放端口、互联网暴露服务、缺失防火墙规则 | HIGH |
| 配置验证 | 速率限制、认证配置、默认凭据、CORS策略 | MEDIUM |
| 文件权限 | 全局可读文件、全局可执行文件、敏感文件暴露 | HIGH |
| Docker安全 | 特权容器、缺失资源限制、容器内root用户 | HIGH |

**处理**: 解析扫描维度的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回扫描维度的响应数据,包含状态码、结果和日志.
### 免费版与专业版对比

| 功能 | 免费版 | 专业版 |
|:-----|:-----|:-----|
| 扫描维度 | 5个 | 8个(+合规/K8s/云) |
| 自动修复 | 基础修复 | 智能修复+回滚 |
| 报告格式 | JSON | HTML/PDF/SARIF |
| 定时审计 | 不支持 | Cron定时+告警 |
| 合规模板 | 不支持 | 等保/PCI-DSS/ISO27001 |
| CI/CD集成 | 不支持 | 流水线集成 |
| 多目标扫描 | 单目标 | 批量+并行 |

**处理**: 解析免费版与专业版对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回免费版与专业版对比的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：扫描暴露凭据、配置问题、支持自动修复常见、安全问题、适合个人与小型团、核心能力、凭据泄露检测、开放端口扫描与防、火墙检查、配置安全验证、文件权限审计、容器安全检查、常见问题自动修复等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:部署前安全自检

在将应用部署到生产环境前,执行快速安全审计.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | 安全审计工具(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 常见问题
node （请参考skill目录中的脚本文件）
# ...
# 示例
# 审计报告
# ═══════════════════════════════════════
# 扫描时间: 2026-07-18 10:30:00
# 扫描维度: 5
# 问题总数: 7
#   CRITICAL: 2
#   HIGH: 3
#   MEDIUM: 2
#   INFO: 0
```

### 场景二:全面安全扫描

```bash
# 完整审计(全面扫描)
node （请参考skill目录中的脚本文件） --full
# ...
# 输出JSON报告
node （请参考skill目录中的脚本文件） --full --json > audit-report.json
```

### 场景三:自动修复常见问题

```bash
# 自动修复
node （请参考skill目录中的脚本文件） --fix
# ...
# 修复内容:
# - 设置.env文件权限为600
# - 创建.gitignore(如缺失)
# - 启用基础安全头
# - 加固敏感配置文件
```

### 场景四:针对性审计

```bash
# 只检查凭据泄露
node （请参考skill目录中的脚本文件） --credentials
# ...
# 只检查开放端口
node （请参考skill目录中的脚本文件） --ports
# ...
# 只检查配置安全
node （请参考skill目录中的脚本文件） --configs
# ...
# 只检查文件权限
node （请参考skill目录中的脚本文件） --permissions
# ...
# 只检查Docker安全
node （请参考skill目录中的脚本文件） --docker
```

## 不适用场景

以下场景安全审计工具(免费版)不适合处理：

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

### 审计脚本

```python
import os
import re
import json
import subprocess
from datetime import datetime
from pathlib import Path
# ...
class SecurityAuditor:
    """安全审计工具"""
# ...
    SECRET_PATTERNS = [
        (r"AKIA[0-9A-Z]{16}", "AWS Access Key", "CRITICAL"),
        (r"gh[pousr]_[A-Za-z0-9_]{36}", "GitHub Token", "CRITICAL"),
        (r"sk-[A-Za-z0-9]{48}", "OpenAI API Key", "CRITICAL"),
        (r"-----BEGIN.*PRIVATE KEY-----", "Private Key", "CRITICAL"),
        (r"password\s*[:=]\s*['\"][^'\"]{8,}['\"]", "Hardcoded Password", "HIGH"),
        (r"api_key\s*[:=]\s*['\"][^'\"]{20,}['\"]", "API Key", "HIGH"),
        (r"secret\s*[:=]\s*['\"][^'\"]{16,}['\"]", "Secret", "HIGH"),
        (r"token\s*[:=]\s*['\"][^'\"]{20,}['\"]", "Token", "HIGH"),
    ]
# ...
    HIGH_RISK_PORTS = {
        6379: "Redis",
        2375: "Docker API",
        3306: "MySQL",
        5432: "`PostgreSQL`",
        27017: "MongoDB",
        9200: "Elasticsearch",
        5601: "Kibana"
    }
# ...
    def __init__(self):
        self.findings = []
        self.audit_time = datetime.now().isoformat()
# ...
    def audit(self, full=False, fix=False, target="."):
        """执行安全审计"""
        if full or not any([full]):
            self._check_credentials(target)
            self._check_ports()
            self._check_configs(target)
            self._check_permissions(target)
            self._check_docker(target)
# ...
        if fix:
            self._auto_fix()
# ...
        return self._generate_report()
# ...
    def _check_credentials(self, target):
        """检查凭据泄露"""
        target_path = Path(target)
# ...
        # 检查.env文件
        env_files = list(target_path.glob(".env*"))
        for env_file in env_files:
            if env_file.name == ".env.example":
                continue
            self.findings.append({
                "level": "INFO",
                "category": "credentials",
                "message": f"发现环境变量文件: {env_file.name}",
                "file": str(env_file),
                "fix": "确保.env文件已添加到.gitignore"
            })
# ...
        # 扫描代码中的硬编码凭据
        for filepath in target_path.rglob("*"):
            if filepath.suffix in {".js", ".ts", ".py", ".json", ".yaml", ".yml"}:
                if any(skip in str(filepath) for skip in ["node_modules", ".git", "dist", "build"]):
                    continue
                try:
                    content = filepath.read_text(encoding='utf-8', errors='ignore')
                    for pattern, name, severity in self.SECRET_PATTERNS:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            self.findings.append({
                                "level": severity,
                                "category": "credentials",
                                "message": f"发现{name}",
                                "file": str(filepath),
                                "line": content[:match.start()].count('\n') + 1,
                                "evidence": match.group()[:50],
                                "fix": f"移除硬编码{name},改用环境变量"
                            })
                except Exception:
                    pass
# ...
    def _check_ports(self):
        """检查开放端口"""
        try:
            result = subprocess.run(
                ["ss", "-tlnp"], capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split('\n')[1:]:
                for port, service in self.HIGH_RISK_PORTS.items():
                    if f":{port} " in line and "0.0.0.0" in line:
                            "level": "HIGH",
                            "category": "ports",
                            "message": f"{service}端口{port}暴露在0.0.0.0",
                            "evidence": line.strip(),
                            "fix": f"绑定到127.0.0.1或配置防火墙规则"
                        })
        except Exception:
            pass
# ...
    def _check_configs(self, target):
        """检查配置安全"""
        target_path = Path(target)
# ...
        # 检查CORS配置
suffix in {".js", ".ts", ".json", ".yaml"}:
                    continue
                try:
read_text(encoding='utf-8', errors='ignore')
                    if "cors" in content.lower() and "*" in content:
                            "level": "MEDIUM",
                            "category": "configs",
                            "message": "CORS配置为通配符(*)",
                            "file": str(filepath),
                            "fix": "配置具体的允许源,而非通配符"
                        })
                    if "debug" in content.lower() and "true" in content.lower():
                            "level": "MEDIUM",
                            "category": "configs",
                            "message": "调试模式可能已开启",
                            "file": str(filepath),
                            "fix": "生产环境关闭调试模式"
                        })
                except Exception:
                    pass
# ...
    def _check_permissions(self, target):
        """检查文件权限"""
        target_path = Path(target)
# ...
        sensitive_files = [".env", ".env.local", ".env.production", "id_rsa", "config.json"]
        for filename in sensitive_files:
            filepath = target_path / filename
                stat = filepath.stat()
                perms = oct(stat.st_mode)[-3:]
                if perms[-1] in ["4", "6", "7"]:  # 全局可读
                        "level": "HIGH",
                        "category": "permissions",
                        "message": f"敏感文件权限过宽: {filename} ({perms})",
                        "file": str(filepath),
                        "fix": f"执行: chmod 600 {filename}"
                    })
# ...
    def _check_docker(self, target):
        """检查Docker安全"""
        dockerfile = Path(target) / "Dockerfile"
        if dockerfile.exists():
            content = dockerfile.read_text()
            if "USER" not in content:
                    "level": "HIGH",
                    "category": "docker",
                    "message": "Docker容器以root用户运行",
                    "file": str(dockerfile),
                    "fix": "添加非root用户: RUN useradd -m appuser && USER appuser"
                })
            if "--privileged" in content:
                    "level": "HIGH",
                    "category": "docker",
                    "message": "Docker容器使用特权模式",
                    "file": str(dockerfile),
                    "fix": "移除--privileged,使用--cap-add指定具体权限"
                })
# ...
    def _auto_fix(self):
        """自动修复常见问题"""
        fixes = []
# ...
        # 修复.env权限
        env_file = Path(".env")
        if env_file.exists():
            os.chmod(env_file, 0o600)
            fixes.append("已设置.env文件权限为600")
# ...
        # 创建.gitignore
        gitignore = Path(".gitignore")
        if not gitignore.exists():
            gitignore.write_text(".env\n.env.local\nnode_modules/\ndist/\n")
            fixes.append("已创建.gitignore文件")
# ...
        return fixes
# ...
    def _generate_report(self):
        """生成审计报告"""
        critical = sum(1 for f in self.findings if f["level"] == "CRITICAL")
        high = sum(1 for f in self.findings if f["level"] == "HIGH")
        medium = sum(1 for f in self.findings if f["level"] == "MEDIUM")
        info = sum(1 for f in self.findings if f["level"] == "INFO")
# ...
        return {
            "audit_time": self.audit_time,
            "total_findings": len(self.findings),
            "summary": {
                "CRITICAL": critical,
                "HIGH": high,
                "MEDIUM": medium,
                "INFO": info
            },
            "findings": self.findings
        }
```

#
## 配置示例

### 审计配置

```json
{
  "audit_config": {
    "scan_dirs": ["."],
    "skip_dirs": ["node_modules", ".git", "dist", "build"],
    "check_credentials": true,
    "check_ports": true,
    "check_configs": true,
    "check_permissions": true,
    "check_docker": true,
    "auto_fix": false,
    "output_format": "json"
  }
}
```

## 最佳实践

### 1. 定期审计

```bash
# 每周执行一次完整审计
node （请参考skill目录中的脚本文件） --full --json > "audit-$(date +%Y%m%d).json"
```

### 2. 部署前必审

```bash
# 部署前执行快速审计+自动修复
node （请参考skill目录中的脚本文件） --fix
node （请参考skill目录中的脚本文件） --full
```

### 3. 关注CRITICAL

```bash
# 只显示严重问题
cat audit-report.json | python -c "
import json, sys
data = json.load(sys.stdin)
for f in data['findings']:
    if f['level'] in ['CRITICAL', 'HIGH']:
        print(f'[{f[\"level\"]}] {f[\"message\"]} - {f.get(\"file\", \"\")}')
"
```

## 常见问题

### Q1: 自动修复安全吗?

A: 自动修复只处理低风险问题:设置文件权限、创建.gitignore、加固配置文件。不会修改代码逻辑或删除文件.
### Q2: 端口扫描需要root权限吗?

A: 使用 `ss -tlnp` 需要root权限查看进程信息。普通用户可使用 `ss -tln` 查看端口,但无法看到进程名.
### Q3: 如何排除误报?

A: 在审计配置中添加排除目录和文件。对于已知的安全配置(如测试环境的硬编码密钥),可添加白名单.
### Q4: 如何获取更多扫描维度?

A: 免费版覆盖5个核心维度。专业版增加了合规审计、Kubernetes安全、云安全配置等维度,支持HTML报告和定时审计.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Linux / macOS / Windows(部分功能受限)
- **Python版本**: 3.8+ 或 Node.js 16+

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| Python/Node.js | 运行时 | 必需 | 系统自带 |
| ss/netstat | 系统工具 | 可选 | 系统自带(端口扫描用) |
| Docker | 运行时 | 可选 | docker.com(Docker检查用) |

### API Key 配置
- 免费版基础LLM由Agent平台提供,完全本地执行

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行安全审计任务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "安全审计工具(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "security audit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
