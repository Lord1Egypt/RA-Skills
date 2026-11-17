---
slug: "pyx-scan-free"
name: "pyx-scan-free"
version: "1.0.0"
displayName: "技能安全扫描(免费版)"
summary: "AI技能安全检查工具，,提供核心能力"
summary_zh: "AI技能安全检查工具，,提供核心能力"
license: "MIT"
description: "|- AI技能安全检查工具，通过Scanner API对技能进行安全评级和风险报告。评估维度 包括恶意指令、数据泄露、权限滥用、供应链风险等。返回信任评分（0-10）、 风险评分（0-10）和置信度百分比。兼容WebFetch和curl两种调用方式。适用于 独立开发者、企业团队和自发化工作流场景。不适用于非AI技能的安全扫描."
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 通用办公
  - 工具
  - 效率
  - 安全
  - owner
  - scanner
  - confidence
  - trust_score
category: "Automation"
pricing_tier: free
---
# 技能安全扫描(免费版)

通过Scanner API对AI技能进行安全评级和风险报告.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 技能安全扫描(免费版)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 核心能力

### 1. 技能安全检查
对指定技能进行安全扫描，评估潜在风险。通过 `https://scanner.pyxmate.com/api/v1/check/` 端点调用，需要提供技能所有者和名称。- 验证返回数据的完整性和格式正确性
- 参考`技能安全检查`的配置文档进行参数调优
### 2. 信任评分
返回 `trust_score`（0-10），分数越高表示技能越可信。10分为最高信任，0分为最低信任.

### 3. 风险评分
返回 `risk_score`（0-10），分数越高表示风险越大。0分为无风险，10分为极高风险.

### 4. 置信度评估
返回 `confidence` 百分比（0-100%），表示评估结果的可信程度。100%为最高置信度.

### 输出格式

完成响应以Markdown格式返回,包含任务状态(成功/失败)、解析摘要和具体输出数据。失败时返回错误码和错误信息,便于定位问题。- 验证返回数据的完整性和格式正确性
- 参考`输出格式`的配置文档进行参数调优
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|:-----|:-----|:-----|
| 单技能安全扫描 | owner/name | 信任评分+风险评分+风险报告 |
| 批量安全扫描 | 多个owner/name | 汇总扫描结果 |

## 使用流程

1. 确认技能信息:owner(所有者)和name(名称),格式为 `owner/name`
2. 调用Scanner API:WebFetch或curl方式
3. 解析结果:根据 `trust_score`、`risk_score` 和 `confidence` 生成评估报告

#
## 示例

### 示例:扫描单个技能

```bash
curl -s "https://scanner.pyxmate.com/api/v1/check/acme-corp/data-processor"
```

输出：
```json
{
  "owner": "acme-corp",
  "name": "data-processor",
  "trust_score": 8.5,
  "risk_score": 2.0,
  "confidence": 92,
  "issues": [
    {
      "severity": "low",
      "type": "data_access",
      "description": "技能请求文件系统读取权限，但范围有限"
    }
  ],
  "scanned_at": "2026-07-21T10:30:00Z"
}
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 技能不存在 | owner/name拼写错误或未注册 | 确认技能名称格式为 `owner/name`，检查拼写 |
| 速率限制 | 短时间内请求过多 | 等待60秒后检查网络连接和配置后重试，批量扫描时增加间隔 |
| 服务器错误 | Scanner服务端异常 | 等待5分钟后检查网络连接和配置后重试，或联系服务管理员 |
| 网络连接失败 | 网络不可达或DNS解析失败 | 检查网络连接和配置后重试，尝试更换DNS |

## 常见问题

### Q1: trust_score和risk_score的关系是什么？
A: `trust_score`（0-10）表示技能可信度，越高越好。`risk_score`（0-10）表示风险等级，越低越好。两者不一定互补——一个技能可能信任度高但仍有已知风险。建议综合参考两者和 `confidence` 值.
### Q2: confidence低于多少不可信？
A: `confidence` 低于50%时结果仅供参考，建议手动审查。低于30%时几乎不可信，可能是技能信息不足或分析样本有限导致.
### Q3: 支持哪些类型的技能扫描？
A: 支持已注册到Scanner平台的AI技能。技能需要以 `owner/name` 格式提供。未注册的技能返回404.
## 已知限制

- 仅支持已注册到Scanner平台的AI技能
- 技能名称格式必须为 `owner/name`
- 有API速率限制，429时需等待60秒重试

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
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
## 升级提示

本免费版提供基础功能。升级到完整版 pyx-scan 获取全部能力和高级特性.