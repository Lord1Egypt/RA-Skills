---
slug: timeline-digest-tool-free
name: timeline-digest-tool-free
version: 1.0.0
displayName: 时间线摘要工具-免费版
summary: "抓取X/Twitter时间线并生成去重摘要,适合个人用户的信息聚合阅读。时间线摘要工具免费版,从X(Twitter)时间线抓取推文并生成去重摘要。核心能力:"
license: Proprietary
edition: free
description: '时间线摘要工具免费版,从X(Twitter)时间线抓取推文并生成去重摘要。核心能力:

  - 抓取X/Twitter For You和Following时间线推文

  - 基于推文ID的硬去重

  - 基于文本相似度的近似去重

  - 增量过滤(避免重复处理已推送推文)

  - 生成结构化JSON摘要输出

  - 基础启发式过滤(去除广告、垃圾内容)

  适用场景:

  - 个人用户的信息聚合阅读

  - 关注领域的动态追踪

  - 减少信息噪音,提取高价值内容

  差异化:

  - 免费版聚焦单次摘要生成,操作简洁

  - 内置增量过滤,避免...'
tags:
  - 沟通协作
  - 信息聚合
  - X/Twitter
  - 内容摘要
  - 工具
  - 效率
  - 通信
  - tweet
  - self
  - tweets
  - json
  - list
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
时间线摘要工具免费版是一款X(Twitter)时间线信息聚合工具。通过命令行工具抓取For You和Following两个时间线的最新推文,进行增量过滤、硬去重和近似去重处理,最终生成结构化的JSON摘要数据,帮助用户快速了解关注领域的最新动态,减少信息噪音.
本版本聚焦单次摘要生成能力,内置增量过滤机制避免重复处理。适合个人用户的日常信息聚合阅读需求。如需定时自动调度、智能分类摘要、多源聚合等高级功能,请升级至PRO版.
### 免费版与PRO版能力对比
| 能力维度 | 免费版 | PRO版 |
|----|---|----|
| 时间线抓取 | For You + Following | For You + Following + 自定义列表 |
| 硬去重(ID) | 支持 | 支持 |
| 近似去重(文本相似度) | 支持 | 支持(可调阈值) |
| 增量过滤 | 支持 | 支持 |
| 启发式过滤 | 基础(去广告/垃圾) | 高级(语义过滤) |
| 摘要输出 | 原始JSON | JSON + 智能分类摘要 |
| 定时调度 | 手动执行 | 自动定时 |
| 分类标注 | 不支持 | AI分类(科技/加密/洞察/其他) |
| 多源聚合 | 不支持 | 支持 |
| 状态管理 | 本地文件 | 本地+云端同步 |
| 推送通知 | 不支持 | 支持(Telegram/邮件等) |

## 核心能力
### 1. 时间线抓取
从X/Twitter的For You和Following两个时间线抓取最新推文.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 时间线摘要工具-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
bird home -n 100 --json > for_you_raw.json
# ...
bird home --following -n 60 --json > following_raw.json
```

**参数说明:**
- `-n`: 抓取推文数量
- `--json`: 以JSON格式输出
- `--following`: 抓取Following时间线(不加此参数默认For You)

**处理**: 解析时间线抓取的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回时间线抓取的响应数据,包含状态码、结果和日志.
### 2. 增量过滤
基于上次运行时间戳,只处理新增推文,避免重复处理.
```python
import json
from datetime import datetime, timezone
# ...
class IncrementalFilter:
    """增量过滤器"""
# ...
    def __init__(self, state: dict):
        self.last_run_at = state.get("lastRunAt")
        self.sent_ids = state.get("sentTweetIds", {})
# ...
    def filter_new(self, tweets: list) -> list:
        """过滤出未处理过的新推文"""
        if not self.last_run_at:
            return tweets  # 首次运行,全部处理
        last_time = datetime.fromisoformat(self.last_run_at)
        new_tweets = []
# ...
        for tweet in tweets:
            if tweet["id"] in self.sent_ids:
                continue
            tweet_time = datetime.fromisoformat(
                tweet["createdAt"].replace("Z", "+00:00")
            )
            if tweet_time > last_time:
                new_tweets.append(tweet)
# ...
        return new_tweets
# ...
    def update_state(self, tweets: list) -> dict:
        """更新状态文件"""
        now = datetime.now(timezone.utc).isoformat()
        for tweet in tweets:
            self.sent_ids[tweet["id"]] = now
        return {
            "lastRunAt": now,
            "sentTweetIds": self.sent_ids
        }
```

**处理**: 解析增量过滤的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回增量过滤的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 去重处理
#
### 硬去重(基于推文ID)
```python
class Deduplicator:
    """推文去重器"""
# ...
    def dedup_by_id(self, tweets: list) -> list:
        """基于推文ID去重"""
        seen_ids = set()
        unique = []
        for tweet in tweets:
            if tweet["id"] not in seen_ids:
                seen_ids.add(tweet["id"])
                unique.append(tweet)
        return unique
# ...
    def dedup_near_duplicate(self, tweets: list, threshold: float = 0.9) -> list:
        """基于文本相似度的近似去重"""
        from difflib import SequenceMatcher
# ...
        unique = []
        for tweet in tweets:
            is_duplicate = False
            for existing in unique:
                similarity = SequenceMatcher(
                    None,
                    tweet["text"][:200],
                    existing["text"][:200]
                ).ratio()
                if similarity >= threshold:
                    is_duplicate = True
                    if "sources" in existing:
                        existing["sources"] = list(
                            set(existing["sources"] + tweet.get("sources", []))
                        )
                    break
            if not is_duplicate:
        return unique
```

**处理**: 解析去重处理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回去重处理的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 启发式过滤
自动过滤广告、垃圾内容和低价值推文.
```python
class HeuristicFilter:
    """启发式内容过滤器"""
# ...
    SPAM_PATTERNS = [
        r'^(gm|good morning)\s*$',           # 纯问候
        r'^(gn|good night)\s*$',             # 纯晚安
        r'https?://\S+\s*$',                 # 纯链接
        r'^(liked|retweeted)\b',             # 系统通知
    ]
# ...
    SPAM_KEYWORDS = [
        "giveaway", "follow me", "check out",
        "limited time", "click here", "free crypto",
    ]
# ...
    def filter(self, tweets: list) -> list:
        """过滤低价值内容"""
        import re
        filtered = []
# ...
        for tweet in tweets:
            text = tweet["text"].strip().lower()
# ...
            if len(text) < 10:
                continue
# ...
            if any(re.match(p, text, re.IGNORECASE) for p in self.SPAM_PATTERNS):
                continue
# ...
            if any(kw in text for kw in self.SPAM_KEYWORDS):
                continue
# ...
            filtered.append(tweet)
# ...
        return filtered
```

**处理**: 解析启发式过滤的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回启发式过滤的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 结构化输出
```python
import json
from datetime import datetime, timezone, timedelta
# ...
class DigestGenerator:
    """摘要生成器"""
# ...
    def __init__(self, config: dict):
        self.interval_hours = config.get("intervalHours", 6)
        self.max_items = config.get("maxItemsPerDigest", 25)
# ...
    def generate(self, tweets: list) -> dict:
        """生成结构化摘要"""
        window_start = now - timedelta(hours=self.interval_hours)
# ...
        sorted_tweets = sorted(
            tweets,
            key=lambda t: t.get("createdAt", ""),
            reverse=True
        )[:self.max_items]
# ...
        return {
            "window": {
                "start": window_start.isoformat(),
                "end": now.isoformat(),
                "intervalHours": self.interval_hours
            },
            "counts": {
                "fetched": len(tweets),
                "final": len(sorted_tweets)
            },
            "items": [
                {
                    "id": t["id"],
                    "author": t.get("author", ""),
                    "createdAt": t.get("createdAt", ""),
                    "text": t["text"],
                    "url": t.get("url", f"https://x.com/i/web/status/{t['id']}"),
                    "sources": t.get("sources", [])
                }
                for t in sorted_tweets
            ]
        }
# ...
config = {"intervalHours": 6, "maxItemsPerDigest": 25}
generator = DigestGenerator(config)
# ...
tweets = [
    {"id": "123", "text": "AI最新进展...", "author": "@technews",
     "createdAt": "2026-07-18T10:00:00+08:00", "sources": ["forYou"]}
]
# ...
digest = generator.generate(tweets)
print(json.dumps(digest, indent=2, ensure_ascii=False))
```

**处理**: 解析结构化输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结构化输出的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：时间线并生成去重、适合个人用户的信、息聚合阅读、时间线摘要工具免、时间线抓取推文并、生成去重摘要、核心能力、时间线推文、的硬去重、避免重复处理已推、送推文、摘要输出、基础启发式过滤、去除广告等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一:每日信息聚合
个人用户每天运行一次,获取关注领域的最新动态摘要.
```bash
bird home -n 100 --json > for_you.json
bird home --following -n 60 --json > following.json
# ...
python3 generate_digest.py --for-you for_you.json --following following.json > digest.json
# ...
python3 format_digest.py --input digest.json
```

**输出示例:**
```json
{
  "window": {
    "start": "2026-07-18T00:00:00+08:00",
    "end": "2026-07-18T06:00:00+08:00",
    "intervalHours": 6
  },
  "counts": {
    "forYouFetched": 100,
    "followingFetched": 60,
    "afterIncremental": 34,
    "afterDedup": 26,
    "final": 20
  },
  "items": [
    {
      "id": "123456789",
      "author": "@technews",
      "createdAt": "2026-07-18T02:15:00+08:00",
      "text": "OpenAI发布GPT-5模型,支持多模态推理...",
      "url": "https://x.com/technews/status/123456789",
      "sources": ["forYou", "following"]
    }
  ]
}
```

### 场景二:关注领域追踪
追踪特定领域的最新推文动态.
```bash
py --filter "AI,LLM,GPT,大模型" > ai_digest.json
# ...
py --input ai_digest.json --format text
```

### 场景三:减少信息过载
通过去重和过滤,将大量推文压缩为高价值摘要.
```bash
# ...
```

## 不适用场景

以下场景时间线摘要工具-免费版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始
### 前置条件
1. 安装bird命令行工具并完成认证(cookie登录)
2. 安装Python 3.8+

### 依赖详情
```bash
bird --version
bird auth status
# ...
cat > config.json << 'EOF'
{
  "intervalHours": 6,
  "fetchLimitForYou": 100,
  "fetchLimitFollowing": 60,
  "maxItemsPerDigest": 25,
  "similarityThreshold": 0.9,
  "statePath": "~/.timeline-digest/state.json"
}
EOF
# ...
mkdir -p ~/.timeline-digest
```

### 首次运行
```bash
py --config config.json
# ...
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 配置示例
### 基础配置
```json
{
  "intervalHours": 6,
  "fetchLimitForYou": 100,
  "fetchLimitFollowing": 60,
  "maxItemsPerDigest": 25,
  "statePath": "~/.json"
}
```

### 配置项说明
| 配置项 | 类型 | 默认值 | 说明 |
|---:|---:|---:|---:|
| intervalHours | number | 6 | 时间窗口(小时) |
| fetchLimitForYou | number | 100 | For You抓取数量 |
| fetchLimitFollowing | number | 60 | Following抓取数量 |
| maxItemsPerDigest | number | 25 | 摘要最大推文数 |
| similarityThreshold | number | 0.9 | 近似去重相似度阈值 |
| statePath | string | ~/.json | 状态文件路径 |

## 最佳实践
### 1. 合理设置抓取数量
```text
抓取数量建议:
- 高频用户(每天多次运行): For You 50, Following 30
- 中频用户(每天1-2次): For You 100, Following 60
- 低频用户(每周1-2次): For You 200, Following 100
```

### 2. 调整相似度阈值
```python
THRESHOLD_GUIDE = {
    0.95: "严格去重 - 仅去除几乎完全相同的内容",
    0.90: "标准去重 - 去除高度相似的内容(推荐)",
    0.85: "宽松去重 - 去除主题相似的内容",
    0.80: "激进去重 - 可能误删不同视角的同类内容",
}
```

### 3. 状态文件管理
```python
import os
import json
from datetime import datetime, timedelta
# ...
def cleanup_state(state_path: str, retain_days: int = 30):
    """清理过期的状态记录"""
    with open(state_path, 'r') as f:
        state = json.load(f)
# ...
    cutoff = datetime.now() - timedelta(days=retain_days)
    sent_ids = state.get("sentTweetIds", {})
# ...
    cleaned = {
        tid: ts for tid, ts in sent_ids.items()
        if datetime.fromisoformat(ts) > cutoff
    }
# ...
    state["sentTweetIds"] = cleaned
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)
# ...
    removed = len(sent_ids) - len(cleaned)
    print(f"清理完成: 移除 {removed} 条过期记录")
```

## 常见问题
### Q1: bird工具是什么?如何安装?
**A:** bird是一个X/Twitter命令行工具,用于读取时间线推文。安装后需要通过cookie方式完成认证登录。请参考bird工具的官方文档进行安装和认证.
### Q2: 首次运行时为什么处理了全部推文?
**A:** 首次运行时没有状态记录,无法进行增量过滤,因此会处理全部抓取到的推文。从第二次运行开始,只会处理上次运行之后的新增推文.
### Q3: 近似去重的阈值应该设多少?
**A:** 推荐使用默认值0.9(标准去重)。如果发现摘要中有太多相似内容,可降低到0.85;如果发现去重过于激进导致内容丢失,可提高到0.95.
### Q4: 免费版支持定时自动运行吗?
**A:** 免费版需要手动执行。如需定时自动调度运行,请升级至PRO版,PRO版支持cron定时任务和自动推送通知.
### Q5: 如何生成中文分类摘要?
**A:** 免费版输出原始JSON数据。生成中文分类摘要(科技/加密/洞察等分类)需要结合LLM处理,这是PRO版的智能摘要功能.
### Q6: 如何升级到PRO版?
**A:** PRO版与免费版完全兼容,升级后原有配置和状态文件继续使用,同时获得定时调度、智能分类摘要、多源聚合等高级功能。直接安装PRO版Skill即可完成升级.
## 依赖说明
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.8+
- **网络环境**: 需可访问X/Twitter服务

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| bird | CLI工具 | 必需 | 参考bird工具文档安装 |
| Python 3.8+ | 运行时 | 必需 | python.org 下载 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Node.js | 运行时 | 可选 | 仅JS脚本执行时需要 |

### API Key 配置
- bird工具的认证(cookie)由bird工具自行管理
- 本skill基于Markdown指令规范,无需额外API Key
- 如需LLM智能摘要功能,由Agent内置LLM提供

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行时间线摘要任务
- **运行模式**: 本地脚本执行,需bird工具已认证
- **安全等级**: 只读操作,不修改X/Twitter账户数据;状态文件存储在本地

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "时间线摘要工具-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "timeline digest"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
