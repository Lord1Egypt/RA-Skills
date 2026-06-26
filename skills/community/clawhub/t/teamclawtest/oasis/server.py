"""
OASIS Forum - FastAPI Server

A standalone discussion forum service where resident expert agents
debate user-submitted questions in parallel.

Start with:
    uvicorn oasis.server:app --host 0.0.0.0 --port 51202
    or
    python -m oasis.server
"""

import os
import sys
import asyncio
import uuid
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import uvicorn
import aiosqlite
import yaml as _yaml
import json

from dotenv import load_dotenv

# --- Path setup ---
_this_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_this_dir)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

env_path = os.path.join(_project_root, "config", ".env")
load_dotenv(dotenv_path=env_path)

from oasis.models import (
    CreateTopicRequest,
    TopicDetail,
    TopicSummary,
    PostInfo,
    TimelineEventInfo,
    DiscussionStatus,
)
from oasis.forum import DiscussionForum
from oasis.engine import DiscussionEngine

# Ensure src/ is importable for helper reuse
_src_path = os.path.join(_project_root, "src")
if _src_path not in sys.path:
    sys.path.insert(0, _src_path)
try:
    from mcp_oasis import _yaml_to_layout_data
except Exception:
    _yaml_to_layout_data = None


# --- In-memory storage ---
discussions: dict[str, DiscussionForum] = {}
engines: dict[str, DiscussionEngine] = {}
tasks: dict[str, asyncio.Task] = {}


# --- Helpers ---

def _get_forum_or_404(topic_id: str) -> DiscussionForum:
    forum = discussions.get(topic_id)
    if not forum:
        raise HTTPException(404, "Topic not found")
    return forum


def _check_owner(forum: DiscussionForum, user_id: str):
    """Verify the requester owns this discussion."""
    if forum.user_id != user_id:
        raise HTTPException(403, "You do not own this discussion")


# --- Lifespan ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    loaded = DiscussionForum.load_all()
    discussions.update(loaded)
    print(f"[OASIS] 🏛️ Forum server started (loaded {len(loaded)} historical discussions)")
    yield
    for tid, forum in discussions.items():
        if forum.status == "discussing":
            forum.status = "error"
            forum.conclusion = "服务关闭，讨论被终止"
        forum.save()
    print("[OASIS] 🏛️ Forum server stopped (all discussions saved)")


app = FastAPI(
    title="OASIS Discussion Forum",
    description="Multi-expert parallel discussion service",
    lifespan=lifespan,
)


# ------------------------------------------------------------------
# Background task runner
# ------------------------------------------------------------------
async def _run_discussion(topic_id: str, engine: DiscussionEngine):
    """Run a discussion engine in the background, then fire callback if configured."""
    forum = discussions.get(topic_id)
    try:
        await engine.run()
    except Exception as e:
        print(f"[OASIS] ❌ Topic {topic_id} background error: {e}")
        if forum:
            forum.status = "error"
            forum.conclusion = f"讨论出错: {str(e)}"

    if forum:
        forum.save()

    # Fire callback notification
    cb_url = getattr(engine, "callback_url", None)
    if cb_url:
        conclusion = forum.conclusion if forum else "（无结论）"
        status = forum.status if forum else "error"
        cb_session = getattr(engine, "callback_session_id", "default") or "default"
        user_id = forum.user_id if forum else "anonymous"
        internal_token = os.getenv("INTERNAL_TOKEN", "")

        text = (
            f"[OASIS 子任务完成通知]\n"
            f"Topic ID: {topic_id}\n"
            f"状态: {status}\n"
            f"主题: {forum.question if forum else '?'}\n\n"
            f"📋 结论:\n{conclusion}"
        )
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                await client.post(
                    cb_url,
                    json={"user_id": user_id, "text": text, "session_id": cb_session},
                    headers={"X-Internal-Token": internal_token},
                )
            print(f"[OASIS] 📨 Callback sent for {topic_id} → {cb_session}")
        except Exception as cb_err:
            print(f"[OASIS] ⚠️ Callback failed for {topic_id}: {cb_err}")


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------

@app.post("/topics", response_model=dict)
async def create_topic(req: CreateTopicRequest):
    """Create a new discussion topic. Returns topic_id for tracking."""
    topic_id = str(uuid.uuid4())[:8]

    forum = DiscussionForum(
        topic_id=topic_id,
        question=req.question,
        user_id=req.user_id,
        max_rounds=req.max_rounds,
    )
    discussions[topic_id] = forum
    forum.save()

    engine = DiscussionEngine(
        forum=forum,
        schedule_yaml=req.schedule_yaml,
        schedule_file=req.schedule_file,
        bot_enabled_tools=req.bot_enabled_tools,
        bot_timeout=req.bot_timeout,
        user_id=req.user_id,
        early_stop=req.early_stop,
        discussion=req.discussion,
    )
    engine.callback_url = req.callback_url
    engine.callback_session_id = req.callback_session_id
    engines[topic_id] = engine

    task = asyncio.create_task(_run_discussion(topic_id, engine))
    tasks[topic_id] = task

    return {
        "topic_id": topic_id,
        "status": "pending",
        "message": f"Discussion started with {len(engine.experts)} experts",
    }


@app.delete("/topics/{topic_id}")
async def cancel_topic(topic_id: str, user_id: str = Query(...)):
    """Force-cancel a running discussion."""
    forum = _get_forum_or_404(topic_id)
    _check_owner(forum, user_id)

    if forum.status != "discussing":
        return {"topic_id": topic_id, "status": forum.status, "message": "Discussion already finished"}

    engine = engines.get(topic_id)
    if engine:
        engine.cancel()

    task = tasks.get(topic_id)
    if task and not task.done():
        task.cancel()

    forum.save()
    return {"topic_id": topic_id, "status": "cancelled", "message": "Discussion cancelled"}


@app.post("/topics/{topic_id}/purge")
async def purge_topic(topic_id: str, user_id: str = Query(...)):
    """Permanently delete a discussion record."""
    forum = _get_forum_or_404(topic_id)
    _check_owner(forum, user_id)

    if forum.status in ("pending", "discussing"):
        engine = engines.get(topic_id)
        if engine:
            engine.cancel()
        task = tasks.get(topic_id)
        if task and not task.done():
            task.cancel()

    storage_path = forum._storage_path()
    if os.path.exists(storage_path):
        os.remove(storage_path)

    discussions.pop(topic_id, None)
    engines.pop(topic_id, None)
    tasks.pop(topic_id, None)

    return {"topic_id": topic_id, "message": "Discussion permanently deleted"}


@app.delete("/topics")
async def purge_all_topics(user_id: str = Query(...)):
    """Delete all topics for a specific user."""
    global discussions, engines, tasks

    to_delete = [
        tid for tid, forum in discussions.items()
        if forum.user_id == user_id
    ]

    deleted_count = 0
    for tid in to_delete:
        forum = discussions.get(tid)
        if forum:
            if forum.status in ("pending", "discussing"):
                engine = engines.get(tid)
                if engine:
                    engine.cancel()
                task = tasks.get(tid)
                if task and not task.done():
                    task.cancel()

            storage_path = forum._storage_path()
            if os.path.exists(storage_path):
                os.remove(storage_path)

            discussions.pop(tid, None)
            engines.pop(tid, None)
            tasks.pop(tid, None)
            deleted_count += 1

    return {"deleted_count": deleted_count, "message": f"Deleted {deleted_count} topics"}


@app.get("/topics/{topic_id}", response_model=TopicDetail)
async def get_topic(topic_id: str, user_id: str = Query(...)):
    """Get full discussion detail."""
    forum = _get_forum_or_404(topic_id)
    _check_owner(forum, user_id)

    posts = await forum.browse()
    return TopicDetail(
        topic_id=forum.topic_id,
        question=forum.question,
        user_id=forum.user_id,
        status=DiscussionStatus(forum.status),
        current_round=forum.current_round,
        max_rounds=forum.max_rounds,
        posts=[
            PostInfo(
                id=p.id,
                author=p.author,
                content=p.content,
                reply_to=p.reply_to,
                upvotes=p.upvotes,
                downvotes=p.downvotes,
                timestamp=p.timestamp,
                elapsed=p.elapsed,
            )
            for p in posts
        ],
        timeline=[
            TimelineEventInfo(
                elapsed=e.elapsed,
                event=e.event,
                agent=e.agent,
                detail=e.detail,
            )
            for e in forum.timeline
        ],
        discussion=forum.discussion,
        conclusion=forum.conclusion,
    )


@app.get("/topics/{topic_id}/stream")
async def stream_topic(topic_id: str, user_id: str = Query(...)):
    """SSE stream for real-time discussion updates."""
    forum = _get_forum_or_404(topic_id)
    _check_owner(forum, user_id)

    async def event_generator():
        last_count = 0
        last_round = 0
        last_timeline_idx = 0      # 已发送的 timeline 事件索引

        while forum.status in ("pending", "discussing"):
            if forum.discussion:
                # ── 讨论模式：原有逻辑，按帖子轮询 ──
                posts = await forum.browse()

                if forum.current_round > last_round:
                    last_round = forum.current_round
                    yield f"data: 📢 === 第 {last_round} 轮讨论 ===\n\n"

                if len(posts) > last_count:
                    for p in posts[last_count:]:
                        prefix = f"↳回复#{p.reply_to}" if p.reply_to else "📌"
                        yield (
                            f"data: {prefix} [{p.author}] "
                            f"(👍{p.upvotes}): {p.content}\n\n"
                        )
                    last_count = len(posts)
            else:
                # ── 执行模式：timeline 事件当普通消息发送 ──
                tl = forum.timeline

                while last_timeline_idx < len(tl):
                    ev = tl[last_timeline_idx]
                    last_timeline_idx += 1

                    if ev.event == "start":
                        yield f"data: 🚀 执行开始\n\n"
                    elif ev.event == "round":
                        yield f"data: 📢 {ev.detail}\n\n"
                    elif ev.event == "agent_call":
                        yield f"data: ⏳ {ev.agent} 开始执行...\n\n"
                    elif ev.event == "agent_done":
                        yield f"data: ✅ {ev.agent} 执行完成\n\n"
                    elif ev.event == "conclude":
                        yield f"data: 🏁 执行完成\n\n"

            await asyncio.sleep(1)

        if forum.discussion:
            if forum.conclusion:
                yield f"data: \n🏆 === 讨论结论 ===\n{forum.conclusion}\n\n"
        else:
            yield f"data: ✅ 已完成\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/topics", response_model=list[TopicSummary])
async def list_topics(user_id: str = Query(...)):
    """List discussion topics for a specific user."""
    items = []
    for f in discussions.values():
        if f.user_id != user_id:
            continue
        items.append(
            TopicSummary(
                topic_id=f.topic_id,
                question=f.question,
                user_id=f.user_id,
                status=DiscussionStatus(f.status),
                post_count=len(f.posts),
                current_round=f.current_round,
                max_rounds=f.max_rounds,
                created_at=f.created_at,
            )
        )
    items.sort(key=lambda x: x.created_at, reverse=True)
    return items


@app.get("/topics/{topic_id}/conclusion")
async def get_conclusion(topic_id: str, user_id: str = Query(...), timeout: int = 300):
    """Get the final conclusion (blocks until discussion finishes)."""
    forum = _get_forum_or_404(topic_id)
    _check_owner(forum, user_id)

    elapsed = 0
    while forum.status not in ("concluded", "error") and elapsed < timeout:
        await asyncio.sleep(1)
        elapsed += 1

    if forum.status == "error":
        raise HTTPException(500, f"Discussion failed: {forum.conclusion}")
    if forum.status != "concluded":
        raise HTTPException(504, "Discussion timed out")

    return {
        "topic_id": topic_id,
        "question": forum.question,
        "conclusion": forum.conclusion,
        "rounds": forum.current_round,
        "total_posts": len(forum.posts),
    }


# ------------------------------------------------------------------
# Expert persona CRUD
# ------------------------------------------------------------------

@app.get("/experts")
async def list_experts(user_id: str = ""):
    """List all available expert agents (public + user custom)."""
    from oasis.experts import get_all_experts
    configs = get_all_experts(user_id or None)
    return {
        "experts": [
            {
                "name": c["name"],
                "tag": c["tag"],
                "persona": c["persona"],
                "source": c.get("source", "public"),
            }
            for c in configs
        ]
    }


@app.get("/sessions/oasis")
async def list_oasis_sessions(user_id: str = Query("")):
    """List all oasis-managed sessions by scanning the agent checkpoint DB.

    Query param: user_id (optional). If provided, only sessions for that user are returned.
    """
    db_path = os.path.join(_project_root, "data", "agent_memory.db")
    if not os.path.exists(db_path):
        return {"sessions": []}

    prefix = f"{user_id}#" if user_id else None
    sessions = []
    try:
        async with aiosqlite.connect(db_path) as db:
            if prefix:
                cursor = await db.execute(
                    "SELECT DISTINCT thread_id FROM checkpoints WHERE thread_id LIKE ? ORDER BY thread_id",
                    (f"{prefix}%#oasis%",),
                )
            else:
                cursor = await db.execute(
                    "SELECT DISTINCT thread_id FROM checkpoints WHERE thread_id LIKE ? ORDER BY thread_id",
                    (f"%#oasis%",),
                )
            rows = await cursor.fetchall()
            for (thread_id,) in rows:
                # thread_id format: "user#session_id"
                if "#" in thread_id:
                    user_part, sid = thread_id.split("#", 1)
                else:
                    user_part = ""
                    sid = thread_id
                tag = sid.split("#")[0] if "#" in sid else sid

                # get latest checkpoint message count
                ckpt_cursor = await db.execute(
                    "SELECT type, checkpoint FROM checkpoints WHERE thread_id = ? ORDER BY ROWID DESC LIMIT 1",
                    (thread_id,),
                )
                ckpt_row = await ckpt_cursor.fetchone()
                msg_count = 0
                if ckpt_row:
                    try:
                        # Try to decode JSON-like checkpoint; conservative approach
                        ckpt_blob = ckpt_row[1]
                        if isinstance(ckpt_blob, (bytes, bytearray)):
                            ckpt_blob = ckpt_blob.decode('utf-8', errors='ignore')
                        ckpt_data = json.loads(ckpt_blob) if isinstance(ckpt_blob, str) else {}
                        messages = ckpt_data.get("channel_values", {}).get("messages", [])
                        msg_count = len(messages)
                    except Exception:
                        msg_count = 0

                sessions.append({
                    "user_id": user_part,
                    "session_id": sid,
                    "tag": tag,
                    "message_count": msg_count,
                })
    except Exception as e:
        raise HTTPException(500, f"扫描 session 失败: {e}")

    return {"sessions": sessions}


class WorkflowSaveRequest(BaseModel):
    user_id: str
    name: str
    schedule_yaml: str
    description: str = ""
    save_layout: bool = False  # deprecated, layout is now generated on-the-fly from YAML


@app.post("/workflows")
async def save_workflow(req: WorkflowSaveRequest):
    """Save a YAML workflow under data/user_files/{user}/oasis/yaml/."""
    user = req.user_id
    name = req.name
    if not name.endswith((".yaml", ".yml")):
        name += ".yaml"

    # validate YAML
    try:
        data = _yaml.safe_load(req.schedule_yaml)
        if not isinstance(data, dict) or "plan" not in data:
            raise ValueError("must contain 'plan'")
    except Exception as e:
        raise HTTPException(400, f"YAML 解析失败: {e}")

    yaml_dir = os.path.join(_project_root, "data", "user_files", user, "oasis", "yaml")
    os.makedirs(yaml_dir, exist_ok=True)
    filepath = os.path.join(yaml_dir, name)
    content = (f"# {req.description}\n" if req.description else "") + req.schedule_yaml
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(500, f"保存失败: {e}")

    return {"status": "ok", "file": name, "path": filepath}


@app.get("/workflows")
async def list_workflows(user_id: str = Query(...)):
    yaml_dir = os.path.join(_project_root, "data", "user_files", user_id, "oasis", "yaml")
    if not os.path.isdir(yaml_dir):
        return {"workflows": []}
    files = sorted(f for f in os.listdir(yaml_dir) if f.endswith((".yaml", ".yml")))
    items = []
    for fname in files:
        fpath = os.path.join(yaml_dir, fname)
        desc = ""
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                first = f.readline().strip()
                if first.startswith("#"):
                    desc = first.lstrip("# ")
        except Exception:
            pass
        items.append({"file": fname, "description": desc})
    return {"workflows": items}


class LayoutFromYamlRequest(BaseModel):
    user_id: str
    yaml_source: str
    layout_name: str = ""


@app.post("/layouts/from-yaml")
async def layouts_from_yaml(req: LayoutFromYamlRequest):
    """Generate a layout from YAML on-the-fly (no file saved; layout is ephemeral)."""
    user = req.user_id
    yaml_src = req.yaml_source
    yaml_content = ""
    source_name = ""
    if "\n" not in yaml_src and yaml_src.strip().endswith(('.yaml', '.yml')):
        yaml_dir = os.path.join(_project_root, "data", "user_files", user, "oasis", "yaml")
        fpath = os.path.join(yaml_dir, yaml_src.strip())
        if not os.path.isfile(fpath):
            raise HTTPException(404, f"YAML 文件不存在: {yaml_src}")
        with open(fpath, "r", encoding="utf-8") as f:
            yaml_content = f.read()
        source_name = yaml_src.replace('.yaml','').replace('.yml','')
    else:
        yaml_content = yaml_src
        source_name = "converted"

    if _yaml_to_layout_data is None:
        raise HTTPException(500, "layout 功能不可用（缺少实现）")

    try:
        layout = _yaml_to_layout_data(yaml_content)
    except Exception as e:
        raise HTTPException(400, f"YAML 转换失败: {e}")

    layout_name = req.layout_name or source_name
    layout["name"] = layout_name
    return {"status": "ok", "layout": layout_name, "data": layout}


class UserExpertRequest(BaseModel):
    user_id: str
    name: str = ""
    tag: str = ""
    persona: str = ""
    temperature: float = 0.7


@app.post("/experts/user")
async def add_user_expert_route(req: UserExpertRequest):
    from oasis.experts import add_user_expert
    try:
        expert = add_user_expert(req.user_id, req.model_dump())
        return {"status": "ok", "expert": expert}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/experts/user/{tag}")
async def update_user_expert_route(tag: str, req: UserExpertRequest):
    from oasis.experts import update_user_expert
    try:
        expert = update_user_expert(req.user_id, tag, req.model_dump())
        return {"status": "ok", "expert": expert}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/experts/user/{tag}")
async def delete_user_expert_route(tag: str, user_id: str = Query(...)):
    from oasis.experts import delete_user_expert
    try:
        deleted = delete_user_expert(user_id, tag)
        return {"status": "ok", "deleted": deleted}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ------------------------------------------------------------------
# OpenClaw session discovery
# ------------------------------------------------------------------

_OPENCLAW_SESSIONS_FILE = os.getenv(
    "OPENCLAW_SESSIONS_FILE",
    "",
)


@app.get("/sessions/openclaw")
async def list_openclaw_sessions(filter: str = Query("")):
    """List OpenClaw sessions from sessions.json file."""
    if not os.path.exists(_OPENCLAW_SESSIONS_FILE):
        return {"sessions": [], "available": False, "message": "OpenClaw sessions file not found"}

    try:
        with open(_OPENCLAW_SESSIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise HTTPException(500, f"Failed to read OpenClaw sessions: {e}")

    # Support both dict (key->session) and list formats
    sessions = []
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, dict):
                v.setdefault("key", k)
                sessions.append(v)
    elif isinstance(data, list):
        sessions = data

    # Keyword filter
    if filter:
        sessions = [s for s in sessions if filter.lower() in s.get("key", "").lower()]

    # Sort by updatedAt descending
    sessions.sort(key=lambda s: s.get("updatedAt", 0), reverse=True)

    result = [
        {
            "key": s.get("key"),
            "sessionId": s.get("sessionId"),
            "kind": s.get("kind"),
            "channel": s.get("channel"),
            "model": s.get("model"),
            "updatedAt": s.get("updatedAt"),
            "contextTokens": s.get("contextTokens", 0),
            "totalTokens": s.get("totalTokens", 0),
        }
        for s in sessions
    ]

    # Strip /v1/chat/completions suffix — .env stores the full URL,
    # but canvas / YAML only needs the base URL (engine auto-appends the path)
    raw_url = os.getenv("OPENCLAW_API_URL", "")
    base_url = raw_url.replace("/v1/chat/completions", "").rstrip("/")

    return {
        "sessions": result,
        "available": True,
        # Provide OpenClaw-specific endpoint config for auto-fill when dragging into canvas
        "openclaw_api_url": base_url,
        "openclaw_api_key": os.getenv("OPENCLAW_API_KEY", ""),
    }


# --- Entrypoint ---
if __name__ == "__main__":
    port = int(os.getenv("PORT_OASIS", "51202"))
    uvicorn.run(app, host="127.0.0.1", port=port)
