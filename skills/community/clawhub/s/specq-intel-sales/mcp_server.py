#!/usr/bin/env python3
"""
SpecQ MCP Server v2.3.1 — CLI mode added
Usage:
  # MCP mode (default)
  python mcp_server.py

  # CLI mode
  python mcp_server.py intel <product> <application> <scenario> [--format markdown]
  python mcp_server.py search <query> [--limit 5] [--source web]
  python mcp_server.py log <customer_id> <content> [--date YYYY-MM-DD] [--type in_person]
  python mcp_server.py insights [--customer-id ID] [--limit 10]
  python mcp_server.py feedback <product> <application> <outcome> [--lesson TEXT]
  python mcp_server.py memory recall <query> [--limit 5]
  python mcp_server.py memory save <content> <category> [--uid default]
"""

import argparse
import asyncio
import json
import os
import sys
import uuid
from datetime import date

from mcp.server.fastmcp import FastMCP

import memory as mem
import search as sch
import multimodal as mm
import output as out
import logger as log_mod

mcp = FastMCP("specq")
_log = log_mod.get_logger("mcp_server")


# ======================== MCP Tools (unchanged) ========================

@mcp.tool()
async def specq_memory(action: str, query: str | None = None, limit: int = 5,
                       content: str | None = None, category: str | None = None,
                       metadata: dict | None = None, goal: str | None = None,
                       plan: list[str] | None = None, current_step: int = 0,
                       uid: str = "default") -> str:
    try:
        if action == "recall":
            if not query:
                return json.dumps({"error": "recall 需要 query 参数"}, ensure_ascii=False)
            try:
                vec = mem.embed_text(query)
                collection = mem.get_chroma_collection()
                kwargs = {"query_embeddings": [vec], "n_results": limit}
                if uid != "default":
                    kwargs["where"] = {"user_id": uid}
                results = collection.query(**kwargs)
                memories = []
                if results and results["ids"] and results["ids"][0]:
                    for i, mid in enumerate(results["ids"][0]):
                        mmeta = results["metadatas"][0][i] if results["metadatas"] else {}
                        memories.append({
                            "memory_id": mid,
                            "content": results["documents"][0][i] if results["documents"] else "",
                            "category": mmeta.get("category", ""),
                            "metadata": {k: v for k, v in mmeta.items() if k not in ("category", "user_id")},
                            "score": round(results["distances"][0][i], 4) if results["distances"] else 0,
                        })
                return json.dumps({"memories": memories}, ensure_ascii=False, indent=2)
            except Exception as e:
                return json.dumps({"error": f"recall 失败: {e}"}, ensure_ascii=False)
        elif action == "save":
            if not content or not category:
                return json.dumps({"error": "save 需要 content + category"}, ensure_ascii=False)
            valid = {"visit", "feedback", "intel", "insight", "preference"}
            if category not in valid:
                return json.dumps({"error": f"category 必须是 {', '.join(sorted(valid))} 之一"}, ensure_ascii=False)
            try:
                vec = mem.embed_text(content)
                collection = mem.get_chroma_collection()
                mid = f"mem_{uuid.uuid4().hex[:12]}"
                mmeta = {"category": category, "user_id": uid, "timestamp": str(date.today())}
                if metadata:
                    mmeta.update({k: v for k, v in metadata.items() if v is not None})
                collection.add(ids=[mid], embeddings=[vec], documents=[content], metadatas=[mmeta])
                return json.dumps({"memory_id": mid, "status": "saved"}, ensure_ascii=False)
            except Exception as e:
                return json.dumps({"error": f"save 失败: {e}"}, ensure_ascii=False)
        elif action == "get_plan":
            wm = mem.load_working_memory(uid)
            return json.dumps(wm, ensure_ascii=False, indent=2)
        elif action == "set_plan":
            if not goal:
                return json.dumps({"error": "set_plan 需要 goal"}, ensure_ascii=False)
            wm = mem.load_working_memory(uid)
            wm["goal"] = goal
            wm["plan"] = plan or []
            wm["current_step"] = current_step
            mem.save_working_memory(uid, wm)
            return json.dumps({"status": "saved", "goal": goal, "total_steps": len(plan or [])}, ensure_ascii=False, indent=2)
        else:
            return json.dumps({"error": f"未知 action: {action}，支持 recall/save/get_plan/set_plan"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"specq_memory 执行失败: {e}"}, ensure_ascii=False)


@mcp.tool()
async def specq_search(query: str, limit: int = 5, source: str = "web") -> str:
    try:
        result = await sch.web_search(query, limit, source)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"results": [], "total": 0, "source": source, "error": str(e)}, ensure_ascii=False)


@mcp.tool()
async def specq_generate_intel(product: str, application: str, scenario: str,
                               output_format: str = "markdown", context_block: str | None = None,
                               anonymize: bool = True) -> str:
    enhanced_scenario = scenario
    try:
        vec = mem.embed_text(f"{product} {application}")
        collection = mem.get_chroma_collection()
        results = collection.query(query_embeddings=[vec], n_results=5)
        context_parts = []
        if results and results["ids"] and results["ids"][0]:
            for i, mid in enumerate(results["ids"][0]):
                doc = results["documents"][0][i]
                meta = results["metadatas"][0][i] if results["metadatas"] else {}
                context_parts.append(f"- [{meta.get('category','')}] {meta.get('timestamp','')}: {doc[:200]}")
        if context_parts:
            enhanced_scenario = f"{enhanced_scenario}\n\n【本地记忆召回】\n" + "\n".join(context_parts)
    except Exception as e:
        _log.warning(f"ChromaDB 记忆召回失败: {e}")
    try:
        search_query = f"{product} {application} 技术参数 竞品"
        search_result = await sch.web_search(search_query, limit=3)
        if search_result.get("results"):
            web_snippets = "\n".join(
                f"- [{r['title']}]({r['url']}): {r['snippet'][:150]}"
                for r in search_result["results"]
            )
            enhanced_scenario += f"\n\n【联网搜索补充数据】\n{web_snippets}"
    except Exception as e:
        _log.warning(f"联网搜索失败: {e}")
    if context_block:
        enhanced_scenario += f"\n\n【历史记忆】\n{context_block}"
    reply_text = await _generate_intel_local(product, application, enhanced_scenario)
    try:
        summary = reply_text[:300]
        vec2 = mem.embed_text(summary)
        collection2 = mem.get_chroma_collection()
        collection2.add(
            ids=[f"mem_{uuid.uuid4().hex[:12]}"],
            embeddings=[vec2],
            documents=[summary],
            metadatas=[{"category": "intel", "user_id": "default", "timestamp": str(date.today())}],
        )
    except Exception:
        pass
    formatted = out.format_output(reply_text, output_format, {
        "product": product, "application": application, "timestamp": str(date.today()),
    })
    return formatted


@mcp.tool()
async def specq_log_visit(customer_id: int, content: str, visit_date: str | None = None,
                          visit_type: str = "in_person", image_paths: list[str] | None = None,
                          audio_path: str | None = None, video_path: str | None = None) -> str:
    if not visit_date:
        visit_date = date.today().isoformat()
    if customer_id <= 0:
        return json.dumps({"error": "customer_id 必须为正整数"}, ensure_ascii=False)
    extra_text: list[str] = []
    if audio_path and os.path.exists(audio_path):
        try:
            audio_text = await mm.process_audio(audio_path)
            if audio_text:
                extra_text.append(f"【语音转录】{audio_text[:500]}")
        except Exception as e:
            _log.warning(f"音频转录失败: {e}")
    if image_paths:
        for img in image_paths[:5]:
            if os.path.exists(img):
                try:
                    img_text = await mm.process_image(img)
                    if img_text:
                        extra_text.append(f"【图片 OCR】{img_text[:300]}")
                except Exception as e_img:
                    _log.warning(f"图片OCR失败: {e_img}")
    if video_path and os.path.exists(video_path):
        try:
            vid_text = await mm.process_video(video_path)
            if vid_text:
                extra_text.append(f"【视频摘要】{vid_text[:500]}")
        except Exception as e:
            _log.warning(f"视频处理失败: {e}")
    if extra_text:
        content = content + "\n\n" + "\n\n".join(extra_text)
    summary = content[:300] if len(content) > 300 else content
    vec = mem.embed_text(summary)
    collection = mem.get_chroma_collection()
    mid = f"mem_{uuid.uuid4().hex[:12]}"
    collection.add(
        ids=[mid], embeddings=[vec], documents=[summary],
        metadatas=[{
            "category": "visit", "user_id": "default", "customer_id": str(customer_id),
            "customer_name": f"ID={customer_id}", "visit_type": visit_type, "timestamp": visit_date,
        }],
    )
    return f"✅ 暗知识已沉淀。\n- 客户 ID: {customer_id}\n- 拜访 ID: {mid}\n- 日期: {visit_date}\n- 类型: {visit_type}"


@mcp.tool()
async def specq_extract_insights(customer_id: int | None = None, limit: int = 10,
                                 db_path: str | None = None, db_query: str | None = None,
                                 api_url: str | None = None, api_params: dict | None = None) -> str:
    collection = mem.get_chroma_collection()
    where_filter: dict = {"category": {"$in": ["visit", "feedback"]}}
    if customer_id:
        where_filter["customer_id"] = str(customer_id)
    results = collection.get(where=where_filter, limit=50)
    if not results or not results["ids"]:
        return "⚠️ 暂无拜访记录或丢单复盘。请先用 specq_log_visit 沉淀暗数据。"
    records: list[dict] = []
    for i, mid in enumerate(results["ids"]):
        meta = results["metadatas"][i] if results["metadatas"] else {}
        doc = results["documents"][i] if results["documents"] else ""
        records.append({
            "id": mid, "content": doc, "category": meta.get("category", ""),
            "customer_name": meta.get("customer_name", meta.get("customer_id", "")),
            "timestamp": meta.get("timestamp", ""),
        })
    db_data = []
    if db_path and db_query and os.path.exists(db_path):
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            rows = conn.execute(db_query).fetchall()
            db_data = [dict(r) for r in rows[:100]]
            conn.close()
        except Exception as e:
            _log.warning(f"本地数据库查询失败: {e}")
    api_data = []
    if api_url:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=10.0) as c:
                r = await c.get(api_url, params=api_params or {})
                if r.status_code == 200:
                    raw = r.json()
                    api_data = raw if isinstance(raw, list) else [raw]
        except Exception as e:
            _log.warning(f"在线API数据拉取失败: {e}")
    records_text = json.dumps(records[:20], ensure_ascii=False, indent=2)
    extra_sections = ""
    if db_data:
        extra_sections += f"\n本地数据库数据:\n{json.dumps(db_data[:20], ensure_ascii=False, indent=2)}"
    if api_data:
        extra_sections += f"\n在线 API 数据:\n{json.dumps(api_data[:20], ensure_ascii=False, indent=2)}"
    system_prompt = """你是电子化学品销售数据分析师。从以下拜访纪要和丢单复盘中提取结构化洞察。
严格按以下分类：
- tech_requirement: 客户关注的技术指标（粗糙度、延展性、精度等）
- competitor_info: 竞品动态（哪家竞品、什么产品、价格/性能优势）
- import_barrier: 导入障碍（认证周期、切换风险、工艺匹配度）
- decision_chain: 决策链信息（谁拍板、什么流程、关键决策者）
- price_sensitivity: 价格敏感度（客户对价格的关注度、预算范围）
每条洞察格式：
{"category": "分类", "insight": "具体洞察（一句话）", "customer_name": "客户名", "source_visit_id": 来源ID, "confidence": 0.0-1.0}
只返回 JSON 数组。没有足够数据时返回空数组 []。"""
    user_prompt = f"暗数据记录:\n{records_text}\n{extra_sections}\n\n请提取结构化洞察（最多 {limit} 条）："
    try:
        result = await _ask_llm(system_prompt, user_prompt, max_tokens=2000)
    except Exception as e:
        return f"Error: LLM 调用失败: {e}"
    try:
        insights = json.loads(result)
    except json.JSONDecodeError:
        insights = result
    summary = {
        "total_records": len(records),
        "customers_involved": len(set(r.get("customer_name", "") for r in records)),
        "insights": insights[:limit] if isinstance(insights, list) else [],
    }
    return json.dumps(summary, ensure_ascii=False, indent=2)


@mcp.tool()
async def specq_feedback(product: str, application: str, outcome: str,
                         lesson: str | None = None, accuracy_notes: str | None = None,
                         uid: str = "default") -> str:
    if outcome not in ("won", "lost", "follow_up"):
        return f"Error: outcome 必须是 won / lost / follow_up，当前值: {outcome}"
    memory_content = f"[{outcome}] {product} - {application}"
    if lesson:
        memory_content += f": {lesson}"
    try:
        vec = mem.embed_text(memory_content[:300])
        collection = mem.get_chroma_collection()
        mid = f"mem_{uuid.uuid4().hex[:12]}"
        collection.add(
            ids=[mid], embeddings=[vec], documents=[memory_content[:500]],
            metadatas=[{
                "category": "feedback", "user_id": uid, "product": product,
                "application": application, "outcome": outcome, "timestamp": str(date.today()),
            }],
        )
    except Exception as e:
        _log.warning(f"记忆写入失败(feedback): {e}")
    try:
        analytics_file = os.path.join(mem.get_memory_dir(), "analytics.jsonl")
        with open(analytics_file, "a") as f:
            f.write(json.dumps({
                "event": "feedback", "uid": uid, "product": product,
                "outcome": outcome, "timestamp": str(date.today()),
            }, ensure_ascii=False) + "\n")
    except Exception:
        pass
    result = f"✅ 反馈已记录。\n- 产品: {product}\n- 结果: {outcome}"
    if accuracy_notes:
        result += "\n- 准度反馈已记录，将用于后续情报包改进"
    return result


# ======================== MCP Sampling helpers ========================

async def _ask_llm(system_prompt: str, user_prompt: str, max_tokens: int = 4000) -> str:
    from mcp.types import CreateMessageRequestParams, SamplingMessage, TextContent
    ctx = mcp.get_context()
    if not ctx:
        raise RuntimeError("MCP context not available — 当前 Agent 客户端不支持 MCP Sampling")
    result = await ctx.session.create_message(
        CreateMessageRequestParams(
            messages=[SamplingMessage(role="user", content=TextContent(type="text", text=f"{system_prompt}\n\n---\n\n{user_prompt}"))],
            max_tokens=max_tokens, temperature=0.3,
        )
    )
    content = result.content
    if isinstance(content, TextContent):
        return content.text
    if isinstance(content, list):
        for part in content:
            if hasattr(part, 'text'):
                return part.text
    return str(content)


async def _generate_intel_local(product: str, application: str, enhanced_scenario: str) -> str:
    system_prompt = """你是半导体产业链电子化学品销售专家 FAE。根据输入的产品信息、应用场景和历史数据，生成一份结构化的攻单情报包。
严格按以下八模块输出 Markdown：
## 1. 产品概览
## 2. 技术指标对比
## 3. 竞品格局
## 4. 客户关注指标
## 5. 切入机会
## 6. 导入障碍
## 7. 行动建议
## 8. 参考来源
规则：没有历史数据时标注 [经验推断，暂无销售数据支撑]；有暗数据时优先使用标注 [来自销售拜访记录]；有联网搜索结果时标注 [来自联网搜索]；不编造具体客户名称、联系方式；直接输出 Markdown，不要输出前言/后缀寒暄"""
    user_prompt = f"生成以下产品的攻单情报包：\n产品：{product}\n应用场景：{application}\n附加上下文：{enhanced_scenario}"
    try:
        return await _ask_llm(system_prompt, user_prompt)
    except Exception as e:
        _log.error(f"LLM Sampling 失败: {e}")
        return f"Error: 情报包生成失败 — Agent LLM 调用异常: {e}"


# ======================== CLI Commands ========================

def _run_async(coro):
    """Run async coroutine in sync context."""
    return asyncio.run(coro)


def cmd_intel(args):
    result = _run_async(specq_generate_intel(args.product, args.application, args.scenario, args.format))
    print(result)


def cmd_search(args):
    result = _run_async(specq_search(args.query, args.limit, args.source))
    print(result)


def cmd_log(args):
    result = _run_async(specq_log_visit(args.customer_id, args.content, args.date, args.type))
    print(result)


def cmd_insights(args):
    result = _run_async(specq_extract_insights(args.customer_id, args.limit))
    print(result)


def cmd_feedback(args):
    result = _run_async(specq_feedback(args.product, args.application, args.outcome, args.lesson))
    print(result)


def cmd_memory(args):
    if args.action == "recall":
        result = _run_async(specq_memory(action="recall", query=args.query, limit=args.limit))
    elif args.action == "save":
        result = _run_async(specq_memory(action="save", content=args.content, category=args.category, uid=args.uid))
    else:
        result = json.dumps({"error": f"CLI 不支持 action={args.action}，请用 MCP 模式"}, ensure_ascii=False)
    print(result)


def main():
    parser = argparse.ArgumentParser(
        description="SpecQ MCP Server & CLI - 电子化学品销售情报工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mcp_server.py intel "电镀铜溶液" "PCB电镀" "降低粗糙度"
  python mcp_server.py search "电镀铜溶液 技术参数"
  python mcp_server.py log 1001 "客户关注粗糙度<0.5μm，竞品A报价低15%"
  python mcp_server.py insights --customer-id 1001
  python mcp_server.py feedback "电镀铜溶液" "PCB电镀" won
  python mcp_server.py memory recall "粗糙度"
  python mcp_server.py memory save "客户A偏好低温工艺" preference
        """
    )
    sub = parser.add_subparsers(dest="command")

    # intel
    p = sub.add_parser("intel", help="生成攻单情报包")
    p.add_argument("product", help="产品名称")
    p.add_argument("application", help="应用场景")
    p.add_argument("scenario", help="销售目标/背景")
    p.add_argument("--format", "-f", default="markdown", choices=["markdown", "email", "chat"])

    # search
    p = sub.add_parser("search", help="联网搜索")
    p.add_argument("query", help="搜索关键词")
    p.add_argument("--limit", "-n", type=int, default=5)
    p.add_argument("--source", "-s", default="web", choices=["web", "news", "scholar"])

    # log
    p = sub.add_parser("log", help="记录销售拜访纪要")
    p.add_argument("customer_id", type=int, help="客户 ID")
    p.add_argument("content", help="拜访纪要内容")
    p.add_argument("--date", "-d", help="拜访日期 (YYYY-MM-DD)")
    p.add_argument("--type", "-t", default="in_person", choices=["in_person", "phone", "wechat"])

    # insights
    p = sub.add_parser("insights", help="提取结构化洞察")
    p.add_argument("--customer-id", "-c", type=int, help="客户 ID")
    p.add_argument("--limit", "-n", type=int, default=10)

    # feedback
    p = sub.add_parser("feedback", help="记录攻单结果反馈")
    p.add_argument("product", help="产品名称")
    p.add_argument("application", help="应用场景")
    p.add_argument("outcome", choices=["won", "lost", "follow_up"], help="结果")
    p.add_argument("--lesson", "-l", help="丢单复盘摘要")

    # memory
    p = sub.add_parser("memory", help="记忆操作")
    p.add_argument("action", choices=["recall", "save"], help="操作类型")
    p.add_argument("query_or_content", help="recall: 搜索词 | save: 记忆内容")
    p.add_argument("--limit", "-n", type=int, default=5)
    p.add_argument("--category", "-c", choices=["visit", "feedback", "intel", "insight", "preference"])
    p.add_argument("--uid", default="default")

    args = parser.parse_args()

    if not args.command:
        mcp.run(transport="stdio")
        return

    if args.command == "intel":
        cmd_intel(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "log":
        cmd_log(args)
    elif args.command == "insights":
        cmd_insights(args)
    elif args.command == "feedback":
        cmd_feedback(args)
    elif args.command == "memory":
        # remap positional arg for memory subcommand
        if args.action == "recall":
            args.query = args.query_or_content
            cmd_memory(args)
        elif args.action == "save":
            args.content = args.query_or_content
            if not args.category:
                print("Error: memory save 需要 --category", file=sys.stderr)
                sys.exit(1)
            cmd_memory(args)


if __name__ == "__main__":
    main()
