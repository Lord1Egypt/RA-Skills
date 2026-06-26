---
name: skillsmp-search
description: 从 SkillsMP 市场搜索 AI Agent Skills。支持关键词搜索和 AI 语义搜索。
homepage: https://skillsmp.com
metadata:
  {
    "openclaw": {
      "emoji": "🔍"
    }
  }
---

# SkillsMP Search

从 [SkillsMP](https://skillsmp.com) 市场搜索 AI Agent Skills。

## 配置

### 环境变量

```bash
# 必需：你的 SkillsMP API Key
export SKILLSMP_API_KEY="sk_live_xxxxxxxxxxxx"

# 可选：搜索结果数量 (默认: 10)
export SKILLSMP_LIMIT=20
```

### 获取 API Key

1. 访问 https://skillsmp.com/docs/api
2. 注册账号
3. 在个人设置中获取 API Key

## 使用方法

### 基本搜索

```bash
skillsmp-search "关键词"
```

### 高级搜索

```bash
# 限制结果数量
skillsmp-search "twitter" --limit 5

# 搜索特定分类
skillsmp-search "数据分析" --category development
```

## API 文档

SkillsMP 提供两个搜索接口：

1. **关键词搜索**
   ```
   GET https://skillsmp.com/api/v1/skills/search?q=关键词
   ```

2. **AI 语义搜索**
   ```
   GET https://skillsmp.com/api/v1/skills/ai-search?q=关键词
   ```

详细文档: https://skillsmp.com/docs/api

## 示例

```bash
# 搜索推特相关 skills
skillsmp-search "twitter"

# 搜索视频下载
skillsmp-search "video download"

# 搜索数据分析
skillsmp-search "data analysis"
```
