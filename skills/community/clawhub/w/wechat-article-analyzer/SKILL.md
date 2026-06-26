---
name: 微信公众号文章深度分析
description: |
  微信公众号文章深度分析工具。
  当用户发送微信公众号文章链接时，可以读取文章内容并进行深度分析。
  功能：自动提取文章标题和正文、提取时间线、识别关键人物/公司、提取核心事实、进行主题分析、生成报告。
  支持输出格式：Markdown 报告、OpenCLI 适配器、JSON 数据。
triggers:
  - "mp.weixin.qq.com"
  - "微信公众号"
  - "公众号文章"
  - "分析公众号文章"
  - "wechat article analyze"
  - "wechat mp article"
---

# 微信公众号文章分析器

## 功能

1. **📖 自动读取**微信公众号文章内容
2. **📅 提取时间线** - 识别关键事件和时间节点
3. **👥 识别关键人物/组织** - 提取公司、组织、个人
4. **📊 提取核心事实** - 金额、百分比、漏洞编号等
5. **🎯 主题分析** - 识别核心议题和战略意义
6. **💬 引语提取** - 收集重要引语
7. **📄 生成报告** - Markdown / OpenCLI 适配器 / JSON

## 技术方案

### 核心流程
```
用户发送链接 → 读取文章内容 → NLP分析 → 生成结构化数据 → 输出报告
```

### 文章读取
- **请求库**: Python `requests` + Mac Chrome UA
- **解析方式**: 正则表达式提取结构化数据

### 分析维度

| 维度 | 说明 |
|------|------|
| **Timeline** | 事件时间线，关键节点 |
| **Stakeholders** | 关键人物、公司、角色 |
| **Facts** | 核心事实、数据、日期 |
| **Themes** | 主题分析、战略意义 |
| **Quotes** | 重要引语 |

## 使用方法

### 命令行

```bash
# 基本分析 - 输出到控制台
python3 scripts/analyze_wechat.py <微信公众号链接>

# 生成 Markdown 报告
python3 scripts/analyze_wechat.py <链接> --format markdown --output report.md

# 生成 OpenCLI 适配器
python3 scripts/analyze_wechat.py <链接> --format opencli --output adapter.yaml

# 生成 JSON 数据
python3 scripts/analyze_wechat.py <链接> --format json --output data.json

# 生成所有格式
python3 scripts/analyze_wechat.py <链接> --format all

# 显示详细过程
python3 scripts/analyze_wechat.py <链接> --verbose
```

### 作为 Skill 使用

```python
from skills.wechat_article_analyzer import analyze_wechat

result = analyze_wechat.analyze_article("https://mp.weixin.qq.com/s/xxx")
print(result['timeline'])
print(result['stakeholders'])
```

### 自动触发

当用户发送微信公众号链接或关键词时，自动执行分析。

## 输出格式

### Markdown - 人类可读
- 事件时间线
- 关键人物/组织
- 核心事实数据
- 主题分析
- 重要引语

### OpenCLI 适配器 - YAML
- 结构化数据
- 可直接注册到 OpenCLI
- 包含所有分析维度

### JSON - 程序友好
- 完整的结构化数据
- 便于后续处理
- 可导入其他系统

## 依赖

- Python 3.7+
- requests>=2.25.0
- pyyaml>=5.4.0

## 许可证

MIT

## 作者

Created by OpenClaw
