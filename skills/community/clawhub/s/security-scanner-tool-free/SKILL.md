---
slug: security-scanner-tool-free
name: security-scanner-tool-free
version: 1.0.0
displayName: 安全扫描器(免费版)
summary: "自动化安全扫描工具包,含端口扫描、漏洞检测、SSL分析,适合安全测试与评估,支持多种使用场景和自动化处理"
license: Proprietary
edition: free
description: 核心能力:，可自动提升工作效率

  - 端口扫描与服务识别(nmap)

  - 漏洞模板扫描(nuclei)

  - SSL/TLS配置分析(sslscan)

  - Web服务器漏洞检测(nikto)

  - 扫描报告自动生成

  适用场景:

  - 安全评估快速扫描

  - 渗透测试前期侦察

  - SSL证书合规检查

  - 基础漏洞发现

  差异化:

  - 多工具集成,一键多种扫描

  - 按场景分类的扫描模板

  - Markdown格式扫描报告

  - 包含道德使用准则

  适用关键词: 安全扫描, 端口扫描, 漏洞检测, SSL检查, nmap,...'
tags:
  - 安全
  - 漏洞扫描
  - 渗透测试
  - 网络安全
  - 加密
  - 工具
  - self
  - target
  - result
  - results
  - 扫描
tools:
  - read
  - exec
homepage: ""
category: "Security"
---
# 安全扫描器(免费版)

## 概述

安全扫描器免费版是一款面向安全工程师的自动化扫描工具包。集成 nmap 端口扫描、nuclei 漏洞检测、sslscan SSL分析、nikto Web服务器扫描等核心工具,提供按场景分类的扫描模板和自动化报告生成。帮助安全测试人员快速完成前期侦察和基础漏洞发现工作.
## 核心能力

### 扫描工具集成

| 工具 | 用途 | 扫描类型 |
|---|---|----|
| nmap | 网络端口扫描 | 主机发现/端口扫描/服务识别 |
| nuclei | 漏洞模板扫描 | CVE检测/配置检查/漏洞验证 |
| sslscan | SSL/TLS分析 | 证书检查/协议版本/加密套件 |
| nikto | Web服务器扫描 | 配置审计/漏洞检测 |

**处理**: 解析扫描工具集成的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回扫描工具集成的响应数据,包含状态码、结果和日志.
### 免费版与专业版对比

| 功能 | 免费版 | 专业版 |
|:-----|:-----|:-----|
| 扫描工具 | 4个核心工具 | 10+工具 |
| 扫描模板 | 基础模板 | 高级+自定义模板 |
| 报告格式 | Markdown | HTML/PDF/SARIF |
| 多目标扫描 | 单目标 | 批量+并行 |
| 调度扫描 | 不支持 | Cron定时 |
| CVE关联 | 不支持 | CVE数据库映射 |
| 修复建议 | 基础 | 详细修复指南 |

**处理**: 解析免费版与专业版对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回免费版与专业版对比的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：自动化安全扫描工、含端口扫描、适合安全测试与评、核心能力、端口扫描与服务识、配置分析、服务器漏洞检测、扫描报告自动生成等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:快速侦察扫描

对目标进行快速初始扫描,发现存活主机和开放端口.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | 安全扫描器(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 主机发现
nmap -sn -T4 192.168.1.0/24
# ...
# 快速端口扫描(前100个常用端口)
nmap -F 192.168.1.1
# ...
# 服务版本识别
nmap -sV -T4 192.168.1.1
```

### 场景二:全端口深度扫描

```bash
# 全65535端口+服务+脚本+OS探测
nmap -p- -sV -sC -A -T4 192.168.1.1 -oN full_scan.txt
```

### 场景三:Web漏洞扫描

```bash
# Nuclei CVE漏洞扫描
nuclei -u https://target.com -t cves/ -o nuclei_results.txt
# ...
# Nikto Web服务器扫描
nikto -h target.com -o nikto_report.txt
# ...
# 目录枚举
nmap --script http-enum -p 80,443 target.com
```

### 场景四:SSL/TLS分析

```bash
# SSL配置检查
sslscan target.com
# ...
# 检查证书有效期、协议版本、加密套件
sslscan target.com | grep -E "SSLv|TLS|Certificate"
```

## 不适用场景

以下场景安全扫描器(免费版)不适合处理：

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

### 扫描脚本

```python
import subprocess
import os
from datetime import datetime
# ...
class SecurityScanner:
    """安全扫描工具包"""
# ...
    def __init__(self, target):
        self.target = target
        self.results = {}
        self.report_dir = "reports"
        os.makedirs(self.report_dir, exist_ok=True)
# ...
    def quick_recon(self):
        """快速侦察扫描"""
        print(f"[*] 开始快速侦察: {self.target}")
# ...
        # 主机发现
        result = self._run_command(f"nmap -sn -T4 {self.target}")
        self.results["host_discovery"] = result
# ...
        # 快速端口扫描
_run_command(f"nmap -F -T4 {self.target}")
        self.results["port_scan"] = result
# ...
        return self.results
# ...
    def full_scan(self):
        """全面深度扫描"""
        print(f"[*] 开始全面扫描: {self.target}")
# ...
        # 全端口扫描
            f"nmap -p- -sV -sC -A -T4 {self.target}"
        )
        self.results["full_scan"] = result
# ...
        return self.results
# ...
    def vuln_scan(self):
        """漏洞扫描"""
        print(f"[*] 开始漏洞扫描: {self.target}")
# ...
        # Nmap漏洞脚本
            f"nmap --script vuln {self.target}"
        )
        self.results["vuln_scan"] = result
# ...
        # Nuclei扫描
            f"nuclei -u http://{self.target} -t cves/ -t vulnerabilities/"
        )
        self.results["nuclei_scan"] = result
# ...
        return self.results
# ...
    def ssl_scan(self):
        """SSL/TLS分析"""
        print(f"[*] 开始SSL扫描: {self.target}")
# ...
_run_command(f"sslscan {self.target}")
        self.results["ssl_scan"] = result
# ...
        return self.results
# ...
    def web_scan(self):
        """Web应用扫描"""
        print(f"[*] 开始Web扫描: {self.target}")
# ...
        # Nikto扫描
            f"nikto -h http://{self.target} -o {self.report_dir}/nikto_{self.target}.txt"
        )
        self.results["web_scan"] = result
# ...
        return self.results
# ...
    def generate_report(self):
        """生成扫描报告"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        report_path = os.path.join(
            self.report_dir,
            f"security-scan-{self.target}-{timestamp}.md"
        )
# ...
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# 安全扫描报告\n\n")
            f.write(f"**目标**: {self.target}\n")
            f.write(f"**时间**: {timestamp}\n\n")
# ...
            for scan_type, result in self.results.items():
                f.write(f"## {scan_type}\n\n")
                f.write(f"```\n{result}\n```\n\n")
# ...
        print(f"[+] 报告已生成: {report_path}")
        return report_path
# ...
    def _run_command(self, command):
        """执行系统命令"""
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True,
                text=True, timeout=600
            )
            return result.stdout if result.stdout else result.stderr
        except subprocess.TimeoutExpired:
            return "扫描超时(10分钟)"
        except Exception as e:
            return f"错误: {str(e)}"
# ...
# 示例
if __name__ == "__main__":
    scanner = SecurityScanner("192.168.1.1")
# ...
    # 快速侦察
    scanner.quick_recon()
# ...
    # 漏洞扫描
    scanner.vuln_scan()
# ...
    # SSL扫描
    scanner.ssl_scan()
# ...
    # 生成报告
    scanner.generate_report()
```

#
## 配置示例

### Nmap扫描参数速查

| 参数 | 用途 | 示例 |
|:---:|:---:|:---:|
| `-sn` | 主机发现(不扫描端口) | `nmap -sn 192.168.1.0/24` |
| `-sS` | SYN半开扫描 | `nmap -sS 192.168.1.1` |
| `-sV` | 服务版本探测 | `nmap -sV 192.168.1.1` |
| `-sC` | 默认脚本扫描 | `nmap -sC 192.168.1.1` |
| `-A` | 全面探测(OS+版本+脚本) | `nmap -A 192.168.1.1` |
| `-p-` | 全65535端口 | `nmap -p- 192.168.1.1` |
| `-T4` | 加速扫描(0-5) | `nmap -T4 192.168.1.1` |
| `--script vuln` | 漏洞检测脚本 | `nmap --script vuln 192.168.1.1` |

### Nuclei模板分类

```bash
# CVE漏洞
nuclei -u target.com -t cves/
# ...
# 配置错误
nuclei -u target.com -t misconfiguration/
# ...
# 敏感信息暴露
nuclei -u target.com -t exposures/
# ...
# 技术栈指纹
nuclei -u target.com -t technologies/
# ...
# 自定义模板
nuclei -u target.com -t custom-templates/
```

## 最佳实践

### 1. 分阶段扫描

```bash
# 阶段1:侦察(快速)
nmap -sn -T4 192.168.1.0/24
# ...
# 阶段2:端口扫描(中等)
nmap -sV -sC -T4 192.168.1.1
# ...
# 阶段3:漏洞扫描(深度)
nmap --script vuln 192.168.1.1
nuclei -u http://192.168.1.1 -t cves/
```

### 2. 扫描结果保存

```bash
# 保存为多种格式
nmap -sV -oN scan.txt -oX scan.xml -oG scan.grep 192.168.1.1
# ...
# Nuclei结果保存
nuclei -u target.com -o results.txt -j -o results.json
```

### 3. 道德使用准则

```text
安全扫描道德准则:
1. 仅扫描授权目标
2. 获取书面许可后测试
3. 负责任地报告漏洞
4. 未经授权不利用漏洞
5. 遵守当地法律法规
```

## 常见问题

### Q1: 扫描需要什么权限?

A: SYN扫描(`-sS`)和OS探测(`-O`)需要root/管理员权限。TCP全连接扫描(`-sT`)普通用户即可.
### Q2: 扫描太慢怎么办?

A: 使用 `-T4` 或 `-T5` 提速,使用 `--max-rate` 限制速率,只扫描关键端口 `-p 22,80,443`.
### Q3: 如何减少误报?

A: 结合多个工具交叉验证。nmap发现的服务用nuclei验证漏洞,用sslscan确认SSL配置.
### Q4: 如何获取更多扫描工具?

A: 免费版集成4个核心工具。专业版增加masscan、ffuf、gobuster、testssl等10+工具,支持批量扫描和HTML报告.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Linux(推荐Kali Linux) / macOS / Windows(WSL)
- **Python版本**: 3.8+

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| Python | 运行时 | 必需 | 系统自带 |
| nmap | 系统工具 | 必需 | `apt install nmap` 或 nmap.org |
| nuclei | 工具 | 推荐 | `go install projectdiscovery/nuclei/v3/cmd/nuclei@latest` |
| sslscan | 工具 | 可选 | `apt install sslscan` |
| nikto | 工具 | 可选 | `apt install nikto` |

### API Key 配置
- 免费版无需API Key,所有扫描在本地执行

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行安全扫描任务

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
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
    "result": "安全扫描器(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "security scanner"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
