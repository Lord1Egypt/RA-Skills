---
name: xiaohongshu-radar
description: 小红书搜索雷达｜无需登录小红书账号，支持关键词搜索/爆款笔记挖掘/竞品分析/KOL筛选/趋势洞察，适配营销报告/内容策划场景
license: MIT
metadata:
  openclaw:
    type: command
    runtime: "nodejs@16.14.0+"
    version: "1.0.1"
    requires:
      bins: ["node"]
      env: ["GUAIKEI_API_TOKEN"]
    env_desc:
      GUAIKEI_API_TOKEN: "小红书搜索API访问令牌；私有TOKEN可通过wx 13395823479 申请"
    category:
      - "Data&APIs"
      - "数据分析"
    tags:
      - "xiaohongshu"
      - "search"
      - "小红书搜索"
      - "小红书运营"
      - "小红书竞品分析"
      - "内容营销"
      - "content-analysis"
      - "数据挖掘"
      - "小红书关键词搜索"
      - "小红书笔记详情查询"
      - "小红书数据采集"
      - "workflow"
      - "insight"
      - "automation"
    examples:
      - "搜索'露营装备'的热门小红书笔记: node src/xiaohongshu/search-cli.js 露营装备 --type 1 --sort 2 --limit 10"
      - "分析这篇笔记的评论区情绪: node src/xiaohongshu/detail-cli.js 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy'"
      - "监控'早春穿搭'关键词(最新排序+图文类型): node src/xiaohongshu/search-cli.js --keyword '早春穿搭' --type 2 --sort 1"
---

# 📕 小红书搜索雷达

> **💡一句话价值**：一键搜索小红书笔记、互动数据，帮你做爆款选题、竞品分析。
>
> **🔥核心优势**
>
> - 轻量: 无需部署服务，Node.js 一键运行
> - 灵活: 支持多维度筛选、批量操作、多格式导出
> - 实用: 日志自动归档，适配营销报告 / 内容策划场景
> - 安全: 无需登录你的小红书账号，不担心风控风险 / 封号问题

## 1. ✅ 我能帮你解决什么（10 秒判断）

- 🔍 按关键词搜小红书笔记（最新/最多点赞/最多评论/最多收藏排序）：找爆款选题、分析高赞笔记规律
- 🦸 竞品监控：批量抓取对标账号所有公开作品数据，分析内容策略
- 📡 热点追流：实时获取小红书热搜，抢占流量风口
- 📊 数据导出：自动生成JSON日志，方便二次使用

## 2. 🚀 最快上手（复制就能跑，30 秒出结果）

> Note: 请先通过微信 <13395823479> 申请 API TOKEN，配置环境变量 GUAIKEI_API_TOKEN 后才能正常运行。

### 2.1 🔎 小红书关键词搜索（最简单）

```bash
node src/xiaohongshu/search-cli.js 数据分析
```

### 2.2 🔎 按点赞排序找爆款（最常用）

```bash
node src/xiaohongshu/search-cli.js --keyword "AI" --sort 2
```

### 2.3 🔎 按最新排序找风口（最常用）

```bash
node src/xiaohongshu/search-cli.js --keyword "AI" --sort 1
```

### 2.4 📕 小红书笔记详情查询（内容分析）

```bash
node src/xiaohongshu/detail-cli.js "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"
```

## 3. 📌 适用场景（我该不该用？）

- 你需要做小红书笔记选题 → 关键词搜索 + 点赞排序
- 你需要模仿爆款文案 → 查看高赞笔记详情
- 你需要做营销报告 → 导出结构化数据

## 4. 🔧 参数详解表

### 🔎 小红书关键词搜索

| 参数        | 缩写 | 作用       | 可选值                                                           | 必填 |
| :---------- | :--: | :--------- | :--------------------------------------------------------------- | :--: |
| `--keyword` | `-k` | 搜索关键词 | 2-50 个汉字                                                      |  是  |
| `--type`    | `-t` | 内容类型   | 0 = 全部 / 1 = 视频 / 2 = 图文                                   |  否  |
| `--sort`    | `-s` | 排序方式   | 0 = 综合 / 1 = 最新 / 2 = 最多点赞 / 3 = 最多评论 / 4 = 最多收藏 |  否  |
| `--limit`   | `-l` | 搜索数量   | 1-60 条                                                          |  否  |
| `--output`  | `-o` | 输出格式   | json / markdown                                                  |  否  |

### 📕 小红书笔记详情获取

| 参数      | 缩写 | 类型    | 说明                     |
| :-------- | :--- | :------ | :----------------------- |
| `--url`   | `-u` | 字符串  | 必填，笔记链接           |
| `--limit` | `-l` | 1-60000 | 获取笔记评论数量 (默认6) |

> **💡"笔记链接"说明**
>
> - 完整链接：必须包含 xsec_token 参数（如 <https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy> ）
> - 短链接：<https://xhslink.com/m/xxx> （自动兼容，无需手动解析）
> - ❌ 错误：链接含空格、无xsec_token的完整链接会直接报错

## 5. ⚠️ 重要限制（不踩坑）

- 仅抓取抖音公开数据，不支持私密 / 隐藏内容
- 需要配置 GUAIKEI_API_TOKEN 才能正常运行
- 数据仅限个人 / 团队内部使用，禁止违规分发

## 6. ❓ 常见问题（秒解决）

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
> - 搜索任务日志: 默认保存为「时间戳*关键词*类型*排序*数量\_search.json」
> - 详情任务日志: 默认保存为「时间戳\_笔记ID_detail.json」
>
> **💡Q：支持 Windows/Mac/Linux 吗？**
>
> A：全平台支持，仅需安装 Node.js 环境
