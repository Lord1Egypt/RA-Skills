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
import argparse, asyncio, sys, time
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# 复用 search.py + answer.py 的核心函数
sys.path.insert(0, str(Path(__file__).parent))
import search as s
import answer as a

app = FastAPI(title="star-search API", version="17.2",
              description="免费中文搜索 API · 16 引擎 · 智能去重 · 智能缓存 · LLM 答案层 🌟🌟🌟")

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
    answer: bool = Field(default=False, description="v17.2: 是否同时返回 LLM 生成的答案 (200-400字+来源)")

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
async def search(req: SearchRequest):
    start = time.time()
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

    elapsed = time.time() - start
    resp_data = {
        "query": req.query,
        "mode": req.mode,
        "engine": req.engine,
        "count": len(results),
        "elapsed_ms": int(elapsed * 1000),
        "results": results[:req.top],
        "cache_stats": s._cache_stats.copy(),
    }

    # v17.2: LLM 答案生成 (可选)
    if req.answer and results:
        answer_data = await a.generate_answer(req.query, results[:req.top], mode=req.mode)
        if answer_data.get("answer"):
            resp_data["answer"] = answer_data

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
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
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
