---
name: SEO优化检查器
description: 输入网址一键输出SEO诊断报告，检查标题/描述/Headers/关键词密度/图片alt/页面速度/移动端适配/Meta标签，输出可执行优化建议
version: 1.0.0
author: AI Skill 商业生产
tags: [SEO, 网站优化, 搜索引擎优化, 诊断, 网页分析]
price: 19.9
---

# SEO优化检查器

## 功能概述

输入网址一键输出SEO诊断报告。检查网页的标题、描述、Headers、关键词密度、图片alt、页面速度、移动端适配、Meta标签，输出可执行的优化建议。

## 使用方法

```bash
# 基础SEO检查
python3 seo_checker.py https://example.com

# 保存报告到文件
python3 seo_checker.py https://example.com --output report.md

# 启用AI增强分析（需OPENAI_API_KEY）
python3 seo_checker.py https://example.com --ai

# 检查多个页面
python3 seo_checker.py https://example.com/page1 https://example.com/page2
```

## 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `OPENAI_API_KEY` | AI模式必填 | OpenAI API 密钥 |
| `OPENAI_MODEL` | 否 | 模型名，默认 gpt-4o-mini |

## 检查项

- [x] 标题标签（Title Tag）
- [x] Meta Description
- [x] Headings 层级（H1-H6）
- [x] 关键词密度
- [x] 图片 Alt 属性
- [x] Canonical URL
- [x] Open Graph / Twitter Card
- [x] 页面大小与加载速度
- [x] 移动端 meta viewport
- [x] robots / noindex 指令
- [x] 链接检查（断链/外部链接）
- [x] 结构化数据（JSON-LD）

## 依赖

```bash
pip install requests beautifulsoup4
```
