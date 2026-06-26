---
name: xhs-content-analytics
description: 小红书自动化运营工具-支持：搜索笔记、查看笔记详情及评论。 当用户提及 xiaohongshu、小红书、RedNote，或需要在该平台进行内容调研时使用。
license: MIT
metadata:
  version: "1.0.1"
  category:
    - "Data&APIs"
    - "数据分析"
  tags:
    - "小红书关键词搜索"
    - "小红书笔记详情查询"
    - "小红书评论抓取"
    - "小红书内容排序筛选"
    - "小红书爆款选题"
    - "小红书竞品监控"
    - "小红书营销报告制作"
    - "小红书热点追踪"
    - "无需登录"
  capabilityBoundary:
    - "支持小红书公开内容抓取，不支持私密笔记/付费内容"
    - "评论获取上限60000条，搜索结果上限60条"
    - "无需登录小红书账号，无封号/风控风险"
  examples:
    - scenario: "找露营装备类高赞爆款视频笔记（内容选题）"
      command: "node src/xiaohongshu/search-cli.js -k 露营装备 -t 1 -s 2 -l 10"
      paramExplain: "-k=露营装备（搜索关键词）、-t=1（仅视频）、-s=2（最多点赞）、-l=10（返回10条）"
      outputExpect: "输出10条露营装备高赞视频笔记，含标题、链接、点赞/收藏数等核心数据"
    - scenario: "分析单篇笔记评论区情绪（用户反馈分析）"
      command: "node src/xiaohongshu/detail-cli.js -u 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy'"
      paramExplain: "-u=笔记PC链接（必填），默认获取6条评论"
      outputExpect: "返回笔记基础信息+6条评论内容，支持情绪分析"
    - scenario: "导出AI图文笔记收藏排序数据（营销报告）"
      command: "node src/xiaohongshu/search-cli.js --keyword AI --type 2 --sort 4 --limit 20 --output json"
      paramExplain: "--keyword=AI、--type=2（图文）、--sort=4（最多收藏）、--limit=20、--output=json"
      outputExpect: "生成JSON文件，含20条AI图文笔记全量数据，可用于报告可视化"
---

# 📊 小红书内容分析 - 获取小红书内容表现数据

> **💡一句话价值**：一键搜索小红书笔记、互动数据，帮你做爆款选题、竞品分析。
>
> **🔥核心优势**
>
> - 轻量: 无需部署服务，OpenClaw一键运行
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

### 2.1 🔎 小红书关键词搜索

```bash
node src/xiaohongshu/search-cli.js -k 数据分析
```

### 2.2 🔎 按点赞排序找爆款

```bash
node src/xiaohongshu/search-cli.js --keyword "AI" --sort 2
```

### 2.3 🔎 按最新排序找风口

```bash
node src/xiaohongshu/search-cli.js --keyword "AI" --sort 1
```

### 2.4 📕 小红书笔记详情查询

```bash
node src/xiaohongshu/detail-cli.js -u "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"
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
> - PC链接: <https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy>
> - 短链接: <https://xhslink.com/m/xxx>

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
