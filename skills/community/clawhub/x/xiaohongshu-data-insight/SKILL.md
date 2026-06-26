---
name: xiaohongshu-data-insight
description: 小红书数据洞察大师｜支持关键词搜索/笔记详情获取，无需登录您的小红书账号，可获取小红书笔记数据，轻松达成爆款挖掘、竞品分析、趋势洞察等
license: MIT
metadata:
  openclaw:
    type: command
    runtime: "nodejs@16.14.0+"
    version: "1.0.0"
    requires:
      bins:
        - "node"
      env:
        - "GUAIKEI_API_TOKEN"
    env_desc:
      GUAIKEI_API_TOKEN: "小红书数据API访问令牌；需联系开发者wx 13395823479 获取"
    category: "数据分析/内容创作"
    tags:
      [
        "xiaohongshu",
        "Xiaohongshu Keyword Search",
        "Xiaohongshu Note Details Query",
        "Xiaohongshu Data Crawler",
        "Xiaohongshu Competitor Monitoring",
      ]
    keywords:
      [
        "Xiaohongshu",
        "Market Research",
        "Data Mining",
        "Market Research",
        "Competitor Analysis",
        "Xiaohongshu Keyword Search",
        "Xiaohongshu Note Details Query",
        "Xiaohongshu Comment Analysis",
        "Xiaohongshu Competitor Monitoring",
      ]
    examples:
      - "搜索'数据分析'的热门小红书笔记: node src/xiaohongshu/search-cli.js 数据分析 --type 1 --sort 2 --limit 10"
      - "分析这篇小红书笔记的评论区情绪: node src/xiaohongshu/detail-cli.js 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy'"
      - "监控小红书'数据挖掘'关键词(最新排序+图文类型): node src/xiaohongshu/search-cli.js --keyword '数据挖掘' --type 2 --sort 1"
    capabilities:
      - "检索小红书关键词相关笔记（支持多维度筛选，输出结构化数据）"
      - "解析小红书笔记链接，提取详情数据（含互动、评论、内容信息）"
      - "分析笔记评论区情绪倾向，输出量化分析结果"
      - "监控关键词热度趋势，生成时间维度的热度数据"
      - "输出Markdown/JSON格式数据，支持运营报表直接复用"
    input_schema:
      search:
        required: ["keyword"]
        properties:
          keyword:
            {
              type: "string",
              minLength: 2,
              maxLength: 50,
              description: "搜索关键词，2-50个汉字，避免特殊符号",
            }
          type:
            {
              type: "integer",
              enum: [0, 1, 2],
              default: 0,
              description: "0-全部，1-视频，2-图文",
            }
          sort:
            {
              type: "integer",
              enum: [0, 1, 2, 3, 4],
              default: 0,
              description: "0-综合，1-最新，2-最多点赞，3-最多评论，4-最多收藏",
            }
          limit:
            {
              type: "integer",
              minimum: 1,
              maximum: 60,
              default: 10,
              description: "搜索数量",
            }
          output:
            {
              type: "string",
              enum: ["json", "markdown"],
              default: "json",
              description: "输出格式",
            }
      detail:
        required: ["url"]
        properties:
          url:
            {
              type: "string",
              pattern: "^(https://www.xiaohongshu.com/explore/|https://xhslink.com/m/)",
              description: "小红书笔记链接，支持完整链接（含xsec_token）或短链接",
            }
    output_schema:
      search_result:
        {
          type: "array",
          items:
            {
              type: "object",
              properties:
                {
                  note_id: "string",
                  title: "string",
                  like_count: "integer",
                  comment_count: "integer",
                  collect_count: "integer",
                  content_type: "string",
                  link: "string",
                },
            },
        }
      detail_result:
        {
          type: "object",
          properties:
            {
              note_info: "object",
              comment_analysis: "object",
              interaction_data: "object",
            },
        }
    invocation_example:
      - command: "node src/xiaohongshu/search-cli.js 数据分析 --type 1 --sort 2 --limit 10"
        input: { keyword: "数据分析", type: 1, sort: 2, limit: 10 }
        output_type: "json"
        description: "获取10条数据分析相关的小红书热门视频笔记"
---

# 📊 小红书数据洞察大师 - 爆款挖掘与竞品分析专家

## 一、工具概述

### 1.1 核心价值

小红书数据挖掘工具，无需登录小红书账号即可获取笔记数据，通过数据驱动实现爆款挖掘、竞品分析、趋势洞察、KOL 筛选等核心目标，覆盖内容创作、品牌营销、市场分析全场景。

### 1.2 核心能力矩阵

| 能力模块        | 核心功能                     | 解决痛点                         |
| :-------------- | :--------------------------- | :------------------------------- |
| **🔍 爆款挖掘** | 热门笔记发现、高互动内容检索 | 找不到选题灵感，不知道什么内容火 |
| **🕵️ 竞品分析** | 对标账号监控、笔记表现追踪   | 竞品涨粉快的原因及策略不明确     |
| **👥 KOL 筛选** | 博主粉丝画像、互动率分析     | 投放博主选择难，担心数据造假     |
| **📈 趋势监控** | 关键词热度追踪、话题趋势分析 | 错过热点，无法预判市场风向       |

### 1.3 适用人群

小红书内容创作者 / 运营、品牌营销 / 市场人员、数据分析师、MCN 机构 / 博主经纪人。

## 1.4 核心使用场景

| 场景         | 具体价值                                                   |
| ------------ | ---------------------------------------------------------- |
| 内容创作选题 | 输入关键词筛选「最多点赞」笔记，快速定位爆款选题方向       |
| 品牌竞品监控 | 分析竞品账号 / 笔记的互动数据、内容风格，制定差异化策略    |
| KOL投放筛选  | 解析 KOL 笔记真实互动率，规避数据造假的博主                |
| 市场趋势分析 | 定时监控关键词「最新排序」，捕捉热点风向并提前布局内容     |
| 数据报表生成 | 输出 Markdown 格式结果，直接嵌入运营周报，减少手动整理成本 |

## 二、快速使用指南

### 2.1 前置条件

- 安装Node.js 16.14.0 及以上版本
- 配置环境变量 `GUAIKEI_API_TOKEN`（默认TOKEN仅用于体验，私有TOKEN需申请）

### 2.2 环境配置

```bash
# 验证Node.js版本
node -v

# Linux/Mac配置环境变量
export GUAIKEI_API_TOKEN="你的令牌"

# Windows配置环境变量
set GUAIKEI_API_TOKEN="你的令牌"
```

### 2.3 核心命令使用

#### 2.3.1 小红书关键词搜索

```bash
# 基础语法
node src/xiaohongshu/search-cli.js <关键词> [选项]

# 完整选项说明
--keyword -k <关键词>: 搜索关键词（必填，2-50个汉字，避免特殊符号）
--type -t <0/1/2>: 内容类型，0-全部（默认），1-视频，2-图文
--sort -s <0-4>: 排序规则，0-综合（默认），1-最新，2-最多点赞，3-最多评论，4-最多收藏
--limit -l <1-60>: 搜索数量，1-60（默认10）
--output -o <json/markdown>: 输出格式（默认json）
--help -h: 显示帮助信息

# 使用示例

#搜索“数据挖掘”最多点赞的20条笔记
node src/xiaohongshu/search-cli.js "数据挖掘" --sort 2 --limit 20
#搜索“数据分析”的图文笔记，输出Markdown格式
node src/xiaohongshu/search-cli.js --keyword "数据分析" --type 2 --output markdown
#爆款挖掘：数据分析（图文+最多点赞）
node src/xiaohongshu/search-cli.js "数据分析" --type 2 --sort 2
#趋势监控：数据挖掘（最新排序）（定时执行）
node src/xiaohongshu/search-cli.js "数据挖掘" --sort 1
```

#### 2.3.2 小红书笔记详情查询

```bash
# 基础语法
node src/xiaohongshu/detail-cli.js <笔记链接> [选项]

# 选项说明
--url -u <笔记链接>: 笔记链接（支持https://www.xiaohongshu.com/explore/xxx 或 http://xhslink.com/m/xxx）
--help -h: 显示帮助信息

# 链接格式要求
1. 完整链接：必须包含 xsec_token 参数（如 https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy）
2. 短链接：https://xhslink.com/m/xxx（自动兼容，无需手动解析）
❌ 错误：链接含空格、无xsec_token的完整链接会直接报错

# 使用示例
node src/xiaohongshu/detail-cli.js "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"
node src/xiaohongshu/detail-cli.js --url "http://xhslink.com/m/xxx"
```

## 三、数据合规说明

✅ 仅抓取小红书**公开可见**内容，无隐私数据泄露风险
✅ 本技能不登录小红书账号，仅依赖API获取公开数据
✅ 数据仅用于商业分析参考，需遵守小红书平台使用条款
✅ 所有输出数据均做脱敏处理，不涉及用户个人信息
✅ 本工具依赖第三方 API 进行数据获取。数据仅供参考，第三方服务可能存在不稳定或接口变更的情况。请勿用于高频爬虫或侵犯用户隐私的场景
⚠️ 高频调用（如1分钟>10次）可能触发API频率限制

## 四、技术说明

- 系统：Windows/Linux/MacOS（仅需 Node.js，无额外依赖）
- 运行环境：Node.js 16.14.0+，需提前配置 `GUAIKEI_API_TOKEN` 环境变量
- 网络：需正常访问网络，国内服务器无需代理
- 权限：普通用户权限即可运行，无需管理员权限

### 4.1 日志说明

- 运行时会输出彩色日志：INFO(蓝色)、SUCCESS(绿色)、WARN(黄色)、ERROR(红色)；
- 启动时会打印工具Banner，方便确认是否正确执行；
- 所有任务结果会自动保存到 `logs/` 目录（按时间+关键词/链接命名）。

## 五、版本更新日志

### v1.0.0

- 首发上线：实现小红书关键词搜索、小红书笔记详情与评论获取自动化工具。
- 支持热门笔记挖掘、竞品分析、趋势监控等核心商业分析功能。
- 增加多选项参数（类型、排序、输出格式、搜索数量）灵活定制搜索。
- 提供开放式命令行用法与使用示例，适配 Node.js 16.14.0+ 环境。
