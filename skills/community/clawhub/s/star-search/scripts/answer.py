"""
star-search 答案生成 (LLM 总结)
v17.2: 把 8 条 search results 总结成 1 段答案 + 来源
- DeepSeek-V4-Flash via new-api (免费)
- 失败/超时降级返原始 results

环境变量 (可选, 默认 62.234.39.247:8080):
  LLM_BASE_URL  - LLM API base URL
  LLM_API_KEY   - LLM API key
  LLM_MODEL     - 模型名 (默认 DeepSeek-V4-Flash)
"""

import os
import json
import re
import time
import asyncio
import urllib.request
import urllib.error

# 加载多个可能的 key 源 (按优先级)
# 1) env var LLM_API_KEY
# 2) /home/ubuntu/star-search/.env (server-specific)
# 3) ~/.hermes/auth.json (local dev)
_NEWAPI_KEY = None

# 2) server .env
_env_path = os.path.expanduser("~/star-search/.env")
if os.path.exists(_env_path):
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("LLM_API_KEY=") and "=" in line:
                _NEWAPI_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
                break

# 3) local ~/.hermes/auth.json
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
LLM_MODEL = os.environ.get("LLM_MODEL", "DeepSeek-V4-Flash")
LLM_TIMEOUT = int(os.environ.get("LLM_TIMEOUT", "15"))  # 答案生成 15s 上限
ANSWER_CACHE_TTL = int(os.environ.get("ANSWER_CACHE_TTL", "1800"))  # v17.6: 答案缓存 30min

# ============ v17.6: 答案缓存 ============
import hashlib
import os.path as _osp
import os as _os
_ANSWER_CACHE_DIR = _osp.expanduser("~/.star-search-cache/answers")
_os.makedirs(_ANSWER_CACHE_DIR, exist_ok=True)


def _answer_cache_key(query: str, category: str, n_results: int) -> str:
    """v17.6: 生成 cache key
    归一化 query (小写 + 去空格) + category + results 数量级
    """
    q_norm = query.lower().strip()
    # 数量级分桶: 0/1-3/4-6/7+ (避免 8 vs 9 命中不同 cache)
    n_bucket = "0" if n_results == 0 else f"{(n_results - 1) // 3}"
    raw = f"{q_norm}|{category}|{n_bucket}"
    return hashlib.md5(raw.encode()).hexdigest()[:16]


def _answer_cache_get(key: str):
    """从磁盘 cache 读答案, 过期返 None"""
    path = _osp.join(_ANSWER_CACHE_DIR, f"{key}.json")
    if not _osp.exists(path):
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        ts = data.get('ts', 0)
        if time.time() - ts > ANSWER_CACHE_TTL:
            return None
        # 移除 ts 字段 (返回时不带时间戳)
        data.pop('ts', None)
        return data
    except Exception:
        return None


def _answer_cache_set(key: str, answer_dict: dict):
    """写答案到磁盘 cache"""
    path = _osp.join(_ANSWER_CACHE_DIR, f"{key}.json")
    data = dict(answer_dict)
    data['ts'] = time.time()
    try:
        with open(path, 'w') as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass  # 缓存写失败不影响主流程


def _classify_query(query: str) -> str:
    """v17.5: 把 query 分类, 不同类别用不同 prompt 模板
    返回: 'finance' / 'tech' / 'news' / 'general'
    """
    q = query.lower()

    # 财经关键词
    finance_kw = ('股票', '股价', '股市', 'a股', 'A股', '大盘', '上证', '深证', '沪深',
                  '港股', '美股', '纳斯达克', '道琼斯', '标普', '基金', '基金净值',
                  '行情', '涨停', '跌停', '个股', '板块', '开盘', '收盘', '市值',
                  '财报', '营收', '利润', 'pe', 'pb', '估值', '成份股', '龙虎榜',
                  '北向资金', '融资融券', 'etf', '指数', '今日股价', '今日行情')
    if any(kw in query for kw in finance_kw):
        return 'finance'

    # 科技关键词
    tech_kw = ('gpt', 'claude', 'llm', 'ai', '人工智能', '机器学习', '深度学习',
               '神经网络', '大模型', 'openai', 'anthropic', 'google ai', 'gemini',
               '芯片', 'gpu', 'cuda', '半导体', 'ar/vr', '元宇宙', '区块链',
               'python', 'javascript', 'rust', 'golang', 'kubernetes', 'docker',
               'react', 'vue', 'api', 'sdk', 'github', '开源', '算法', 'transformer')
    if any(kw in q for kw in tech_kw):
        return 'tech'

    # 新闻关键词 (时间敏感)
    news_kw = ('新闻', '今天', '昨日', '最新', '今日', '本周', '上周', '本月', '消息',
              '报道', '官方', '宣布', '发布', '发表', '声明', '回应', '辟谣', '热搜',
              '突发', '现场', '记者', '媒体')
    if any(kw in query for kw in news_kw):
        return 'news'

    return 'general'


# ============ 4 个 Prompt 模板 (v17.5) ============

SYSTEM_PROMPT_FINANCE = """你是一个专业的中文财经分析师, 风格类似彭博/华尔街见闻.

输入: 用户 query (股价/指数/财报/基金/财经新闻) + 来自不同源的搜索结果 (每条标了 [1] [2] [3] 序号).

输出要求:
1. **数字优先**: 股价/指数/百分比/成交量/市值必须用粗体强调 (**XX**)
2. **诚实原则**: 如果源文 snippet 没给具体数字, 绝不能编, 必须说"实时数据请查询东方财富/新浪财经/同花顺等行情网站"
3. **时间敏感**: 标注数据时间 (今日/昨日/本周/近 X 天)
4. **多空观点**: 如果有分歧, 列出多方和空方观点
5. **v17.7 内联引用**: 重要数据/事件后面追加 [N] (N 对应搜索结果 [1]/[2]/[3]... 的序号), 例如 "比亚迪销量**5月**结束**8个月**下滑[2]"
6. **末尾来源**: 3-5 个域名, 优先权威源 (东方财富/新浪财经/同花顺 > 雪球/百度 > 知乎/微信)

格式: 200-300 字, 3-4 句
1. 直接报数字 (或明确说查行情网站) + 重要事实标 [N]
2. 简短分析 (涨跌原因/资金流向/政策影响) + 引用 [N]
3. 多空观点 (如有分歧)
4. 来源: domain1 / domain2 / domain3

⚠️ 财经 query 严禁编造数字!
- 没找到具体价格 → "实时股价请查询东方财富/新浪财经..."
- 源文只有新闻 → 列出新闻要点, 不报数字
- 数据过期 → 标注"截至 YYYY-MM-DD"
- 引用 [N] 必须有源文支撑, 不编序号

禁忌: 不要"根据以上资料", 不要免责声明, 不要"仅供参考"."""

SYSTEM_PROMPT_TECH = """你是一个中文科技资讯编辑, 风格类似 36kr / 极客公园.

输入: 用户 query (AI/产品/技术/编程/开源) + 来自不同源的搜索结果 (每条标了 [1] [2] [3] 序号).

输出要求:
1. **事实优先**: 谁/什么/什么时候/参数/价格/发布日期
2. **数字强调**: 版本号/参数/价格/发布日期用粗体 (**XX**)
3. **时间标注**: 注明事件时间 (今天/Yesterday/本周)
4. **专业准确**: 区分官方公告 vs 第三方解读
5. **v17.7 内联引用**: 重要事实 (版本/参数/价格/日期) 后面追加 [N] (N 对应 [1]/[2]/[3] 序号)
6. **末尾来源**: 3-5 个域名, 优先权威源 (官方文档/知名科技媒体/知名博客)

格式: 200-350 字, 3-5 句
1. 核心事实 (1-2 句, 含数字) + [N]
2. 关键参数/特性 (1-2 句) + [N]
3. 行业影响/对比 (1 句, 可选) + [N]
4. 来源: domain1 / domain2 / domain3

⚠️ 科技 query 重点:
- 模型/产品名 + 版本号要精确 (不要 GPT-4 写成 GPT-4.0)
- 发布日期/价格要有具体数字
- 区分官方 (openai.com, anthropic.com) vs 媒体解读 (36kr, ithome, sspai)
- 中文/英文术语都要准
- 引用 [N] 必须有源文支撑, 不编序号

禁忌: 不要广告, 不要 PR 文, 不要"非常优秀", 不要"划时代"."""

SYSTEM_PROMPT_NEWS = """你是一个中文新闻编辑, 风格类似 澎湃新闻 / 财新.

输入: 用户 query (新闻/事件/政策/社会热点) + 来自不同源的搜索结果 (每条标了 [1] [2] [3] 序号).

输出要求:
1. **时间敏感**: 标注事件时间, 区分 今日/昨日/本周
2. **多角度**: 至少 2 个不同观点/角度
3. **事实优先**: 5W1H (谁/什么/什么时候/哪里/为什么/如何)
4. **数字具体**: 人数/金额/比例/排名
5. **v17.7 内联引用**: 关键事实 (时间/数字/数据) 后面追加 [N] (N 对应 [1]/[2]/[3] 序号)
6. **末尾来源**: 3-5 个域名, 优先主流媒体 (新华社/人民网/澎湃/财新 > 36kr/虎嗅)

格式: 200-300 字, 3-4 句
1. 核心事件 (时间/地点/人物) + [N]
2. 关键细节 (数据/影响) + [N]
3. 不同角度 (如有分歧) + [N]
4. 来源: domain1 / domain2 / domain3

⚠️ 新闻 query 重点:
- 区分事实 vs 评论
- 标注"据 X 报道"或"X 官方称"
- 不预测未来, 只总结已知信息
- 多个源说同一事 → 直接给结论
- 源说矛盾 → 列出分歧
- 引用 [N] 必须有源文支撑

禁忌: 不预判, 不评论, 不站队, 不引战."""

SYSTEM_PROMPT_GENERAL = """你是一个中文搜索引擎答案生成器, 风格类似 Perplexity AI.

输入: 用户 query + 8-10 条来自不同源的搜索结果 (每条标了 [1] [2] [3] 序号).

输出要求:
1. 用 200-400 字中文给出直接答案 (3-5 句)
2. 数字答案要突出 (**XX**)
3. **v17.7 内联引用**: 重要事实后面追加 [N] (N 对应 [1]/[2]/[3] 序号)
4. 末尾列出 3-5 个来源域名
5. 多个来源一致 → 直接给答案
6. 来源矛盾 → 列出分歧
7. 只基于提供的资料, 不要编造任何信息

⚠️ 重要诚实原则:
- 数字必须从源文 snippet 中能直接找到, 否则不写
- 如果搜索结果没有相关数据, 告诉用户查更权威的源
- 旧数据要标注时间
- 引用 [N] 必须有源文支撑, 不编序号

禁忌: 不要"根据搜索结果", 不要"以上信息仅供参考", 不要免责声明, 不要编造任何源文没有的数字, 直接给答案, 像 Perplexity 一样"""


# query 类别 → prompt
_PROMPTS = {
    'finance': SYSTEM_PROMPT_FINANCE,
    'tech': SYSTEM_PROMPT_TECH,
    'news': SYSTEM_PROMPT_NEWS,
    'general': SYSTEM_PROMPT_GENERAL,
}


def _extract_domain(url: str) -> str:
    """从 URL 提取干净域名"""
    if not url:
        return ""
    m = re.search(r'https?://(?:www\.|m\.)?([^/]+)', url)
    if m:
        return m.group(1)
    return ""


def _format_results_for_llm(results: list, max_n: int = 10) -> str:
    """把 results 格式化成 LLM 易读的文本
    v17.7: 每条前面加 [N] 序号, 让 LLM 引用
    """
    lines = []
    for i, r in enumerate(results[:max_n], 1):
        title = r.get('title', '').strip()
        url = r.get('url', '').strip()
        snippet = r.get('snippet', '').strip() or r.get('desc', '').strip() or r.get('content', '').strip()
        engine = r.get('engine', '')
        domain = _extract_domain(url)
        lines.append(f"[{i}] {title}")
        if domain:
            lines.append(f"   来源: {domain}")
        if snippet:
            lines.append(f"   {snippet[:200]}")
        lines.append("")
    return "\n".join(lines)


def _extract_citations(answer: str, results: list) -> dict:
    """v17.7: 从 answer 里提取 [N] 引用, 返回 {1: title, 2: title, ...}
    用于前端 hover 显示来源标题
    """
    import re
    citations = {}
    for m in re.finditer(r'\[(\d+)\]', answer):
        try:
            n = int(m.group(1))
            if 1 <= n <= len(results):
                if n not in citations:
                    title = results[n-1].get('title', f'来源 {n}')
                    url = results[n-1].get('url', '')
                    citations[n] = {'title': title[:60], 'url': url}
        except ValueError:
            pass
    return citations


async def generate_answer(query: str, results: list, mode: str = "deep") -> dict:
    """
    用 LLM 总结 search results 成一段答案

    Returns:
        {
            "answer": "比亚迪 94.78 元 (-2.05%)...\\n\\n来源: eastmoney.com / ...",
            "model": "DeepSeek-V4-Flash",
            "elapsed_ms": 2370,
            "tokens": 413,
            "sources": ["eastmoney.com", "sina.com.cn", "xueqiu.com"]
        }

    失败/超时: 返回 {"answer": None, "error": "..."}
    """
    if not results:
        return {"answer": None, "error": "no results to summarize"}

    if not LLM_API_KEY:
        return {"answer": None, "error": "LLM_API_KEY not configured"}

    formatted = _format_results_for_llm(results)

    # 提取来源域名 (去重)
    domains = []
    seen = set()
    for r in results[:8]:
        d = _extract_domain(r.get('url', ''))
        if d and d not in seen:
            seen.add(d)
            domains.append(d)

    # v17.5: 分类 query, 选 prompt 模板
    category = _classify_query(query)
    system_prompt = _PROMPTS[category]

    # v17.6: 答案缓存 (按 query 归一化 + category, 30min TTL)
    cache_key = _answer_cache_key(query, category, len(results))
    cached = _answer_cache_get(cache_key)
    if cached is not None:
        cached['cached'] = True
        return cached

    # 调 LLM (异步, 避免阻塞)
    def _call_llm():
        req_data = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"query: {query}\n\n搜索结果:\n{formatted}"}
            ],
            "temperature": 0.3,
            "max_tokens": 450,  # v17.5: 略大以容纳多空观点/参数/影响分析
        }
        req = urllib.request.Request(
            f"{LLM_BASE_URL}/chat/completions",
            data=json.dumps(req_data).encode(),
            headers={
                "Authorization": f"Bearer {LLM_API_KEY}",
                "Content-Type": "application/json"
            }
        )
        with urllib.request.urlopen(req, timeout=LLM_TIMEOUT) as resp:
            return json.loads(resp.read())

    try:
        t0 = time.time()
        data = await asyncio.get_event_loop().run_in_executor(None, _call_llm)
        elapsed = time.time() - t0

        answer = data['choices'][0]['message']['content'].strip()
        usage = data.get('usage', {})

        # 验证: 如果 LLM 没自然包含来源, 追加
        if "来源" not in answer and domains:
            answer += f"\n\n来源: {' / '.join(domains[:5])}"

        result = {
            "answer": answer,
            "model": LLM_MODEL,
            "elapsed_ms": int(elapsed * 1000),
            "tokens": usage.get('total_tokens', 0),
            "sources": domains[:5],
            "category": category,  # v17.5: 提示 query 类别
            "followups": _generate_followups(query, answer, domains, category),  # v17.4: 相关问题
            "citations": _extract_citations(answer, results),  # v17.7: 内联引用
        }
        # v17.6: 写答案到 cache
        _answer_cache_set(cache_key, result)
        return result
    except urllib.error.URLError as e:
        return {"answer": None, "error": f"LLM timeout: {e}"}
    except Exception as e:
        return {"answer": None, "error": f"LLM error: {e}"}


def _generate_followups(query: str, answer: str, domains: list, category: str) -> list:
    """
    v17.4: 基于 query + 答案, 智能生成 3 个相关问题
    让用户能深挖信息

    Returns: list of str, e.g. ["比亚迪 5月销量详情", "比亚迪 vs 特斯拉对比", ...]

    实现: 用 LLM 生成 (max_tokens=120, 单独调用, 1-2s 延迟, 30-50 tokens)
          失败时降级到启发式模板
    """
    if not answer or len(answer) < 20:
        return []

    # 启发式模板 (fallback)
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

    # LLM 生成
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

    def _call_llm():
        req_data = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": followup_prompt.format(query=query, answer=answer[:500])}],
            "temperature": 0.7,
            "max_tokens": 120,
        }
        req = urllib.request.Request(
            f"{LLM_BASE_URL}/chat/completions",
            data=json.dumps(req_data).encode(),
            headers={"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())

    try:
        data = _call_llm()  # 同步阻塞 (answer 已 1-3s, followup 再 +1s OK)
        text = data['choices'][0]['message']['content'].strip()
        # 解析 3 行
        lines = [l.strip().lstrip('1234567890.-、) ').rstrip('?？') for l in text.split('\n') if l.strip()]
        # 过滤太短/太长的
        valid = [l for l in lines if 5 <= len(l) <= 25]
        return valid[:3] if valid else _template_fallback()
    except Exception:
        return _template_fallback()


# CLI 调试
if __name__ == "__main__":
    import sys
    test_results = [
        {"title": "比亚迪(002594)_最新价格_行情—东方财富网", "url": "https://quote.eastmoney.com/SZ002594.html", "snippet": "比亚迪 002594 最新价 94.78 (-2.05%)", "engine": "bing_cn"},
        {"title": "比亚迪94.78 (-2.05%)_新浪财经", "url": "https://finance.sina.com.cn/realstock/company/sz002594/nc.shtml", "snippet": "当前价 94.78 跌 2.05%", "engine": "bing_cn"},
    ]
    r = asyncio.run(generate_answer("比亚迪股价", test_results))
    print(json.dumps(r, ensure_ascii=False, indent=2))
