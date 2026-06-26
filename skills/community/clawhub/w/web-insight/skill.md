---
name: web-insight
description: "互联网内容洞察技能。面向全域网络信息监测与情报分析场景，提供多条件组合精准检索能力，可覆盖全网新闻、社交、资讯等多渠道公开内容。支持关键词、情感、时间、平台等多条件组合查询，依托 NLP 智能解析，实现内容去重、关键信息抽取与数据结构化输出，一键供 AI Agent 调用。适用于品牌管理、市场分析、竞品追踪、风险感知等场景。触发词：搜索、检索、查找、查询、舆情、信息、内容检索、监测、情报分析。前置条件：必须在技能项目根目录配置环境变量 FEEDAX_SEARCH_API_KEY（在 https://www.feedax.cn 申请，勿使用仓库内示例或他人 Key）。"
requires_env:
  - FEEDAX_SEARCH_API_KEY
install: "pip install -r requirements.txt"
---
# 互联网内容洞察 (WebInsight)

面向全域网络信息监测与情报分析场景，提供多条件组合精准检索能力，可覆盖全网新闻、社交、资讯等多渠道公开内容。

---

## 一、前置条件：配置 API Key

**使用本技能前，必须先配置 API Key。**

### 检查配置

```bash
cat .env | grep FEEDAX_SEARCH_API_KEY
```

### 如果未配置

在 `.env` 文件中添加：

```env
FEEDAX_SEARCH_API_KEY=your_api_key_here
```

> API Key 请前往 https://www.feedax.cn 免费申请

### 错误码说明

| 错误码 | 说明          | 解决方案                          |
| ------ | ------------- | --------------------------------- |
| GE1003 | 未配置API Key | 前往 https://www.feedax.cn 申请   |
| GE1004 | API Key已失效 | 检查有效性或重新申请              |
| GE1005 | API Key已过期 | 重新申请                          |
| GE1006 | API Key无效   | 重新申请                          |
| GE1007 | 账户余额不足  | 前往充值                          |

---

## 二、CLI 命令行工具

**文件**: `scripts/search_cli.py`

### 2.1 基础用法

```bash
# 基础搜索
python3 scripts/search_cli.py --query "医疗问题"

# 搜索指定地域（最近7天）
python3 scripts/search_cli.py --query "南京 315" --area "南京" --days 7

# 搜索指定媒体平台和情感倾向
python3 scripts/search_cli.py --query "医疗问题" --media "微博,抖音" --sentiment negative
```

### 2.2 参数说明

#### 必填参数

| 参数      | 简写 | 说明       |
| --------- | ---- | ---------- |
| `--query` | `-q` | 搜索关键词 |

**关键词语法**:
- `|` = 或（OR），如 `北京|上海`
- `&` = 与（AND），如 `(南京|金陵)&(杀人|凶杀)`
- `()` = 分组

#### 分页与排序

| 参数           | 简写 | 默认值       | 说明                                   |
| -------------- | ---- | ------------ | -------------------------------------- |
| `--size`       | `-s` | 50           | 返回条数（1-10000）                    |
| `--search-after` |    |              | 深度分页游标，首次传空                  |
| `--sort`       |      | publish_time | 排序字段                               |
| `--sort-order` |      | desc         | 排序方式：asc/desc                     |

**排序字段可选值**:
- `publish_time` - **默认**，按发布时间
- `interact_count` - 按互动数（热度）
- `comments_count` - 按评论数
- `likes_count` - 按点赞数
- `reposts_count` - 按转发数
- `fans_count` - 按粉丝数

#### 内容筛选

| 参数             | 简写 | 说明                                |
| ---------------- | ---- | ----------------------------------- |
| `--media`        | `-m` | 媒体平台，逗号分隔                  |
| `--author`       |      | 作者名称，精确匹配                  |
| `--msg-type`     |      | 消息类型：original/comment/repost   |
| `--content-type` |      | 内容类型：video/picture/text        |
| `--sentiment`    |      | 情感：negative/neutral/positive/all |
| `--media-class`  |      | 媒体分类：央媒/省媒/地市/商业/其他  |
| `--domain`       |      | 内容领域                            |
| `--scene`        |      | 业务场景                            |
| `--area`         | `-a` | 地域名称（支持省/市/区县）          |
| `--noise-flag`   |      | 噪声标识：0=非噪声，1=噪声          |
| `--ai-abstract`  |      | 摘要类型：0=算法，1=AI              |
| `--verification` |      | 认证类型：blue/yellow/normal        |

#### 时间筛选

| 参数          | 简写 | 默认值 | 说明                                |
| ------------- | ---- | ------ | ----------------------------------- |
| `--days`      | `-d` | 7      | 时间范围（天）                      |
| `--time-from` |      |        | 开始时间，格式: yyyy-mm-dd HH:MM:SS |
| `--time-to`   |      |        | 结束时间，格式: yyyy-mm-dd HH:MM:SS |

#### 互动数据筛选

| 参数             | 说明       |
| ---------------- | ---------- |
| `--min-interact` | 最小互动数 |
| `--max-interact` | 最大互动数 |
| `--min-comments` | 最小评论数 |
| `--max-comments` | 最大评论数 |
| `--min-reposts`  | 最小转发数 |
| `--max-reposts`  | 最大转发数 |
| `--min-likes`    | 最小点赞数 |
| `--max-likes`    | 最大点赞数 |
| `--min-fans`     | 最小粉丝数 |
| `--max-fans`     | 最大粉丝数 |

#### 输出控制

| 参数           | 简写 | 默认值                     | 说明             |
| -------------- | ---- | -------------------------- | ---------------- |
| `--output-dir` | `-o` | ~/Desktop/舆情搜索结果/    | JSON文件输出目录 |
| `--show-count` |      | 5                          | 对话展示条数     |

### 2.3 输出配置

| 配置项   | 值                                                                             |
| -------- | ------------------------------------------------------------------------------ |
| 输出目录 | `~/Desktop/舆情搜索结果/`                                                      |
| 文件命名 | `查询词_时间戳.json`                                                           |
| 标准字段 | `title`, `summary`, `authorName`, `publishTime`, `platformName`, `originalUrl` |

### 2.4 完整示例

```bash
# 搜索南京315相关负面信息，最近一周，只看微博抖音
python3 scripts/search_cli.py \
    --query "(南京|金陵)&(315|消协|投诉|维权)" \
    --area "南京" \
    --days 7 \
    --media "微博,抖音" \
    --sentiment negative \
    --size 20 \
    --show-count 5
```

---

## 三、解析规则

### 3.1 关键词解析

从用户输入中提取核心检索关键词：

| 用户输入         | --query 参数                     |
| ---------------- | -------------------------------- |
| 南京杀人案       | `(南京|金陵)&(杀人|凶杀|行凶)`   |
| 比亚迪汽车召回   | `比亚迪&(召回|退市|下架)`        |
| 北京暴雨         | `(北京|首都)&(暴雨|大雨|洪涝)`   |

**规则**:
1. 提取2-3个核心关键词
2. 为地名、动作词添加同义词
3. 人名/品牌不扩充
4. 情感词通过 `--sentiment` 参数控制

### 3.2 媒体平台映射

| 用户表述           | --media 参数                     |
| ------------------ | -------------------------------- |
| 抖音、快手、小红书 | `"抖音,快手,小红书"`             |
| 短视频平台         | `"抖音,快手,火山,西瓜"`          |
| 财经平台           | `"同花顺,股吧,东方财富,雪球"`    |

### 3.3 情感倾向映射

| 用户表述      | --sentiment 参数 |
| ------------- | ---------------- |
| 负面/负面信息 | `negative`       |
| 正面/正面信息 | `positive`       |
| 中性          | `neutral`        |
| 全部情感      | `all`            |

### 3.4 媒体级别映射

| 用户表述      | --media-class 参数 |
| ------------- | ------------------ |
| 央媒/央级媒体 | `"央媒"`           |
| 省媒/省级媒体 | `"省媒"`           |
| 省级及以上    | `"央媒,省媒"`      |

### 3.5 消息类型映射

| 用户表述    | --msg-type 参数 |
| ----------- | --------------- |
| 原发/原创   | `original`      |
| 评论/评论区 | `comment`       |
| 转发        | `repost`        |

### 3.6 认证类型映射

| 用户表述            | --verification 参数 |
| ------------------- | ------------------- |
| 蓝V/官方账号/机构号 | `blue`              |
| 黄V/个人认证/大V    | `yellow`            |
| 普通用户/素人       | `normal`            |

### 3.7 时间范围映射

| 用户表述    | --days 参数 |
| ----------- | ----------- |
| 6小时       | 不支持      |
| 24小时/一天 | `1`         |
| 3天         | `3`         |
| 7天/一周    | `7`         |
| 30天/一个月 | `30`        |

### 3.8 排序方式映射

**默认规则**：除非用户明确要求，否则使用 `publish_time`

| 用户表述           | --sort 参数      |
| ------------------ | ---------------- |
| **无明确要求**     | `publish_time`   |
| 按热度/热门/最火的 | `interact_count` |
| 按评论数/最多评论  | `comments_count` |
| 按点赞数/最多点赞  | `likes_count`    |
| 最新/最近/新发布的 | `publish_time`   |

---

## 四、参考数据

### 4.1 媒体平台列表

抖音、快手、微博、今日头条、火山、哔哩哔哩、小红书、微信、百家号、搜狐新闻、同花顺、股吧、东方财富、百度贴吧、网易、豆瓣网、知乎、西瓜、好看、黑猫投诉、腾讯新闻、新浪财经等

### 4.2 领域分类 (--domain)

**一级分类**: 社会民生、城市管理、社会问题、司法相关、涉政相关、生态环境、教育相关、三农相关、突发事件、涉警相关

**二级分类示例**:
- **社会民生**: 劳动就业、消费问题、征地拆迁、医疗问题、住房问题、交通问题
- **突发事件**: 自然灾害、事故灾难、公共卫生事件、社会安全事件
- **涉警相关**: 治安管理、人身安全、涉毒、涉黑涉恶、诈骗

详见 `references/domains.json`

### 4.3 场景分类 (--scene)

**一级场景**: 非法烟花、实名举报、自然灾害、维权场景、城市管理、交通事故、打架斗殴、涉警信息、校园安全、环境污染、医疗卫生、安全事故

**二级场景示例**:
- **自然灾害**: 洪涝场景、沙尘雾霾
- **维权场景**: 讨薪维权、业主维权、拆迁维权
- **安全事故**: 火灾事故、坍塌事故、溺水事故

详见 `references/scenes.json`

### 4.4 参考文件

- `references/domains.json` - 领域分类完整列表
- `references/scenes.json` - 场景分类完整列表
- `references/media_names.json` - 媒体平台完整列表
- `assets/area_codes.json` - 国标区域编码数据

---

## 五、执行流程

收到用户搜索请求后，按以下步骤执行：

### Step 1: 检查 API Key 配置

```bash
cat .env | grep FEEDAX_SEARCH_API_KEY
```

- 如果返回空或文件不存在，提示用户前往 https://www.feedax.cn 申请
- 如果存在有效的 API Key，继续下一步

### Step 2: 解析用户输入

从用户自然语言中提取参数，映射到 CLI 参数：

| 提取项   | CLI 参数         | 示例                                       |
| -------- | ---------------- | ------------------------------------------ |
| 关键词   | `--query`        | "医疗问题" → `--query "医疗问题"`          |
| 返回条数 | `--size`         | "返回100条" → `--size 100`                 |
| 媒体平台 | `--media`        | "微博、抖音" → `--media "微博,抖音"`       |
| 作者     | `--author`       | "央视新闻" → `--author "央视新闻"`         |
| 消息类型 | `--msg-type`     | "原发" → `--msg-type original`             |
| 内容类型 | `--content-type` | "视频" → `--content-type video`            |
| 情感倾向 | `--sentiment`    | "负面" → `--sentiment negative`            |
| 媒体分类 | `--media-class`  | "央媒" → `--media-class "央媒"`            |
| 领域     | `--domain`       | "医疗问题" → `--domain "社会民生-医疗问题"` |
| 场景     | `--scene`        | "交通事故" → `--scene "交通事故"`          |
| 地域     | `--area`         | "南京" → `--area "南京"`                   |
| 认证类型 | `--verification` | "蓝V" → `--verification blue`              |
| 时间范围 | `--days`         | "最近3天" → `--days 3`                     |
| 开始时间 | `--time-from`    | "从3月1日" → `--time-from "2026-03-01"`    |
| 结束时间 | `--time-to`      | "到3月15日" → `--time-to "2026-03-15"`     |
| 互动数   | `--min-interact` | "互动超过1000" → `--min-interact 1000`     |
| 排序方式 | `--sort`         | "按热度" → `--sort interact_count`         |

### Step 3: 构建并执行搜索命令

根据解析结果构建命令：

```bash
python3 scripts/search_cli.py \
    --query "关键词表达式" \
    --days 7 \
    --area "地域" \
    --media "平台1,平台2" \
    --sentiment negative \
    --domain "领域" \
    --size 50
```

### Step 4: 返回结果

- 在对话中展示前5条数据摘要
- 完整数据自动保存至 `~/Desktop/舆情搜索结果/` 目录

---

## 六、执行示例

### 示例1：基础舆情搜索

**用户输入**: "搜索最近3天南京关于医疗问题的负面舆情，只看微博和抖音"

```bash
python3 scripts/search_cli.py \
    --query "(南京|金陵)&(医疗|就医|看病)" \
    --days 3 \
    --area "南京" \
    --media "微博,抖音" \
    --sentiment negative \
    --domain "社会民生-医疗问题"
```

### 示例2：热点事件追踪

**用户输入**: "搜索比亚迪汽车召回相关信息，按热度排序，返回100条"

```bash
python3 scripts/search_cli.py \
    --query "比亚迪&(召回|退市|下架|缺陷)" \
    --days 7 \
    --sort interact_count \
    --size 100
```

### 示例3：官方账号监测

**用户输入**: "搜索央视新闻发布的关于教育的内容，最近一周"

```bash
python3 scripts/search_cli.py \
    --query "教育" \
    --author "央视新闻" \
    --days 7 \
    --msg-type original
```

### 示例4：短视频平台监测

**用户输入**: "搜索抖音快手上关于交通事故的视频，互动数超过1000"

```bash
python3 scripts/search_cli.py \
    --query "交通事故" \
    --media "抖音,快手" \
    --content-type video \
    --scene "交通事故" \
    --min-interact 1000
```

### 示例5：大V账号舆情

**用户输入**: "搜索蓝V账号发布的关于食品安全的负面信息"

```bash
python3 scripts/search_cli.py \
    --query "(食品安全|食品卫生|食物中毒)" \
    --verification blue \
    --sentiment negative \
    --domain "社会民生-食品安全"
```

### 示例6：精确时间范围搜索

**用户输入**: "搜索2026年3月1日到3月15日期间上海的房价相关信息"

```bash
python3 scripts/search_cli.py \
    --query "(上海|沪)&(房价|楼市|房产)" \
    --area "上海" \
    --time-from "2026-03-01 00:00:00" \
    --time-to "2026-03-15 23:59:59" \
    --domain "社会民生-住房问题"
```

### 示例7：省级媒体监测

**用户输入**: "搜索央媒和省媒关于环境污染的报道"

```bash
python3 scripts/search_cli.py \
    --query "(环境污染|空气污染|水污染|土壤污染)" \
    --media-class "央媒,省媒" \
    --domain "生态环境" \
    --msg-type original
```
