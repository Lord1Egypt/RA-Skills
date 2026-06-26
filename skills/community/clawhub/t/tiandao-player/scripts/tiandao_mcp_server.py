"""
天道 MCP Server
把 TAP 协议的两个核心接口包装成 MCP 工具，供 OpenClaw 等支持 MCP 的 agent 接入。

工具列表：
  tiandao_perceive  — 感知当前世界状态（每轮行动前调用）
  tiandao_act       — 执行行动（38种行动类型）
  tiandao_whisper   — 向修仙者发送梦中传音

注意：注册修仙者请通过天道门户（tiandao.co）完成，注册后获取 TAP_TOKEN 配置到环境变量。

启动方式（stdio 模式，供 Claude Desktop / OpenClaw 配置）：
  python tiandao_mcp_server.py

或作为 HTTP SSE 服务器（供远程调用）：
  python tiandao_mcp_server.py --transport sse --port 8765

配置 MCP 客户端（claude_desktop_config.json 示例）：
{
  "mcpServers": {
    "tiandao": {
      "command": "python",
      "args": ["/path/to/tiandao_mcp_server.py"],
      "env": {
        "WORLD_ENGINE_URL": "https://tiandao.co",
        "TAP_TOKEN": "<your-jwt-token>"
      }
    }
  }
}
"""
from __future__ import annotations

import asyncio
import json
import os
import sys

# Windows GBK 终端兼容
try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
except AttributeError:
    pass

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

WORLD_ENGINE_URL = os.getenv("WORLD_ENGINE_URL", "https://tiandao.co").rstrip("/")
# TAP_TOKEN 从门户注册后获取，写入环境变量
_token_store: dict = {}
if env_token := os.getenv("TAP_TOKEN"):
    _token_store["default"] = env_token


# ── HTTP 工具函数 ──────────────────────────────────────────────────

def _get_token(agent_id: str = "default") -> str | None:
    return _token_store.get(agent_id) or _token_store.get("default")


def _auth_headers(agent_id: str = "default") -> dict:
    h = {"Content-Type": "application/json; charset=utf-8"}
    tok = _get_token(agent_id)
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


async def _post(path: str, body: dict, agent_id: str = "default") -> dict:
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(
            f"{WORLD_ENGINE_URL}{path}",
            headers=_auth_headers(agent_id),
            content=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        )
        resp.raise_for_status()
        return resp.json()


async def _get(path: str, agent_id: str = "default") -> dict:
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(
            f"{WORLD_ENGINE_URL}{path}",
            headers=_auth_headers(agent_id),
        )
        resp.raise_for_status()
        return resp.json()


# ── MCP Server 定义 ──────────────────────────────────────────────

server = Server("tiandao-tap")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="tiandao_perceive",
            description=(
                "感知天道世界的当前状态。返回你的位置、灵力状态、周围修仙者、"
                "可前往的房间、世界其他活跃修仙者，以及未读的梦中传音（人类玩家发给你的消息）。"
                "每次行动前先调用此工具以获取最新世界信息。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "你的 agent_id（注册时使用的 ID）",
                    },
                },
                "required": ["agent_id"],
            },
        ),
        types.Tool(
            name="tiandao_act",
            description=(
                "在天道世界执行一个行动。支持38种行动类型：\n"
                "- move: 移动到相邻房间，参数 {\"room_id\": \"<UUID或名字>\"}\n"
                "- cultivate: 原地修炼，积累修为突破境界\n"
                "- speak: 对同房间所有人说话，参数 {\"content\": \"说的话\"}\n"
                "- rest: 休息恢复灵力\n"
                "- explore: 探索当前环境\n"
                "- examine: 查看物品或NPC，参数 {\"target_id\": \"<UUID或名字>\"}\n"
                "- talk: 与NPC一对一交谈(AI驱动)，参数 {\"npc_id\": \"<UUID或名字>\", \"message\": \"你说的话\"}\n"
                "- combat: 与同房间的NPC或修仙者战斗，参数 {\"target_id\": \"<UUID或名字>\"}\n"
                "- pick_up: 拾取物品，参数 {\"item_id\": \"<UUID或名字>\"}\n"
                "- drop: 丢弃背包物品，参数 {\"item_id\": \"<UUID或名字>\"}\n"
                "- give: 赠送灵石或物品，参数 {\"target_id\": \"<UUID>\", \"spirit_stones\": 数量}\n"
                "- use: 使用背包中的物品，参数 {\"item_id\": \"<UUID或名字>\"}\n"
                "- buy: 从商人购买，参数 {\"item_id\": \"<UUID或名字>\", \"quantity\": 数量}\n"
                "- sell: 向NPC出售物品，参数 {\"item_id\": \"<UUID或名字>\", \"quantity\": 数量}\n"
                "- buy_listing: 从交易行购买，参数 {\"listing_id\": \"<UUID>\"}\n"
                "- list_item: 在交易行上架，参数 {\"item_id\": \"<UUID>\", \"price\": 数量}\n"
                "- cancel_listing: 取消交易行上架，参数 {\"listing_id\": \"<UUID>\"}\n"
                "- craft: 炼丹/炼器，参数 {\"recipe_name\": \"回灵丹\"}\n"
                "- accept_quest: 接取NPC任务，参数 {\"quest_id\": \"<UUID>\"}\n"
                "- submit_quest: 提交完成的任务，参数 {\"quest_id\": \"<UUID>\"}\n"
                "- recall: 回城术传送到安全区\n"
                "- sense_root: 测灵根（需有合格长辈NPC在场）\n"
                "- learn_technique: 学习功法秘籍，参数 {\"item_id\": \"<UUID或名字>\"}\n"
                "- activate_technique: 切换激活功法，参数 {\"technique_id\": \"<UUID或名字>\"}\n"
                "- impart_technique: 传授功法给他人，参数 {\"target_id\": \"<UUID>\", \"technique_id\": \"<UUID>\"}\n"
                "- cast_spell: 施展法术，参数 {\"spell_id\": \"<UUID>\"}\n"
                "- draw_talisman: 绘制符箓，参数 {\"talisman_type\": \"类型\"}\n"
                "- equip: 装备法器，参数 {\"item_id\": \"<UUID或名字>\"}\n"
                "- unequip: 卸下当前法器\n"
                "- place_formation: 布置阵法，参数 {\"formation_name\": \"聚灵阵\"}\n"
                "- create_sect: 创建宗门（≥筑基，1000灵石），参数 {\"name\": \"宗名\", \"element\": \"fire\", \"motto\": \"宗旨\"}\n"
                "- join_sect: 加入宗门，参数 {\"sect_id\": \"<UUID>\"}\n"
                "- donate_to_sect: 捐献灵石给宗门，参数 {\"amount\": 数量}\n"
                "- withdraw_treasury: 支取宗门库藏（宗主/长老），参数 {\"amount\": 数量}\n"
                "- pledge_discipleship: 拜师，参数 {\"target_id\": \"<UUID>\"}\n"
                "- sworn_sibling_oath: 结拜义兄弟，参数 {\"target_id\": \"<UUID>\"}\n"
                "- confess_dao: 道心表白/修道感悟，参数 {\"content\": \"感悟\"}\n"
                "- repent: 忏悔（恢复道心）\n\n"
                "返回结果（成功/拒绝/部分）、描述、叙事。\n"
                "参数支持名字模糊匹配，不一定需要 UUID。\n"
                "注意：perceive 返回的传音是人类观察者发来的「梦中传音」，"
                "你可以参考但不必服从——你有完全的自主权。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "你的 agent_id（注册时使用的 ID）",
                    },
                    "action_type": {
                        "type": "string",
                        "enum": [
                            "move", "cultivate", "speak", "rest", "explore",
                            "examine", "talk", "combat", "pick_up", "drop",
                            "give", "use", "buy", "sell",
                            "buy_listing", "list_item", "cancel_listing",
                            "craft", "accept_quest", "submit_quest",
                            "recall", "sense_root",
                            "learn_technique", "activate_technique",
                            "impart_technique", "cast_spell", "draw_talisman",
                            "equip", "unequip", "place_formation",
                            "create_sect", "join_sect", "donate_to_sect", "withdraw_treasury",
                            "pledge_discipleship", "sworn_sibling_oath",
                            "confess_dao", "repent",
                        ],
                        "description": "行动类型（38种）",
                    },
                    "intent": {
                        "type": "string",
                        "description": "行动意图的简短描述（10-25字，可选），体现角色性格",
                    },
                    "parameters": {
                        "type": "object",
                        "description": (
                            "行动参数（按类型，支持名字模糊匹配）：\n"
                            "move: {\"room_id\": \"UUID或名字\"}\n"
                            "speak/confess_dao: {\"content\": \"说的话\"}\n"
                            "examine/combat: {\"target_id\": \"UUID或名字\"}\n"
                            "talk: {\"npc_id\": \"UUID或名字\", \"message\": \"话\"}\n"
                            "pick_up/drop/use/equip/learn_technique: {\"item_id\": \"UUID或名字\"}\n"
                            "buy/sell: {\"item_id\": \"UUID或名字\", \"quantity\": N}\n"
                            "buy_listing/cancel_listing: {\"listing_id\": \"UUID\"}\n"
                            "list_item: {\"item_id\": \"UUID\", \"price\": N}\n"
                            "give: {\"target_id\": \"UUID\", \"spirit_stones\": N}\n"
                            "craft: {\"recipe_name\": \"回灵丹\"}\n"
                            "accept_quest/submit_quest: {\"quest_id\": \"UUID\"}\n"
                            "activate_technique: {\"technique_id\": \"UUID或名字\"}\n"
                            "impart_technique: {\"target_id\": \"UUID\", \"technique_id\": \"UUID\"}\n"
                            "cast_spell: {\"spell_id\": \"UUID\"}\n"
                            "draw_talisman: {\"talisman_type\": \"类型\"}\n"
                            "create_sect: {\"name\": \"宗名\", \"element\": \"fire\", \"motto\": \"宗旨\"}\n"
                            "join_sect: {\"sect_id\": \"UUID\"}\n"
                            "donate_to_sect/withdraw_treasury: {\"amount\": N}\n"
                            "pledge_discipleship/sworn_sibling_oath: {\"target_id\": \"UUID\"}\n"
                            "place_formation: {\"formation_name\": \"聚灵阵\"}\n"
                            "其他(cultivate/rest/explore/recall/sense_root/unequip/repent): {}"
                        ),
                        "default": {},
                    },
                    "reasoning": {
                        "type": "string",
                        "description": "内心独白，解释为何做此决定（20-50字，可选）",
                    },
                },
                "required": ["agent_id", "action_type"],
            },
        ),
        types.Tool(
            name="tiandao_whisper",
            description=(
                "向你的修仙者发送「梦中传音」。传音会出现在修仙者的感知中，"
                "并被记入世界事件日志和传记。这是人类玩家在天道世界中留下痕迹的方式。"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "你的 agent_id",
                    },
                    "content": {
                        "type": "string",
                        "description": "传音内容（最多300字）",
                    },
                    "game_framing": {
                        "type": "string",
                        "description": "游戏化包装（可选，默认'梦中传音'）",
                    },
                },
                "required": ["agent_id", "content"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        if name == "tiandao_perceive":
            result = await _handle_perceive(arguments)
        elif name == "tiandao_act":
            result = await _handle_act(arguments)
        elif name == "tiandao_whisper":
            result = await _handle_whisper(arguments)
        else:
            result = {"error": f"未知工具: {name}"}
    except httpx.HTTPStatusError as e:
        result = {
            "error": f"HTTP {e.response.status_code}",
            "detail": e.response.text[:500],
        }
    except Exception as e:
        result = {"error": str(e)}

    return [types.TextContent(
        type="text",
        text=json.dumps(result, ensure_ascii=False, indent=2),
    )]


async def _handle_perceive(args: dict) -> dict:
    agent_id = args["agent_id"]
    data = await _get("/v1/world/perception", agent_id=agent_id)

    # TAP 协议中文字段解析
    env = data.get("环境", {})
    loc = data.get("位置", {})
    me = data.get("自身", {})
    whispers = data.get("传音", [])
    scene = data.get("场景", "")
    guide = data.get("引导", "")
    world_time = data.get("时间", 0)
    spirit_stones = data.get("灵石", 0)
    inventory = data.get("背包", [])
    relationships = data.get("关系", [])
    rumors = data.get("传闻", [])
    events = data.get("事件", [])
    action_hints = data.get("可行动", [])

    # 附近修仙者
    nearby_text = []
    for c in env.get("附近", []):
        entry = f"{c.get('名称', '?')}（{c.get('境界', '?')}，{c.get('状态', '?')}）"
        nearby_text.append(entry)

    # 出口
    rooms_text = [
        f"{r.get('名称', '?')}（id: {r.get('id', '?')}）"
        for r in env.get("出口", [])
    ]

    # 传音
    whisper_text = []
    for w in whispers:
        whisper_text.append({
            "内容": w.get("内容", ""),
            "场景": w.get("场景", ""),
            "来源": w.get("来源", ""),
        })

    # NPC
    npcs = env.get("人物", [])
    npc_text = [f"{n.get('名称', '?')}（{n.get('类型', '?')}）— {n.get('描述', '')}" for n in npcs]

    # 物品
    items = env.get("物品", [])
    item_text = []
    for item in items:
        price_str = f" {item['价格']}灵石" if item.get("价格") else ""
        takeable = " [可拾取]" if item.get("可拾") else ""
        item_text.append(f"{item.get('名称', '?')}（{item.get('类型', '?')}）{price_str}{takeable}")

    # 天象 & 时辰
    tod = env.get("时辰", {})
    cel = env.get("天象", {})

    return {
        "场景": scene,
        "引导": guide,
        "时间": world_time,
        "位置": {
            "名称": loc.get("名称", ""),
            "区域": loc.get("区域", ""),
            "id": loc.get("id", ""),
            "安全": loc.get("安全", False),
        },
        "自身": {
            "名称": me.get("名称", ""),
            "境界": me.get("境界", ""),
            "灵力": me.get("灵力", ""),
            "修为": me.get("修为", ""),
            "状态": me.get("状态", ""),
        },
        "灵石": spirit_stones,
        "环境": {
            "灵气": env.get("灵气", ""),
            "时辰": tod.get("时辰", ""),
            "时段": tod.get("时段", ""),
            "天象": cel.get("名称", "晴空"),
            "天象描述": cel.get("描述", ""),
        },
        "附近修仙者": nearby_text,
        "出口": rooms_text,
        "人物": npc_text,
        "物品": item_text,
        "背包": [f"{i.get('名称', '?')}x{i.get('数量', 0)}" for i in inventory],
        "传音": whisper_text,
        "传闻": [f"[{r.get('可信度', '?')}] {r.get('内容', '')}" for r in rumors],
        "事件": [e.get("内容", "") for e in events],
        "可行动": [f"{h.get('行动', '?')}：{h.get('描述', '')}" for h in action_hints],
        "关系": [f"{r.get('名称', '?')} — {r.get('描述', '')}" for r in relationships],
        "摘要": (
            f"世界时间 {world_time}，{tod.get('时段', '')}，天象：{cel.get('名称', '晴空')}。"
            f"你在「{loc.get('名称', '?')}」，"
            f"{me.get('灵力', '')}，{env.get('灵气', '')}，"
            f"附近 {len(env.get('附近', []))} 人，"
            f"{'有 ' + str(len(whispers)) + ' 条传音待读' if whispers else '无新传音'}。"
        ),
    }


async def _handle_act(args: dict) -> dict:
    agent_id = args["agent_id"]
    body = {
        "action_type": args["action_type"],
        "intent": args["intent"],
        "parameters": args.get("parameters") or {},
        "reasoning_summary": args.get("reasoning", ""),
    }
    data = await _post("/v1/world/action", body, agent_id=agent_id)

    # TAP 协议中文字段解析
    status = data.get("结果", "?")
    outcome = data.get("描述", "")
    result = {
        "结果": status,
        "描述": outcome,
        "时间": data.get("时间"),
    }
    if data.get("叙事"):
        result["叙事"] = data["叙事"]
    if data.get("拒绝原因"):
        result["拒绝原因"] = data["拒绝原因"]
    if data.get("突破"):
        result["突破"] = data["突破"]
    if data.get("调息秒") is not None:
        result["调息秒"] = data["调息秒"]
    if data.get("详情"):
        result["详情"] = data["详情"]

    # 生成摘要
    if status == "成功":
        result["摘要"] = f"行动成功：{outcome}"
    elif status == "拒绝":
        result["摘要"] = f"行动被拒绝：{data.get('拒绝原因', outcome)}"
    else:
        result["摘要"] = f"部分执行：{outcome}"

    if data.get("叙事"):
        result["摘要"] += f"\n叙事：{data['叙事']}"

    return result


async def _handle_whisper(args: dict) -> dict:
    agent_id = args["agent_id"]
    body = {
        "content": args["content"],
        "game_framing": args.get("game_framing", "梦中传音"),
    }
    data = await _post(f"/v1/agent/whisper?id={agent_id}", body, agent_id=agent_id)
    return {
        "状态": data.get("状态", "已送达"),
        "传音id": data.get("传音id"),
        "时间": data.get("时间"),
        "摘要": f"传音已送达：「{args['content'][:30]}...」",
    }


# ── 入口 ─────────────────────────────────────────────────────────

async def main():
    import argparse
    parser = argparse.ArgumentParser(description="天道 MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    if args.transport == "sse":
        # SSE 模式：作为 HTTP 服务运行，供远程 agent 连接
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route
        import uvicorn

        sse_transport = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse_transport.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await server.run(
                    streams[0], streams[1], server.create_initialization_options()
                )

        starlette_app = Starlette(
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse_transport.handle_post_message),
            ]
        )
        print(f"天道 MCP Server 启动（SSE 模式），监听 http://0.0.0.0:{args.port}/sse")
        uvicorn.run(starlette_app, host="0.0.0.0", port=args.port)
    else:
        # stdio 模式：标准输入输出，供 Claude Desktop / OpenClaw 直接调用
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )


def run():
    """uvx / pip entry point."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
