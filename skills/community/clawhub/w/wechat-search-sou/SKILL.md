---
name: wechat-search
description: 微信搜一搜实时搜索工具。支持WECHAT文章、视频、图片实时搜索数据获取，当需要获取微信搜索结果时使用。
license: MIT
contact: 微信13395823479 | 官网https://www.guaikei.com
metadata:
  enabled: true
  type: command
  requires:
    bins:
      - "node"
    env:
      - "GUAIKEI_API_TOKEN"
  category:
    - "Data&APIs"
    - "内容创作"
  tags:
    - "wechat"
    - "search"
    - "video"
    - "article"
    - "channel"
    - "content-analysis"
    - "competitor-analysis"
    - "微信"
    - "微信搜索"
    - "数据挖掘"
    - "内容分析"
    - "竞品分析"
  schemas:
    - name: "文章搜索入参"
      file: "assets/article_cli_req.schema.json"
    - name: "文章搜索出参"
      file: "assets/article_cli_resp.schema.json"
    - name: "视频搜索入参"
      file: "assets/video_cli_req.schema.json"
    - name: "视频搜索出参"
      file: "assets/video_cli_resp.schema.json"
  examples:
    - name: 搜索"AI"的微信文章
      command: node scripts/wechat/article-cli.js --keyword AI
      description: 快速获取关键词相关文章数据，助力内容创作灵感
    - name: 搜索"AI"的热门微信文章
      command: node scripts/wechat/article-cli.js --keyword AI --sort 2
      description: 挖掘爆款文章特征，优化内容策略
    - name: 搜索"AI"的最近1天发布的微信文章
      command: node scripts/wechat/article-cli.js --keyword AI --publishTime 1
      description: 获取最新关键词相关文章数据，把握内容窗口期
    - name: 搜索"AI"的微信视频
      command: node scripts/wechat/video-cli.js --keyword AI
      description: 快速获取关键词相关视频数据，助力内容创作灵感
    - name: 搜索"AI"的最新微信视频
      command: node scripts/wechat/video-cli.js --keyword AI --sort 1
      description: 获取最新关键词相关视频数据，把握内容窗口期
    - name: 搜索长度在5-20分钟的"AI"的微信视频
      command: node scripts/wechat/video-cli.js --keyword AI --sort 2 --duration 2
      description: 监控长期内容趋势，制定内容规划
---

# 微信搜一搜实时检索：实时获取微信生态最新内容（文章/视频/图片）

> 🔥 核心价值
>
> 极致实时: 对接微信搜一搜底层入口，秒级获取突发事件/行业动态。
>
> 权威可信: 内容来自微信认证主体/权威媒体，信源比开放互联网更纯净
>
> 轻量安全: 仅需Node.js环境，无需提供微信账号，仅关键词即可检索
>
> 全平台兼容: 支持Windows/Mac/Linux，日志自动留存，便于数据复用

## 1. ✅ 我能帮你解决什么

- 🔍 按关键词搜微信视频（最新/热门/视频时长）
- 🔍 按关键词搜微信文章（最新/热门/发布时间）

## 2. 🚀 最快上手

> **Note:** 请先通过微信 <13395823479> 申请TOKEN ，或访问[微信搜索技能官网](https://www.guaikei.com)开通TOKEN，配置环境变量 `GUAIKEI_API_TOKEN` 后才能正常运行。

### 2.1 🔎 微信视频关键词搜索

```bash
node scripts/wechat/video-cli.js 搜索关键词
```

### 2.2 🔎 微信文章关键词搜索

```bash
node scripts/wechat/article-cli.js 搜索关键词
```

## 3. 🔧 参数详解表

> 详细选项参数说明， 可参阅 [完整选项说明](references/options.md)
>
> LLM理解技能的详细选项，可参阅技能 `assets` 目录中文件，其遵循 JSON Schema draft-07 版本规范。
>
> - 微信文章搜索入参: [入参规范](assets/article_cli_req.schema.json)
> - 微信文章搜索出参: [出参规范](assets/article_cli_resp.schema.json)
> - 微信视频搜索入参: [入参规范](assets/video_cli_req.schema.json)
> - 微信视频搜索出参: [出参规范](assets/video_cli_resp.schema.json)

## 4. ⚠️ 重要限制

- 需要配置 GUAIKEI_API_TOKEN 才能正常运行
- 数据仅限个人 / 团队内部使用，禁止违规分发

## 5. ❓ 常见问题

> **💡Q：运行报错，提示无权限？**
>
> A：先配置环境变量：`set GUAIKEI_API_TOKEN=你的TOKEN`
>
> - 私有TOKEN申请后请留意使用安全，避免泄露给他人
>
> **💡Q：输出文件在哪里？**
>
> A：自动保存在技能目录的 `logs` 文件夹下
>
> - 视频搜索日志: 默认保存为「时间戳\_关键词\_video.json」
> - 文章搜索日志: 默认保存为「时间戳\_关键词\_article.json」
>
> **💡Q：支持 Windows/Mac/Linux 吗？**
>
> A：全平台支持，仅需安装 Node.js 环境

## 6. 🤖 LLM调用规则

### 触发条件

当用户提出以下需求时，触发本工具调用：

- 需求包含“微信搜索”+“关键词”+“文章/视频/图片”
- 需求涉及“实时微信内容”“微信最新动态”“微信生态舆情”

### 调用参数要求

必须传入：

- keyword: 搜索关键词（字符串，必填）
- token: 用户的GUAIKEI_API_TOKEN（字符串，必填）
