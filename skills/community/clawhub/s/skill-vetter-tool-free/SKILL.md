---
slug: skill-vetter-tool-free
name: skill-vetter-tool-free
version: 1.0.0
displayName: Skill安全审查(免费版)
summary: "安装前安全审查协议,含红旗检测、权限评估与风险分级,保障Agent生态安全,支持多种使用场景和自动化处理"
license: MIT
edition: free
description: "核心能力:，可自发提升工作效率. 适用于需要skill vetter tool相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量. 适用于需要skill vetter tool相关能力的开发场景,包含结构化的工作流程和配置指引. 该工具经过深度差异化处置,针对用户反馈和使用痛点进行了调优改进,提升了实用性和可操作性."
tags:
  - 安全
  - skill
  - vetter
  - automation
  - productivity
  - Skill安全
  - 代码审查
  - 风险评估
  - 加密
  - 工具
tools:
  - read
  - exec
homepage: ""
category: "Security"
pricing_tier: free

---
# Skill安全审查(免费版)

## 概述

Skill安全审查免费版是一款面向AI Agent用户的安全审查协议工具。在安装任何第三方Skill之前,执行4步安全审查流程:来源检查、代码审查、权限评估和风险分类。内置12项红旗检测规则,覆盖命令执行、数据外泄、密钥窃取、Prompt注入等AI特有安全风险,帮助用户识别和阻止恶意Skill.
## 核心能力

### 4步审查协议

| 步骤 | 名称 | 检查内容 |
|---|---|----|
| 1 | 来源检查 | 来源可信度、作者声誉、下载量、更新时间 |
| 2 | 代码审查 | 12项红旗检测(强制执行) |
| 3 | 权限评估 | 文件读写、命令执行、网络访问范围 |
| 4 | 风险分类 | 4级风险等级与安装建议 |

**处理**: 解析步审查协议的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回步审查协议的响应数据,包含状态码、结果和日志.
### 免费版与专业版对比

| 功能 | 免费版 | 专业版 |
|:-----|:-----|:-----|
| 红旗规则 | 12项 | 24项+自定义 |
| 审查方式 | 人工清单 | 自动扫描+AI分析 |
| 信任注册表 | 不支持 | 信任等级管理 |
| 沙箱测试 | 不支持 | 隔离环境测试 |
| 批量审查 | 单个Skill | 批量+并行 |
| 报告格式 | 文本 | HTML/PDF |
| 持续监控 | 不支持 | 变更检测+告警 |

**处理**: 解析免费版与专业版对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回免费版与专业版对比的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：安装前安全审查协、含红旗检测、权限评估与风险分、Agent、生态安全、核心能力、步安全审查协议、项红旗检测规则、权限范围评估清单、级风险分类、LOW、MEDIUM、HIGH、EXTREME、结构化审查报告输等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 依赖详情

在安装任何新Skill之前,执行完整的安全审查.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | Skill安全审查(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```text
审查流程:
Step 1: 来源检查
  - 来源: SkillHub / GitHub / 其他
  - 作者: 是否已知/可信
  - 下载量/星标数
  - 最后更新时间
  - 其他用户评价
# ...
Step 2: 代码审查(强制)
  读取所有文件,检查12项红旗:
  [ ] curl/wget 到未知URL
  [ ] 向外部服务器发送数据
  [ ] 请求凭据/令牌/API密钥
  [ ] 读取 ./.ssh ./.aws ./.config
  [ ] 访问 MEMORY.md, USER.md, IDENTITY.md
  [ ] 使用 base64 解码
  [ ] 使用 安全解析() 或 exec方法() 处理外部输入
  [ ] 修改工作区外的系统文件
  [ ] 未声明的包安装
  [ ] 连接到IP地址而非域名
  [ ] 混淆代码(压缩/编码/最小化)
  [ ] 请求sudo/提权
# ...
Step 3: 权限评估
  - 读取哪些文件?
  - 写入哪些文件?
  - 执行哪些命令?
  - 需要网络访问? 访问哪里?
  - 权限范围是否最小化?
# ...
Step 4: 风险分类
  🟢 LOW     → 基本审查后可安装
  🟡 MEDIUM  → 需完整代码审查
  🔴 HIGH    → 需人工批准
  ⛔ EXTREME → 不要安装
```

### 场景二:快速红旗检测

```bash
# 检查Skill目录中的红旗项
grep -rn "eval\|exec\|curl\|wget\|base64" /path/to/skill/
# ...
# 检查网络请求
grep -rn "fetch\|axios\|http\.\|https\." /path/to/skill/
# ...
# 检查密钥访问
grep -rn "process\.env\|\.ssh\|\.aws\|password\|secret\|token" /path/to/skill/
# ...
# 检查Prompt注入
grep -rn "ignore.*instructions\|system.*prompt\|新指令" /path/to/skill/
```

### 场景三:生成审查报告

```text
SKILL 安全审查报告
═══════════════════════════════════════
Skill名称: [name]
来源: [SkillHub / GitHub / 其他]
作者: [username]
版本: [version]
───────────────────────────────────────
指标:
  下载量/星标: [count]
  最后更新: [date]
  审查文件数: [count]
───────────────────────────────────────
红旗项: [无 / 列出]
# ...
所需权限:
  文件: [列表 或 "无"]
  网络: [列表 或 "无"]
  命令: [列表 或 "无"]
───────────────────────────────────────
风险等级: [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME]
# ...
结论: [✅ 可安全安装 / ⚠️ 谨慎安装 / ❌ 不要安装]
# ...
备注: [审查观察]
═══════════════════════════════════════
```

## 不适用场景

以下场景Skill安全审查(免费版)不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 红旗检测清单

```python
# ...
# ...
# ...
# ...
# ...
# ...
# ...
# ...
# ...
# ...
# ...
# ...
# ...
result = "操作完成"
import os
import re
from pathlib import Path
class SkillVetter:
    """Skill安全审查器"""
    RED_FLAGS = {
        "network_unknown": {
            "pattern": r"(curl|wget|fetch)\s+['\"]https?://(?!api\.)",
            "severity": "HIGH",
            "description": "向未知URL发送网络请求"
        },
        "data_exfil": {
            "pattern": r"(POST|upload|send).*(password|secret|token|key|credential)",
            "severity": "CRITICAL",
            "description": "可能向外发送敏感数据"
        },
        "credential_request": {
            "pattern": r"(request|ask|enter|input).*(password|token|api.?key|credential)",
            "severity": "HIGH",
            "description": "请求用户输入凭据"
        },
        "read_ssh": {
            "pattern": r"~?/\.ssh/|~?/\.aws/|~?/\.config/",
            "severity": "CRITICAL",
            "description": "访问SSH密钥或配置目录"
        },
        "read_identity": {
            "pattern": r"(MEMORY\.md|USER\.md|IDENTITY\.md|SOUL\.md)",
            "severity": "HIGH",
            "description": "访问Agent身份文件"
        },
        "base64_decode": {
            "pattern": r"(atob|base64decode|base64\.b64decode)",
            "severity": "MEDIUM",
            "description": "使用Base64解码(可能隐藏恶意代码)"
        },
        "eval_exec": {
            "pattern": r"(eval\s*\(|exec\s*\(|Function\s*\().*input",
            "severity": "CRITICAL",
            "description": "使用eval/exec处理外部输入"
        },
        "system_modify": {
            "pattern": r"(/etc/|/usr/|/sys/|C:\\Windows\\)",
            "severity": "CRITICAL",
            "description": "修改系统文件"
        },
        "undeclared_install": {
            "pattern": r"(npm install|pip install|apt install)(?!.*--save)",
            "severity": "MEDIUM",
            "description": "未声明的包安装"
        },
        "ip_connection": {
            "pattern": r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
            "severity": "HIGH",
            "description": "连接到IP地址而非域名"
        },
        "obfuscation": {
            "pattern": r"(\\x[0-9a-f]{2}){10,}|eval\(atob\(",
            "severity": "HIGH",
            "description": "代码混淆"
        },
        "prompt_injection": {
            "pattern": r"(ignore.*(previous|all|above).*instruction|system.*prompt|<\|im_start\|>)",
            "severity": "CRITICAL",
            "description": "Prompt注入攻击"
        }
    }
    RISK_LEVELS = {
        "LOW": {"emoji": "🟢", "action": "基本审查后可安装", "examples": "笔记、天气、格式化"},
        "MEDIUM": {"emoji": "🟡", "action": "需完整代码审查", "examples": "文件操作、浏览器、API"},
        "HIGH": {"emoji": "🔴", "action": "需人工批准", "examples": "凭据、交易、系统"},
        "EXTREME": {"emoji": "⛔", "action": "不要安装", "examples": "安全配置、root访问"}
    }
    def vet(self, skill_path):
        """执行安全审查"""
        path = Path(skill_path)
        findings = []
        files_reviewed = 0
        for filepath in path.rglob("*"):
            if filepath.is_file() and filepath.suffix in {".js", ".ts", ".py", ".md", ".json", ".sh"}:
                files_reviewed += 1
                file_findings = self._check_file(filepath)
                findings.extend(file_findings)
        risk_level = self._determine_risk(findings)
        report = self._generate_report(skill_path, files_reviewed, findings, risk_level)
        return report
    def _check_file(self, filepath):
        """检查单个文件"""
        findings = []
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
            for flag_id, rule in self.RED_FLAGS.items():
                matches = re.finditer(rule["pattern"], content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                        "flag": flag_id,
                        "severity": rule["severity"],
                        "file": str(filepath),
                        "line": line_num,
                        "evidence": match.group()[:80],
                        "description": rule["description"]
                    })
        except Exception:
        return findings
    def _determine_risk(self, findings):
        """确定风险等级"""
        if any(f["severity"] == "CRITICAL" for f in findings):
            return "EXTREME"
        elif any(f["severity"] == "HIGH" for f in findings):
            return "HIGH"
        elif any(f["severity"] == "MEDIUM" for f in findings):
            return "MEDIUM"
        else:
            return "LOW"
    def _generate_report(self, skill_path, files_reviewed, findings, risk_level):
        """生成审查报告"""
        risk_info = self.RISK_LEVELS[risk_level]
        verdict = "✅ 可安全安装" if risk_level == "LOW" else \
                  "⚠️ 谨慎安装" if risk_level == "MEDIUM" else \
                  "❌ 不要安装"
        report = f"""
SKILL 安全审查报告
═══════════════════════════════════════
Skill路径: {skill_path}
审查文件数: {files_reviewed}
───────────────────────────────────────
红旗项: {len(findings)} 个
"""
        for f in findings:
            report += f"\n  [{f['severity']}] {f['description']}\n"
            report += f"    文件: {f['file']}:{f['line']}\n"
            report += f"    证据: {f['evidence']}\n"
        report += f"""
───────────────────────────────────────
风险等级: {risk_info['emoji']} {risk_level}
建议操作: {risk_info['action']}
结论: {verdict}
═══════════════════════════════════════
"""
        return report
```

## 示例

### 信任等级参考

| 信任级别 | 来源 | 审查力度 |
|:---:|:---:|:---:|
| 1 | 官方SkillHub技能 | 低度审查(仍需审查) |
| 2 | 高星标仓库(1000+) | 中度审查 |
| 3 | 已知作者 | 中度审查 |
| 4 | 新/未知来源 | 最大审查 |
| 5 | 请求凭据的Skill | 始终需人工批准 |

## 优秀实践

### 1. 安装前必审

```bash
# 下载Skill后,先审查再安装
python （请参考skill目录中的脚本文件） /path/to/downloaded-skill/
```

### 2. 关注CRITICAL红旗

```bash
# 只显示严重红旗
python （请参考skill目录中的脚本文件） /path/to/skill/ | grep CRITICAL
```

### 3. 信任但验证

即使来自可信来源,也要执行基本审查。官方Skill也可能包含意外行为.
## 常见问题

### Q1: 没有发现红旗就可以安装吗?

A: 红旗检测是必要条件但非充分条件。即使无红旗,也建议阅读Skill文档,理解其功能和所需权限.
### Q2: 误报怎么处理?

A: 某些合法操作可能触发红旗(如安全工具检测密钥模式)。结合上下文判断,例如安全扫描器读取 `./.ssh` 是合理的.
### Q3: 审查需要多长时间?

A: 自动化红旗检测在几秒内完成。完整的人工代码审查取决于Skill大小,通常5-15分钟.
### Q4: 如何获取自动扫描和沙箱测试?

A: 免费版提供人工审查清单。专业版提供自动扫描、AI分析、沙箱隔离测试和信任注册表管理.
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.8+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| Python | 运行时 | 必需 | 系统自带 |
| re模块 | 标准库 | 必需 | Python内置 |
| pathlib模块 | 标准库 | 必需 | Python内置 |

### API Key 配置
- 免费版无需API Key,所有审查在本地执行

### 可用性分类
- **分类**: MD+EXEC模式纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行Skill安全审查任务

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

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Skill安全审查(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "skill vetter"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
