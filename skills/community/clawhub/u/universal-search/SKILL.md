---
name: universal-search
description: 全网搜索接口 - 孙永乐开发的高质量全网搜索API，返回结构化结果，带可信度评分和交叉验证。
homepage: https://49srjp57sf.coze.site
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3"],"env":["UNIVERSAL_SEARCH_URL","UNIVERSAL_SEARCH_TOKEN"]},"primaryEnv":""}}
---

# 全网搜索接口

孙永乐开发的高质量全网搜索API，返回结构化结果，带可信度评分和交叉验证。

## 搜索

```bash
python3 {baseDir}/scripts/search.py "搜索关键词"
python3 {baseDir}/scripts/search.py "搜索关键词" --timeout 120
python3 {baseDir}/scripts/search.py "搜索关键词" --json
```

## Options

- `--timeout <seconds>`: 超时时间（默认：120秒）
- `--json`: 输出JSON格式而不是格式化文本

## 返回结果格式

接口返回结构化内容，包含：
- **答案摘要**: 简洁的总结
- **详细说明**: 分点详细说明，带来源标注
- **来源列表**: 所有参考来源的链接
- **验证结果**: 带可信度评分的交叉验证（0-10分）

## 配置

需要配置环境变量（可选，脚本已内置默认配置）：
- `UNIVERSAL_SEARCH_URL`: 搜索接口地址
- `UNIVERSAL_SEARCH_TOKEN`: Authorization Bearer Token

## 特点

- 🔍 **高质量搜索**: 结构化返回，交叉验证
- ⭐ **可信度评分**: 0-10分可信度评分
- 📋 **来源标注**: 每个信息都带来源
- 🎯 **AI优化**: 专为AI助手设计的返回格式

## 开发者

- 开发者：孙永乐
- 接口地址：https://49srjp57sf.coze.site/run
