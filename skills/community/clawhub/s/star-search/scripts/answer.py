"""
star-search 答案生成 (LLM 总结)
v17.2: 把 8 条 search results 总结成 1 段答案 + 来源
- DeepSeek-V4-Flash via new-api (免费)
- 失败/超时降级返原始 results

环境变量 (可选, 默认 <server-ip>:8080):
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
_env_overrides = {}
if os.path.exists(_env_path):
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k == "LLM_API_KEY":
                _NEWAPI_KEY = v
                _env_overrides[k] = v  # 同步到 os.environ
            elif k in ("LLM_BASE_URL", "LLM_MODEL", "LLM_TIMEOUT", "ANSWER_CACHE_TTL"):
                _env_overrides[k] = v
import os as _os
for _k, _v in _env_overrides.items():
    _os.environ.setdefault(_k, _v)

# 3) local ~/.hermes/auth.json
if not _NEWAPI_KEY:
    try:
        auth_path = os.path.expanduser("~/.hermes/auth.json")
        if os.path.exists(auth_path):
            with open(auth_path) as f:
                raw = f.read()
            m = re.search(r'sk-[A-Z0-9]{4,}[a-zA-Z0-9]+', raw)
            if m:
                _NEWAPI_KEY = m.group()
    except Exception:
        pass

LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "http://<server-ip>:8080/v1")
LLM_API_KEY = os.environ.get("LLM_API_KEY", _NEWAPI_KEY or "")
LLM_MODEL = os.environ.get("LLM_MODEL", "DeepSeek-V4-Flash")
LLM_TIMEOUT = int(os.environ.get("LLM_TIMEOUT", "25"))  # v20.37: 12s 足够 300 tokens 答案 + 2s buffer (实测 8s 不够, 10s 实际 + overhead)
ANSWER_CACHE_TTL = int(os.environ.get("ANSWER_CACHE_TTL", "1800"))  # v17.6: 答案缓存 30min

# ============ v17.6: 答案缓存 ============
import hashlib
import os.path as _osp
import os as _os
_ANSWER_CACHE_DIR = _osp.expanduser("~/.star-search-cache/answers")
_os.makedirs(_ANSWER_CACHE_DIR, exist_ok=True)


def _answer_cache_key(query: str, category: str, n_results: int, fmt: str = "default") -> str:
    """v17.6 + v20.42: 生成 cache key
    归一化 query + category + results 数量级 + format
    """
    q_norm = query.lower().strip()
    n_bucket = "0" if n_results == 0 else f"{(n_results - 1) // 3}"
    raw = f"{q_norm}|{category}|{n_bucket}|{fmt}"
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
    """v17.5 + v18.0 + v20.103: 把 query 分类, 不同类别用不同 prompt 模板
    返回: 'finance' / 'tech' / 'news' / 'general' / 'english'

    v18.0 改进: 扩充品牌/产品关键词, 解决"比亚迪销量"被判 general 的问题
    v20.103: 纯英文 query (>= 8 字符 + 无中文) 优先返回 'english'
    原则: 用户语言优先于内容分类
    """
    # v20.103: 语言优先判定 (在 keywords 之前)
    if not re.search(r"[一-鿿]", query) and re.search(r"[a-zA-Z]", query) and len(query) >= 8:
        return 'english'

    q = query.lower()

    # 财经关键词 (v18.0 扩充: 加品牌 + 业务术语)
    finance_kw = (
        # 通用术语
        '股票', '股价', '股市', 'a股', 'A股', '大盘', '上证', '深证', '沪深',
        '港股', '美股', '纳斯达克', '道琼斯', '标普', '基金', '基金净值',
        '行情', '涨停', '跌停', '个股', '板块', '开盘', '收盘', '市值',
        '财报', '营收', '利润', r'\bpe\b', r'\bpb\b', '估值', '成份股', '龙虎榜',
        '北向资金', '融资融券', 'etf', '指数', '今日股价', '今日行情',
        # 业务术语
        '销量', '销售额', '出货量', '交付量', '订单', '供需', '供需关系',
        '业绩', '亏损', '盈利', '增长', '下滑', '同比', '环比', '环比增长',
        '股价上涨', '股价下跌', '市值蒸发', '净流入', '净流出',
        # A股/港股/美股 知名公司 (v18.0 新增)
        '比亚迪', '蔚来', '小鹏', '理想', '小米集团', '宁德时代', '宁王',
        '茅台', '五粮液', '中国平安', '招商银行', '工商银行', '建设银行',
        '腾讯控股', '阿里巴巴', '美团', '京东', '拼多多', '百度', '网易',
        '苹果', '特斯拉', '微软', '英伟达', 'meta', '亚马逊', '谷歌',
        # 行业关键词
        '新能源汽车', '新能源车', '光伏', '锂电池', '半导体', '银行股',
    )
    if any((kw in query) if isinstance(kw, str) else kw.search(query) for kw in finance_kw):
        return 'finance'

    # 科技关键词 (v18.0 扩充: 加模型/产品名)
    tech_kw = (
        # 通用 AI/ML
        'gpt', 'claude', 'llm', 'ai', '人工智能', '机器学习', '深度学习',
        '神经网络', '大模型', 'openai', 'anthropic', 'google ai', 'gemini',
        '芯片', 'gpu', 'cuda', '半导体', 'ar/vr', '元宇宙', '区块链',
        'python', 'javascript', 'rust', 'golang', 'kubernetes', 'docker',
        'react', 'vue', 'api', 'sdk', 'github', '开源', '算法', 'transformer',
        # 模型/产品 (v18.0 新增)
        'deepseek', 'qwen', '通义千问', '千问', '文心一言', '讯飞星火', '智谱',
        'glm', 'llama', 'mistral', 'grok', 'o1', 'o3', 'gpt-4', 'gpt-5',
        'claude 4', 'claude 3.5', 'claude 3.7', 'sonnet', 'opus', 'haiku',
        # 技术术语
        'mcp', '协议', 'embedding', 'rag', 'agent', '智能体', 'function call',
        'function calling', 'prompt', 'token', 'tokens', '微调', 'fine-tuning',
        'rag', '向量', '向量数据库', '知识库', '训练', '推理', '部署',
    )
    if any(kw in q for kw in tech_kw):
        return 'tech'

    # 新闻关键词 (时间敏感) - v18.0: 放最后, 避免误判 finance/tech
    news_kw = ('新闻', '昨日', '最新', '本周', '上月', '本月', '消息',
              '报道', '官方', '宣布', '发表', '声明', '回应', '辟谣', '热搜',
              '突发', '现场', '记者', '媒体', '外交部', '国务院', '央行')
    if any(kw in query for kw in news_kw):
        return 'news'

    # v20.103: 纯英文 query → english (第 5 个 prompt 模板)
    if not re.search(r"[一-鿿]", query) and re.search(r"[a-zA-Z]", query) and len(query) >= 8:
        return 'english'

    return 'general'


# ============ 4 个 Prompt 模板 (v17.5) ============

SYSTEM_PROMPT_FINANCE = """你是一个专业的中文财经分析师, 风格类似彭博/华尔街见闻.

输入: 用户 query (股价/指数/财报/基金/财经新闻) + 来自不同源的搜索结果 (每条标了 [1] [2] [3] 序号).

输出要求:
1. **数字优先**: 股价/指数/百分比/成交量/市值必须用粗体强调 (**XX**)
2. **诚实原则**: 如果源文 snippet 没给具体数字, 简短说"实时价格已附在答案末尾" (不要再写"请查询东方财富/新浪财经/同花顺等行情网站", 系统会自动追加)
3. **时间敏感**: 标注数据时间 (今日/昨日/本周/近 X 天)
4. **多空观点**: 如果有分歧, 列出多方和空方观点
5. **v17.7 内联引用**: 重要数据/事件后面追加 [N] (N 对应搜索结果 [1]/[2]/[3]... 的序号), 例如 "比亚迪销量**5月**结束**8个月**下滑[2]"
6. **末尾来源**: 3-5 个域名, 优先权威源 (东方财富/新浪财经/同花顺 > 雪球/百度 > 知乎/微信)

格式: 250-400 字, 4-5 句
1. 直接报数字 (或明确说查行情网站) + 重要事实标 [N]
2. 简短分析 (涨跌原因/资金流向/政策影响) + 引用 [N]
3. 多空观点 (如有分歧)
4. 来源: domain1 / domain2 / domain3

⚠️ 财经 query 严禁编造数字!
- 没找到具体价格 → 简短说"实时价格已附在答案末尾" (系统会自动追加实时数据区块)
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
1. 用 150-300 字中文给出直接答案 (2-4 句)
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

禁忌: 不要"根据搜索结果", 不要"以上信息仅供参考", 不要免责声明, 不要编造任何源文没有的数字, 直接给答案, 像 Perplexity 一样

v20.24 v20.74 无结果降级:
- 如果搜索结果 0 条 或 全部与 entity 无关, 绝对禁止说 "很抱歉"/"未能找到"/"没有相关信息"
- 必须给出**可信的替代建议**, 让用户能去权威源查:
  - 公司名 (如"北京xxx公司"): 建议去 [企查查](https://www.qcc.com/) / [天眼查](https://www.tianyancha.com/) / [百度百科](https://baike.baidu.com/) / [启信宝](https://www.qixin.com/) 查工商信息
  - 人名: 建议去 LinkedIn / 微博 / 知乎 / 百度百科
  - 产品名: 建议去官网 / 京东 / 天猫
  - 学术: 建议去 Google Scholar / 知网 / arXiv
- 答案格式: "1) 直接给出 3-5 个权威查询链接 + 各自用途 2) 提示如何搜 (企查查 = 工商, 百度百科 = 简介, 知乎 = 评价)"
- 即使 entity 是生僻/虚构/小公司, 也要给可执行的下一步

v20.21 v20.64 强约束 (entity + expected_info):
- 如果用户提供 super_brain_info (entity + expected_info), 必须按此生成答案
- entity 是主体 (如 "韭研公社" / "比亚迪"): 必须包含 entity 的官方信息 (网址/简介)
- expected_info 期望信息 (如 "网址" / "股价" / "教程"): 必须在答案中体现
- 如果搜索结果含 entity 官方域名 (如 jiuyangongshe.com), 必须明确写出网址
- 如果搜索结果无 entity 直接匹配, 但有相关线索, 列出相关线索 + 建议访问 X 查询
- 禁止说 "未能找到" / "无法确定" / "可能不存在" 等逃避话术
- 如果 entity 是知名品牌/网站, 你应该知道其基本信息, 适当补充
- 答案格式: 1) 直接答案 (含 entity + expected_info) 2) 关键事实 [N] 3) 建议下一步 (如有)"""


# v20.42: 结构化输出格式 hint
FORMAT_TABLE = chr(10).join([
    '',
    '# 输出格式要求: Markdown 表格',
    '请用 Markdown 表格形式呈现答案. 表格要求:',
    '- 第一行是表头 (2-4 列, 如: 项目 | 数值 | 来源)',
    '- 5-8 行数据, 关键事实用 **加粗**',
    '- 表格上方一句话总结核心结论',
    '- 表格下方列出来源域名',
])

FORMAT_JSON = chr(10).join([
    '',
    '# 输出格式要求: 结构化 JSON',
    '请输出一个结构化 JSON 对象 (用 json 代码块包裹). 字段:',
    '- summary: 一句话核心结论 (30-80 字)',
    '- key_points: 3-5 条要点 (字符串数组)',
    '- data: 关键数据对象 (key-value 数组)',
    '- sources: 来源域名数组',
    'JSON 必须合法可解析, 用双引号.',
])

FORMAT_MERMAID = chr(10).join([
    '',
    '# 输出格式要求: Mermaid 思维导图',
    '请用 Mermaid 语法画一张思维导图. 用 mermaid 代码块包裹.',
    '- 根节点是问题的核心主题',
    '- 3-5 个二级分支 (关键要点)',
    '- 重要的二级分支可继续延伸 1-2 级',
    '- 节点文字 5-15 字, 简洁',
])

_FORMAT_HINTS = {
    'default': '',
    'table': FORMAT_TABLE,
    'json': FORMAT_JSON,
    'mermaid': FORMAT_MERMAID,
}

# query 类别 → prompt
SYSTEM_PROMPT_ENGLISH = """You are a professional English-language research analyst. Your style: precise, evidence-based, cites sources like Nature/arXiv/Wikipedia.

Input: user query (English) + search results from multiple sources (each numbered [1] [2] [3]).

Output requirements:
- Answer in English (mirror user's query language)
- Citations mandatory: [1] [2] [3] format, refer to source domain
- If brain_info provided (entity + expected_info), follow strictly
- For company/product/entity queries: include official URL + brief description
- For technical concepts (RAG, transformer, etc.): include definition + 1-2 typical use cases
- For comparative queries: use Markdown table
- Length: 200-400 words, concise but complete
- Cite every factual claim; never invent information not in search results

Output format:
1) Direct answer (with key facts)
2) Key facts [N] (numbered)
3) Sources (domain list)
4) Suggested next step (optional)
"""

_PROMPTS = {
    'finance': SYSTEM_PROMPT_FINANCE,
    'tech': SYSTEM_PROMPT_TECH,
    'news': SYSTEM_PROMPT_NEWS,
    'general': SYSTEM_PROMPT_GENERAL,
    'english': SYSTEM_PROMPT_ENGLISH,
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



def fetch_url(url: str, timeout: int = 8) -> dict:
    """v18.0 v20.32: 抓取 URL 全文 (HTML → 主文本)
    返回: {"ok": True, "text": "正文 ~1000 字", "title": "..."} 或 {"ok": False, "error": "..."}
    """
    import re as _re
    import urllib.request as _ur

    try:
        # 1. fetch HTML
        req = _ur.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/<server-ip> Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        with _ur.urlopen(req, timeout=timeout) as resp:
            ct = resp.headers.get('Content-Type', '')
            # 非 HTML 直接返回 (PDF/图片等不抓)
            if 'text/html' not in ct and 'application/xhtml' not in ct:
                return {"ok": False, "error": f"non-HTML content: {ct}"}
            raw = resp.read()
        # 2. 解码 (HTML 头里 charset 优先, 默认 utf-8)
        charset = 'utf-8'
        m = _re.search(rb'<meta[^>]+charset=["\']?([\w-]+)', raw[:2000], _re.IGNORECASE)
        if m:
            try:
                charset = m.group(1).decode('ascii', errors='ignore').lower()
            except Exception:
                pass
        html = raw.decode(charset, errors='ignore')
        # 3. 提取 title
        title_m = _re.search(r'<title[^>]*>([^<]+)</title>', html, _re.IGNORECASE)
        title = title_m.group(1).strip() if title_m else url
        title = _re.sub(r'\s+', ' ', title)[:100]
        # 4. 提取主文本 (简单版: 去 script/style/head/nav/footer, 取最长 <p> 段落)
        # 去无用标签
        html = _re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=_re.DOTALL|_re.IGNORECASE)
        html = _re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=_re.DOTALL|_re.IGNORECASE)
        html = _re.sub(r'<head[^>]*>.*?</head>', ' ', html, flags=_re.DOTALL|_re.IGNORECASE)
        html = _re.sub(r'<nav[^>]*>.*?</nav>', ' ', html, flags=_re.DOTALL|_re.IGNORECASE)
        html = _re.sub(r'<footer[^>]*>.*?</footer>', ' ', html, flags=_re.DOTALL|_re.IGNORECASE)
        html = _re.sub(r'<header[^>]*>.*?</header>', ' ', html, flags=_re.DOTALL|_re.IGNORECASE)
        # 优先取 article/main 内容
        main_m = _re.search(r'<(article|main)[^>]*>(.*?)</\1>', html, _re.DOTALL|_re.IGNORECASE)
        target = main_m.group(2) if main_m else html
        # 提取所有 <p> 段落
        paras = _re.findall(r'<p[^>]*>(.*?)</p>', target, _re.DOTALL|_re.IGNORECASE)
        # 清理 HTML 标签 + 实体
        clean = []
        for p in paras:
            text = _re.sub(r'<[^>]+>', ' ', p)
            text = _re.sub(r'&[a-z]+;', ' ', text)
            text = _re.sub(r'&#[0-9]+;', ' ', text)
            text = _re.sub(r'\s+', ' ', text).strip()
            if len(text) > 20:  # 过滤太短段落
                clean.append(text)
        text = '\n'.join(clean[:30])  # 最多 30 段
        if len(text) < 100:  # 提取失败 fallback (用整 HTML 去标签)
            text = _re.sub(r'<[^>]+>', ' ', target)
            text = _re.sub(r'&[a-z]+;', ' ', text)
            text = _re.sub(r'\s+', ' ', text).strip()[:2000]
        text = text[:3000]  # 截断 3000 字
        return {"ok": True, "text": text, "title": title, "url": url}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200], "url": url}


def fetch_github_repo(owner: str, repo: str) -> dict:
    """v18.0 v20.32: GitHub 仓库专项 (无 token 60次/小时/IP)
    拉: README (前 2000 字) + description + topics + language + star + last_update
    """
    import json as _json
    import urllib.request as _ur

    try:
        out = {"ok": True, "owner": owner, "repo": repo}
        # 1. repo info
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        req = _ur.Request(api_url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'star-search/18.0'})
        with _ur.urlopen(req, timeout=8) as resp:
            data = _json.loads(resp.read())
        out["description"] = data.get("description", "")
        out["language"] = data.get("language", "")
        out["stars"] = data.get("stargazers_count", 0)
        out["forks"] = data.get("forks_count", 0)
        out["open_issues"] = data.get("open_issues_count", 0)
        out["topics"] = data.get("topics", [])
        out["default_branch"] = data.get("default_branch", "main")
        out["created_at"] = data.get("created_at", "")
        out["updated_at"] = data.get("updated_at", "")
        out["homepage"] = data.get("homepage", "")
        out["license"] = (data.get("license") or {}).get("spdx_id", "")

        # 2. README (raw)
        readme = ""
        for branch in [out["default_branch"], "main", "master"]:
            try:
                rurl = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
                rreq = _ur.Request(rurl, headers={'User-Agent': 'star-search/18.0'})
                with _ur.urlopen(rreq, timeout=5) as rresp:
                    readme = rresp.read().decode('utf-8', errors='ignore')[:3000]
                if readme:
                    break
            except Exception:
                continue
        out["readme"] = readme
        return out
    except Exception as e:
        return {"ok": False, "error": str(e)[:200], "owner": owner, "repo": repo}



def fetch_pdf(url: str, timeout: int = 12) -> dict:
    """v18.0 v20.33: 抓 PDF, 提取文本 (无外部依赖, 内置 PDF 解析器)

    简单版: 找 PDF 中的字符串 (type1 standard 14 fonts 不解码)
    适合: 学术论文 PDF, 简单结构 PDF
    """
    import urllib.request as _ur
    import zlib as _zlib
    try:
        req = _ur.Request(url, headers={'User-Agent': 'star-search/18.0'})
        with _ur.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
        if not data.startswith(b'%PDF'):
            return {"ok": False, "error": "not a PDF file", "url": url}
        # 提取 streams 中的文本 (BT...ET 块)
        text_parts = []
        for m in re.finditer(rb'stream\r?\n(.*?)endstream', data, re.DOTALL):
            stream = m.group(1)
            # 跳过二进制 stream
            try:
                decoded = stream.decode('latin-1', errors='ignore')
                if 'BT' in decoded and 'ET' in decoded:
                    # 提取 (text) Tj/TJ 操作符中的字符串
                    for tm in re.finditer(r'\(((?:[^\\)\n]|\\.)*)\)\s*T[Jj]', decoded):
                        s = tm.group(1)
                        # PDF 字符串转义
                        s = s.replace('\\(', '(').replace('\\)', ')')
                        s = s.replace('\\\\', '\\')
                        if s.strip():
                            text_parts.append(s)
            except Exception:
                continue
        full_text = '\n'.join(text_parts)[:5000]  # 截断 5000 字
        if len(full_text) < 50:
            return {"ok": False, "error": "PDF text extraction empty (可能是图片扫描件)", "url": url}
        return {"ok": True, "text": full_text, "url": url, "chars": len(full_text)}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200], "url": url}


def fetch_arxiv(query: str) -> dict:
    """v18.0 v20.33: arXiv 论文搜索 (无 key, 公共 API)
    支持: arxiv id (2501.12345) 或 query 关键词
    返回: top 3 论文 (title, summary, authors, year, link)
    """
    import urllib.request as _ur
    import urllib.parse as _up
    import xml.etree.ElementTree as _ET
    try:
        # 检测是否是 arxiv id (YYMM.NNNNN 格式)
        id_m = re.search(r'\b(\d{4}\.\d{4,5}(?:v\d+)?)\b', query)
        if id_m:
            arxiv_id = id_m.group(1)
            url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        else:
            # 关键词搜
            q = re.sub(r'arxiv|论文|paper|关于|找', '', query, flags=re.IGNORECASE).strip() or query
            params = _up.urlencode({
                'search_query': f'all:{q}',
                'start': 0, 'max_results': 3,
                'sortBy': 'relevance', 'sortOrder': 'descending'
            })
            url = f"http://export.arxiv.org/api/query?{params}"
        req = _ur.Request(url, headers={'User-Agent': 'star-search/18.0'})
        with _ur.urlopen(req, timeout=10) as resp:
            xml_data = resp.read().decode('utf-8', errors='ignore')
        # 解析 atom xml
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        root = _ET.fromstring(xml_data)
        papers = []
        for entry in root.findall('atom:entry', ns):
            title = (entry.find('atom:title', ns).text or '').strip().replace('\n', ' ')
            summary = (entry.find('atom:summary', ns).text or '').strip()[:1000]
            link = entry.find('atom:id', ns).text or ''
            authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
            published = entry.find('atom:published', ns).text or ''
            year = published[:4] if published else '?'
            papers.append({
                'title': title, 'summary': summary, 'link': link,
                'authors': authors[:3], 'year': year
            })
        return {"ok": True, "papers": papers, "count": len(papers)}
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


async def _async_fetch_url(url: str, timeout: int = 8) -> dict:
    """v18.0 v20.33: async 单 URL 读 (内部, 给并发用)"""
    import asyncio
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fetch_url, url)


async def _async_fetch_multi_urls(urls: list, timeout: int = 8) -> list:
    """v18.0 v20.33: 并发读多 URL (asyncio.gather)
    5 URL 串行 25s -> 并发 ~5-8s
    """
    tasks = [_async_fetch_url(u, timeout) for u in urls]
    return await asyncio.gather(*tasks, return_exceptions=False)




def _detect_special_intent(query: str) -> dict:
    """v18.0 v20.32: 检测 query 里的 URL 或 GitHub 仓库, 提前读

    Returns:
        {"type": "url", "url": "...", "data": {...}} 或
        {"type": "github", "owner": "...", "repo": "...", "data": {...}} 或
        {} (无特殊意图)
    """
    import re as _re
    # 1. URL 检测
    url_m = _re.search(r'https?://[^\s,;，。；！!？?]+', query)
    if url_m:
        url = url_m.group().rstrip('.,;:?!，。；：！？)')
        # 排除搜索引擎自身/无效 URL
        if not any(s in url for s in ['localhost', '<server-ip>', '<server-ip>']):
            if url.lower().endswith('.pdf'):
                data = fetch_pdf(url)
            else:
                data = fetch_url(url)
            if data.get("ok") and (data.get("text") or data.get("papers")):
                return {"type": "pdf" if url.lower().endswith('.pdf') else "url", "url": url, "data": data}

    # 1.5 PDF 链接检测 (无 .pdf 后缀的 PDF, 通过 arxiv pdf 链接)
    pdf_m = _re.search(r'https?://arxiv\.org/pdf/([\d.]+(?:v\d+)?)\.pdf', query)
    if pdf_m:
        arxiv_id = pdf_m.group(1)
        # 走 arxiv api 拿摘要, 不必读全文
        arxiv_data = fetch_arxiv(arxiv_id)
        if arxiv_data.get("ok") and arxiv_data.get("papers"):
            return {"type": "arxiv", "arxiv_id": arxiv_id, "data": arxiv_data}

    # 1.6 arXiv 论文搜索
    if 'arxiv' in query.lower() or _re.search(r'\b\d{4}\.\d{4,5}\b', query):
        arxiv_data = fetch_arxiv(query)
        if arxiv_data.get("ok") and arxiv_data.get("papers"):
            return {"type": "arxiv", "data": arxiv_data}
    # 2. GitHub 仓库检测 (文本模式: owner/repo 或 github.com/owner/repo)
    gh_m = _re.search(r'([A-Za-z0-9][\w.-]+)/([A-Za-z0-9][\w.-]+?)(?:\.git|[\s,，。；?!]|$)', query)
    if gh_m:
        owner, repo = gh_m.group(1), gh_m.group(2)
        # 排除明显不是仓库的 (common words)
        if owner.lower() not in ('the','a','an','is','are','and','or','with','from','for','to','in','on','of') and len(repo) > 1:
            data = fetch_github_repo(owner, repo)
            if data.get("ok"):
                return {"type": "github", "owner": owner, "repo": repo, "data": data}
    return {}



def _check_source_quality(results: list, query: str) -> str:
    """v18.0: 源文质量检测

    如果源文 snippet 总长度 < 500 字, 提示用户"信息有限"
    如果源文 < 3 条, 提示"来源不足"

    Returns: warning string or empty
    """
    warnings = []

    # 1. 源文总长度
    total_chars = 0
    relevant_count = 0
    for r in results[:8]:
        snippet = r.get('snippet', '') or r.get('desc', '') or r.get('content', '')
        total_chars += len(snippet)
        if snippet and len(snippet) > 20:
            relevant_count += 1

    if total_chars < 500:
        # 推断 query 类别, 给精准提示
        cat = _classify_query(query)
        tips = {
            'finance': '请直接查询东方财富/新浪财经/同花顺等行情网站获取实时数据',
            'tech': '请查阅官方文档或 GitHub 仓库获取最新信息',
            'news': '请关注新华社/人民网/澎湃新闻等主流媒体获取最新报道',
            'general': '建议细化搜索关键词或参考专业网站'
        }
        warnings.append(f'搜索结果信息有限（总文字 {total_chars} 字），{tips.get(cat, tips["general"])}')

    # 2. 来源不足
    if relevant_count < 3:
        warnings.append(f'仅找到 {relevant_count} 条相关结果，建议补充更具体的搜索词')

    return ' / '.join(warnings)


def _extract_citations(answer: str, results: list) -> dict:
    """v17.7 + v18.0: 从 answer 里提取 [N] 引用, 返回 {1: title, 2: title, ...}
    用于前端 hover 显示来源标题

    v18.0 修: regex 同时支持 [1] 和 [N1] (markdown 风格) 两种格式
    """
    import re
    citations = {}
    # v18.0: 同时匹配 [1] [12] [N1] [N12] 三种格式
    pattern = re.compile(r'\[(?:N)?(\d+)\]')
    for m in pattern.finditer(answer):
        try:
            n = int(m.group(1))
            if 1 <= n <= len(results):
                if n not in citations:
                    title = results[n-1].get('title', f'来源 {n}')
                    url = results[n-1].get('url', '')
                    citations[n] = {'title': title[:60], 'url': url}
        except (ValueError, IndexError):
            pass
    return citations


async def generate_answer(query: str, results: list, mode: str = "deep", history: list = None, fmt: str = "default", brain_ctx: str = None, entity_card_url: str = None) -> dict:
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

    import re as _re
    formatted = _format_results_for_llm(results)

    # v20.39 多轮对话: 把历史对话拼到 prompt
    history_text = ""
    if history:
        history_text = "\n\n=== 之前的对话 ===\n"
        for h in history[-6:]:  # 最多 6 轮
            hq = h.get('q', '') if isinstance(h, dict) else ''
            ha = h.get('a', '') if isinstance(h, dict) else ''
            if hq and ha:
                history_text += f"用户: {hq[:200]}\n助手: {ha[:500]}\n---\n"
        history_text += "\n请基于以上对话和下面的搜索结果回答当前问题。\n"
        formatted = history_text + formatted

    # v18.0 v20.33: 检测多个 URL (并发读)
    all_urls = _re.findall(r'https?://[^\s,;，。；！!？?]+', query)
    if len(all_urls) > 1:
        import asyncio as _aio
        multi_results = _aio.run(_async_fetch_multi_urls(all_urls[:5]))
        multi_text = []
        for i, mr in enumerate(multi_results, 1):
            if mr.get("ok") and mr.get("text"):
                multi_text.append(f"[URL {i}] {mr.get('title', mr.get('url',''))}\n{mr['text'][:1500]}")
        if multi_text:
            formatted = "\n\n".join(multi_text) + f"\n\n===其他搜索结果===\n{formatted}"

    # v18.0 v20.32: URL / GitHub 专项 (提前读, 注入到 LLM 上下文)
    special = _detect_special_intent(query)
    if special:
        if special["type"] == "url":
            url_data = special["data"]
            url_text = f"[URL全文] {url_data['title']}\n{url_data['text']}"
            formatted = f"{url_text}\n\n===其他搜索结果===\n{formatted}"
        elif special["type"] == "github":
            gh = special["data"]
            gh_text = f"[GitHub仓库] {gh['owner']}/{gh['repo']}\n"
            gh_text += f"描述: {gh.get('description','')}\n"
            gh_text += f"语言: {gh.get('language','')} | Star: {gh.get('stars',0)} | Fork: {gh.get('forks',0)}\n"
            gh_text += f"Topics: {','.join(gh.get('topics',[]))}\n"
            gh_text += f"主页: {gh.get('homepage','')}\n"
            gh_text += f"许可证: {gh.get('license','')}\n"
            gh_text += f"更新时间: {gh.get('updated_at','')}\n\n"
            gh_text += f"--- README (前 2000 字) ---\n{gh.get('readme','')[:2000]}"
            formatted = f"{gh_text}\n\n===其他搜索结果===\n{formatted}"
        elif special["type"] == "arxiv":
            papers = special.get("data", {}).get("papers", [])
            ax_text = "[arXiv 论文] 找到 {} 篇相关论文:\n\n".format(len(papers))
            for i, p in enumerate(papers, 1):
                ax_text += f"--- 论文 {i} ---\n"
                ax_text += f"标题: {p.get('title','')}\n"
                ax_text += f"作者: {', '.join(p.get('authors',[])[:3])}\n"
                ax_text += f"年份: {p.get('year','')}\n"
                ax_text += f"链接: {p.get('link','')}\n"
                ax_text += f"摘要: {p.get('summary','')}\n\n"
            formatted = f"{ax_text}\n===其他搜索结果===\n{formatted}"

    # v18.0: 源文质量检测
    quality_warning = _check_source_quality(results, query)

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
    format_hint = _FORMAT_HINTS.get(fmt, '')
    if format_hint:
        system_prompt = system_prompt + format_hint

    # v20.68: 注入 super_brain context (让 LLM 知道 entity/expected_info)
    if brain_ctx:
        brain_inject = """

v20.24 v20.68 brain 上下文 (super_brain 已分析):
""" + brain_ctx + """

基于以上分析, 你应该:
- 重点是 expected_info 期望的信息
- 答案必须围绕 entity 主体词展开
- 如果 intent 是 navigation (找官网), 必给 official_url
- 如果 intent 是 comparison (对比), 用表格/对比格式
- 如果 entity 是知名品牌/网站, 必出标准信息 (简介/网址/标签)
- 如果搜索结果未含 entity 直接信息, 也可基于你知识补充"""
        system_prompt = system_prompt + brain_inject

    # v20.81: entity_card 官方网址强优先 (让 LLM 必引)
    if entity_card_url:
        ec_inject = f"""

v20.30 v20.81 实体知识卡片官方网址 (必须引用):
- entity 在知识库中有官方网址: {entity_card_url}
- 你的答案中**必须包含这个网址** (在引用块/相关链接中)
- 如果搜索结果 URL 列表中没有这个网址, 仍然要主动引用
- 优先用 KB 官方网址, 而非搜索结果的次级链接"""
        system_prompt = system_prompt + ec_inject

    # v17.6: 答案缓存 (按 query 归一化 + category, 30min TTL)
    cache_key = _answer_cache_key(query, category, len(results), fmt)
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
            "max_tokens": 300,  # v20.37: GLM-4-Flash 46 tok/s, 300 tokens = 6.5s 写 ~350 字答案 (6.5s vs 17s 之前)
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

        # v18.0: 源文太短检测 (prompt 注入方式)
        if quality_warning:
            answer += f"\n\n⚠️ {quality_warning}"

        result = {
            "answer": answer,
            "model": LLM_MODEL,
            "elapsed_ms": int(elapsed * 1000),
            "tokens": usage.get('total_tokens', 0),
            "sources": domains[:5],
            "category": category,  # v17.5: 提示 query 类别
            "followups": _generate_followups(query, answer, domains, category),  # v17.4: 相关问题
            "citations": _extract_citations(answer, results),  # v17.7: 内联引用
            "special_intent": special.get("type") if special else None,  # v18.0 v20.32: url/github
            "special_data": {
                "url": special.get("url") if special.get("type") == "url" else None,
                "github": f"{special['owner']}/{special['repo']}" if special.get("type") == "github" else None,
                "arxiv_id": special.get("arxiv_id") if special.get("type") == "arxiv" else None,
                "paper_count": special.get("data", {}).get("count", 0) if special.get("type") == "arxiv" else None,
            } if special else None,
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
