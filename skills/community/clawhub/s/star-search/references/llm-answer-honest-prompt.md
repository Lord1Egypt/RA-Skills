# LLM 答案层 — 诚实优先 Prompt (v17.2)

## 核心哲学

**诚实 > 编造**。LLM 看到 8 条搜索结果, **有具体数字才写**, **没数据就告诉用户查行情网站/官方源, 不要猜**。

这是 v17.2 的关键差异化 — v17.1 早期版本 LLM 拿到全是新闻的结果, 自己**编出** "比亚迪 94.78 元 -2.05%" 的价格 (实际是旧数据幻觉), 比不回答还糟糕。

## System Prompt 核心

```python
SYSTEM_PROMPT = """你是一个中文搜索引擎答案生成器, 风格类似 Perplexity AI.

输入: 用户 query + 8-10 条来自不同源(东方财富/新浪/雪球/IT之家/36kr/百度/搜狗等)的搜索结果.

输出要求:
1. 用 200-400 字中文给出直接答案 (3-5 句)
2. 数字答案要突出 (价格/数值/百分比)
3. 末尾列出 3-5 个来源域名, 格式: \\n\\n来源: domain1.com / domain2.com / domain3.com
4. 多个来源一致 → 直接给答案
5. 来源矛盾 → 列出分歧
6. 只基于提供的资料, 不要编造任何信息

⚠️ 重要诚实原则:
- 如果搜索结果是新闻/资讯/公告 (不是实时报价页), 不能编出具体价格数字
- 如果搜索结果没有具体的"当前股价 X 元", 应该说"实时股价请查询东方财富/新浪财经/同花顺等行情网站", 不要猜测
- 如果搜索结果是 5天/30天前的旧数据, 必须标注"截至 YYYY-MM-DD, ..."或"近期"
- 数字必须从源文 snippet 中能直接找到, 否则不写

财经 query 特殊处理:
- 股票 query → 优先找含"当前价/收盘/股价/涨幅"等词的源, 没有就告诉用户查行情网站
- 指数 query → 找具体点位, 没有就报"实时指数请查东方财富/新浪财经"
- 财报 query → 找具体数字, 没有就列已找到的关键数据

科技 query 特殊处理:
- 突出事实要点 (谁/什么/什么时候)
- 数字答案 (参数/价格/发布日期)

禁忌:
- 不要说"根据搜索结果"
- 不要说"以上信息仅供参考"
- 不要免责声明
- 不要编造任何源文没有的数字
- 直接给答案, 像 Perplexity 一样"""
```

## 关键 4 条诚实原则

| 原则 | 触发场景 | 行为 |
|---|---|---|
| **不能编价格** | 搜索结果全是新闻/资讯 | "实时报价请查询东方财富..." |
| **不能冒充今日** | 结果是 5/20 的旧数据 | "截至 5月20日, ..."或"近期..." |
| **数字必须源文有** | LLM 凭印象写数字 | 拒绝写, 改写"建议查 X" |
| **多源矛盾** | A 说升 B 说降 | 列出分歧, 不强行统一 |

## 答案行为矩阵 (实测)

| Query | 答案 | 评估 |
|---|---|---|
| "比亚迪股价" (结果全是新闻) | "实时股价请查询东方财富/新浪财经..." | ✅ 诚实 |
| "比亚迪 5月汽车销量" (结果没销量数据) | "未找到...建议查产销快报..." | ✅ 诚实 |
| "GPT-5 发布时间" (结果是第三方攻略) | "OpenAI 尚未公布...以官方为准" | ✅ 诚实 |
| "上证指数今日收盘" (有具体数字) | "上证指数最新 4075.10 点 涨幅 0.43%" | ✅ 准确 |
| "王者荣耀 S40 赛季" (结果是下载链接) | "尚未正式公布...建议查官网" | ✅ 诚实 |

## LLM 选型 — DeepSeek-V4-Flash via new-api

**为什么选它**:
- **完全免费** (new-api 渠道 12 已接入)
- **中文** 比英文模型强
- **2-3s** 生成 (比 GPT-4o 快 5 倍)
- **400-700 tokens** 答案长度刚好
- **走 new-api 62.234.39.247:8080** — 跟 star-search 同服务器, 网络 0 延迟

**为什么不用 GPT-4o/Claude**: 收费, 跟星尘的"完全免费中文版 Tavily"定位冲突。

## API key 配置 — 服务器 .env 模式

**问题**: 服务器是 `ubuntu` 用户, **没有 `~/.hermes/auth.json`**, `pip install mcp` 也被用户拒绝 (新依赖约束)。

**解法**: 写 server 专用 .env 文件, `answer.py` 优先级 加载:

```python
_NEWAPI_KEY = None

# 优先级 1: env var (用户主动设)
_NEWAPI_KEY = os.environ.get("LLM_API_KEY")

# 优先级 2: server-specific .env
if not _NEWAPI_KEY:
    _env_path = os.path.expanduser("~/star-search/.env")
    if os.path.exists(_env_path):
        with open(_env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("LLM_API_KEY=") and "=" in line:
                    _NEWAPI_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

# 优先级 3: 本地 dev ~/.hermes/auth.json
if not _NEWAPI_KEY:
    try:
        auth_path = os.path.expanduser("~/.hermes/auth.json")
        if os.path.exists(auth_path):
            with open(auth_path) as f:
                raw = f.read()
            m = re.search(r'sk-2ME[a-zA-Z0-9]+', raw)
            if m:
                _NEWAPI_KEY = m.group()
    except Exception:
        pass

LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "http://62.234.39.247:8080/v1")
LLM_API_KEY = os.environ.get("LLM_API_KEY", _NEWAPI_KEY or "")
```

**/home/ubuntu/star-search/.env** (server 专用):
```
LLM_BASE_URL=http://62.234.39.247:8080/v1
LLM_API_KEY=sk-2ME...DhYT
LLM_MODEL=DeepSeek-V4-Flash
LLM_TIMEOUT=15
```

## 调 LLM 模板

```python
import urllib.request, json

def generate_answer(query, results, mode=None):
    """调 DeepSeek 生成答案 + 降级返原始 results"""

    # 拼 8 条结果 (含 title + url + snippet)
    results_text = "\n\n".join([
        f"[{i+1}] {r.get('title', '')}\n{r.get('snippet', '')[:300]}\n{r.get('url', '')}"
        for i, r in enumerate(results[:10])
    ])

    user_msg = f"用户 query: {query}\n\n搜索结果:\n{results_text}\n\n请生成答案。"

    req_data = {
        "model": "DeepSeek-V4-Flash",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.3,  # 低温度, 减少幻觉
        "max_tokens": 800
    }

    try:
        req = urllib.request.Request(
            f"{LLM_BASE_URL}/chat/completions",
            data=json.dumps(req_data).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LLM_API_KEY}"
            }
        )
        resp = urllib.request.urlopen(req, timeout=LLM_TIMEOUT)
        data = json.loads(resp.read())
        answer_text = data["choices"][0]["message"]["content"].strip()
        sources = list({r.get('domain', '') for r in results if r.get('domain')})[:5]
        return {
            "answer": answer_text,
            "model": "DeepSeek-V4-Flash",
            "elapsed_ms": ...,
            "tokens": data.get("usage", {}).get("total_tokens", 0),
            "sources": sources
        }
    except Exception as e:
        # 降级: 调 LLM 失败 → 返 None (api_server 走 results 路径)
        return None
```

## 降级策略

**LLM 失败/超时 → 自动降级返原始 results 列表, 不影响主流程**:
```python
if req.answer:
    answer_data = await a.generate_answer(req.query, results[:req.top], mode=req.mode)
    if not answer_data:
        answer_data = {"answer": None, "degraded": True}  # 降级标记

resp_data = {
    "query": req.query,
    "count": len(results),
    "results": results[:req.top],
    "answer": answer_data  # 永远有 (None 或真实)
}
```

## 用户实测反馈

星尘在 v17.2 完成后说:
> "诚实 > 编造"

实测 query "比亚迪股价" (结果全是新闻), 答案 "实时股价请查询东方财富/新浪财经...", **没编价格**。用户评价 **"比之前强 100 倍"**。

## Pitfalls

1. **temperature 不要设太高** (>0.5 会让 LLM 自由发挥编数字) — 用 0.3
2. **max_tokens 不要太大** (>1000 会让答案变成长篇大论, 用户没耐心看) — 用 800
3. **timeout 不要太长** (>30s 用户会等不及) — 用 15s
4. **降级** 是必须的 — LLM 99% 成功率, 但 1% 失败要 graceful degrade
5. **不能把 sources 写死** — 从 results 动态取, LLM 答案末尾也带, 双重保险
6. **答案长度** — 200-400 字最佳, 太短没价值, 太长用户跳过
