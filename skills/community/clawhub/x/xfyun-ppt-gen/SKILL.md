---
name: ppt-generator
description: Generate professional, structured PowerPoint presentations from optimized topic keywords.
homepage: https://www.xfyun.cn/doc/spark/PPTv2.html
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": {
          "bins": ["python"],
          "env": ["XF_PPT_APP_ID", "XF_PPT_API_SECRET"]
        },
        "primaryEnv": "XF_PPT_APP_ID"
      }
  }
---

# 📊 PPT Generator

Generate a complete, logically structured, and presentation-ready PowerPoint deck from a professionally optimized topic phrase.

Designed for business, technical, and training scenarios.

---

## ✨ Features

- Automatic slide outline generation  
- Clear logical hierarchy  
- Business-ready formatting  
- One-command execution  
- Deterministic single-output generation  

---

## 🚀 Usage

```bash
python {baseDir}/scripts/index.py generate_ppt "<optimized-topic>"
```

Example:

```
python {baseDir}/scripts/index.py generate_ppt "Artificial Intelligence Industry Trends"
```

## 🧠 Input Specification (Strict Contract)

Before invoking the skill, the topic must undergo **semantic compression optimization**.

### Final Topic Requirements

- 5–10 words
- Formal report-style title
- Clear and domain-specific
- No conversational language
- Not a full sentence

------

### Input Optimization Examples

| Raw User Request                    | Optimized Topic  |
| ----------------------------------- | ---------------- |
| 帮我做一个关于人工智能发展现状的PPT | 人工智能发展现状 |
| 我要介绍一下公司今年的技术规划      | 公司年度技术规划 |
| 做一份给新员工的Java培训PPT         | Java新员工培训   |

------

## ⚠ Constraints

- One invocation generates one complete PPT
- Raw user input must NOT be passed directly
- Environment variables must be configured before execution

------

## 🔧 Environment Setup

Required:

- Python available in PATH
- Environment variables configured:

```
export XF_PPT_APP_ID=your_app_id
export XF_PPT_API_SECRET=your_api_secret
```

------

## 📦 Output

- Fully structured PPT file
- Multi-level slide organization
- Presentation-ready content layout
- Business-standard formatting

------

## 🎯 Target Use Cases

- Business reports
- Strategy planning
- Technical presentations
- Internal training materials
- Academic summaries

------

## 🛠 Extensibility

Future enhancements may include:

- Slide count configuration
- Language selection
- Theme customization
- Template switching
- AI-assisted topic compression

------

Built for automation workflows and AI-driven document generation.