# 简历与 JD 智能匹配系统

> 批量解析简历并与岗位 JD 进行 AI 智能匹配，生成结构化匹配报告（Excel）

**作者**: fly  
**版本**: 2.0.3  
**许可**: MIT License  
**联系邮箱**: 13416145728@163.com  

---

## 🎯 功能特性

- ✅ 支持 PDF/Word 格式简历解析
- ✅ 自动匹配岗位 JD 与简历
- ✅ AI 智能分析匹配度（6 个等级）
- ✅ 生成 Excel 匹配报告（含分析详情）
- ✅ 自动生成应聘者总体评估表
- ✅ 支持增量处理（跳过已处理简历）
- ✅ 双模式支持（OpenClaw / 独立脚本）

## 🚀 快速开始

### 方式 1：OpenClaw 中使用（推荐）

1. **确保模式配置为 subagent**

```yaml
# config_resume_match.yaml
mode: "subagent"
```

2. **发送消息触发**

```
帮我匹配 D:\JL 目录下的简历
```

3. **等待完成**

程序会自动处理所有简历，输出到 `D:\jg\AI_Resume_All_YYYYMMDD_HHMM.xlsx`

### 方式 2：独立脚本运行

1. **安装依赖**

```bash
pip install openpyxl requests python-docx pyyaml pdfplumber
```

2. **配置 API**

```yaml
# config_resume_match.yaml
mode: "api"
api:
  active_provider: tencent
  api_providers:
    tencent:
      api_key: "sk_xxxxx"
      api_url: "https://..."
```

3. **运行程序**

```bash
cd C:\Users\Administrator\.openclaw\workspace
python resume_match.py
```

## 📁 目录结构

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
├── AI_Resume_All_20260403_1415.xlsx
└── resume_match_20260403_1415.log
```

## 📊 输出示例

### 简历匹配结果

| 应聘者名称 | 应聘岗位 | 任职要求 | 匹配度 | AI 分析详情 | 处理时间 |
|-----------|---------|---------|-------|-----------|---------|
| 张三 | 投资岗 | 3 年以上投资经验... | 完全匹配 | 候选人具备... | 2026-04-03 14:15 |
| 李四 | 投资岗 | 3 年以上投资经验... | 高度匹配 | 候选人具备... | 2026-04-03 14:16 |

### 应聘者总体评估表

| 应聘岗位 | 应聘者名称 | 得分 |
|---------|-----------|-----|
| 投资岗 | 张三 | 95.00 |
| 投资岗 | 李四 | 87.50 |

## ⚙️ 配置说明

### 运行模式

```yaml
mode: "subagent"  # OpenClaw 模式（无需 API）
# 或
mode: "api"       # 独立脚本模式（需 API Key）
```

### 路径配置

```yaml
paths:
  jd_folder: "D:\\JD"      # JD 文件目录
  jl_folder: "D:\\JL"      # 简历目录
  output_folder: "D:\\jg"  # 输出目录
```

## 🔧 高级功能

### 增量处理

程序会自动检测已处理的简历，跳过重复处理。

如需重新处理，删除输出目录中的 Excel 文件即可。

### 日志查看

日志文件位于输出目录：
```
D:\jg\resume_match_YYYYMMDD_HHMM.log
```

包含详细的处理过程、AI 分析结果、错误信息等。

## 🆚 模式对比

| 特性 | subagent 模式 | api 模式 |
|------|-------------|---------|
| 配置 | 无需 | 需 API Key |
| 执行环境 | OpenClaw | 任意 Python |
| 单次耗时 | ~6 秒 | ~2 秒 |
| 批量 50 份 | ~5-10 分钟 | ~2-3 分钟 |
| 费用 | OpenClaw 配额 | API 供应商 |
| 适用场景 | OpenClaw 用户 | 独立脚本 |

## 📝 版本历史

- **V2.0.0** (2026-04-03) - 双模式架构重构
- **V1.9.6** (2026-03-20) - 修复 AI 返回语言
- **V1.9.4** (2026-03-16) - 新增多 API 供应商切换
- **V1.6** (2026-03-10) - 初始版本

## 🐛 常见问题

### Q: 子 Agent 模式超时？
A: 检查网络连接，或增加 `timeout` 配置（默认 60 秒）。

### Q: PDF 解析失败？
A: 当前仅支持文本型 PDF，扫描件需要 OCR 支持（未来版本）。

### Q: 如何切换 API 供应商？
A: 修改 `config_resume_match.yaml` 中 `api.active_provider`。

## 📦 依赖

```txt
openpyxl>=3.0.0
requests>=2.28.0
python-docx>=0.8.0
pyyaml>=6.0.0
pdfplumber>=0.11.0
```

## 📄 License

MIT License

Copyright (c) 2026 fly

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

## 👤 Author

**fly**  
📧 13416145728@163.com
