---
name: robust-text-auditor
description: (已验证) 高可靠性文本审核器，结合本地规则、百度 API 和 AI 深度分析，提供三层合规性审查。
metadata:
  version: 1.0.0
  source: https://github.com/your-repo/robust-text-auditor
  author: an
  tags: [text-auditing, compliance, baidu-api, nlp, security]
  license: MIT
  requirements:
    - python
    - "pip:requests"
---

# SKILL.md for robust-text-auditor

## Description

这是一个高可靠性的组合技能，它通过一个统一的 `run.ps1` 脚本，将**本地规则扫描**、**百度 API 机审**和**AI 模型深度分析**三层审核步骤，封装成一个单一、可靠的原子操作。

AI 助手只需调用此脚本并提供待审核的文本，即可获得一份包含三层审核结果的、完整的、最终的合规性报告提示词，再应用提示词实现报告输出。这个设计确保了审核流程的完整性、专业性和结果的绝对可靠性。

## ⚠️ Prerequisites (前置条件)

**在使用本技能前，您必须在主配置文件 `~/.openclaw/config.json` 中添加您的百度云 API 凭证：**

```json
{
  "baidu_api_key": "YOUR_BAIDU_API_KEY",
  "baidu_secret_key": "YOUR_BAIDU_SECRET_KEY"
}
```

## How to Use

该技能的核心是 `run.ps1` 脚本，它负责调度所有内部子脚本。

### Parameters

*   **`-InputFile <path>`**: 待审核的文本文件的路径。
*   **`-TextToAudit <string>`**: 待审核的短文本字符串。

*注意：`-InputFile` 和 `-TextToAudit` 两个参数必须提供一个。*

### Example Invocation

**通过文件进行审核:**
```powershell
# AI 应动态查找此技能的路径
path/to/run.ps1 -InputFile "C:\path\to\your\file.txt"
```

**通过字符串进行审核:**
```powershell
# AI 应动态查找此技能的路径
path/to/run.ps1 -TextToAudit "这是一段需要进行合规性审核的文本内容。"
```

## Output

该技能执行成功后，会在技能目录的根路径下生成一个 `final_prompt.txt` 文件。这个文件是一个包含了所有审核层级结果的、可以直接使用的大语言模型提示词。

AI 代理应读取该文件的内容，并将其作为输入提交给大语言模型，即可生成最终的、详尽的审核报告。
