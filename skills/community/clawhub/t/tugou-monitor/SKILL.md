---
name: tugou-monitor
description: Read public Web2 trending news and hot-search feeds from 土狗气象台, then extend promising topics with Binance Web3 public data. Supports status checks, latest messages, group filtering, hot-search inspection, meme-priority review, Chinese-topic token mapping, token audit, wallet/address lookup, smart-money cross-check, and meme/topic market validation workflows for OpenClaw agents.
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "\U0001F43E"
    install:
      - id: curl
        kind: brew
        formula: curl
        label: curl (HTTP client)
    os:
      - darwin
      - linux
      - win32
  version: 2.3.1
---

# 土狗气象台 Open Skill

读取土狗气象台公开热点 API，并在需要时联动 Binance Web3 的公开查询能力，把 Web2 热点补成可研判的链上题材。

这个 skill 的核心目标不是“自动找币”，而是：

- 先看热点和热搜
- 再提取关键词、人物、题材、梗词
- 再判断有没有链上映射
- 只有在出现明确 token / CA / 地址后，才继续做审计、聪明钱和持仓分析

默认公共入口：

- 土狗气象台：`https://tugoumeme.fun`
- Binance Web3：`https://web3.binance.com`

## 何时使用

当用户要做下面这些事时，用这个 skill：

- 看今天最值得关注的热点、热搜、重点消息
- 从 Web2 热点里找可能映射到链上的题材
- 检查某个 token / CA / 地址值不值得继续跟
- 判断某条热点是不是已经从 Web2 传播成链上交易话题
- 做 meme 币研究，尤其是中文区热点、中文梗和中文社区题材

## 能力矩阵

### 土狗气象台公开能力

- 系统状态：`GET /api/status`
- 消息列表：`GET /api/messages`
- 分组统计：`GET /api/channels/groups`
- 全平台热搜：`GET /api/hot-search/`
- 单平台热搜：`GET /api/hot-search/{source}`
- 热点搜索：`GET /api/hot-search/search`
- Meme 潜力榜：`GET /api/hot-search/ranking`

### Binance Web3 增强能力

- 关键词 / 题材 -> token 映射
- token search / meta / dynamic info
- token audit
- wallet holdings
- smart money
- social hype / unified rank
- meme rush / topic rush

## 土狗气象台 API

### 查看系统状态

```bash
curl -s "https://tugoumeme.fun/api/status"
```

### 获取最新消息

```bash
curl -s "https://tugoumeme.fun/api/messages?page=1&page_size=20"
```

### 按分组过滤

```bash
curl -s --get "https://tugoumeme.fun/api/messages" \
  --data-urlencode "group_name=微博监控" \
  --data-urlencode "page=1" \
  --data-urlencode "page_size=20"
```

### 获取重点消息

```bash
curl -s --get "https://tugoumeme.fun/api/messages" \
  --data-urlencode "is_meme=true" \
  --data-urlencode "page=1" \
  --data-urlencode "page_size=10"
```

### 获取分组统计

```bash
curl -s "https://tugoumeme.fun/api/channels/groups"
```

### 获取热搜

```bash
curl -s "https://tugoumeme.fun/api/hot-search/"
curl -s "https://tugoumeme.fun/api/hot-search/weibo"
curl -s "https://tugoumeme.fun/api/hot-search/douyin"
```

### 按关键词搜索热点

```bash
curl -s --get "https://tugoumeme.fun/api/hot-search/search" \
  --data-urlencode "keyword=OpenAI" \
  --data-urlencode "days=7" \
  --data-urlencode "limit=10"
```

### 获取 Meme 潜力榜

```bash
curl -s --get "https://tugoumeme.fun/api/hot-search/ranking" \
  --data-urlencode "window_hours=24" \
  --data-urlencode "limit=10"
```

## 关键词提取规则

默认不要假设 Web2 消息里会直接出现 CA。绝大多数情况下，先提取题材线索，再做链上映射。

优先提取：

1. 品牌 / 产品名
2. 人名 / 组织名
3. 事件 / 议题名
4. 梗词 / 出圈短语
5. token-like 线索，如 `$TRUMP`
6. 明确 CA / 钱包地址

优先从这些字段取词：

1. `content`
2. `ai_summary`
3. `ai_tags`
4. 热搜标题

默认去噪：

- 纯新闻套话：通报、表示、回应、发布
- 纯宏观词：社会、网友、平台、部门
- 纯情绪词：震惊、离谱、爆了
- 过泛行业词：AI、教育、金融、医疗

关键词分层：

- 高置信度：明确品牌、人名、项目名、`$TOKEN`
- 中置信度：明确事件或题材组合词
- 低置信度：只有情绪词或模糊口号

默认只对高置信度和中置信度词做 Binance 查询。

## 中文 Token / 中文梗优先映射

很多热点、meme 币线索和社区讨论先出现的是中文词，而不是英文符号。中文题材默认优先保留中文原词，不要过早翻译。

以下情况优先走中文映射：

- 热点本身是中文梗、中文短语、中文外号
- 社区讨论主要用中文
- 用户直接给出中文 token 名或中文 CA 线索
- 题材明显来自微博、公众号、抖音、华语 X 账号

中文映射顺序：

1. 中文原词
2. 中文变体 / 简繁体
3. 拼音
4. 明确社区别名
5. 已知 CA

不要做的事：

- 把中文梗直接翻成宽泛英文后硬搜
- 把中文动物梗直接映射成泛英文动物类老币
- 只因为英文语义接近就认定是同一个 token

中文映射结果分层：

- 强映射：中文原词本身就能锁定 token / 热度 / CA
- 弱映射：有候选，但证据不足
- 无映射：中文、拼音、变体都没有稳定结果

如果中文原词已经能锁定 token，就不要强行把结论改成英文。

## 高置信度中文锚点示例

### 龙虾热点

如果热点、KOL 发文、社区讨论或用户输入里明确提到：

- `龙虾`
- `养龙虾`
- `龙虾热点`

并且用户明确给出 CA：

- `0xeccbb861c0dda7efd964010085488b69317e4444`

那么默认应把：

- 中文题材：`龙虾`
- 主映射对象：`龙虾`
- CA：`0xeccbb861c0dda7efd964010085488b69317e4444`

视为高置信度锚点，然后继续做：

- token meta
- dynamic info
- audit
- social hype / meme rush
- smart money

这种情况不需要先从英文候选里反推主对象，应直接把中文题材 `龙虾` 作为主映射起点。

## 链上映射决策

如果只有关键词，没有 CA，按这个顺序查：

1. `token search`
2. `unified rank`
3. `social hype`
4. `meme rush / topic rush`
5. `smart money`
6. `audit`

如果是中文题材，先查：

1. 中文原词
2. 中文变体 / 简繁体
3. 拼音
4. 社区别名
5. 已知 CA

映射结果分成四档：

- 无映射
- 弱映射
- 明确映射
- 强映射

不要强行下结论的情况：

- 只有同名 token，没有热度和流动性
- 关键词过泛，命中无关老币
- 只有社交讨论，没有排行 / 资金 / 交易信号
- 搜到很多重名 token，但没有足够证据指向其中一个
- 只有英文近义词命中，但中文原词本身没有证据

这时应该写：

- “存在候选 token，但映射不稳定”
- “当前仅能确认弱映射，不能确认主映射对象”

## Meme 币研究模式

当热点明显偏梗、人物、抽象、争议、社区传播时，优先切换到 meme 模式。

常见触发信号：

- `is_meme=true`
- `ai_tags` 或 `ai_summary` 中出现：梗、二创、抽象、整活、出圈、共鸣、争议
- 热点来自微博热搜、抖音热搜、高频自媒体号
- 标题明显是人物梗、事件梗、台词梗、中文动物梗、中文谐音梗
- 用户明确说“meme”“梗币”“土狗”“有没有题材币”

不适合走 meme 模式：

- 严肃政经新闻
- 权威通报 / 官方数据
- 纯政策条文
- 没有情绪、没有人物、没有圈层传播感的硬新闻

Meme 查询链建议：

1. 提取 1-3 个高置信度梗词 / 人名 / 题材
2. `token search`
3. `social hype`
4. `meme rush / topic rush`
5. `unified rank`
6. `smart money`
7. `audit`

默认链优先级：

1. Solana：`CT_501`
2. BSC：`56`
3. Base：`8453`

## Binance Web3 常用查询

### Token Search

```bash
curl --location "https://web3.binance.com/bapi/defi/v5/public/wallet-direct/buw/wallet/market/token/search?keyword=pepe&chainIds=56,8453,CT_501&orderBy=volume24h" \
  --header "Accept-Encoding: identity"
```

### Token Meta

```bash
curl --location "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/dex/market/token/meta/info?chainId=56&contractAddress=<CA>" \
  --header "Accept-Encoding: identity"
```

### Token Dynamic Info

```bash
curl --location "https://web3.binance.com/bapi/defi/v4/public/wallet-direct/buw/wallet/market/token/dynamic/info?chainId=56&contractAddress=<CA>" \
  --header "Accept-Encoding: identity"
```

### Token Audit

如果当前环境不能稳定生成唯一 `requestId`，可以跳过这步，并明确告诉用户未执行审计。

```bash
curl --location "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/security/token/audit" \
  --header "Content-Type: application/json" \
  --header "source: agent" \
  --header "Accept-Encoding: identity" \
  --data '{
    "binanceChainId": "56",
    "contractAddress": "<CA>",
    "requestId": "<UUID-V4>"
  }'
```

### Wallet Holdings

```bash
curl --location "https://web3.binance.com/bapi/defi/v3/public/wallet-direct/buw/wallet/address/pnl/active-position-list?address=<ADDRESS>&chainId=56&offset=0" \
  --header "clienttype: web" \
  --header "clientversion: 1.2.0" \
  --header "Accept-Encoding: identity"
```

### Smart Money

```bash
curl --location "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money" \
  --header "Content-Type: application/json" \
  --header "Accept-Encoding: identity" \
  --data '{"smartSignalType":"","page":1,"pageSize":50,"chainId":"56"}'
```

### Social Hype / Unified Rank / Meme Rush

```bash
curl "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/social/hype/rank/leaderboard?chainId=56&sentiment=All&socialLanguage=ALL&targetLanguage=zh&timeRange=1" \
  -H "Accept-Encoding: identity"

curl -X POST "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/unified/rank/list" \
  -H "Content-Type: application/json" \
  -H "Accept-Encoding: identity" \
  -d '{"rankType":10,"chainId":"56","period":50,"sortBy":70,"orderAsc":false,"page":1,"size":20}'

curl -X POST "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list" \
  -H "Content-Type: application/json" \
  -H "Accept-Encoding: identity" \
  -d '{"chainId":"56","rankType":10,"limit":20}'
```

## 推荐工作流

### 工作流 A：热点巡检

1. 拉取 `/api/messages?page=1&page_size=50`
2. 优先看 `is_meme=true` 或 `ai_confidence>=70`
3. 同类去重后输出 5 条重点

### 工作流 B：热点 -> 关键词 / 题材映射

1. 从热点消息中提取关键词、品牌、人名、事件名、梗词、题材词
2. 先用土狗搜索确认热度时间跨度
3. 再用 Binance Token Search / Unified Rank / Social Hype 搜同关键词
4. 判断是 Web2 讨论、弱映射、明确映射还是强映射

### 工作流 C：热点 -> CA 增强分析

1. 确认 CA 与可能链
2. 查 token meta + dynamic info
3. 如可生成唯一 `requestId`，再查 audit
4. 输出项目名、符号、链、价格、市值、流动性、持有人、风险项

### 工作流 D：热点 -> Smart Money 验证

1. 若只有关键词，先做 token mapping
2. 若已有 CA，再查 token info
3. 再查 smart money
4. 输出是否有资金在跟、方向、是否仍 active、maxGain / exitRate

### 工作流 E：中文 meme 热点验证

1. 优先保留中文原词
2. 再查中文变体、拼音、社区别名
3. 若已给出 CA，直接进入 CA 分析
4. 最终保留中文主名称，不强制改成英文标题

## 输出模板

### 模板 A：关键词映射结果

- 原始热点：
- 提取关键词：
- 中文原词：
- 中文变体 / 拼音：
- 链上映射状态：无映射 / 弱映射 / 明确映射 / 强映射
- 候选 token：
- 主映射依据：
- 热度证据：
- 风险点：
- 下一步动作：

### 模板 B：已确认 CA 的研究卡片

- 对应热点：
- Token / Symbol：
- Chain：
- CA：
- 市场数据：
- 风险审计：
- Smart Money：
- 结论：

### 模板 C：Meme 题材研究卡

- 原始热点：
- 梗词 / 人物 / 题材：
- 查询链：
- 候选 token：
- 映射等级：观察级 / 叙事级 / 交易级 / 高风险级
- 热度证据：
- 资金证据：
- 风险证据：
- 结论：

## Agent 行为规则

1. 默认先用土狗气象台 API 做第一层热点提取，不要一上来就调用 Binance。
2. 只有在满足以下至少一项时，再调 Binance Web3：
   - 出现明确关键词 / 题材 / token 线索
   - 出现 CA / contract address
   - 出现明确钱包地址
   - 用户明确要求查币、查链上、查风险、查聪明钱
   - 热点明显是币圈题材
3. 如果链不确定，不要强行编造。可以给出可能链，但必须标记为推断。
4. 如果只有关键词没有 CA，优先用 Token Search / Unified Rank / Social Hype / Meme Rush，不要直接做 Audit。
5. Audit 结果仅作参考，不得表述成投资建议。
6. 如果 `hasResult != true` 或 `isSupported != true`，不要输出安全 / 不安全的强结论。
7. 地址和 CA 分析结果要保留原始链接或原始热点来源。
8. 默认是只读研究型 skill，不执行交易、不自动发帖、不调用任何私钥操作。

## 推荐提示词

- “帮我看今天最值得跟的 5 个热点，并判断哪些已经映射到链上。”
- “这个热点有没有对应 token / CA，可以继续研究吗？”
- “用中文题材优先映射规则看一下‘龙虾’这个热点。”
- “查这个 CA 值不值得继续跟，补上风险和聪明钱。”

## 故障排查

- 如果土狗气象台返回空或 5xx，先检查站点和 `/api/*` 是否在线。
- 如果 Binance Web3 返回空，先检查 chainId、CA、地址和 `Accept-Encoding: identity`。
- 如果 Audit 无法执行，通常是 `requestId` 不合格或当前 token 不支持审计。
- 如果没有 CA / 地址 / token 线索，但存在明确关键词或题材，可以先做 token mapping。
- 如果连关键词映射都没有结果，不要硬接 Binance 能力，直接保留为 Web2 热点分析。
