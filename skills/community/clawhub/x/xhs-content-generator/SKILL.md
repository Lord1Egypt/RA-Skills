# XHS Content Generator - 小红书爆款内容生成器

## 功能描述

根据热点和主题生成小红书爆款标题和内容框架。支持多个热门主题：AI副业、AI工具、赚钱方法等。

## 使用方法

```bash
python generate.py --topic "AI副业" --hot_topic "ChatGPT副业赚钱"
python generate.py --topic "AI工具" --hot_topic "AI写作神器"
python generate.py --topic "赚钱方法" --hot_topic "2024新风口"
```

## 输入参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --topic | 主题类别 | AI副业 |
| --hot_topic | 当前热点/关键词 | 空 |

## 支持主题

1. **AI副业** - AI相关的副业赚钱方法
2. **AI工具** - AI工具推荐和使用技巧
3. **赚钱方法** - 各种赚钱方法和项目

## 输出格式

生成内容包含：
- 10个爆款标题选项（带emoji）
- 3个完整内容框架（开头+正文+结尾）
- 热门标签建议
- 互动引导话术

## 工作流程

1. 分析热点话题
2. 生成吸引眼球的标题
3. 构建内容框架
4. 输出完整方案

---
*Author: ClawHub Skill Developer*
*Version: 1.0.0*