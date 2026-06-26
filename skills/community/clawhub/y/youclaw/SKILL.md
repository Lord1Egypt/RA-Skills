---
name: youclaw
description: 有米云智能营销分析助手，深度拆解广告创意，挖掘品牌投放策略，支持创意策略讨论、营销策略探讨。触发：关键词 分析品牌, 品牌分析, 策略探索, 投放策略, 创意质询, 压力测试, 创意激发, 创意打磨；命令 /youclaw、/youmiyun、/creative-chat、/grill-chat、/grill-youclaw、/grill
homepage: https://www.youcloud.com
metadata:
  {
    "openclaw": {
      "slug": "youclaw",
      "version": "1.2.1",
      "author": "youcloud",
      "emoji": "📊",
      "requires": {
        "env": ["YOUCLOUD_API_KEY"]
      }
    }
  }
---

# youclaw

有米云智能营销分析助手，对接有数AI API，可深度拆解广告创意、挖掘品牌投放策略，也可针对广告创意进行深度质询与压力测试，激发符合算法逻辑的优质创意。

## 权限说明
仅对有米有数 **策略版**、**策略 pro 版**和**至尊版**用户开放。获取API Key方式：登录有数 → 个人中心 → 企业信息。

## 触发方式
- 关键词：分析品牌、品牌分析、策略探索、投放策略、创意质询、压力测试、创意激发、创意打磨
- 命令：
  - `/youclaw`、`/youmiyun` → 调用Skill，自动判断模式
  - `/creative-chat` → 强制走策略探索模式
  - `/grill-chat`、`/grill-youclaw`、`/grill` → 强制走灵感激发模式

## 执行流程
1. **检查API Key**（从环境变量读取）：
   - 读取环境变量 `YOUCLOUD_API_KEY`：
     - 有值 → 继续
     - 为空 → 提示用户配置：
       ```
       请先配置API Key：
       1. 登录有数 → 个人中心 → 企业信息 获取API Key
       2. 设置为环境变量 YOUCLOUD_API_KEY，例如：
          - Linux/macOS: export YOUCLOUD_API_KEY="your-key-here"
          - Windows: $env:YOUCLOUD_API_KEY="your-key-here"
          - 或写入 ~/.bashrc / ~/.zshrc 永久生效
       3. 配置完成后重新发送请求即可。
       ```
   - ✅ 规则：**没有有效 API Key，绝不发送请求**

2. **⚠️ 强制红线规则（公共Skill必须严格遵守）**
   - API 请求超时为 **600秒**
   - **🔴 绝对禁止：未到超时时间不得中断请求，不得提前给用户发送任何「正在处理」「需要等待」「结果出来后告诉你」这类消息**
   - **必须：一直等待API返回结果，拿到完整结果后再一次性回复给用户**
   - 只有两种情况允许发消息：
     1. API返回了完整分析结果 → 直接输出结果
     2. API超时/请求报错 → 输出错误提示

3. **确定chat_mode：**
   - **强制模式（命令触发优先）：**
     - `/creative-chat` → 强制 **策略探索模式（chat_mode=2）** → 直接输出完整分析报告
     - `/grill-chat`、`/grill-youclaw`、`/grill` → 强制 **灵感激发模式（chat_mode=5）** → 渐进式追问深度打磨
   - **自动判断（关键词/内容触发）：**
     - **规则一（关键词优先）：** 用户输入包含「打磨、讨论、探讨、质询、压力测试、创意激发、深入聊聊」→ 走**灵感激发模式（chat_mode=5）**
     - **规则二（内容判断）：**
       - 内容简短（仅给出产品/品牌，没有明确说要讨论）→ 默认走**策略探索模式（chat_mode=2）** → 直接输出完整报告
       - 内容已经具体，用户明确问"怎么改进、如何做、帮我看看、一起聊聊" → 走**灵感激发模式（chat_mode=5）**
   - **总结：** 命令可以强制指定模式，没有命令则自动判断；默认出完整方案，明确要讨论才进入渐进追问
   - 调用API，响应返回后直接展示结果。

4. **跟进处理**：
   - 相关跟进提问（关于之前的分析/创意打磨） → 复用之前的`session_id`，**不传`chat_mode`**（沿用会话已有模式）
   - 新的分析/创意请求 → 开启新会话，不携带`session_id`，传`chat_mode`

## API Specification
- URL: `https://aichat.youshu.youcloud.com/aichat/claw`
- Method: POST JSON
- Headers: `Authorization: Bearer {KEY}`, `Content-Type: application/json`
- Parameters:
  - `input`: User question (required)
  - `session_id`: For follow-up questions, omit for new conversations
  - `chat_mode`: Chat mode, 2=策略探索（直接出完整报告），5=灵感激发（渐进式质询打磨）。**仅新对话（无session_id时）需要传，连续对话不传，沿用会话已有模式**
- Response: Output `output` (markdown) **as-is, DO NOT modify**; save `session_id` for future follow-ups
- Timeout: ≥600s

## PowerShell 调用模板
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$apiKey = $env:YOUCLOUD_API_KEY
$body = @{input="Your analysis request"; chat_mode=2} | ConvertTo-Json -Compress
$params = @{
  Uri = "https://aichat.youshu.youcloud.com/aichat/claw"
  Method = "Post"
  ContentType = "application/json; charset=utf-8"
  Headers = @{Authorization="Bearer $apiKey"}
  Body = $body
  TimeoutSec = 600
}
Invoke-RestMethod @params | Select-Object -ExpandProperty output
```

## 错误处理
- 401/认证失败：
  ```
  API Key 认证失败，请检查密钥是否激活/过期？请在个人中心-企业信息 获取Api Key，或向售后人员咨询。
  ```
- 超时："还在分析中，稍后再问我结果或者再次请求。"
- 其他错误："请求返回错误 (code={code})，请检查API Key权限、账号配额或联系客服"

## 示例
完整输入输出示例请看 [references/example.md](references/example.md)
