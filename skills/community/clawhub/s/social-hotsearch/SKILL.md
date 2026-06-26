---
name: 社媒热搜助手
description: 微博/小红书/抖音/知乎/百度热搜与舆情分析助手。一句话查热搜榜、对话题做声量/情感/互动/平台分布分析、采样原帖样本。适配营销选题、品牌讨论分析、社媒舆情、PR 传播效果场景,覆盖头部消费品牌、热门事件、品类词。免费 200 次,无需注册。
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# 社媒热搜助手 (social-hotsearch)

面向**社会化营销 / 内容运营 / 公关 PR / 媒介投放 / 行业研究**从业者的热搜情报与社媒舆情分析技能。
零配置,首次使用自动注册,免费 200 次调用额度。

## 你能用它做什么(双能力)

| 能力 | 工具 | 典型用途 |
|---|---|---|
| **A. 看热搜找选题** | `query_hot_list` | "今天有什么火?给我推选题" |
| **B. 对已知话题做多维剖析** | `analyze_topic` + `sample_posts` | "我已有目标(品牌/事件/品类),想看它在社媒的全貌" |

> 注:能力 B **不依赖热搜状态**,只要话题/品牌有足够的社媒讨论量(头部消费品牌、热门事件、品类词)即可分析。

## 适合谁用 + 典型场景

### 社会化营销 / 内容运营(追热点、找选题)
- "看下小红书最近'夏日防晒'有哪些爆款话题,我要做种草选题"
- "618 大促期间国货美妆品牌在抖音的热度排行"

### 公关 / 品牌(口碑监测、传播复盘)
- "瑞幸最近一周在微博和小红书的口碑怎么样,正面率多少"
- "某品牌发布会后两天网友都在说什么,对比微博/小红书/抖音的讨论"

### 媒介投放(评估热度与价值)
- "某热播综艺这一周的全网讨论量级,值不值得投"
- "新能源车这波话题在抖音的互动量级有多大"

### 行业研究 / 咨询(跨平台情报)
- "AI 大模型最近一周在知乎 vs 微博的话题分布"
- "宠物经济在小红书 vs 抖音的内容差异"

## 核心入口(三个 CLI 脚本)

### 1. 查询热搜榜单 → `scripts/query_hot_list.py`

```bash
python3 ./scripts/query_hot_list.py --source 微博 --size 20
python3 ./scripts/query_hot_list.py --source 抖音 --keyword 国货
python3 ./scripts/query_hot_list.py --source 知乎 --date 2026-05-13
```

**参数:**
- `--source` (必填):平台,可选 `微博 / 抖音 / 知乎 / 百度`(**热搜榜不支持小红书**,要查小红书话题用下面的 `analyze_topic`)
- `--size`:返回数量,默认 50,最多 100
- `--keyword`:可选,过滤包含特定关键词的话题
- `--date`:可选,日期 YYYY-MM-DD,默认今天

**消耗:** 1 次额度

### 2. 单话题深度分析 → `scripts/analyze_topic.py`

```bash
python3 ./scripts/analyze_topic.py --topic '瑞幸'
python3 ./scripts/analyze_topic.py --topic '618' --days 7
python3 ./scripts/analyze_topic.py --topic '夏日防晒' --datasource 小红书 --search-fields title content screenshot
python3 ./scripts/analyze_topic.py --topic '某综艺' --datasource 抖音 --search-fields title content video_asr video_ocr
```

**参数:**
- `--topic` (必填):话题关键词
- `--days`:时间窗口天数,默认 3(**最少 1 个完整自然日**,即 `--days 1` 起步)
- `--datasource`:平台列表,**默认 `微博 小红书 短视频`**(覆盖营销/PR 三大主力)。可选:`小红书 / 微博 / 短视频 / 视频 / 微信 / 电商 / 博客 / 问答 / 新闻 / 论坛`
- `--search-fields`:搜索范围,默认 `title content`(标题+正文)。短视频场景可加 `video_asr video_ocr`,图文场景可加 `screenshot`
- `--with-clusters`:同时返回相关话题聚类(**额外消耗 1 次额度**,用户没明确要求时不要加)

**输出:** 声量、情感指数、互动数、用户数、平台分布、(可选)关联话题
**消耗:** 基础 1 次,加 `--with-clusters` 共 2 次

### 3. 话题原帖采样 → `scripts/sample_posts.py`

```bash
python3 ./scripts/sample_posts.py --topic '瑞幸' --size 20
python3 ./scripts/sample_posts.py --topic '夏日防晒' --datasource 小红书 --order 互动数
python3 ./scripts/sample_posts.py --topic '某新品' --search-fields title content video_asr video_ocr
```

**参数:**
- `--topic` (必填):话题关键词
- `--days`:时间窗口,默认 3
- `--datasource`:平台列表,**默认 `微博 小红书 短视频`**(同上,可选项也同上)
- `--search-fields`:搜索范围,同 `analyze_topic`
- `--size`:采样数量,默认 20,最多 100
- `--order`:排序,可选 `综合/发布时间/互动数/阅读数/曝光量`

**输出:** 帖子列表(标题/内容/作者/链接/互动数据;含视频帖子时会带 ASR/OCR 字段)
**消耗:** 1 次额度

### 4. 查询当前剩余额度 → `scripts/ensure_user.py`

```bash
python3 ./scripts/ensure_user.py
```

输出 user_id、已用、剩余次数。**首次运行会自动注册,不消耗额度。**

## 操作规则(给 AI 看的)

### 1. 首次使用
任何脚本第一次调用时会自动通过 `~/.config/social-hotsearch/user.json` 注册新用户,无需用户手动配置。

### 2. 配额耗尽时
脚本退出码为 `3`,stderr 输出引导用户填写飞书表单的提示。**直接把表单 URL 转告用户,不要尝试绕过**。

### 3. 平台名两套体系(关键)
- **`query_hot_list`(热搜榜)** 用具体站点名:`微博 / 抖音 / 知乎 / 百度`,**不支持小红书**(用户问"小红书热搜",告知"热搜榜暂不支持小红书,要查小红书话题请改用 analyze_topic")
- **`analyze_topic` / `sample_posts`(分析/采样)** 用 platform 大类:`小红书 / 微博 / 短视频 / 视频 / 微信 / 电商 / 博客 / 问答 / 新闻 / 论坛`
- **脚本已内置归一化**:用户/AI 传 `抖音` / `快手` 会自动转为 `短视频`,`B站 / 哔哩哔哩` 转为 `视频`,`公众号 / 微信公众号` 转为 `微信`。所以可以放心传口语化平台名

### 4. 数据少时的诊断流程(重要)
如果 `analyze_topic` 返回的声量/`sample_posts` 返回的 `count` 明显偏少(例如声量 < 100),按顺序尝试:
1. **检查关键词是否过长**:`瑞幸咖啡品牌` → 改成 `瑞幸`(关键词太具体会过滤掉大量相关讨论)
2. **加视频字段**:加 `--search-fields title content video_asr video_ocr screenshot` —— 短视频内容的核心信息常在语音/画面字幕里
3. **扩大 datasource**:从默认 3 平台扩到 `--datasource 微博 小红书 短视频 视频 微信`(覆盖更多内容生态)
4. **放宽时间窗**:`--days 7` 或 `--days 30`(注意:最大 365 天)

### 5. 配额节省
- 用户问"看看 XX 热搜"通常只需要 `query_hot_list`,不要叠加 `analyze_topic` + `sample_posts` 三连击
- 用户没明确要求关联话题时,**不要加 `--with-clusters`**(单独消耗 1 次额度)

### 6. 结果解读
返回的 JSON 较长时,用 `head` / `jq` 截取关键字段展示给用户;**不要把完整 JSON 灌给用户看**。

## 典型工作流

**场景 A - 用户:"今天微博热搜前 10 是什么?"**
```bash
python3 ./scripts/query_hot_list.py --source 微博 --size 10
```
解读 top 10,简单评论。**消耗 1 次**

**场景 B - 用户:"分析一下瑞幸最近一周的口碑"**
```bash
python3 ./scripts/analyze_topic.py --topic '瑞幸' --days 7
```
基于声量/情感/互动数据给出洞察(默认覆盖微博+小红书+短视频)。**消耗 1 次**

**场景 C - 用户:"看看小红书上'夏日防晒'用户都在说什么"**
```bash
python3 ./scripts/sample_posts.py --topic '夏日防晒' --datasource 小红书 --size 30 --order 互动数 --search-fields title content screenshot
```
拉高互动样本,提炼用户态度。`screenshot` 字段帮你捞到图片 OCR 内容(小红书图文笔记的核心信息常在图里)。**消耗 1 次**

**场景 D - 完整热搜情报(用户明确要深度分析)**
```bash
# 1. 看榜
python3 ./scripts/query_hot_list.py --source 微博 --size 20
# 2. 用户挑一个话题
python3 ./scripts/analyze_topic.py --topic '挑出的话题' --with-clusters
# 3. 取代表帖
python3 ./scripts/sample_posts.py --topic '挑出的话题' --size 30 --order 互动数
```
**消耗 4 次**(榜单 1 + 分析含聚类 2 + 采样 1)

## 能力边界(诚实告知)

✅ **擅长**:
- 已上热搜的话题(`query_hot_list` 直接拉)
- **头部消费品牌**(瑞幸/喜茶/小米/泡泡玛特等)的多维度社媒分析
- **品类词**(国货美妆/夏日防晒/新能源车/宠物经济)的跨平台对比
- **热门事件**(618/双十一/某热播综艺/某品牌发布会)的传播分析

❌ **不擅长**:
- **长尾/小品牌/B2B 类目**:讨论量太低,情感占比、平台分布等指标没有统计意义
- **实时危机预警**:数据 T+1,做不了"刚发生 5 分钟"级别的监测
- **热搜榜上的小红书**:小红书没有热搜榜接入(用 `analyze_topic` 查任意话题在小红书的表现仍然完整可用)
- **未公开内容**:私域/群聊/封闭社区数据不在范围

## 异常处理

| 异常 | 含义 | 处理 |
|---|---|---|
| 退出码 3 + stderr 飞书 URL | 配额耗尽 | 转告用户,引导填表升级 |
| 退出码 2 + JSON `error` | 网络/服务异常 | 提示稍后重试,不要循环重试 |
| `count: 0` 或声量极低 | 该话题在该时间窗内数据稀疏 | 走"数据少时的诊断流程"(见上) |
| 退出码 1 | 参数错误 | 检查 `--source` / `--topic` / `--datasource` 是否正确 |
| `当前选择的时间范围不足一个自然日` | `--days` 太小或时间窗跨度 < 24h | 改成 `--days 1` 起步 |

## 数据时效

- 热搜榜单:实时(5 分钟级延迟)
- 话题分析/原帖:T+1(前一天数据完整)

## 升级到无限额度

免费 200 次用完后,填写以下飞书表单联系商务:
**https://tj4ovkghqw.feishu.cn/share/base/form/shrcnHBiiUFOUhRO7Y6H6eeEbQd**
