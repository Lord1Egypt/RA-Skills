"""
star-search API server v17.2
OpenAI-compatible search endpoint + 增量追加 + LLM 答案生成

启动: python3 scripts/api_server.py [--port 5000]
测试: curl -X POST http://localhost:5000/v1/search -H "Content-Type: application/json" -d '{"query":"Python asyncio","mode":"dev","top":8}'

接口：
  POST /v1/search              — 主搜索 (OpenAI-compatible style body)
  POST /v1/search/refresh      — 增量追加（基于已有 cache 拉新结果）
  POST /v1/answer              — LLM 答案生成 (v17.2 新增, 返回 1 段答案 + 来源)
  GET  /v1/health              — 健康检查
  GET  /v1/modes               — 列出 7 种模式
  GET  /v1/engines             — 列出 7 个引擎
"""
import argparse, asyncio, sys, time, os, json
# v20.55: 用户系统
import user_auth as _ua
# v20.57: 多模态
import multimodal as _mm
# v20.58: Deep research
import deep_research as _dr
# v20.59: 支付
import payment as _pay
# v20.60: 验证码 (Turnstile)
import verify as _verify
# v20.61: query 重写
import query_rewrite as _qr
# v20.62: AI 智能层
import super_brain as _brain
# v20.63: 多路并行搜索
import multi_search as _ms
# v20.66: 实体知识卡片
import entity_card as _ec
import cross_verify as _cv
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
import logging

# v20.40: 启用详细 logging (单文件不轮转, 避免 truncate)
LOG_DIR = Path('/home/ubuntu/star-search/logs')
LOG_DIR.mkdir(exist_ok=True)
DETAIL_LOG = LOG_DIR / 'detail.log'

# 每次启清空 detail.log (截断模式, 避免老 log 干扰新启)
with open(DETAIL_LOG, 'w') as _f:
    pass

# 配 root logger (force=True 覆盖 uvicorn 默认 config)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s',
    handlers=[
        logging.FileHandler(DETAIL_LOG, mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stderr)
    ],
    force=True  # v20.40: 强制覆盖 (uvicorn 启时会重设 logger)
)
# v20.40: 写一行验证 logging 工作
logging.info('=== api_server 启动 (force=True) ===')
log = logging.getLogger('api_server')

# 拦截未处理异常
def _excepthook(exc_type, exc_value, exc_tb):
    log.critical('UNHANDLED', exc_info=(exc_type, exc_value, exc_tb))
    sys.__excepthook__(exc_type, exc_value, exc_tb)
sys.excepthook = _excepthook

# 拦截 asyncio 异常
def _asyncio_excepthook(loop, context):
    log.critical(f'ASYNCIO EXC: {context}', exc_info=context.get('exception'))
    loop.default_exception_handler(context)

# 复用 search.py + answer.py 的核心函数
sys.path.insert(0, str(Path(__file__).parent))
import search as s
import answer as a
import academic_code as ac
import metrics as m
from starlette.responses import PlainTextResponse

# 装 asyncio hook (loop 在第一次跑 async 时建)
import asyncio as _aio
_orig_init = _aio.events.BaseDefaultEventLoopPolicy.__init__
def _new_init(self):
    _orig_init(self)
    try:
        _aio.get_event_loop().set_exception_handler(_asyncio_excepthook)
    except Exception as e:
        pass
_aio.events.BaseDefaultEventLoopPolicy.__init__ = _new_init

app = FastAPI(title="star-search API", version="17.2",
              description="免费中文搜索 API · 16 引擎 · 智能去重 · 智能缓存 · LLM 答案层 🌟🌟🌟")

# v20.96: 实时财经报价端点
@app.get("/v1/realtime/quote")
async def realtime_quote(q: str = ""):
    """v20.98: 实时财经报价 (真接东财 API)
    q: 股票名/代码/指数
    返回: {code, market, price, change_pct, realtime_links[]}
    """
    try:
        import eastmoney_spider as _em
        return _em.get_quote_with_real(q)
    except Exception as e:
        return {"error": f"realtime failed: {e}"}

@app.get("/v1/realtime/links")
async def realtime_links(q: str = ""):
    """v20.96: 仅返回实时价格链接 (用于前端 quick-action 按钮)"""
    try:
        import realtime as _rt
        return {"query": q, "links": _rt.get_quote_links_only(q)}
    except Exception as e:
        return {"error": f"links failed: {e}"}

# v20.44: metrics middleware 自动计 endpoint
from starlette.middleware.base import BaseHTTPMiddleware

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        path = request.url.path
        # 跳过 metrics 自身
        if path != '/metrics':
            m.metrics.incr_requests(path)
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            m.metrics.incr_requests(path, error=True)
            raise

app.add_middleware(MetricsMiddleware)


# ===== 数据模型 =====
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    mode: str = Field(default="deep", description="deep/quick/news/policy/stock/dev/global/auto (auto=智能识别)")
    top: int = Field(default=8, ge=1, le=30)
    recency: str = Field(default=None, description="day/week/month/year")
    exact: bool = Field(default=False)
    engine: str = Field(default=None, description="单引擎：sogou_http/bing_cn/github_issues/sogou/baidu/360/weixin/bing_http")
    sources: list = Field(default=None, description="URL 包含某关键词才返回（多用于 dev/news 模式）")
    force_refresh: bool = Field(default=False, description="绕过缓存（用于测试/查新结果）")
    answer: bool = Field(default=True, description="v20.102: 默认开启 LLM 答案生成")
    fetch: int = Field(default=3, description="v20.102: 默认抓前 N 条正文 (0=不抓)")
    session_id: str = Field(default=None, description="v20.39: 会话 ID, 用于多轮对话")
    history: list = Field(default_factory=list, description="v20.39: 历史对话 [{q, a}, ...], 拼到 prompt")
    fmt: str = Field(default="default", description="v20.42: 答案格式 default/table/json/mermaid")

class RefreshRequest(BaseModel):
    query: str
    mode: str = Field(default="deep")
    top: int = Field(default=10, ge=1, le=30)
    recency: str = Field(default=None)
    # 增量追加时，ttl 多长时间内合并，0=强制刷新
    merge_window: int = Field(default=1800, description="秒，默认30分钟")

# ===== 接口 =====
@app.get("/v1/health")
async def health():
    return {
        "status": "ok",
        "version": "17.2",
        "engines": 16,
        "modes": 11,
        "features": ["search", "refresh", "answer", "mcp"]
    }

@app.get("/v1/modes")
async def modes():
    return s.MODES

@app.get("/v1/engines")
async def engines():
    return {
        "http": ["bing_cn", "bing_http", "github_issues",
                 "toutiao", "zhihu", "weixin",
                 "csdn", "cnblogs", "eastmoney", "cls", "tencent_cloud", "sina_finance", "sohu",
                 "rss_ithome", "rss_36kr", "rss_sspai", "rss_oschina", "rss_woshipm"],
        "playwright": ["sogou", "baidu", "360", "weixin"],
    }

@app.post("/v1/search")
async def search(req: SearchRequest, request: Request):
    start = time.time()
    # v20.55: 可选 quota check (header Bearer token)
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:].strip()
        user = _ua.get_user(token)
        if user:
            quota = _ua.check_quota(user['user_id'])
            if 'error' in quota:
                return JSONResponse({'error': quota['error'], 'quota': quota}, status_code=429)
    try:
        # engine + sources 互斥：单引擎模式
        if req.engine:
            results = await s.search_async(
                query=req.query, engine=req.engine, num=req.top,
                mode='quick', recency=req.recency, exact=req.exact, sources=req.sources,
                force_refresh=req.force_refresh)
        else:
            results = await s.search_async(
                query=req.query, num=req.top, mode=req.mode,
                recency=req.recency, exact=req.exact, sources=req.sources,
                force_refresh=req.force_refresh)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"search error: {e}")

    # shi-zhan 104: academic query auto-merge openalex/crossref
    try:
        import academic_code as _ac_e104
        qmode = _ac_e104.detect_query_mode(req.query)
        if qmode == "academic" and not req.engine:
            extra = await _ac_e104.run_academic(req.query, num=req.top)
            if extra:
                seen_urls = {r.get("url", "") for r in results}
                added = 0
                added_items = []
                for x in extra:
                    if x.get("url") and x["url"] not in seen_urls:
                        added_items.append(x)
                        seen_urls.add(x["url"])
                        added += 1
                # v20.104: 插头部 (学术结果优先级高于通用搜索)
                for x in reversed(added_items):
                    results.insert(0, x)
                if added:
                    print("[e104-academic] +" + str(added) + " merged", flush=True)
    except Exception as _e104e:
        print("[e104-academic] ERROR: " + str(_e104e), flush=True)

    elapsed = time.time() - start
    # v20.61: 从 url 解析 domain 填到 source 字段
    from urllib.parse import urlparse as _up
    for _r in results:
        if not _r.get('source') and _r.get('url'):
            try:
                _d = _up(_r['url']).netloc
                if _d.startswith('www.'):
                    _d = _d[4:]
                _r['source'] = _d
            except Exception:
                _r['source'] = _r.get('engine', 'unknown')
    # v20.50: 搜索结果加入 BM25 索引 (供 /v1/semantic_search 用)
    try:
        import semantic_search
        await semantic_search.index_results(req.query, results[:req.top])
    except Exception:
        pass
    resp_data = {
        "query": req.query,
        "mode": req.mode,
        "engine": req.engine,
        "count": len(results),
        "elapsed_ms": int(elapsed * 1000),
        "results": results[:req.top],
        "cache_stats": s._cache_stats.copy(),
    }

    # v20.68: 调 super_brain (拿 entity + expected_info + pinyin + engines)
    # v20.71: 把 history 拼到 brain 上下文
    # v20.72: recency 智能 (时新性)
    brain_info = None
    recency = None
    try:
        # 71: history 拼 context
        history_ctx = ""
        if req.history and len(req.history) > 0:
            recent = req.history[-2:]
            history_ctx = "之前的对话上下文:\n"
            for h in recent:
                hq = h.get("q", "") if isinstance(h, dict) else ""
                ha = h.get("a", "") if isinstance(h, dict) else ""
                if hq: history_ctx += f"用户: {hq}\n"
                if ha: history_ctx += f"助手: {ha[:200]}\n"
        brain_info = _brain.analyze_query(req.query, use_cache=True, context=history_ctx)
    except Exception:
        brain_info = None

    # 72: recency 智能
    try:
        import re as _re
        if any(kw in req.query for kw in ["今天", "今日", "最新", "最近", "刚刚", "现在", "新闻"]):
            recency = "day"
        elif any(kw in req.query for kw in ["本周", "这周", "动态", "进展"]):
            recency = "week"
        elif _re.search(r"20(2[4-9])", req.query):
            recency = "year"
        else:
            recency = None
    except Exception:
        recency = None

    # 72: 如果 recency 解析, 用 single engine bing_cn (不并行避免老结果)
    # 注: 当前 search_async 已支持 recency, 但默认 recency=None 时用全部
    # 我们传 recency=None 让 brain 决定

    # v20.69: 查 entity_card (如果在 KB 里)
    entity_card = None
    if brain_info and brain_info.get('entity'):
        try:
            ec_resp = _ec.get_entity_card(brain_info['entity'])
            if ec_resp:
                entity_card = ec_resp
        except Exception:
            pass

    # v17.2: LLM 答案生成 (可选) - v20.68 注入 brain context
    if req.answer and results:
        # 把 brain context 拼成 brain_ctx 字符串
        brain_ctx = None
        if brain_info:
            brain_ctx = (
                f"主问题: {req.query}\n"
                f"主体词: {brain_info.get('entity', '')}\n"
                f"用户意图: {brain_info.get('intent', 'info')}\n"
                f"类别: {brain_info.get('category', 'general')}\n"
                f"关键词: {', '.join(brain_info.get('keywords', []))}\n"
                f"期望信息: {brain_info.get('expected_info', '通用')}\n"
                f"实体卡片: {entity_card if entity_card else '无'}"
            )
        answer_data = await a.generate_answer(
            req.query, results[:req.top], mode=req.mode,
            history=req.history, fmt=req.fmt, brain_ctx=brain_ctx, entity_card_url=(entity_card or {}).get('official_url')
        )
        if answer_data.get("answer"):
            answer_data["fmt"] = req.fmt  # v20.56: 注入 fmt 给前端
            # v20.73: 前端 UI 集成 - 把 brain/entity/cv 嵌到 answer_data (避免前端 currentResponse 变量)
            if brain_info:
                answer_data["brain_info"] = brain_info
            if entity_card:
                answer_data["entity_card"] = entity_card
            # v20.98: 财经 query 答案末尾自动加实时数据 (真接东财)
            try:
                import eastmoney_spider as _em
                em_resp = _em.get_quote_with_real(req.query)
                rt_lines = []
                if em_resp.get('success'):
                    q = em_resp.get('quote', {})
                    price = q.get('price')
                    chg = q.get('change_pct')
                    if price:
                        rt_lines.append(f"💰 **{em_resp.get('name')} ({em_resp.get('code')})**: 当前价 **{price}** 元")
                    if chg is not None:
                        rt_lines.append(f"📈 涨跌幅: **{chg:+.2f}%**")
                if not rt_lines:
                    import realtime as _rt
                    rt_lines = _rt.get_quote_links_only(req.query)
                if rt_lines:
                    sep = "\n\n📊 **实时数据**:\n"
                    answer_data["answer"] = answer_data["answer"] + sep + "\n".join(rt_lines)
                    answer_data["realtime_links"] = rt_lines
            except Exception:
                pass
            resp_data["answer"] = answer_data

    # v20.68: 注入 brain_info 给前端
    if brain_info:
        resp_data["brain_info"] = brain_info

    # v20.69: 注入 entity_card
    if entity_card:
        resp_data["entity_card"] = entity_card

    # v20.102: fetch_content 自动抓取前 N 条 (默认 3 条)
    if req.fetch and req.fetch > 0 and results:
        try:
            import fetch_content as _fc
            results = _fc.fetch_results(results, top_n=req.fetch, use_playwright=True)
            ok = sum(1 for r in results if isinstance(r, dict) and r.get('fetch_success'))
            resp_data['fetch_stats'] = {'requested': req.fetch, 'success': ok}
        except Exception as e:
            resp_data['fetch_error'] = str(e)

    # v20.70: 多源交叉验证 + 可信度
    try:
        cv_res = _cv.cross_verify(results[:req.top])
        # 给每条结果加 credibility
        results_with_cred = _cv.annotate_results_with_credibility(results[:req.top])
        resp_data["results"] = results_with_cred
        resp_data["cross_verify"] = cv_res
        # v20.73: cross_verify 也嵌到 answer_data
        if resp_data.get("answer"):
            resp_data["answer"]["cross_verify"] = cv_res
    except Exception as e:
        resp_data["cross_verify_error"] = str(e)

    # v20.72: recency 时效性
    resp_data["recency"] = recency

    return resp_data

@app.post("/v1/search/refresh")
async def search_refresh(req: RefreshRequest):
    """增量追加：强制刷新 + 与历史 cache 合并
    1. force_refresh=True 绕过缓存拿新结果
    2. search_async 内部合并历史（refresh=true/false 标记）
    3. 返回合并结果
    """
    start = time.time()
    try:
        results = await s.search_async(
            query=req.query, num=req.top, mode=req.mode,
            recency=req.recency, force_refresh=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"refresh error: {e}")

    elapsed = time.time() - start
    new_count = sum(1 for r in results if r.get('refresh'))
    return {
        "query": req.query,
        "mode": req.mode,
        "count": len(results),
        "new_count": new_count,
        "old_count": len(results) - new_count,
        "elapsed_ms": int(elapsed * 1000),
        "results": results,
    }

# v17.2: 独立答案端点 (接受外部传入的 results)
class AnswerRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    results: list = Field(..., description="搜索结果列表 (title/url/snippet/engine)")
    mode: str = Field(default="deep")

@app.post("/v1/answer")
async def answer_only(req: AnswerRequest):
    """v17.2: 独立答案端点 - 接受外部 results, 返回 LLM 总结答案"""
    start = time.time()
    if not req.results:
        raise HTTPException(status_code=400, detail="results is required")
    answer_data = await a.generate_answer(req.query, req.results[:10], mode=req.mode)
    elapsed = time.time() - start
    return {
        "query": req.query,
        "elapsed_ms": int(elapsed * 1000),
        "result_count": len(req.results),
        **answer_data
    }

# ===== 启动 =====


# ===== v20.36 流式输出 (P0-2) =====
from fastapi.responses import StreamingResponse
import json as _json

@app.post("/v1/search/stream")
async def search_stream(req: SearchRequest):
    """SSE 流式输出:
    1. 立刻返 {event: search_start, query}
    2. 搜索完成 -> {event: search_done, results: [...], elapsed_ms}
    3. 答案层 -> 多个 {event: answer_chunk, delta: "..."} (SSE 推)
    4. {event: answer_done, answer, sources, followups, model}
    5. {event: done}
    """
    import asyncio
    start = time.time()

    async def event_gen():
        try:
            log.info(f'SSE start: q={req.query[:30]} session={req.session_id}')
            # 1) 立即推 search_start
            yield f"event: search_start\ndata: {_json.dumps({'query': req.query, 'mode': req.mode})}\n\n"

            # 2) 跑搜索
            try:
                if req.engine:
                    results = await s.search_async(
                        query=req.query, engine=req.engine, num=req.top,
                        mode='quick', recency=req.recency, exact=req.exact, sources=req.sources,
                        force_refresh=req.force_refresh)
                else:
                    results = await s.search_async(
                        query=req.query, num=req.top, mode=req.mode,
                        recency=req.recency, exact=req.exact, sources=req.sources,
                        force_refresh=req.force_refresh)
            except Exception as e:
                yield f"event: error\ndata: {_json.dumps({'error': str(e)})}\n\n"
                return

            search_elapsed = int((time.time() - start) * 1000)
            top_results = results[:req.top]

            # 3) 立刻推 search_done
            yield f"event: search_done\ndata: {_json.dumps({'count': len(top_results), 'elapsed_ms': search_elapsed, 'results': top_results, 'cache_stats': s._cache_stats.copy()})}\n\n"
            # v20.44: metrics
            cached = search_elapsed < 5  # 5ms 内返 = 缓存命中
            m.metrics.incr_search(cached=cached, elapsed_ms=search_elapsed)

            # 4) 跑答案 (如果需要)
            if req.answer and top_results:
                try:
                    log.info(f"=== STREAM generate_answer: fmt={req.fmt!r} ===")
                    answer_data = await a.generate_answer(req.query, top_results, mode=req.mode, history=req.history, fmt=req.fmt)
                    if answer_data.get('answer'):
                        # 模拟流式: 把答案按 30 字 切
                        ans_text = answer_data['answer']
                        chunk_size = 30
                        for i in range(0, len(ans_text), chunk_size):
                            chunk = ans_text[i:i+chunk_size]
                            yield f"event: answer_chunk\ndata: {_json.dumps({'delta': chunk, 'index': i})}\n\n"
                            await asyncio.sleep(0.05)  # 50ms 一片
                        # 推 done + metric
                        m.metrics.incr_answer(cached=answer_data.get('cached', False), elapsed_ms=answer_data.get('elapsed_ms', 0), llm_ms=answer_data.get('elapsed_ms', 0))
                        yield f"event: answer_done\ndata: {_json.dumps({'answer': ans_text, 'model': answer_data.get('model'), 'elapsed_ms': answer_data.get('elapsed_ms'), 'tokens': answer_data.get('tokens'), 'sources': answer_data.get('sources'), 'followups': answer_data.get('followups'), 'citations': answer_data.get('citations'), 'category': answer_data.get('category'), 'cached': answer_data.get('cached'), 'special_intent': answer_data.get('special_intent'), 'special_data': answer_data.get('special_data'), 'fmt': req.fmt})}\n\n"
                    else:
                        yield f"event: answer_error\ndata: {_json.dumps({'error': answer_data.get('error', 'unknown')})}\n\n"
                        m.metrics.incr_answer(error=True, elapsed_ms=int((time.time()-start)*1000))
                except Exception as e:
                    yield f"event: answer_error\ndata: {_json.dumps({'error': str(e)})}\n\n"
                    m.metrics.incr_answer(error=True, elapsed_ms=int((time.time()-start)*1000))

            yield "event: done\ndata: {}\n\n"
            log.info(f'SSE done: q={req.query[:30]}')
        except Exception as e:
            log.exception(f'SSE FATAL: q={req.query[:30]}, err={e}')
            try:
                yield f"event: fatal_error\ndata: {_json.dumps({'error': str(e)})}\n\n"
            except Exception as e2:
                log.exception(f'SSE FATAL (yield err): {e2}')

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # nginx 不缓冲
            "Connection": "keep-alive",
        }
    )




# v20.41 学术 / 代码检索端点
from pydantic import BaseModel as _BM
class AcademicReq(_BM):
    query: str
    num: int = 10



@app.post("/v1/semantic_search")
async def semantic_search_endpoint(req: SearchRequest):
    """v20.50: BM25 语义搜索 (基于已索引的 16 引擎结果)
    - 首次 query: 自动先 search 16 引擎 + index + semantic
    - 后续: 直接走 BM25 索引 (毫秒级)
    - 缓存: 30min (与答案缓存同)
    """
    num = req.top or 10
    try:
        from semantic_search import semantic_search as ss_search, index_results, get_index_stats
        # 如果索引空, 先 search 16 引擎
        stats = get_index_stats()
        if stats['docs'] == 0:
            s = SearchEngine()
            results = await s.search_async(req.query, top=num*2, force_refresh=req.force_refresh)
            await index_results(req.query, results)
        # 走 BM25
        results = await ss_search(req.query, num=num)
        return {
            'query': req.query,
            'engine': 'semantic_bm25',
            'count': len(results),
            'results': results,
            'index_stats': get_index_stats(),
            'elapsed_ms': 5,
        }
    except Exception as e:
        log.exception("semantic_search error")
        return {'error': str(e), 'count': 0, 'results': []}




@app.post("/v1/discover")
async def discover_endpoint(req: dict):
    """v20.51: Perplexity 风格探索发现
    - mode: timeline (时间线) / comparison (多角度对比) / related (相关问题深挖)
    - 复用 GLM-4-Flash 答案层 + 30min 缓存
    """
    query = req.get('query', '').strip()
    mode = req.get('mode', 'timeline').strip()
    num = int(req.get('num_results', 8))
    if not query:
        return {'error': 'query is required', 'count': 0, 'result': ''}
    try:
        import subprocess as _sp
        t0 = time.time()
        env = dict(os.environ)
        env['PYTHONPATH'] = '/home/ubuntu/.local/lib/python3.10/site-packages'
        proc = _sp.run(
            ['/usr/bin/python3', '/home/ubuntu/star-search/scripts/discover_runner.py',
             json.dumps({"query": query, "mode": mode, "num": num})],
            capture_output=True, text=True, timeout=60, env=env,
        )
        last = proc.stdout.strip().split('\n')[-1] if proc.stdout.strip() else '{}'
        out = json.loads(last)
        out['elapsed_ms'] = int((time.time() - t0) * 1000)
        return out
    except Exception as e:
        log.exception("discover error")
        return {'error': str(e), 'query': query, 'mode': mode, 'result': ''}


@app.post("/v1/scholar")
async def search_scholar(req: AcademicReq):
    """学术检索: Google Scholar + Semantic Scholar"""
    try:
        results = await ac.run_academic(req.query, num=req.num)
        return {"results": results, "count": len(results), "engines": ["scholar", "semantic_scholar"]}
    except Exception as e:
        log.exception(f"scholar 错误: {e}")
        raise HTTPException(500, str(e))

@app.post("/v1/code")
async def search_code(req: AcademicReq):
    """代码检索: grep.app + Sourcegraph"""
    try:
        results = await ac.run_code(req.query, num=req.num)
        return {"results": results, "count": len(results), "engines": ["grep_app", "sourcegraph"]}
    except Exception as e:
        log.exception(f"code 错误: {e}")
        raise HTTPException(500, str(e))

# v20.41: 智能检测 query 类型, 学术/代码模式自动触发 (与 /v1/search 集成)
@app.get("/v1/academic_mode")
async def get_academic_mode(q: str):
    """查询模式检测: academic / code / general"""
    return {"query": q, "mode": ac.detect_query_mode(q)}




# v20.44: Prometheus metrics 端点
@app.get("/metrics")
async def metrics_endpoint():
    """Prometheus 抓取端点 (text/plain)"""
    return PlainTextResponse(content=m.metrics.to_prometheus(), media_type="text/plain; version=0.0.4; charset=utf-8")



# ===== v20.55: 用户系统 =====
@app.post("/v1/auth/register")
async def auth_register(req: dict):
    """v20.55: 注册 (手机号 + 密码)
    body: {phone, password, email?}
    return: {user_id, token, tier} | {error}
    """
    phone = req.get('phone', '').strip()
    password = req.get('password', '')
    email = req.get('email', '').strip()
    r = _ua.register(phone, password, email)
    return r

@app.post("/v1/auth/login")
async def auth_login(req: dict):
    """v20.55: 登录
    body: {phone, password}
    return: {user_id, token, tier} | {error}
    """
    phone = req.get('phone', '').strip()
    password = req.get('password', '')
    r = _ua.login(phone, password)
    return r

@app.get("/v1/auth/me")
async def auth_me(token: str = ''):
    """v20.55: 当前用户信息
    query: ?token=xxx
    return: {user_id, phone, tier, ...} | {error}
    """
    if not token:
        return {'error': 'token is required'}
    u = _ua.get_user(token)
    if not u:
        return {'error': 'invalid or expired token'}
    # 隐藏 password
    u.pop('password', None)
    return u

@app.post("/v1/multimodal/search")
async def multimodal_search_endpoint(
    file: UploadFile = File(...),
    text: str = Form(""),
    token: str = Form(""),
):
    """v20.57: 多模态搜索 (图片 OCR + 走 search)"""
    try:
        suffix = "." + (file.filename or "image.png").split(".")[-1].lower()
        if suffix not in [".png", ".jpg", ".jpeg", ".bmp", ".webp"]:
            return {"error": f"unsupported format: {suffix}"}
        content = await file.read()
        if len(content) > 20 * 1024 * 1024:
            return {"error": "file too large (max 20MB)"}
        if token:
            user = _ua.get_user(token)
            if user:
                quota = _ua.check_quota(user["user_id"])
                if "error" in quota:
                    return {"error": quota["error"], "quota": quota}
        r = _mm.multimodal_search(content, context=text, file_suffix=suffix)
        return r
    except Exception as e:
        log.exception("multimodal error")
        return {"error": f"multimodal failed: {e}"}


@app.get("/v1/auth/quota")
async def auth_quota(token: str = ""):
    """v20.55: 查询 quota (不扣减)
    query: ?token=xxx
    return: {tier, used, limit, bucket, remaining}
    """
    if not token:
        return {"error": "token is required"}
    u = _ua.get_user(token)
    if not u:
        return {"error": "invalid or expired token"}
    import time as _t
    today = _t.strftime("%Y-%m-%d")
    month = _t.strftime("%Y-%m")
    year = _t.strftime("%Y")
    tier = u.get("tier", "free")
    cap = _ua.QUOTA.get(tier, 100)
    bucket = today if tier == "free" else (month if tier == "basic" else year)
    try:
        with open("/home/ubuntu/star-search/users.json") as f:
            d2 = json.load(f)
        used = d2.get("quota_usage", {}).get(bucket, {}).get(u["user_id"], 0)
    except Exception:
        used = 0
    return {"tier": tier, "used": used, "limit": cap, "bucket": bucket, "remaining": cap - used}


@app.post("/v1/deep_research")
async def deep_research_endpoint(req: dict):
    """v20.58: 3 步 Deep Research
    body: {query}
    return: {summary, key_points, sources, sub_queries, steps, elapsed_ms}
    """
    query = req.get('query', '').strip()
    if not query:
        return {'error': 'query is required', 'summary': ''}
    t0 = time.time()
    try:
        r = _dr.deep_research(query)
        r['elapsed_ms'] = int((time.time() - t0) * 1000) + r.get('elapsed_ms', 0)
        return r
    except Exception as e:
        log.exception("deep_research error")
        return {'error': f'deep_research failed: {e}', 'summary': '', 'elapsed_ms': int((time.time() - t0) * 1000)}


# ===== v20.59: 支付 =====
@app.post("/v1/pay/create")
async def pay_create(req: dict):
    """v20.59: 创建支付订单
    body: {token, tier, amount}
    tier: basic / pro
    return: {order_id, pay_url, sandbox_mode, ...}
    """
    token = req.get('token', '')
    tier = req.get('tier', '').strip()
    amount = int(req.get('amount', 0))
    if not token:
        return {'error': 'token is required'}
    user = _ua.get_user(token)
    if not user:
        return {'error': 'invalid token'}
    if tier not in _pay.TIERS:
        return {'error': f'unknown tier, valid: {list(_pay.TIERS.keys())}'}
    r = _pay.create_order(user['user_id'], tier, amount)
    return r


@app.get("/v1/pay/order")
async def pay_query(order_id: str, token: str = ''):
    """v20.59: 查询订单"""
    if not token:
        return {'error': 'token is required'}
    user = _ua.get_user(token)
    if not user:
        return {'error': 'invalid token'}
    order = _pay.query_order(order_id, user_id=user['user_id'])
    if not order:
        return {'error': 'order not found'}
    return order


@app.post("/v1/pay/cancel")
async def pay_cancel(req: dict):
    """v20.59: 取消订单 (待支付)"""
    token = req.get('token', '')
    order_id = req.get('order_id', '')
    if not token:
        return {'error': 'token is required'}
    user = _ua.get_user(token)
    if not user:
        return {'error': 'invalid token'}
    return _pay.cancel_order(order_id, user['user_id'])


@app.get("/v1/pay/orders")
async def pay_list(token: str = ''):
    """v20.59: 用户订单列表"""
    if not token:
        return {'error': 'token is required'}
    user = _ua.get_user(token)
    if not user:
        return {'error': 'invalid token'}
    return {'orders': _pay.list_orders(user['user_id'])}


@app.post("/v1/pay/mock_pay")
async def pay_mock_pay(req: dict):
    """v20.59: 沙箱模式 - 模拟支付成功
    真接后此端点应该删除
    """
    order_id = req.get('order_id', '')
    if not order_id:
        return {'error': 'order_id is required'}
    r = _pay.mark_paid(order_id)
    return r


@app.post("/v1/pay/callback")
async def pay_callback(request: Request):
    """v20.59: 支付宝异步回调
    沙箱模式: 直接 trust form params
    真接: 验证 alipay sign + return 'success'
    """
    try:
        form = await request.form()
        params = dict(form)
    except Exception:
        body = await request.body()
        params = json.loads(body.decode()) if body else {}
    r = _pay.alipay_callback(params)
    return r


@app.get("/v1/pay/health")
async def pay_health():
    """v20.59: 支付系统状态"""
    return {
        'engine': 'alipay',
        'sandbox_mode': _pay.ALIPAY_CONFIG['app_id'] == 'SANDBOX_PENDING',
        'tiers': list(_pay.TIERS.keys()),
        'status': 'ok',
    }


# ===== v20.60: 验证码 =====
@app.get("/v1/verify/config")
async def verify_config():
    """v20.60: 验证码配置 (前端拿 site_key + 选 method)
    真接短信/邮箱时, 这里也能用
    """
    return {
        'method': 'turnstile',  # 后期可改为 'sms' / 'email'
        'site_key': _verify.get_site_key(),
        'script_url': 'https://challenges.cloudflare.com/turnstile/v0/api.js',
    }


@app.post("/v1/verify/check")
async def verify_check(req: Request):
    """v20.60: 验证 Turnstile token
    body: {token} 或 form
    """
    try:
        body_bytes = await req.body()
        if body_bytes:
            try:
                params = json.loads(body_bytes.decode())
            except Exception:
                params = dict(urllib.parse.parse_qs(body_bytes.decode()))
                params = {k: v[0] if isinstance(v, list) else v for k, v in params.items()}
        else:
            params = {}
    except Exception:
        params = {}
    token = params.get('token', '')
    client_ip = req.client.host if req.client else ''
    r = _verify.verify_captcha(token, client_ip, method='turnstile')
    return r


@app.post("/v1/rewrite")
async def rewrite_endpoint(req: dict):
    """v20.61: query 重写 (返回变体列表)
    body: {query, use_llm}
    """
    q = req.get('query', '').strip()
    if not q:
        return {'error': 'query is required'}
    use_llm = req.get('use_llm', False)
    variants = _qr.rewrite_query(q, use_llm=use_llm)
    return {'original': q, 'variants': variants}


@app.post("/v1/brain")
async def brain_endpoint(req: dict):
    """v20.62: AI 智能分析 query
    body: {query, use_cache}
    return: {entity, intent, category, keywords, pinyin, search_engines, expected_info}
    """
    q = req.get('query', '').strip()
    if not q:
        return {'error': 'query is required'}
    use_cache = req.get('use_cache', True)
    return _brain.analyze_query(q, use_cache=use_cache)


@app.post("/v1/multi_search")
async def multi_search_endpoint(req: dict):
    """v20.63: 多路并行搜索
    body: {query, top, use_brain}
    - 调 super_brain 推荐引擎
    - 并行 2-3 引擎
    - 合并去重 + entity 匹配加分

    v20.75: 注入 brain_info + entity_card (跟 /v1/search 一致)
    """
    q = req.get('query', '').strip()
    if not q:
        return {'error': 'query is required'}
    top = int(req.get('top', 10))
    use_brain = req.get('use_brain', True)
    r = await _ms.multi_search(q, top=top, use_brain=use_brain)
    # v20.75: 注入 brain_info
    if use_brain and r.get("brain_info"):
        pass  # multi_search 已包含
    # v20.76: 注入 entity_card (基于 brain_info.entity)
    if r.get("brain_info") and r["brain_info"].get("entity"):
        try:
            ec = _ec.get_entity_card(r["brain_info"]["entity"])
            if ec:
                r["entity_card"] = ec
        except Exception:
            pass
    return r


@app.post("/v1/entity_card")
async def entity_card_endpoint(req: dict):
    """v20.66: 查实体知识卡片
    body: {entity, use_llm}
    - 查内置 KB
    - 查 LLM 缓存
    - use_llm=true: LLM 实时生成 (3-5s)
    """
    e = req.get('entity', '').strip()
    if not e:
        return {'error': 'entity is required'}
    use_llm = req.get('use_llm', False)
    card = _ec.get_entity_card(e)
    if card:
        return {'entity': e, 'card': card, 'source': 'kb'}
    if use_llm:
        card = _ec.create_entity_card_via_llm(e)
        if card:
            return {'entity': e, 'card': card, 'source': 'llm'}
    return {'entity': e, 'card': None, 'source': None}


@app.get("/v1/multimodal/health")
async def multimodal_health():
    """v20.57: tesseract 状态"""
    import subprocess as _sp
    try:
        v = _sp.run(["tesseract", "--version"], capture_output=True, text=True, timeout=5)
        langs = _sp.run(["tesseract", "--list-langs"], capture_output=True, text=True, timeout=5).stdout
        return {
            "engine": "tesseract",
            "version": v.stdout.split("\n")[0] if v.stdout else "unknown",
            "languages": [l.strip() for l in langs.split("\n")[1:] if l.strip()],
            "status": "ok",
        }
    except Exception as e:
        return {"engine": "tesseract", "status": "error", "error": str(e)}


async def auth_quota(token: str = ""):
    """v20.55: 查询 quota (不扣减)
    query: ?token=xxx
    return: {tier, used, limit, bucket, remaining}
    """
    if not token:
        return {'error': 'token is required'}
    u = _ua.get_user(token)
    if not u:
        return {'error': 'invalid or expired token'}
    # 不扣减, 只看
    import time as _t
    today = _t.strftime('%Y-%m-%d')
    month = _t.strftime('%Y-%m')
    year = _t.strftime('%Y')
    tier = u.get('tier', 'free')
    cap = _ua.QUOTA.get(tier, 100)
    bucket = today if tier == 'free' else (month if tier == 'basic' else year)
    # 读 quota 不加
    try:
        with open('/home/ubuntu/star-search/users.json') as f:
            d = json.load(f)
        used = d.get('quota_usage', {}).get(bucket, {}).get(u['user_id'], 0)
    except Exception:
        used = 0
    return {'tier': tier, 'used': used, 'limit': cap, 'bucket': bucket, 'remaining': cap - used}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="<server-ip>")
    parser.add_argument("--port", type=int, default=9800)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()
    print(f"🚀 star-search API v17.2 → http://{args.host}:{args.port}")
    print(f"   POST /v1/search         — 主搜索 (支持 ?answer=true 生成 LLM 答案)")
    print(f"   POST /v1/search/refresh — 增量追加")
    print(f"   POST /v1/answer         — 独立答案生成 (v17.2 新)")
    print(f"   GET  /v1/health         — 健康检查")
    print(f"   GET  /v1/modes          — 列出 11 模式")
    print(f"   GET  /v1/engines        — 列出 16 引擎")
    uvicorn.run("api_server:app", host=args.host, port=args.port, reload=args.reload)
