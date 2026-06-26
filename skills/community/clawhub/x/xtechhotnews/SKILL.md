---
name: x_techcon_hotnews
description: 获取 X-TechCon 网站的科技热点新闻。当用户输入指定的触发词时，调用 API 获取最新的科技热点新闻并格式化输出。
author: Edward
version: 1.0.0
triggers:
  - "X-TechCon 科技热点"
  - "科技区角热点"
  - "科技新闻热点"
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["python3"],"pyPackages":["requests"]}}}
---

# X-TechCon 科技热点 Skill

## 技能描述

这是一个极简版的 OpenClaw Skill，用于获取 X-TechCon 网站的科技热点新闻。当用户输入指定的触发词时，技能会调用 API 获取最新的科技热点新闻，并将结果格式化输出给用户。

## 触发词

- X-TechCon 科技热点
- 科技区角热点
- 科技新闻热点

## 功能说明

1. 接收用户输入，判断是否包含触发词
2. 如果包含触发词，调用 API 获取科技热点新闻
3. 将返回的新闻按序号排版，每条包含标题、摘要和链接
4. 结尾提示用户访问网站获取更多内容
5. 如果不包含触发词，返回提示信息

## API 调用

- API 地址：https://www.x-techcon.com/api/hot_news
- 请求方式：GET
- 返回格式：
  ```json
  {
    "code": 200,
    "msg": "success",
    "data": [
      {
        "id": 114366,
        "title": "新闻标题",
        "summary": "新闻摘要",
        "url": "https://www.x-techcon.com/article/114366.html"
      }
      // 更多新闻...
    ]
  }
  ```

## 使用示例

### 示例 1：触发词 "X-TechCon 科技热点"

用户输入：X-TechCon 科技热点

技能输出：
```
科技热点新闻：

1. 标题：新闻标题 1
   摘要：新闻摘要 1
   链接：https://www.x-techcon.com/article/114366.html

2. 标题：新闻标题 2
   摘要：新闻摘要 2
   链接：https://www.x-techcon.com/article/114367.html

...

更多内容请访问 https://www.x-techcon.com
```

### 示例 2：非触发词

用户输入：今天天气怎么样

技能输出：
```
暂不支持，请说'X-TechCon 科技热点''科技区角热点'或'科技新闻热点'获取最新科技新闻
```

## 部署说明

1. 安装依赖：`pip install -r requirements.txt`
2. 将 `openclaw_skill.py` 文件部署到 OpenClaw 平台
3. 配置技能参数，确保 `skill_main` 函数能被正确调用

## 后续优化

- 添加更详细的异常处理
- 增加缓存机制，减少 API 调用频率
- 支持更多触发词和用户意图
