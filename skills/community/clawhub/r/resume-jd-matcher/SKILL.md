---
name: resume-jd-matcher
version: 2.0.3
description: 批量解析简历并与岗位 JD 进行 AI 智能匹配，生成结构化匹配报告（Excel）
author: fly
authorEmail: 13416145728@163.com
license: MIT
tags: [hr, resume, jd, matching, excel, ai]
---

# Resume-JD-Matcher

批量解析简历并与岗位 JD 进行 AI 智能匹配，生成结构化匹配报告（Excel）。

## 🎯 功能

- 从 Word (.docx) 文件提取岗位任职要求
- 解析 PDF/Word 格式简历
- AI 智能分析简历与 JD 的匹配度
- 生成 Excel 匹配报告（含分析详情和总体评估表）
- 支持增量处理（跳过已处理的简历）

## 🚀 使用方式

### 方式 1：OpenClaw 消息触发（推荐，Subagent 模式）

在 OpenClaw 中发送消息：

```
帮我匹配 D:\JL 目录下的简历
```

或使用命令：

```
/skill resume-jd-matcher
```

**优势**：
- ✅ 无需配置 API
- ✅ 自动使用你已配置的大模型
- ✅ 支持批量并发处理（默认 3 个并发）
- ✅ 支持自然语言交互

**批量处理流程**：
1. 扫描简历目录（按岗位分类）
2. 为每份简历的每条任职要求创建子 Agent 任务
3. 并发调用多个子 Agent 分析（默认最多 3 个同时运行）
4. 收集所有结果，生成 Excel 报告

**性能参考**：
- 单次分析：~6-8 秒
- 10 份简历 × 5 条要求 = 50 个任务 ≈ 2-3 分钟（并发 3）
- 50 份简历 × 5 条要求 = 250 个任务 ≈ 10-15 分钟（并发 3）

### 方式 2：独立脚本运行（API 模式）

```bash
cd C:\Users\Administrator\.openclaw\workspace
python resume_match.py
```

**适用场景**：批量离线处理、定时任务、无 OpenClaw 环境

## ⚙️ 配置

编辑 `config_resume_match.yaml`：

### 运行模式（必填）

```yaml
# "subagent" - OpenClaw 模式（无需 API 配置）
# "api" - 独立脚本模式（需要配置 API）
mode: "subagent"
```

### 路径配置（必填）

```yaml
paths:
  jd_folder: "D:\\JD"      # JD 文件目录
  jl_folder: "D:\\JL"      # 简历目录（按岗位分类）
  output_folder: "D:\\jg"  # 输出目录
```

### API 配置（仅当 mode="api" 时需要）

```yaml
mode: "api"
api:
  active_provider: tencent
  api_providers:
    tencent:
      name: "腾讯 Hunyuan"
      api_key: "sk_xxxxx"
      api_url: "https://api.hunyuan.tencent.com/v1/chat/completions"
      model: "hunyuan-t1"
```

## 📁 目录结构要求

```
D:\JD\                    # 岗位 JD 目录
├── 投资岗.docx
├── 合规岗.docx
└── ...

D:\JL\                    # 简历目录（按岗位文件夹分类）
├── 投资岗/
│   ├── 张三.pdf
│   └── 李四.docx
├── 合规岗/
│   ├── 王五.pdf
│   └── ...
└── ...

D:\jg\                    # 输出目录（自动生成）
└── AI_Resume_All_20260403_1415.xlsx
```

## 📊 输出格式

### Excel 包含两个工作表：

**1. 简历匹配结果**
| 应聘者名称 | 应聘岗位 | 任职要求 | 匹配度 | AI 分析详情 | 处理时间 |
|-----------|---------|---------|-------|-----------|---------|
| 张三 | 投资岗 | 3 年以上投资经验... | 完全匹配 | {"分析": "..."} | 2026-04-03 14:15 |

**2. 应聘者总体评估表**
| 应聘岗位 | 应聘者名称 | 得分 |
|---------|-----------|-----|
| 投资岗 | 张三 | 95.00 |
| 投资岗 | 李四 | 87.50 |

### 匹配等级

- 完全匹配
- 高度匹配
- 匹配
- 部分匹配
- 不匹配
- 无相关信息

## 🔧 高级配置

### 批量性能优化

对于大量简历（50+ 份），建议：

```yaml
# 子 Agent 模式超时时间（秒）
timeout: 60

# 并发限制（未来版本支持）
max_concurrent: 3
```

### 日志配置

日志自动输出到：
- 控制台（实时显示）
- `D:\jg\resume_match_YYYYMMDD_HHMM.log`

## 🆚 模式对比

| 特性 | subagent 模式 | api 模式 |
|------|-------------|---------|
| **配置** | 无需 | 需 API Key |
| **执行环境** | OpenClaw | 任意 Python 环境 |
| **单次耗时** | ~6 秒 | ~2 秒 |
| **批量 50 份** | ~5-10 分钟 | ~2-3 分钟 |
| **费用** | OpenClaw 配额 | API 供应商收费 |
| **适用场景** | OpenClaw 用户 | 独立脚本/定时任务 |

## 📝 版本历史

- **V2.0.0** (2026-04-03) - 双模式架构重构
- **V1.9.6** (2026-03-20) - 修复 AI 返回语言
- **V1.9.4** (2026-03-16) - 新增多 API 供应商切换

## 🐛 常见问题

### Q: subagent 模式报错 "session_spawn not found"
A: 确保在 OpenClaw 环境中运行，检查 `sessions_spawn` 工具是否可用。

### Q: API 模式报错 "No module named 'fitz'"
A: 安装依赖：`pip install PyMuPDF python-docx openpyxl pyyaml requests pdfplumber`

### Q: 如何处理扫描件简历？
A: 当前版本仅支持文本型 PDF/Word，扫描件需要 OCR 支持（未来版本）。

## 📦 依赖

```txt
openpyxl>=3.0.0
requests>=2.28.0
python-docx>=0.8.0
pyyaml>=6.0.0
pdfplumber>=0.11.0
```

## 📄 License

MIT
