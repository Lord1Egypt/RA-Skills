# v17 LLM 答案层完整策略

**版本**: v17.2 → v17.4 → v17.5 三个迭代合成 (2026-06-04)
**核心**: 把 star-search 从"返 8 条蓝链"升级到"返 1 段 AI 答案 + 来源 + 3 个相关问题"
**目标**: 赶超 Perplexity AI 的免费中文版

---

## 1. 核心思路: 三层架构

```
[用户 query]
  → [v17.2 答案生成: DeepSeek-V4-Flash]
    → 1 段 200-400 字答案 + 4-5 个 sources
  → [v17.5 4 类 prompt 分层]
    → query 分类 → 选专用 prompt 模板 → 答案风格差异化
  → [v17.4 follow-up 生成]
    → 3 个相关问题 chips (点击触发新搜索)
```

**总耗时**: 4-9s 端到端 (search 1-3s + answer 2-4s + followups 1-2s)

---

## 2. v17.2 答案生成 (`generate_answer`)

### 2.1 LLM 选型

| 模型 | 优势 | 劣势 |
|---|---|---|
| **DeepSeek-V4-Flash** ⭐ | **免费** (new-api 62.234.39.247:8080), 速度 2-3s, 400-800 tokens, 中文强 | 偶尔简略 |
| GPT-4o-mini | 质量高 | 收费, 慢 |
| Qwen2.5-7B | 中文好 | 需自己部署 |

**默认 LLM_BASE_URL**: `http://62.234.39.247:8080/v1` (new-api 中转)

### 2.2 调用方式

```python
# 异步 + executor 避免阻塞 FastAPI
import asyncio, urllib.request, json

def _call_llm():
    req_data = {
        "model": LLM_MODEL,  # DeepSeek-V4-Flash
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"query: {query}\n\n搜索结果:\n{formatted}"}
        ],
        "temperature": 0.3,
        "max_tokens": 450,
    }
    req = urllib.request.Request(
        f"{LLM_BASE_URL}/chat/completions",
        data=json.dumps(req_data).encode(),
        headers={"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

data = await asyncio.get_event_loop().run_in_executor(None, _call_llm)
```

### 2.3 ⚠️ 关键: 服务器无 `~/.hermes/auth.json` 的部署坑

**问题**: 本地开发时, `~/.hermes/auth.json` 存 newapi key. **服务器是 `ubuntu` 用户, 没有 `~/.hermes/`**, LLM_API_KEY 永远是 None.

**错误现象**:
```json
{"answer": null, "error": "LLM_API_KEY not configured"}
```

**修法** (已 ship 到 `scripts/answer.py`): 三级 key 加载, 按优先级
1. `os.environ.get("LLM_API_KEY")` (env var, 最高)
2. `/home/ubuntu/star-search/.env` 文件解析 (server-specific)
3. `~/.hermes/auth.json` 本地开发 (lowest)

```python
_NEWAPI_KEY = None
_env_path = os.path.expanduser("/home/ubuntu/star-search/.env")
if os.path.exists(_env_path):
    with open(_env_path) as f:
        for line in f:
            if line.startswith("LLM_API_KEY="):
                _NEWAPI_KEY = line.split("=", 1)[1].strip()
                break
if not _NEWAPI_KEY:
    try:
        auth_path = os.path.expanduser("~/.hermes/auth.json")
        if os.path.exists(auth_path):
            with open(auth_path) as f:
                _NEWAPI_KEY = json.load(f).get("providers", {}).get("newapi", {}).get("api_key")
    except Exception:
        pass
LLM_API_KEY = os.environ.get("LLM_API_KEY", _NEWAPI_KEY or "")
```

**部署步骤**:
1. 写 `/home/ubuntu/star-search/.env`:
   ```
   LLM_API_KEY=sk-2ME...
   LLM_BASE_URL=http://62.234.39.247:8080/v1
   LLM_MODEL=DeepSeek-V4-Flash
   ```
2. `chmod 600 .env` (含 key, 不能 world-readable)
3. 验证: `python3 scripts/answer.py` 应该输出 `{"answer": "...", ...}`

### 2.4 返回结构

```json
{
  "answer": "200-400 字答案",
  "model": "DeepSeek-V4-Flash",
  "elapsed_ms": 2600,
  "tokens": 678,
  "sources": ["data.eastmoney.com", "finance.sina.com.cn", ...]
}
```

**v17.5 加**:
```json
{
  "category": "finance",  // finance / tech / news / general
  "followups": ["...3 个相关问题..."]  // v17.4 加
}
```

---

## 3. v17.5 4 类 Prompt 分层 (`_classify_query`)

### 3.1 query 分类逻辑 (关键词匹配, 不调 LLM)

| 类别 | 关键词 (部分) | 提示词来源 |
|---|---|---|
| **finance** | 股票/股价/A股/上证/深证/港股/美股/纳斯达克/道琼斯/标普/基金/行情/涨停/跌停/个股/板块/开盘/收盘/市值/财报/营收/利润/PE/PB/估值/成份股/龙虎榜/北向资金/融资融券/ETF/指数 | 彭博/华尔街见闻风格 |
| **tech** | gpt/claude/llm/ai/人工智能/机器学习/深度学习/神经网络/大模型/openai/anthropic/gemini/芯片/gpu/cuda/半导体/python/javascript/rust/docker/react/vue/api/sdk/github/开源/算法/transformer | 36kr/极客公园风格 |
| **news** | 新闻/今天/昨日/最新/今日/本周/上周/本月/消息/报道/官方/宣布/发布/发表/声明/回应/辟谣/热搜/突发/现场/记者/媒体 | 澎湃/财新风格 |
| **general** | 其余 | Perplexity 风格 |

**注意优先级**: finance > tech > news > general (先匹配先返回)

### 3.2 4 个 Prompt 模板的差异化

| 维度 | finance | tech | news | general |
|---|---|---|---|---|
| **数字处理** | **粗体强制** | **版本号/参数** | **数据出处** | 突出即可 |
| **诚实原则** | 严禁编价格, 必说"查行情网站" | 区分官方/媒体 | 区分事实/评论 | 通用诚实 |
| **结构** | 多空观点 | 核心+参数+影响 | 5W1H+多角度 | 自由 |
| **来源偏好** | 东财/新浪 > 雪球 > 知乎 | 官方/知名媒体 | 主流官方媒体 | 不限 |
| **max_tokens** | 450 | 450 | 450 | 450 |

**完整 4 个 prompt 全文见 `scripts/answer.py:54-191`** (不重复贴, 文件里是 source of truth).

### 3.3 实测 4 类 query

```
=== 比亚迪股价 (finance) ===
"**5月**销量结束**8个月**下滑...
多方认为销量拐点确立; 空方担忧行业价格战...
来源: data.eastmoney.com / finance.sina.com.cn"

=== Python 3.13 (tech) ===
"Python **3.13** 于 **2024年10月** 发布...
**JIT 编译器** + **自由线程**模式 (无需 GIL)..."

=== 特朗普推文 (news) ===
"当地时间**2025-04-04**晚...连发数十条推文...
支持者认为反映基层不满; 批评者指出数据存出入 (3.9% 失业率)..."

=== 如何煮咖啡 (general) ===
"抱歉, 提供的搜索结果不相关...请换关键词..."
```

### 3.4 ⚠️ 易错: 关键词匹配要全小写 or 全大写

```python
tech_kw = ('gpt', 'claude', ...)  # 全小写
q = query.lower()  # 强制小写
if any(kw in q for kw in tech_kw):
    return 'tech'
```

**坑**: `query.lower()` 只对英文友好, 中文不需要. **query 是中文** 也能 work (lowercase 对中文无影响).

### 3.5 3 类常见 query 边界

- `"OpenAI 上市"`: tech (命中 openai)
- `"上证指数今日收盘"`: finance (命中 上证 + 收盘)
- `"今天新闻"`: news (命中 今天 + 新闻, **注意 finance 不会先匹配**, finance 关键词是"今日"而非"今天")
- `"今天股市情况"`: finance (命中 股市)
- `"Python 教程"`: tech (命中 python)
- `"华为最新手机"`: news (命中 最新) - **但实际可能更适合 tech**

**已知缺陷**: 关键词匹配有歧义, **训练分类器或 LLM 分类** 是后续优化方向.

---

## 4. v17.4 Follow-up 问题生成

### 4.1 设计

**目标**: 答案下方加 3 个紫色 chips, 用户能一键深挖, 不用重新输入.

**生成方式**: 用 LLM 单独调一次, max_tokens=120 (30-50 tokens), +1-2s 延迟.

**失败降级**: 启发式模板 (4 类别, `{query} 财务报表` 等).

### 4.2 实现

```python
def _generate_followups(query, answer, domains, category):
    if not answer or len(answer) < 20:
        return []

    # 启发式 fallback
    def _template_fallback():
        if category == 'finance':
            return [f"{query} 财务报表", f"{query} 历史走势", f"{query} 行业对比"]
        elif category == 'tech':
            return [f"{query} 官方文档", f"{query} 实际应用", f"{query} 与同类对比"]
        elif category == 'news':
            return [f"{query} 事件背景", f"{query} 最新进展", f"{query} 各方反应"]
        else:
            return [f"{query} 详细教程", f"{query} 常见问题", f"{query} 相关推荐"]

    if not LLM_API_KEY:
        return _template_fallback()

    followup_prompt = """你是一个中文搜索助手, 根据用户的 query 和已生成的答案, 给出 3 个用户可能想问的相关问题.
要求:
1. 3 个问题, 简短 (5-15 字), 不带问号
2. 跟 query 主题相关但角度不同 (财报/对比/最新/详细等)
3. 适合用作"相关推荐"链接
4. 每行一个, 不要编号
示例 query: "比亚迪股价"
输出:
比亚迪 5月汽车销量
比亚迪 vs 特斯拉 销量对比
比亚迪 今日成交额
现在请根据下面的 query 和答案生成:
query: {query}
答案: {answer}
"""
    # 同步调用 (answer 已 1-3s, followup 再 +1s 可接受)
    req_data = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": followup_prompt.format(query=query, answer=answer[:500])}],
        "temperature": 0.7,
        "max_tokens": 120,
    }
    # ... (与 _call_llm 同)

    # 解析 3 行 (去前缀 "1. " 等, 去问号, 过滤 5-25 字)
    text = data['choices'][0]['message']['content'].strip()
    lines = [l.strip().lstrip('1234567890.-、) ').rstrip('?？')
             for l in text.split('\n') if l.strip()]
    valid = [l for l in lines if 5 <= len(l) <= 25]
    return valid[:3] if valid else _template_fallback()
```

### 4.3 ⚠️ 易错: 同步 vs 异步

`generate_answer` 用 `await run_in_executor` (async). **但 `_generate_followups` 内部调 LLM 用同步 urllib** (因为 answer 函数体已经 await 完, 同步阻塞 OK).

**不要**在 sync 函数里 await, **LSP 会报**: `"await" allowed only within async function`.

### 4.4 前端 chip 渲染 (CSS + JS)

```html
<div id="answer-followups-wrap" class="hidden mt-4">
  <div class="text-xs text-gray-500 mb-2">相关问题</div>
  <div id="answer-followups" class="flex flex-wrap gap-2"></div>
</div>
```

```css
.answer-followup-chip {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 5px 12px;
  background: rgba(168, 85, 247, 0.1);  /* 紫色 */
  border: 1px solid rgba(168, 85, 247, 0.3);
  color: #d8b4fe; font-size: 12px;
  border-radius: 999px; cursor: pointer;
  transition: all 0.2s;
}
.answer-followup-chip:hover {
  background: rgba(168, 85, 247, 0.2);
  border-color: rgba(168, 85, 247, 0.6);
  color: #f3e8ff; transform: translateY(-1px);
  box-shadow: 0 0 12px rgba(168, 85, 247, 0.3);
}
```

```javascript
// 渲染 + 点击触发新搜索
a.followups.forEach(q => {
  const chip = document.createElement('a');
  chip.href = '#';
  chip.className = 'answer-followup-chip';
  chip.textContent = '→ ' + q;
  chip.onclick = (e) => { e.preventDefault(); doSearch(q); };
  followupsEl.appendChild(chip);
});
```

**色系区分**: 来源 chips 蓝色 (`#60a5fa`), 相关问题 紫色 (`#a855f7`) - 视觉不混.

### 4.5 实测 followup 输出

| query | category | followups |
|---|---|---|
| 比亚迪股价 | finance | ["比亚迪 5月销量详情", "比亚迪 股价历史走势", "比亚迪 新能源车市占率"] |
| Python 3.13 | tech | (实测 3 个相关, 角度不同) |
| 特朗普推文 | news | (实测 3 个相关, 角度不同) |

---

## 5. 端到端流程图

```
[用户] 搜 "比亚迪股价"
  ↓
[前端] fetch POST /v1/search {query, top: 5, answer: true}
  ↓
[api_server]
  → search_async(query) → 16 引擎并发 → 5 条 results
  → if answer=true: 调用 answer.generate_answer(query, results, mode)
    → _classify_query → 'finance'
    → 用 SYSTEM_PROMPT_FINANCE
    → 调 LLM 2.4s → 答案 + 5 sources
    → _generate_followups(query, answer) → 3 个问题
  → 返回 {results, answer: {answer, model, elapsed_ms, tokens, sources, category, followups}}
  ↓
[前端] 渲染
  → 答案卡片 (玻璃态 + badge + 200-400 字)
  → 来源 chips (蓝色 5 个)
  → 相关问题 chips (紫色 3 个, 点击触发新搜索)
  → 8 条蓝链 (在下方)
```

---

## 6. 验收标准 (回归测试清单)

每次发版前必跑:

```python
# 4 类 query 分类测试
test_cases = [
    ('比亚迪股价', 'finance'),
    ('上证指数今日收盘', 'finance'),
    ('GPT-5 发布时间', 'tech'),
    ('Python 3.13 新特性', 'tech'),
    ('特朗普最新推文', 'news'),
    ('今日新闻', 'news'),
    ('如何煮咖啡', 'general'),
    ('北京旅游攻略', 'general'),
]
# _classify_query 全部正确

# 答案生成 e2e (公网 https://search.token-star.cn/v1/search)
{
  "query": "比亚迪股价", "top": 5, "answer": true
} → 必须返回
- answer (200-400 字, 含 **粗体**, 含"查行情网站"提示)
- sources (3-5 个域名, 东财/新浪优先)
- category = "finance"
- followups (3 个相关问题, 5-15 字)
- elapsed_ms < 5000
- tokens < 1500
```

---

## 7. 后续可优化方向

| 方向 | 价值 | 难度 |
|---|---|---|
| 答案缓存 (相同 query 30min 复用) | 省 LLM token, 速度↑ | 低 |
| 答案内联引用 [1][2][3] | 信任度↑ | 中 |
| 答案多语言 (英/日) | 国际化 | 中 |
| 答案支持 multi-turn (上下文累积) | 深度研究 | 高 |
| 自训练 query 分类 (代替关键词) | 准确率↑ | 高 |

---

## 8. 文件改动清单 (本策略相关)

- `scripts/answer.py` — 新文件, 6058→14956 bytes (3 次迭代)
- `scripts/api_server.py` — `/v1/search` 加 `answer` 字段, 新增 `/v1/answer` 端点
- `mcp_server.py` — `web_search` schema 加 `answer` 参数
- `index.html` — 加答案卡片 UI + 玻璃态 + 来源 chips (蓝) + followup chips (紫) + shimmer
- `references/v17-llm-answer-quality-strategy.md` — 本文件
