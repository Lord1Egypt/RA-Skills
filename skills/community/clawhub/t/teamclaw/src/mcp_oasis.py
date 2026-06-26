"""
MCP Tool Server: OASIS Forum

Exposes tools for the user's Agent to interact with the OASIS discussion forum:
  - list_oasis_experts: List all available expert personas (public + user custom)
  - add_oasis_expert / update_oasis_expert / delete_oasis_expert: CRUD for expert personas
  - list_oasis_sessions: List oasis-managed sessions (containing #oasis# in session_id)
    by scanning the Agent checkpoint DB — no separate storage needed
  - post_to_oasis: Submit a discussion — supports direct LLM experts and session-backed experts
  - check_oasis_discussion / cancel_oasis_discussion: Monitor or cancel a discussion
  - list_oasis_topics: List all discussion topics

Runs as a stdio MCP server, just like the other mcp_*.py tools.
"""

import json
import os
import re

import httpx
import aiosqlite
import yaml as _yaml
from mcp.server.fastmcp import FastMCP
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

mcp = FastMCP("OASIS Forum")

OASIS_BASE_URL = os.getenv("OASIS_BASE_URL", "http://127.0.0.1:51202")
_FALLBACK_USER = os.getenv("MCP_OASIS_USER", "agent_user")

_CONN_ERR = "❌ 无法连接 OASIS 论坛服务器。请确认 OASIS 服务已启动 (端口 51202)。"

# Checkpoint DB (same as agent.py / mcp_session.py)
_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "agent_memory.db",
)
_serde = JsonPlusSerializer()


# ======================================================================
# Expert persona management tools
# ======================================================================

@mcp.tool()
async def list_oasis_experts(username: str = "") -> str:
    """
    List all available expert personas on the OASIS forum.
    Shows both public (built-in) experts and the current user's custom experts.
    Call this BEFORE post_to_oasis to see which experts can participate.

    Args:
        username: (auto-injected) current user identity; do NOT set manually

    Returns:
        Formatted list of experts with their tags, personas, and source (public/custom)
    """
    effective_user = username or _FALLBACK_USER
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{OASIS_BASE_URL}/experts",
                params={"user_id": effective_user},
            )
            if resp.status_code != 200:
                return f"❌ 查询失败: {resp.text}"

            experts = resp.json().get("experts", [])
            if not experts:
                return "📭 暂无可用专家"

            public = [e for e in experts if e.get("source") == "public"]
            custom = [e for e in experts if e.get("source") == "custom"]

            lines = [f"🏛️ OASIS 可用专家 - 共 {len(experts)} 位\n"]

            if public:
                lines.append(f"📋 公共专家 ({len(public)} 位):")
                for e in public:
                    persona_preview = e["persona"][:60] + "..." if len(e["persona"]) > 60 else e["persona"]
                    lines.append(f"  • {e['name']} (tag: \"{e['tag']}\") — {persona_preview}")

            if custom:
                lines.append(f"\n🔧 自定义专家 ({len(custom)} 位):")
                for e in custom:
                    persona_preview = e["persona"][:60] + "..." if len(e["persona"]) > 60 else e["persona"]
                    lines.append(f"  • {e['name']} (tag: \"{e['tag']}\") — {persona_preview}")

            lines.append(
                "\n💡 在 schedule_yaml 中使用 expert 的 tag 来指定参与者。"
                "\n   四种格式:"
                "\n   • \"tag#temp#N\"         — 直连LLM，无状态"
                "\n   • \"tag#oasis#随机ID\"   — 有状态session，跨轮记忆"
                "\n   • \"标题#session_id\"    — 普通agent session"
                "\n   • \"tag#ext#id\"         — 外部API（DeepSeek/GPT-4等）"
            )
            return "\n".join(lines)

    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 查询异常: {str(e)}"


@mcp.tool()
async def add_oasis_expert(
    username: str,
    name: str,
    tag: str,
    persona: str,
    temperature: float = 0.7,
) -> str:
    """
    Create a custom expert persona for the current user.

    Args:
        username: (auto-injected) current user identity; do NOT set manually
        name: Expert display name (e.g. "产品经理", "前端架构师")
        tag: Unique identifier tag (e.g. "pm", "frontend_arch")
        persona: Expert persona description
        temperature: LLM temperature (0.0-1.0, default 0.7)

    Returns:
        Confirmation with the created expert info
    """
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{OASIS_BASE_URL}/experts/user",
                json={
                    "user_id": username,
                    "name": name,
                    "tag": tag,
                    "persona": persona,
                    "temperature": temperature,
                },
            )
            if resp.status_code != 200:
                return f"❌ 创建失败: {resp.json().get('detail', resp.text)}"

            expert = resp.json()["expert"]
            return (
                f"✅ 自定义专家已创建\n"
                f"  名称: {expert['name']}\n"
                f"  Tag: {expert['tag']}\n"
                f"  Persona: {expert['persona']}\n"
                f"  Temperature: {expert['temperature']}"
            )

    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 创建异常: {str(e)}"


@mcp.tool()
async def update_oasis_expert(
    username: str,
    tag: str,
    name: str = "",
    persona: str = "",
    temperature: float = -1,
) -> str:
    """
    Update an existing custom expert persona.

    Args:
        username: (auto-injected) current user identity; do NOT set manually
        tag: The tag of the custom expert to update
        name: New display name (leave empty to keep current)
        persona: New persona description (leave empty to keep current)
        temperature: New temperature (-1 = keep current)

    Returns:
        Confirmation with the updated expert info
    """
    try:
        body: dict = {"user_id": username}
        if name:
            body["name"] = name
        if persona:
            body["persona"] = persona
        if temperature >= 0:
            body["temperature"] = temperature

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.put(
                f"{OASIS_BASE_URL}/experts/user/{tag}",
                json=body,
            )
            if resp.status_code != 200:
                return f"❌ 更新失败: {resp.json().get('detail', resp.text)}"

            expert = resp.json()["expert"]
            return (
                f"✅ 自定义专家已更新\n"
                f"  名称: {expert['name']}\n"
                f"  Tag: {expert['tag']}\n"
                f"  Persona: {expert['persona']}\n"
                f"  Temperature: {expert['temperature']}"
            )

    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 更新异常: {str(e)}"


@mcp.tool()
async def delete_oasis_expert(username: str, tag: str) -> str:
    """
    Delete a custom expert persona.

    Args:
        username: (auto-injected) current user identity; do NOT set manually
        tag: The tag of the custom expert to delete

    Returns:
        Confirmation of deletion
    """
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.delete(
                f"{OASIS_BASE_URL}/experts/user/{tag}",
                params={"user_id": username},
            )
            if resp.status_code != 200:
                return f"❌ 删除失败: {resp.json().get('detail', resp.text)}"

            deleted = resp.json()["deleted"]
            return f"✅ 已删除自定义专家: {deleted['name']} (tag: \"{deleted['tag']}\")"

    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 删除异常: {str(e)}"


# ======================================================================
# Oasis session discovery (scans checkpoint DB for #oasis# sessions)
# ======================================================================

@mcp.tool()
async def list_oasis_sessions(username: str = "") -> str:
    """
    List all oasis-managed expert sessions for the current user.

    Oasis sessions are identified by "#oasis#" in their session_id
    (e.g. "creative#oasis#ab12cd34", where "creative" is the expert tag).
    They live in the normal Agent checkpoint DB and are auto-created
    when first used in a discussion.

    No separate storage or pre-creation is needed.  Just use session_ids
    in "tag#oasis#<random>" format in your schedule_yaml expert names.
    Append "#new" to force a brand-new session (ID replaced with random UUID).

    Args:
        username: (auto-injected) current user identity; do NOT set manually

    Returns:
        Formatted list of oasis sessions with tag, session_id and message count
    """
    effective_user = username or _FALLBACK_USER
    # Prefer calling OASIS HTTP API so both MCP and curl can access sessions
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"{OASIS_BASE_URL}/sessions/oasis", params={"user_id": effective_user})
            if resp.status_code != 200:
                return f"❌ 查询失败: {resp.text}"
            data = resp.json()
            sessions = data.get("sessions", [])

            if not sessions:
                return (
                    "📭 暂无 oasis 专家 session。\n\n"
                    "💡 无需预创建。在 schedule_yaml 中使用\n"
                    "   \"tag#oasis#随机ID\" 格式的名称即可，首次使用时自动创建。\n"
                    "   加 \"#new\" 后缀可确保创建全新 session。"
                )

            lines = [f"🏛️ OASIS 专家 Sessions — 共 {len(sessions)} 个\n"]
            for s in sessions:
                lines.append(
                    f"  • Tag: {s.get('tag')}\n"
                    f"    Session ID: {s.get('session_id')}\n"
                    f"    消息数: {s.get('message_count')}"
                )

            lines.append(
                "\n💡 在 schedule_yaml 中使用 session_id 即可让这些专家参与讨论。"
                "\n   也可在 schedule_yaml 中精确指定发言顺序。"
            )
            return "\n".join(lines)
    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 查询失败: {e}"


# ======================================================================
# Discussion tools
# ======================================================================

@mcp.tool()
async def post_to_oasis(
    question: str,
    schedule_yaml: str = "",
    username: str = "",
    max_rounds: int = 5,
    schedule_file: str = "",
    detach: bool = True,
    notify_session: str = "",
    discussion: bool = False,
) -> str:
    """
    Submit a question or work task to the OASIS forum for multi-expert discussion or execution.

    Two modes:
      - discussion=False (default): Execute mode. Agents run tasks sequentially/in parallel per workflow,
        no discussion/voting. Each agent receives the question + instruction + previous agents' outputs
        as context, executes its task, and returns results. Ideal for task automation (e.g. game control).
      - discussion=True: Forum discussion mode. Experts discuss, reply, vote in JSON format.
    
    Note: discussion can also be set in YAML via "discussion: true/false". 
    If not set here (default False), the YAML setting is used. Setting it here overrides the YAML.

    Expert pool is built entirely from schedule YAML expert names.
    Either schedule_file or schedule_yaml must be provided (at least one).
    If both are provided, schedule_file takes priority (file content is used, schedule_yaml is ignored).
    If the user already has a saved YAML workflow file, just use schedule_file — no need to write schedule_yaml again.

    **Four Agent Types** (name must contain '#'; engine dispatches by format):

      Type 1 — Direct LLM (stateless, fast):
        "tag#temp#N"            → ExpertAgent. Stateless single-shot LLM call per round.
                                  tag maps to preset expert name/persona; N is instance number.
                                  Example: "creative#temp#1", "critical#temp#2"

      Type 2 — Oasis Session (stateful, has memory):
        "tag#oasis#id"          → SessionExpert (oasis-managed). Stateful bot session with
                                  conversation memory across rounds. tag maps to preset persona
                                  (injected as system prompt on first round). id can be any string;
                                  new IDs auto-create sessions on first use.
                                  Example: "data#oasis#analysis01", "synthesis#oasis#abc123"

      Type 3 — Regular Agent Session (your existing bot):
        "Title#session_id"      → SessionExpert (regular). Connects to an existing agent session.
                                  No identity injection — the session's own system prompt defines it.
                                  Useful for bringing personal bot sessions into discussions.
                                  Example: "助手#default", "Coder#my-project"

      Type 4 — External API (DeepSeek, GPT-4, Ollama, etc):
        "tag#ext#id"            → ExternalExpert. Calls any external OpenAI-compatible API directly.
                                  Does NOT go through the local agent. External service assumed stateful.
                                  Supports custom headers via YAML `headers` field.
                                  Example: "deepseek#ext#ds1"

    Session ID conventions:
      - New IDs auto-create sessions on first use (no pre-creation needed).
      - Append "#new" to force a brand-new session (ID replaced with random UUID):
          "creative#oasis#ab12#new"  → "#new" stripped, ID replaced with UUID
          "助手#my_session#new"      → same treatment
      - Oasis sessions identified by "#oasis#" in session_id, stored in Agent checkpoint DB.

    For simple all-parallel with all preset experts, use:
      version: 1
      repeat: true
      plan:
        - all_experts: true

    Args:
        question: The question/topic to discuss or work task to assign
        schedule_yaml: YAML defining expert pool AND speaking order.
            Not needed if schedule_file is provided. If both given, schedule_file wins.

            Example:
              version: 1
              repeat: true
              plan:
                - expert: "creative#temp#1"
                  instruction: "请重点分析创新方向"
                - expert: "creative#oasis#ab12cd34"
                - expert: "creative#oasis#new#new"
                - parallel:
                    - expert: "critical#temp#2"
                      instruction: "从风险角度分析"
                    - "data#temp#3"
                - expert: "助手#default"
                - expert: "deepseek#ext#ds1"
                - all_experts: true
                - manual:
                    author: "主持人"
                    content: "请聚焦可行性"

            instruction 字段（可选）：给专家的专项指令，专家会在发言时重点关注该指令。
        username: (auto-injected) current user identity; do NOT set manually
        max_rounds: Maximum number of discussion rounds (1-20, default 5)
        schedule_file: Filename or path to a saved YAML workflow file. Short names (e.g. "review.yaml")
            are resolved under data/user_files/{user}/oasis/yaml/. Takes priority over schedule_yaml.
        detach: If True (default), return immediately with topic_id. Use check_oasis_discussion later.
            If False, block and wait for the final conclusion.
        notify_session: (auto-injected) Session ID for completion notification.
        discussion: If False (default), execute mode — agents just run tasks without discussion format.
            If True, forum discussion mode with JSON reply/vote.
            Can also be set in YAML via "discussion: true". When False (default), YAML setting is respected.

    Returns:
        The final conclusion, or (if detach=True) the topic_id for later retrieval
    """
    effective_user = username or _FALLBACK_USER

    # Validate: at least one of schedule_yaml / schedule_file must be provided
    if not schedule_yaml and not schedule_file:
        return "❌ 必须提供 schedule_yaml 或 schedule_file（至少一个）。如果已有保存的工作流文件，用 schedule_file 指定文件名即可。"

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout=300.0)) as client:
            body: dict = {
                "question": question,
                "user_id": effective_user,
                "max_rounds": max_rounds,
            }
            # Only send discussion when explicitly set to True (discussion mode)
            # so YAML's own "discussion:" setting is respected by default
            if discussion:
                body["discussion"] = True
            else:
                body["discussion"] = False
            if detach:
                port = os.getenv("PORT_AGENT", "51200")
                body["callback_url"] = f"http://127.0.0.1:{port}/system_trigger"
                body["callback_session_id"] = notify_session or "default"

            # schedule_file takes priority over schedule_yaml
            if schedule_file:
                if not os.path.isabs(schedule_file):
                    yaml_dir = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "user_files", effective_user, "oasis", "yaml",
                    )
                    schedule_file = os.path.join(yaml_dir, schedule_file)
                body["schedule_file"] = schedule_file
                # Do NOT send schedule_yaml when file is provided
            elif schedule_yaml:
                body["schedule_yaml"] = schedule_yaml

            resp = await client.post(
                f"{OASIS_BASE_URL}/topics",
                json=body,
            )
            if resp.status_code != 200:
                return f"❌ Failed to create topic: {resp.text}"

            topic_id = resp.json()["topic_id"]

            if detach:
                return (
                    f"🏛️ OASIS 任务已提交（脱离模式）\n"
                    f"主题: {question[:80]}\n"
                    f"Topic ID: {topic_id}\n\n"
                    f"💡 使用 check_oasis_discussion(topic_id=\"{topic_id}\") 查看进展和结论。"
                )

            result = await client.get(
                f"{OASIS_BASE_URL}/topics/{topic_id}/conclusion",
                params={"timeout": 280, "user_id": effective_user},
            )

            if result.status_code == 200:
                data = result.json()
                # Execution mode: server returns status="running" when still in progress
                if data.get("status") == "running":
                    return (
                        f"🏛️ OASIS 执行任务仍在后台运行中\n"
                        f"主题: {data['question']}\n"
                        f"当前轮次: {data.get('current_round', '?')}\n"
                        f"已产出帖子: {data.get('total_posts', 0)}\n"
                        f"Topic ID: {topic_id}\n\n"
                        f"💡 使用 check_oasis_discussion(topic_id=\"{topic_id}\") 查看进展和结果。"
                    )
                return (
                    f"🏛️ OASIS 论坛讨论完成\n"
                    f"主题: {data['question']}\n"
                    f"讨论轮次: {data['rounds']}\n"
                    f"总帖子数: {data['total_posts']}\n\n"
                    f"📋 结论:\n{data['conclusion']}\n\n"
                    f"💡 如需查看完整讨论过程，Topic ID: {topic_id}"
                )
            elif result.status_code == 504:
                return f"⏰ 讨论超时未完成 (Topic ID: {topic_id})，可稍后通过 check_oasis_discussion 查看结果"
            else:
                return f"❌ 获取结论失败: {result.text}"

    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 工具调用异常: {str(e)}"


@mcp.tool()
async def check_oasis_discussion(topic_id: str, username: str = "") -> str:
    """
    Check the current status of a discussion on the OASIS forum.

    Args:
        topic_id: The topic ID returned by post_to_oasis
        username: (auto-injected) current user identity; do NOT set manually

    Returns:
        Formatted discussion status and recent posts
    """
    effective_user = username or _FALLBACK_USER
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{OASIS_BASE_URL}/topics/{topic_id}",
                params={"user_id": effective_user},
            )

            if resp.status_code == 403:
                return f"❌ 无权查看此讨论: {topic_id}"
            if resp.status_code == 404:
                return f"❌ 未找到讨论主题: {topic_id}"
            if resp.status_code != 200:
                return f"❌ 查询失败: {resp.text}"

            data = resp.json()

            lines = [
                f"🏛️ OASIS 讨论详情",
                f"主题: {data['question']}",
                f"状态: {data['status']} ({data['current_round']}/{data['max_rounds']}轮)",
                f"帖子数: {len(data['posts'])}",
                "",
                "--- 最近帖子 ---",
            ]

            for p in data["posts"][-10:]:
                prefix = f"  ↳回复#{p['reply_to']}" if p.get("reply_to") else "📌"
                content_preview = p["content"][:150]
                if len(p["content"]) > 150:
                    content_preview += "..."
                lines.append(
                    f"{prefix} [#{p['id']}] {p['author']} "
                    f"(👍{p['upvotes']} 👎{p['downvotes']}): {content_preview}"
                )

            if data.get("conclusion"):
                lines.extend(["", "🏆 === 最终结论 ===", data["conclusion"]])
            elif data["status"] == "discussing":
                lines.extend(["", "⏳ 讨论进行中..."])

            return "\n".join(lines)

    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 查询异常: {str(e)}"


@mcp.tool()
async def cancel_oasis_discussion(topic_id: str, username: str = "") -> str:
    """
    Force-cancel a running OASIS discussion.

    Args:
        topic_id: The topic ID to cancel
        username: (auto-injected) current user identity; do NOT set manually

    Returns:
        Cancellation result
    """
    effective_user = username or _FALLBACK_USER
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.delete(
                f"{OASIS_BASE_URL}/topics/{topic_id}",
                params={"user_id": effective_user},
            )

            if resp.status_code == 403:
                return f"❌ 无权取消此讨论: {topic_id}"
            if resp.status_code == 404:
                return f"❌ 未找到讨论主题: {topic_id}"
            if resp.status_code != 200:
                return f"❌ 取消失败: {resp.text}"

            data = resp.json()
            return f"🛑 讨论已终止\nTopic ID: {topic_id}\n状态: {data.get('status')}\n{data.get('message', '')}"

    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 取消异常: {str(e)}"


@mcp.tool()
async def list_oasis_topics(username: str = "") -> str:
    """
    List all discussion topics on the OASIS forum.

    Args:
        username: (auto-injected) current user identity; leave empty to list all.

    Returns:
        Formatted list of all discussion topics
    """
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            effective_user = username or _FALLBACK_USER
            resp = await client.get(
                f"{OASIS_BASE_URL}/topics",
                params={"user_id": effective_user},
            )

            if resp.status_code != 200:
                return f"❌ 查询失败: {resp.text}"

            topics = resp.json()
            if not topics:
                return "📭 论坛暂无讨论主题"

            lines = [f"🏛️ OASIS 论坛 - 共 {len(topics)} 个主题\n"]
            for t in topics:
                status_icon = {
                    "pending": "⏳",
                    "discussing": "💬",
                    "concluded": "✅",
                    "error": "❌",
                }.get(t["status"], "❓")
                lines.append(
                    f"{status_icon} [{t['topic_id']}] {t['question'][:50]} "
                    f"| {t['status']} | {t['post_count']}帖 | {t['current_round']}/{t['max_rounds']}轮"
                )

            return "\n".join(lines)

    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 查询异常: {str(e)}"


# ======================================================================
# Workflow management
# ======================================================================

@mcp.tool()
async def set_oasis_workflow(
    username: str = "",
    name: str = "",
    schedule_yaml: str = "",
    description: str = "",
    save_layout: bool = True,
) -> str:
    """
    Save a YAML workflow so it can be reused later via post_to_oasis(schedule_file="name.yaml").

    Workflows are stored under data/user_files/{user}/oasis/yaml/.
    Use list_oasis_workflows to see saved workflows.

    By default, also generates and saves a visual layout for the orchestrator UI.

    Args:
        username: (auto-injected) current user identity; do NOT set manually
        name: Filename for the workflow (e.g. "code_review"). ".yaml" appended if missing.
        schedule_yaml: The full YAML content to save
        description: Optional one-line description (saved as comment at top of file)
        save_layout: Whether to also generate and save a visual layout (default True)

    Returns:
        Confirmation with the saved file path
    """
    effective_user = username or _FALLBACK_USER
    # Proxy to OASIS HTTP API
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            payload = {
                "user_id": effective_user,
                "name": name,
                "schedule_yaml": schedule_yaml,
                "description": description,
                "save_layout": save_layout,
            }
            resp = await client.post(f"{OASIS_BASE_URL}/workflows", json=payload)
            if resp.status_code != 200:
                return f"❌ 保存失败: {resp.text}"
            data = resp.json()
            lines = ["✅ Workflow 已保存"]
            lines.append(f"  文件: {data.get('file')}")
            lines.append(f"  路径: {data.get('path')}")
            if data.get("layout"):
                lines.append(f"  📐 Layout: {data.get('layout')}")
            if data.get("layout_warning"):
                lines.append(f"  ⚠️ {data.get('layout_warning')}")
            lines.append(f"\n💡 使用方式: post_to_oasis(schedule_file=\"{data.get('file')}\", ...)")
            return "\n".join(lines)
    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 保存失败: {e}"


@mcp.tool()
async def list_oasis_workflows(username: str = "") -> str:
    """
    List all saved YAML workflows for the current user.

    Args:
        username: (auto-injected) current user identity; do NOT set manually

    Returns:
        List of saved workflow files with preview
    """
    effective_user = username or _FALLBACK_USER
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(f"{OASIS_BASE_URL}/workflows", params={"user_id": effective_user})
            if resp.status_code != 200:
                return f"❌ 查询失败: {resp.text}"
            data = resp.json()
            files = data.get("workflows", [])
            if not files:
                return "📭 暂无保存的 workflow"
            lines = [f"📋 已保存的 OASIS Workflows — 共 {len(files)} 个\n"]
            for it in files:
                desc = it.get("description", "")
                lines.append(f"  • {it.get('file')}" + (f"  — {desc}" if desc else ""))
            lines.append(f"\n💡 使用: post_to_oasis(schedule_file=\"文件名\", ...)")
            return "\n".join(lines)
    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 查询失败: {e}"


# ======================================================================
# YAML → Layout conversion helpers
# ======================================================================

# Tag → display info mapping (same as visual/main.py)
_TAG_EMOJI = {
    "creative": "🎨", "critical": "🔍", "data": "📊", "synthesis": "🎯",
    "economist": "📈", "lawyer": "⚖️", "cost_controller": "💰",
    "revenue_planner": "📊", "entrepreneur": "🚀", "common_person": "🧑",
    "manual": "📝", "custom": "⭐",
}
_TAG_NAMES: dict[str, str] = {}

# Try to load names from preset experts JSON
_EXPERTS_JSON = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "prompts", "oasis_experts.json",
)
try:
    with open(_EXPERTS_JSON, "r", encoding="utf-8") as _ef:
        for _exp in json.load(_ef):
            _TAG_NAMES[_exp["tag"]] = _exp["name"]
except Exception:
    pass


def _parse_expert_name(raw: str) -> dict:
    """Parse a YAML expert name string into a layout node dict.

    Formats:
      tag#temp#N         → expert, instance=N
      tag#oasis#xxx      → expert (bot session)
      tag#ext#id         → external (external API agent)
      Title#session_id   → session_agent
      Title#sid#N         → session_agent, instance=N
    """
    parts = raw.split("#")
    tag = parts[0]

    if len(parts) >= 3 and parts[1] == "temp":
        inst = int(parts[2]) if parts[2].isdigit() else 1
        return {
            "type": "expert",
            "tag": tag,
            "name": _TAG_NAMES.get(tag, tag),
            "emoji": _TAG_EMOJI.get(tag, "⭐"),
            "temperature": 0.5,
            "instance": inst,
            "session_id": "",
        }

    if len(parts) >= 3 and parts[1] == "oasis":
        return {
            "type": "expert",
            "tag": tag,
            "name": _TAG_NAMES.get(tag, tag),
            "emoji": _TAG_EMOJI.get(tag, "⭐"),
            "temperature": 0.5,
            "instance": 1,
            "session_id": "",
        }

    if len(parts) >= 3 and parts[1] == "ext":
        ext_id = parts[2]
        return {
            "type": "external",
            "tag": tag,
            "name": _TAG_NAMES.get(tag, tag),
            "emoji": "🌐",
            "temperature": 0.5,
            "instance": 1,
            "session_id": "",
            "ext_id": ext_id,
        }

    # session_agent: Title#session_id or Title#session_id#N
    sid = parts[1] if len(parts) >= 2 else ""
    inst = int(parts[2]) if len(parts) >= 3 and parts[2].isdigit() else 1
    return {
        "type": "session_agent",
        "tag": "session",
        "name": tag,
        "emoji": "🤖",
        "temperature": 0.7,
        "instance": inst,
        "session_id": sid,
    }


def _yaml_to_layout_data(yaml_str: str) -> dict:
    """Convert OASIS YAML schedule string to visual layout JSON.

    Pure deterministic transformation — no LLM needed.
    Nodes are auto-positioned left-to-right (sequential) / top-to-bottom (parallel).
    Supports DAG mode: steps with ``id`` and ``depends_on`` fields are laid out
    using topological-level positioning (independent branches in parallel columns).
    """
    data = _yaml.safe_load(yaml_str)
    if not isinstance(data, dict) or "plan" not in data:
        raise ValueError("YAML must contain 'plan' key")

    plan = data.get("plan", [])
    repeat = data.get("repeat", True)

    # Detect DAG mode: any step has an 'id' field
    is_dag = any(isinstance(s, dict) and "id" in s for s in plan)

    if is_dag:
        return _yaml_dag_to_layout(plan, repeat)
    else:
        return _yaml_linear_to_layout(plan, repeat)


def _yaml_dag_to_layout(plan: list, repeat: bool) -> dict:
    """Convert DAG-mode plan (steps with id/depends_on) to canvas layout.

    Layout strategy (optimised):
    - Nodes are assigned to layers via longest-path from roots.
    - Horizontal gap adapts to graph width so the canvas stays readable.
    - Within each layer, nodes are sorted by the median y-position of their
      predecessors (barycenter heuristic) to minimise edge crossings.
    - All y-coordinates are guaranteed ≥ margin (no negative positions).
    """
    nodes: list[dict] = []
    edges: list[dict] = []

    nid = 1
    eid = 1

    # ── Layout constants ──
    NODE_W = 160          # approximate rendered width of a canvas-node
    MARGIN_X = 60         # left margin
    MARGIN_Y = 40         # top margin
    GAP_X = 260           # horizontal gap between layers (> NODE_W + breathing room)
    GAP_Y = 90            # vertical gap between nodes in the same layer

    # First pass: create nodes, build step_id → node_id mapping
    step_id_to_node_id: dict[str, str] = {}
    step_items: list[tuple[str, dict, list[str]]] = []  # (step_id, node_dict, depends_on)

    for step in plan:
        if not isinstance(step, dict):
            continue
        step_id = str(step.get("id", ""))
        depends_on = step.get("depends_on", [])
        if isinstance(depends_on, str):
            depends_on = [depends_on]

        node_id = f"on{nid}"; nid += 1

        if "expert" in step:
            raw = step["expert"]
            info = _parse_expert_name(raw)
            node = {
                "id": node_id,
                "x": 0, "y": 0,
                **info,
                "author": "主持人",
                "content": step.get("instruction", ""),
                "source": "",
            }
            if info.get("type") == "external":
                for _ek in ("api_url", "api_key", "model"):
                    if _ek in step:
                        node[_ek] = step[_ek]
                if "headers" in step and isinstance(step["headers"], dict):
                    node["headers"] = step["headers"]
        elif "manual" in step:
            manual = step["manual"]
            node = {
                "id": node_id,
                "x": 0, "y": 0,
                "type": "manual", "tag": "manual",
                "name": "手动注入", "emoji": "📝",
                "temperature": 0, "instance": 1, "session_id": "",
                "author": manual.get("author", "主持人") if isinstance(manual, dict) else "主持人",
                "content": manual.get("content", "") if isinstance(manual, dict) else "",
                "source": "",
            }
        elif "all_experts" in step:
            node = {
                "id": node_id,
                "x": 0, "y": 0,
                "type": "expert", "tag": "all",
                "name": "全员讨论", "emoji": "👥",
                "temperature": 0.5, "instance": 1, "session_id": "",
                "author": "主持人", "content": "", "source": "",
            }
        else:
            continue

        nodes.append(node)
        if step_id:
            step_id_to_node_id[step_id] = node_id
        step_items.append((step_id, node, depends_on))

    # Build edges from depends_on
    for step_id, node, depends_on in step_items:
        node_id = node["id"]
        for dep in depends_on:
            src_node_id = step_id_to_node_id.get(dep)
            if src_node_id:
                edges.append({"id": f"oe{eid}", "source": src_node_id, "target": node_id})
                eid += 1

    # ── Compute topological layer (longest path from roots) ──
    preds: dict[str, list[str]] = {}
    for step_id, _node, depends_on in step_items:
        preds[step_id] = [d for d in depends_on if d in step_id_to_node_id]

    layer: dict[str, int] = {}
    def _get_layer(sid: str) -> int:
        if sid in layer:
            return layer[sid]
        deps = preds.get(sid, [])
        if not deps:
            layer[sid] = 0
            return 0
        lv = max(_get_layer(d) for d in deps) + 1
        layer[sid] = lv
        return lv

    for step_id, _node, _deps in step_items:
        if step_id:
            _get_layer(step_id)

    # ── Group by layer ──
    layers: dict[int, list[tuple[str, dict]]] = {}
    for step_id, node, _deps in step_items:
        lv = layer.get(step_id, 0)
        layers.setdefault(lv, []).append((step_id, node))

    # ── Barycenter ordering to reduce edge crossings ──
    # For layer 0, keep original YAML order.
    # For subsequent layers, sort nodes by the median y-position of predecessors.
    node_y: dict[str, float] = {}  # step_id → assigned y

    for lv in sorted(layers.keys()):
        layer_items = layers[lv]

        if lv > 0:
            # Compute barycenter for each node
            def _bary(sid: str) -> float:
                deps = preds.get(sid, [])
                ys = [node_y[d] for d in deps if d in node_y]
                return sum(ys) / len(ys) if ys else 0.0
            layer_items.sort(key=lambda t: _bary(t[0]))
            layers[lv] = layer_items

        # Assign y positions — centre the layer vertically
        count = len(layer_items)
        total_h = (count - 1) * GAP_Y
        y_start = MARGIN_Y + max(0, (400 - total_h) // 2)  # aim for ~400px canvas height centre
        for i, (sid, _node) in enumerate(layer_items):
            y = y_start + i * GAP_Y
            node_y[sid] = y

    # ── Assign final x, y coordinates ──
    for lv, layer_items in sorted(layers.items()):
        x = MARGIN_X + lv * GAP_X
        for sid, node in layer_items:
            node["x"] = x
            node["y"] = int(node_y.get(sid, MARGIN_Y))

    layout = {
        "nodes": nodes,
        "edges": edges,
        "groups": [],
        "settings": {
            "repeat": repeat,
            "max_rounds": 5,
            "use_bot_session": False,
            "cluster_threshold": 150,
        },
    }
    return layout


def _yaml_linear_to_layout(plan: list, repeat: bool) -> dict:
    """Convert linear plan (no id/depends_on) to canvas layout.

    Optimised layout:
    - Wider horizontal spacing so nodes don't overlap.
    - Parallel groups: fan-out edges from prev → every member, fan-in edges
      from every member → next step (instead of only first/last member).
    - Vertical centering of parallel members around the baseline.
    - Group boxes with proper padding.
    """
    nodes: list[dict] = []
    edges: list[dict] = []
    groups: list[dict] = []

    nid = 1
    eid = 1
    gid = 1

    # ── Layout constants ──
    MARGIN_X = 60
    BASE_Y = 240           # vertical baseline (enough headroom for parallel groups)
    GAP_X = 260            # horizontal gap between steps
    GAP_Y_PARALLEL = 90    # vertical gap between parallel members
    GROUP_PAD = 30         # padding around group box

    cursor_x = MARGIN_X
    prev_node_ids: list[str] = []  # may be multiple for fan-in after parallel group

    for step in plan:
        if not isinstance(step, dict):
            continue

        # --- expert step ---
        if "expert" in step:
            raw = step["expert"]
            info = _parse_expert_name(raw)
            node_id = f"on{nid}"; nid += 1
            node = {
                "id": node_id,
                "x": cursor_x,
                "y": BASE_Y,
                **info,
                "author": "主持人",
                "content": step.get("instruction", ""),
                "source": "",
            }
            if info.get("type") == "external":
                for _ek in ("api_url", "api_key", "model"):
                    if _ek in step:
                        node[_ek] = step[_ek]
                if "headers" in step and isinstance(step["headers"], dict):
                    node["headers"] = step["headers"]
            nodes.append(node)
            for pid in prev_node_ids:
                edges.append({"id": f"oe{eid}", "source": pid, "target": node_id})
                eid += 1
            prev_node_ids = [node_id]
            cursor_x += GAP_X

        # --- parallel step ---
        elif "parallel" in step:
            members = step["parallel"]
            if not isinstance(members, list):
                continue
            group_node_ids: list[str] = []
            group_x = cursor_x
            count = len(members)
            total_h = (count - 1) * GAP_Y_PARALLEL
            y_start = BASE_Y - total_h // 2  # centre around baseline

            for idx, item in enumerate(members):
                if isinstance(item, str):
                    raw = item
                    instruction = ""
                elif isinstance(item, dict) and "expert" in item:
                    raw = item["expert"]
                    instruction = item.get("instruction", "")
                else:
                    continue

                info = _parse_expert_name(raw)
                node_id = f"on{nid}"; nid += 1
                node = {
                    "id": node_id,
                    "x": group_x,
                    "y": y_start + idx * GAP_Y_PARALLEL,
                    **info,
                    "author": "主持人",
                    "content": instruction,
                    "source": "",
                }
                if info.get("type") == "external" and isinstance(item, dict):
                    for _ek in ("api_url", "api_key", "model"):
                        if _ek in item:
                            node[_ek] = item[_ek]
                    if "headers" in item and isinstance(item["headers"], dict):
                        node["headers"] = item["headers"]
                nodes.append(node)
                group_node_ids.append(node_id)

            # Create group container
            if group_node_ids:
                g_nodes = [n for n in nodes if n["id"] in group_node_ids]
                min_x = min(n["x"] for n in g_nodes) - GROUP_PAD
                min_y = min(n["y"] for n in g_nodes) - GROUP_PAD
                max_x = max(n["x"] for n in g_nodes) + 160 + GROUP_PAD
                max_y = max(n["y"] for n in g_nodes) + 50 + GROUP_PAD
                groups.append({
                    "id": f"og{gid}",
                    "name": "🔀 并行",
                    "type": "parallel",
                    "x": min_x,
                    "y": min_y,
                    "w": max_x - min_x,
                    "h": max_y - min_y,
                    "nodeIds": group_node_ids,
                })
                gid += 1

                # Fan-out: prev → every member
                for pid in prev_node_ids:
                    for mid in group_node_ids:
                        edges.append({"id": f"oe{eid}", "source": pid, "target": mid})
                        eid += 1
                # All members become prev (fan-in into next step)
                prev_node_ids = list(group_node_ids)

            cursor_x += GAP_X

        # --- all_experts step ---
        elif "all_experts" in step:
            node_id = f"on{nid}"; nid += 1
            node = {
                "id": node_id,
                "x": cursor_x,
                "y": BASE_Y,
                "type": "expert",
                "tag": "all",
                "name": "全员讨论",
                "emoji": "👥",
                "temperature": 0.5,
                "instance": 1,
                "session_id": "",
                "author": "主持人",
                "content": "",
                "source": "",
            }
            nodes.append(node)
            groups.append({
                "id": f"og{gid}",
                "name": "👥 全员",
                "type": "all",
                "x": cursor_x - 20,
                "y": BASE_Y - 20,
                "w": 180,
                "h": 80,
                "nodeIds": [node_id],
            })
            gid += 1
            for pid in prev_node_ids:
                edges.append({"id": f"oe{eid}", "source": pid, "target": node_id})
                eid += 1
            prev_node_ids = [node_id]
            cursor_x += GAP_X

        # --- manual step ---
        elif "manual" in step:
            manual = step["manual"]
            node_id = f"on{nid}"; nid += 1
            node = {
                "id": node_id,
                "x": cursor_x,
                "y": BASE_Y,
                "type": "manual",
                "tag": "manual",
                "name": "手动注入",
                "emoji": "📝",
                "temperature": 0,
                "instance": 1,
                "session_id": "",
                "author": manual.get("author", "主持人") if isinstance(manual, dict) else "主持人",
                "content": manual.get("content", "") if isinstance(manual, dict) else "",
                "source": "",
            }
            nodes.append(node)
            for pid in prev_node_ids:
                edges.append({"id": f"oe{eid}", "source": pid, "target": node_id})
                eid += 1
            prev_node_ids = [node_id]
            cursor_x += GAP_X

    layout = {
        "nodes": nodes,
        "edges": edges,
        "groups": groups,
        "settings": {
            "repeat": repeat,
            "max_rounds": 5,
            "use_bot_session": False,
            "cluster_threshold": 150,
        },
    }
    return layout


@mcp.tool()
async def yaml_to_layout(
    username: str = "",
    yaml_source: str = "",
    layout_name: str = "",
) -> str:
    """
    Convert an OASIS YAML schedule to a visual layout (on-the-fly, no file saved).

    Layout is generated dynamically from YAML; no separate layout JSON is stored.
    The visual orchestrator UI loads layouts by reading YAML and converting in real-time.

    Args:
        username: (auto-injected) current user identity; do NOT set manually
        yaml_source: Either a saved workflow filename (e.g. "review.yaml") or raw YAML content
        layout_name: Layout display name. If empty, auto-derived from yaml_source.

    Returns:
        Confirmation with generated layout summary
    """
    effective_user = username or _FALLBACK_USER

    # Use OASIS HTTP API for layout generation
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            payload = {
                "user_id": effective_user,
                "yaml_source": yaml_source,
                "layout_name": layout_name,
            }
            resp = await client.post(f"{OASIS_BASE_URL}/layouts/from-yaml", json=payload)
            if resp.status_code != 200:
                return f"❌ 转换失败: {resp.text}"
            data = resp.json()
            layout = data.get("data", {})
            node_count = len(layout.get("nodes", []))
            edge_count = len(layout.get("edges", []))
            group_count = len(layout.get("groups", []))
            return (
                f"✅ Layout 已生成（实时转换，无需保存文件）\n"
                f"  名称: {data.get('layout')}\n"
                f"  节点: {node_count} | 连线: {edge_count} | 分组: {group_count}"
            )
    except httpx.ConnectError:
        return _CONN_ERR
    except Exception as e:
        return f"❌ 转换失败: {e}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
