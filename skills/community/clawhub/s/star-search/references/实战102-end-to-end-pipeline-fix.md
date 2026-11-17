# v20.102 端到端 Pipeline 整合 + 默认值错位修复 (2026-07-01)

## 触发场景

**<owner> 7/1 指导**: "我们开发的是一个对标百度搜索的新一代 AI 搜索引擎，然后我们自己用百度搜索，你这不是疯了吗" + "继续调研，充分调研" + "要分清楚是搜的问题、读的问题、再或者是整理的问题" + "<lead-reviewer> 只是反馈了一个方面，具有特殊性，我们完善的思路是要打造普适性的能力"。

**核心洞察**:
- <lead-reviewer> 反馈的"搜不到/抓不到"只是冰山一角 —— 所有国内 datacenter IP 用户搜中文都会遇到
- **问题不在搜和读，而在整理层** —— Perplexity 区别百度的核心
- **不破反爬，做"信源直连 + 整理层做厚"**

## 端到端实测先于代码改造 (<owner>方法论)

任何 LLM pipeline 改造前, 必须 `curl /v1/search` 跑一次看完整响应。**读 1000 行代码也找不到的 bug, 跑一次 curl 就能看到**。

### 4 个隐藏 bug + 修复

| # | Bug | 根因 | 修复 | 文件 |
|---|---|---|---|---|
| 1 | `answer=false` 默认 | SearchRequest 字段默认值错位 | 改 `default=True` | `api_server.py` line 150 |
| 2 | `cross_verify 'date' not defined` | line 274 调用 `get_source_credibility(url, date, query)` 但 date/query 未定义 | 改 `date_str = r.get('date','')` + `query_str = ''` | `cross_verify.py` line 274 |
| 3 | `brain_info None` | api_server 调 `_brain.analyze_query(query, use_cache=True, context=...)` 但 super_brain 不接受 `context` 参数 → TypeError → except 吞 | 改 `analyze_query(query, use_cache=True, context='', **kwargs)` | `super_brain.py` line 107 |
| 4 | `fetch_content RuntimeWarning: coroutine never awaited` | sync 函数 `asyncio.run(_go())` 在 FastAPI 已运行的 event loop 里冲突 | 改用 `nest_asyncio.apply() + loop.run_until_complete()` 兼容 | `fetch_content.py` |

### 修复后实测数据 (query="华为")

```json
{
  "count": 3,
  "elapsed_ms": 1,
  "brain_info": {"entity": "华为", "intent": "info"},
  "entity_card": {"name": "华为", "official_url": "https://www.huawei.com/"},
  "fetch_stats": {"requested": 3, "success": 2},
  "cross_verify": {"consensus_score": 0, "source_count": 3},
  "answer": {
    "answer": "1. 华为是一家全球领先的通信和信息技术解决方案提供商...\n来源域名: huawei.com, consumer.huawei.com, vmall.com",
    "sources": ["huawei.com", "consumer.huawei.com", "vmall.com"],
    "model": "glm-4-flash",
    "tokens": 949,
    "elapsed_ms": 7050
  }
}
```

## 4 阶段 Pipeline 完整链路 (v20.40 串联)

```
[1] LLM 理解  query → brain_info {entity/intent/category/expected_info}
     (super_brain + few-shot prompt + context 多轮注入)

[2] 智能搜索  brain 推荐引擎 → multi_search → bing_cn HTTP 主搜 (10 条) + 缓存 (TTL 30min)
     + sogou_http / baidu / 360 / weixin (playwright 兜底)

[3] LLM 整理  results → cross_verify (consensus_score + 30+ 来源可信度) + entity_card (KB lookup)
     + brain_ctx 注入 answer prompt

[4] 智能输出  LLM 整合 → fetch_content 自动抓前 3 条 → 响应
     + 标 credibility + fetch_success + content 字段
```

每条结果自动带：
- `credibility` (来源可信度 0-1)
- `fetch_success` (抓取成功标记)
- `content` (抓到的正文片段, 最多 5000 字符)
- `entity_card` (主体实体卡片: 名称/官网/简介/logo/tags)

## 关键工程经验 (必读, 未来迭代必用)

### 经验 1: sync 函数在 FastAPI async 环境里的 asyncio.run() 冲突

```python
# 错: 已有 loop 时 RuntimeWarning: coroutine never awaited
def fetch_url_playwright(url):
    async def _go():
        ...
    data = asyncio.run(_go())  # 这里警告

# 对: nest_asyncio 兼容
def fetch_url_playwright(url):
    import nest_asyncio
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(_go())
```

**症状**: `RuntimeWarning: coroutine 'fetch_url_playwright.<locals>._go' was never awaited`
**根因**: sync 函数嵌套 async + 已运行 loop → asyncio.run 失败但没抛
**修法**: nest_asyncio.apply() 让已运行 loop 可嵌套

### 经验 2: 函数签名匹配调用方期望

api_server 调 `analyze_query(query, use_cache=True, context=history_ctx)` —— 但 super_brain 不接受 context → TypeError → except 吞 → brain_info=None → entity_card 空。

**调试命令**:
```bash
grep -rn 'analyze_query' scripts/ | grep -v 'super_brain.py'
# 看所有调用方, 检查参数是否匹配
```

**修法 1**: super_brain 加 `**kwargs` 兼容
**修法 2**: api_server 去掉 `context=` 参数

### 经验 3: systemd restart 循环死锁

旧 unit `Restart=always` + `RestartSec=5` + 端口 5000 → 端口被僵尸 PID 占 → 新进程 EADDRINUSE → 永远循环。

**症状**: `systemctl status` 显示 `activating (auto-restart)` + `Result: exit-code` 不断刷屏
**根因**: 端口 5000 绑定失败 + systemd 立即重启
**修法**:
- `Restart=on-failure` (只在真崩时重启)
- `RestartSec=15` (足够时间端口释放)
- 不加 `ExecStartPre=sleep 3` (避免干扰 restart cycle)
- `StandardOutput=append:/home/ubuntu/.../logs/stdout.log` (ubuntu 用户可写)
- `Environment="PLAYWRIGHT_BROWSERS_PATH=/home/ubuntu/.cache/ms-playwright"`

### 经验 4: 端到端实测先于代码改造

任何 LLM pipeline 改造前, 必须 curl /v1/search 跑一次看完整响应。读 1000 行代码也找不到的 bug, 跑一次 curl 就能看到。

```bash
# 标准端到端测试
curl -s -X POST 'http://localhost:5000/v1/search' \
  -H 'Content-Type: application/json' \
  -d '{"query":"华为","top":3}' | python3 -m json.tool

# 检查 7 个核心字段
# 1. count (结果数 >0)
# 2. brain_info.entity (LLM 推 entity)
# 3. entity_card (KB 实体卡片)
# 4. fetch_stats (自动抓取)
# 5. cross_verify.consensus_score (多源一致度)
# 6. answer.answer (LLM 整合答案)
# 7. answer.sources (答案引用来源)
```

## systemd unit 完整模板

```ini
[Unit]
Description=star-search API server (v20.102)
Documentation=https://search.<service-domain>
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/star-search
Environment="PYTHONPATH=/home/ubuntu/.local/lib/python3.10/site-packages"
Environment="HOME=/home/ubuntu"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/ubuntu/.local/bin"
Environment="PLAYWRIGHT_BROWSERS_PATH=/home/ubuntu/.cache/ms-playwright"
ExecStart=/usr/bin/python3 /home/ubuntu/star-search/scripts/api_server.py --host <server-ip> --port 5000
Restart=on-failure
RestartSec=15
TimeoutStopSec=10
StandardOutput=append:/home/ubuntu/star-search/logs/stdout.log
StandardError=append:/home/ubuntu/star-search/logs/stderr.log
MemoryMax=512M
TasksMax=64
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/ubuntu/star-search /home/ubuntu/.star-search-cache /home/ubuntu/.cache

[Install]
WantedBy=multi-user.target
```

## 后续方向 (差 5.9pp 到 Perplexity 80% STRAT)

| 卡点 | 当前数据 | 方案 |
|---|---|---|
| BRAIN LLM 不稳 | 88-94% 区间 (同 query 跑 3 次: 88%/93.5%/92.6%) | 1. few-shot 加更多边界 case 2. temperature 降到 0.05 3. GLM-4-Plus 替代 Flash |
| 边界 case | 34/108 错: 模糊意图 (BRAIN 推 info 期望 transaction/news/comparison) | 1. BRAIN prompt 加"query 含价格/股价 必推 transaction" 强规则 2. 加 Tavily API 作 backup 主源 (1 迭代可上) |
| KB 实体覆盖 | 微信文章 (mp.weixin.qq.com) / 知乎 (需登录) / 雪球 (反爬) / 36kr (删文) | 1. miku-ai 集成 (公众号搜索 5/5 验证) 2. 雪球/36kr 专用 fetcher (v20.103) |

## <owner>工作方法论 (v20.102 落地)

1. **任何"用户反馈"先 4 阶段拆解** (搜/读/整/出), 别直接动手
2. **普适性 > 单用户特化** (<lead-reviewer> 只是入口, 问题是通用)
3. **默认值错位检查** (mode=quick + answer=false 这种"看起来对但实际错"的隐藏 bug)
4. **实测端到端一次** (curl /v1/search) > 读 1000 行代码定位
5. **不破反爬, 走"信源直连 + 整理层做厚"路线** (vs 军备竞赛)