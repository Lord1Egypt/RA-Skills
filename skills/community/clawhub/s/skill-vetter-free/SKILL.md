---
slug: "skill-vetter-free"
name: "skill-vetter-free"
version: 1.0.1
displayName: "技能免费版"
summary: "基础版 AI Agent 技能审查工具，执行来源检查和 RED FLAGS 检测。。skill-vetter-free 是安全优先的 AI Agent 技能审查工具基础版。在安装技能前执行来"
summary_zh: "基础版 AI Agent 技能审查工具，执行来源检查和 RED FLAGS 检测。。skill-vetter-free 是安全优先的 AI Agent 技能审查工具基础版。在安装技能前执行来"
license: "MIT"
description: "|-. 适用于需要skill vetter相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  skill-vetter-free 是安全优先的 AI Agent 技能审查工具基础版。在安装技能前执行来源检查和
  RED FLAGS 代码审查，输出基础审查报告。不包含 GitHub API 快速审查命令、权限范围评估、
  信任层级评估和 4 级风险分级。适合快速安全筛查，升级完整版获取全量审查协议.
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 通用办公
  - skill
  - vetter
  - automation
  - productivity
  - 工具
  - 效率
  - github
  - red
  - key
category: "Automation"
pricing_tier: free
---
# Skill Vetter Free

skill-vetter-free 是安全优先的 AI Agent 技能审查工具基础版。**永远不要在未审查前安装任何技能。**

## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Skill Vetter Free处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

### 1. 来源检查（Source Check）
验证技能来源的可靠性。回答 5 个关键问题：技能从哪里来（SkillHub / GitHub / 其他）？
作者是否知名/可信？下载量/星标数是多少？最后更新时间？是否有其他 Agent 的评价？
基础版支持手动来源验证，不包含 GitHub API 自动查询命令.

- 参考`来源检查（Source Check）`的配置文档进行参数调优
### 2. 强制代码审查（Code Review - MANDATORY）
读取技能中的所有文件，逐一检查 RED FLAGS 清单。发现以下任何一项立即拒绝安装：
`curl`/`wget` 到未知 URL；向外部服务器发送数据；请求凭证/令牌/API Key；
读取 `./.ssh`、`./.aws`、`./.config` 路径而无明确理由；访问 `MEMORY.md`、`USER.md`、
`SOUL.md`、`IDENTITY.md` 等身份文件；使用 `安全解析()` 或 `exec方法()` 处理外部输入；
修改工作区外的系统文件；向 IP 地址而非域名发起网络调用；使用混淆代码.
### 3. 基础审查报告生成
生成基础审查报告，包含：技能名称、来源、作者、版本；RED FLAGS 列表（None 或具体列表）；
基础安装建议（SAFE TO INSTALL / DO NOT INSTALL）。基础版不包含风险分级（LOW/MEDIUM/HIGH/EXTREME）
和权限需求详细分析。- 验证返回数据的完整性和格式正确性
- 参考`基础审查报告生成`的配置文档进行参数调优
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

1. 确认技能来源（SkillHub / GitHub / 其他），记录作者和版本
2. 手动查询下载量、星标数和最后更新时间
3. 读取技能中的所有文件，逐一检查 RED FLAGS 清单
4. 生成基础审查报告，输出 RED FLAGS 和安装建议
5. 存在 RED FLAGS 的技能拒绝安装

#
## 示例

### 示例1：技能基础审查

```text
SKILL VETTING REPORT (BASIC)
═══════════════════════════════════════
Skill: my-skill
Source: GitHub (example/skill-repo)
Author: example-user
Version: 1.2.0
───────────────────────────────────────
RED FLAGS:
• （请参考skill目录中的脚本文件）: curl to unknown URL
• （请参考skill目录中的脚本文件）: Network call to IP instead of domain
• （请参考skill目录中的脚本文件）: Reads ./.config without clear reason
# ...
VERDICT: DO NOT INSTALL
# ...
NOTES: install.sh 向未知 IP 发起网络请求，且访问 ./.config 无明确理由.
═══════════════════════════════════════
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| `curl`/`wget` 到未知 URL | 技能尝试从不受信任的源下载数据 | 立即标记为 RED FLAG，拒绝安装 |
| 请求凭证/令牌/API Key | 技能要求用户提供敏感凭证 | 标记为 RED FLAG，拒绝安装 |
| 读取 `./.ssh`/`./.aws`/`./.config` | 技能访问敏感系统路径 | 检查是否有明确理由；无理由则拒绝安装 |
| 访问 `MEMORY.md`/`USER.md`/`SOUL.md`/`IDENTITY.md` | 技能触及 Agent 身份文件 | 立即拒绝安装 |
| 使用 `安全解析()`/`exec方法()` 处理外部输入 | 代码注入风险 | 标记为 RED FLAG，拒绝安装 |

## 常见问题

### Q1: 免费版支持 GitHub API 快速查询吗？
A: 免费版不包含 GitHub API 快速审查命令。需要手动访问 GitHub 页面查看星标数、最后更新时间
等信息。完整版支持 `curl -s "https://api.相关技术文档 自动查询仓库元数据.
### Q2: 免费版的风险分级有哪几个级别？
A: 免费版仅输出两种安装建议：SAFE TO INSTALL 和 DO NOT INSTALL。完整版支持 4 级风险分级
（LOW/MEDIUM/HIGH/EXTREME），并根据级别决定是否需要人工批准.
### Q3: 免费版包含权限范围评估吗？
A: 免费版不包含权限范围评估。完整版支持评估文件读写、命令执行、网络访问的最小权限需求，
并标记超出功能需求的权限请求为风险信号.
### Q4: 免费版支持信任层级评估吗？
A: 免费版不包含 5 级信任层级评估。完整版根据来源（官方技能、高星标仓库 1000+、已知作者、
新/未知来源、请求凭证的技能）应用差异化审查深度.
### Q5: 如何升级到完整版？
A: 将技能替换为完整版 skill-vetter 即可。完整版包含 6 项核心能力、GitHub API 快速审查命令、
4 级风险分级、权限范围评估、5 级信任层级和结构化审查报告.
## 已知限制

- 不包含 GitHub API 自动查询命令，需手动查看仓库信息
- 不包含 4 级风险分级（LOW/MEDIUM/HIGH/EXTREME），仅输出二值安装建议
- 不包含权限范围评估和最小权限分析
- 不包含 5 级信任层级差异化审查
- 不包含结构化审查报告的完整字段（指标、权限需求、附注）

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "Skill Vetter Free处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "skill-vetter"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
