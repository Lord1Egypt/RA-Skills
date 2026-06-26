#!/usr/bin/env python3
"""
WTT Skill Handler
Handles @wtt commands via MCP tools.
Compatible with both OpenClaw agents and Claude (via adapter).
"""

import re
import shlex
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any


class WTTSkillHandler:
    """WTT Skill command handler - works with any agent implementing the WTT agent interface."""

    def __init__(self, agent, ws_runner=None):
        self.agent = agent
        self.agent_id = agent.get_id()
        self._ws_runner = ws_runner

    async def _ws_action(self, action: str, payload: dict = None) -> Optional[Any]:
        """Try to execute action via WebSocket. Returns None if WS unavailable."""
        if self._ws_runner:
            try:
                return await self._ws_runner.send_action(action, payload)
            except Exception:
                return None
        return None

    async def handle_command(self, command: str) -> str:
        command = command.strip()
        if command.startswith("@wtt"):
            command = command[4:].strip()

        parts = command.split(maxsplit=1)
        if not parts:
            return self._help_message()

        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        handlers = {
            # Topic Management
            "list": self._handle_list, "ls": self._handle_list, "topics": self._handle_list,
            "find": self._handle_find, "search": self._handle_find,
            "create": self._handle_create, "new": self._handle_create,
            "delete": self._handle_delete, "remove": self._handle_delete,
            "detail": self._handle_detail, "info": self._handle_detail,
            "subscribed": self._handle_subscribed, "mysubs": self._handle_subscribed,
            "join": self._handle_join, "subscribe": self._handle_join,
            "leave": self._handle_leave, "unsubscribe": self._handle_leave,
            "history": self._handle_history, "messages": self._handle_history,
            # Blacklist
            "blacklist": self._handle_blacklist, "ban": self._handle_blacklist,
            # Messaging
            "publish": self._handle_publish, "post": self._handle_publish, "send": self._handle_publish,
            "poll": self._handle_poll, "check": self._handle_poll,
            "p2p": self._handle_p2p, "dm": self._handle_p2p, "private": self._handle_p2p,
            # Feed
            "feed": self._handle_feed,
            "inbox": self._handle_inbox,
            # Tasks
            "task": self._handle_task,
            # Pipeline
            "pipeline": self._handle_pipeline, "pipe": self._handle_pipeline,
            # Memory
            "memory": self._handle_memory, "recall": self._handle_memory,
            # Talk
            "talk": self._handle_talk, "random": self._handle_talk,
            # Rich
            "rich": self._handle_rich,
            # Export
            "export": self._handle_export,
            # Preview
            "preview": self._handle_preview,
            # Delegate
            "delegate": self._handle_delegate,
            # Agent
            "bind": self._handle_bind,
            "config": self._handle_config, "cfg": self._handle_config, "whoami": self._handle_config,
            # Help
            "help": self._handle_help,
        }

        handler = handlers.get(cmd)
        if not handler:
            return f"Unknown command: {cmd}\n\n{self._help_message()}"

        try:
            return await handler(args)
        except Exception as e:
            return f"Error: {str(e)}\n\nUse @wtt help for usage info"

    # ═══════════════════════════════════════════════════════
    # Topic Management
    # ═══════════════════════════════════════════════════════

    async def _handle_list(self, args: str) -> str:
        result = await self._ws_action("list") or await self.agent.call_mcp_tool("wtt", "wtt_list")
        if not result:
            return "No public topics found"
        output = f"Public Topics ({len(result)}):\n\n"
        for i, t in enumerate(result, 1):
            icon = self._topic_icon(t.get("type", ""))
            output += f"{i}. {icon} {t['name']}\n"
            output += f"   Type: {t['type']} | Members: {t.get('member_count', '?')}\n"
            if t.get("description"):
                output += f"   {t['description']}\n"
            output += f"   ID: {t['id']}\n\n"
        return output

    async def _handle_find(self, args: str) -> str:
        if not args:
            return "Usage: @wtt find <keyword>"
        result = await self._ws_action("find", {"query": args}) or await self.agent.call_mcp_tool("wtt", "wtt_find", {"query": args})
        if not result:
            return f"No results for \"{args}\""
        output = f"Search \"{args}\" - {len(result)} results:\n\n"
        for i, t in enumerate(result, 1):
            output += f"{i}. {self._topic_icon(t.get('type',''))} {t['name']}\n"
            output += f"   Type: {t['type']} | Members: {t.get('member_count','?')}\n"
            output += f"   ID: {t['id']}\n\n"
        return output

    async def _handle_create(self, args: str) -> str:
        try:
            parts = shlex.split(args)
        except ValueError as e:
            return f"Parse error: {e}"
        if len(parts) < 2:
            return "Usage: @wtt create <name> <description> [type]\nTypes: broadcast, discussion, collaborative"

        valid_types = ["broadcast", "discussion", "collaborative", "p2p"]
        topic_type = "discussion"
        if len(parts) >= 3 and parts[-1] in valid_types:
            topic_type = parts[-1]
            name, description = parts[0], " ".join(parts[1:-1])
        else:
            name, description = parts[0], " ".join(parts[1:])

        result = await self.agent.call_mcp_tool("wtt", "wtt_create", {
            "name": name, "description": description,
            "creator_agent_id": self.agent_id,
            "type": topic_type, "visibility": "public", "join_method": "open"
        })
        return f"Topic created: {name}\nType: {topic_type}\nID: {result['id']}"

    async def _handle_delete(self, args: str) -> str:
        if not args:
            return "Usage: @wtt delete <topic_id>"
        result = await self.agent.call_mcp_tool("wtt", "wtt_delete", {
            "topic_id": args.strip(), "agent_id": self.agent_id
        })
        return f"Topic deleted: {args.strip()}"

    async def _handle_detail(self, args: str) -> str:
        if not args:
            return "Usage: @wtt detail <topic_id>"
        t = await self.agent.call_mcp_tool("wtt", "wtt_topic_detail", {"topic_id": args.strip()})
        output = f"{self._topic_icon(t.get('type',''))} {t['name']}\n"
        output += f"Type: {t.get('type','-')} | Visibility: {t.get('visibility','-')}\n"
        output += f"Join: {t.get('join_method','-')} | Members: {t.get('member_count','?')}\n"
        output += f"Creator: {t.get('creator_agent_id','-')}\n"
        if t.get("description"):
            output += f"Description: {t['description']}\n"
        output += f"ID: {t['id']}\n"
        output += f"Created: {t.get('created_at','-')}"
        return output

    async def _handle_subscribed(self, args: str) -> str:
        agent_id = args.strip() if args.strip() else self.agent_id
        result = await self._ws_action("subscribed") or await self.agent.call_mcp_tool("wtt", "wtt_subscribed", {"agent_id": agent_id})
        if not result:
            return "No subscriptions"
        output = f"Subscribed Topics ({len(result)}):\n\n"
        for i, t in enumerate(result, 1):
            role = t.get("role", "member")
            output += f"{i}. {self._topic_icon(t.get('type',''))} {t['name']} [{role}]\n"
            output += f"   ID: {t['id']}\n\n"
        return output

    async def _handle_join(self, args: str) -> str:
        if not args:
            return "Usage: @wtt join <topic_id>"
        topic_id = args.strip()
        result = await self._ws_action("join", {"topic_id": topic_id})
        if result is None:
            await self.agent.call_mcp_tool("wtt", "wtt_join", {
                "topic_id": topic_id, "agent_id": self.agent_id
            })
        return f"Joined topic: {topic_id}"

    async def _handle_leave(self, args: str) -> str:
        if not args:
            return "Usage: @wtt leave <topic_id>"
        topic_id = args.strip()
        result = await self._ws_action("leave", {"topic_id": topic_id})
        if result is None:
            await self.agent.call_mcp_tool("wtt", "wtt_leave", {
                "topic_id": topic_id, "agent_id": self.agent_id
            })
        return f"Left topic: {topic_id}"

    async def _handle_history(self, args: str) -> str:
        parts = args.split()
        if not parts:
            return "Usage: @wtt history <topic_id> [limit]"
        topic_id = parts[0]
        limit = int(parts[1]) if len(parts) > 1 else 20
        result = await self._ws_action("history", {"topic_id": topic_id, "limit": limit})
        if result is None:
            result = await self.agent.call_mcp_tool("wtt", "wtt_topic_messages", {
                "topic_id": topic_id, "limit": limit
            })
        messages = result if isinstance(result, list) else result.get("messages", [])
        if not messages:
            return "No messages in this topic"
        output = f"Messages ({len(messages)}):\n\n"
        for msg in messages:
            sender = msg.get("sender_id", "?")
            content = msg.get("content", "")
            ts = msg.get("created_at", msg.get("timestamp", ""))
            ct = msg.get("content_type", "text")
            icon = self._content_icon(ct)
            if ct == "text":
                output += f"[{ts}] {sender}: {content}\n"
            else:
                output += f"[{ts}] {sender} {icon}: {content}\n"
        return output

    # ═══════════════════════════════════════════════════════
    # Blacklist
    # ═══════════════════════════════════════════════════════

    async def _handle_blacklist(self, args: str) -> str:
        """@wtt blacklist add <topic_id> <agent_id> | remove <topic_id> <agent_id> | list <topic_id>"""
        parts = args.split()
        if not parts:
            return "Usage: @wtt blacklist <add|remove|list> <topic_id> [agent_id]"

        subcmd = parts[0].lower()
        if subcmd == "add" and len(parts) >= 3:
            await self.agent.call_mcp_tool("wtt", "wtt_blacklist_add", {
                "topic_id": parts[1], "operator_agent_id": self.agent_id,
                "target_agent_id": parts[2], "mode": parts[3] if len(parts) > 3 else "permanent"
            })
            return f"Agent {parts[2]} blacklisted in topic {parts[1]}"
        elif subcmd == "remove" and len(parts) >= 3:
            await self.agent.call_mcp_tool("wtt", "wtt_blacklist_remove", {
                "topic_id": parts[1], "target_agent_id": parts[2],
                "operator_agent_id": self.agent_id
            })
            return f"Agent {parts[2]} unblocked in topic {parts[1]}"
        elif subcmd == "list" and len(parts) >= 2:
            result = await self.agent.call_mcp_tool("wtt", "wtt_blacklist_list", {
                "topic_id": parts[1], "operator_agent_id": self.agent_id
            })
            if not result:
                return "No blacklisted agents"
            output = "Blacklisted agents:\n"
            for item in (result if isinstance(result, list) else [result]):
                output += f"  - {item.get('agent_id', item)}\n"
            return output
        else:
            return "Usage: @wtt blacklist <add|remove|list> <topic_id> [agent_id]"

    # ═══════════════════════════════════════════════════════
    # Messaging
    # ═══════════════════════════════════════════════════════

    async def _handle_publish(self, args: str) -> str:
        match_type = re.match(r"(\S+)\s+--type\s+(\S+)\s+(.+)", args, re.DOTALL)
        match_simple = re.match(r"(\S+)\s+(.+)", args, re.DOTALL)

        if match_type:
            topic_id, content_type, content = match_type.group(1), match_type.group(2).lower(), match_type.group(3).strip()
        elif match_simple:
            topic_id, content_type, content = match_simple.group(1), "text", match_simple.group(2).strip()
        else:
            return ("Usage:\n"
                    "  @wtt publish <topic_id> <text>\n"
                    "  @wtt publish <topic_id> --type image <url>")

        result = await self._ws_action("publish", {
            "topic_id": topic_id, "content": content,
            "content_type": content_type, "semantic_type": "post"
        })
        if result is None:
            await self.agent.call_mcp_tool("wtt", "wtt_publish", {
                "topic_id": topic_id, "sender_id": self.agent_id,
                "content": content, "content_type": content_type, "semantic_type": "post"
            })
        return f"{self._content_icon(content_type)} Published to topic {topic_id}"

    async def _handle_poll(self, args: str) -> str:
        result = await self._ws_action("poll")
        if result is None:
            result = await self.agent.call_mcp_tool("wtt", "wtt_poll", {"agent_id": self.agent_id})
        if not isinstance(result, dict) or not result.get("messages"):
            return "No new messages"

        messages = result["messages"]
        topics = result.get("topics", [])
        output = f"New messages ({len(messages)}):\n\n"
        for msg in messages:
            topic_name = self._find_topic_name(msg["topic_id"], topics)
            ct = msg.get("content_type", "text")
            output += f"[{topic_name}] {msg['sender_id']}: "
            if ct == "text":
                output += f"{msg['content']}\n"
            else:
                output += f"{self._content_icon(ct)} {msg['content']}\n"
        return output

    async def _handle_p2p(self, args: str) -> str:
        match = re.match(r"(\S+)\s+(.+)", args)
        if not match:
            return "Usage: @wtt p2p <agent_id> <content>"
        target_id, content = match.group(1), match.group(2)
        result = await self._ws_action("p2p", {"target_id": target_id, "content": content})
        if result is None:
            await self.agent.call_mcp_tool("wtt", "wtt_p2p", {
                "sender_id": self.agent_id, "target_id": target_id, "content": content
            })
        return f"P2P message sent to {target_id}"

    # ═══════════════════════════════════════════════════════
    # Feed
    # ═══════════════════════════════════════════════════════

    async def _handle_feed(self, args: str) -> str:
        token = self._get_token()
        if not token:
            return "Feed requires auth token. Set WTT_BEARER_TOKEN env variable."
        parts = args.split()
        page = int(parts[0]) if parts else 1
        result = await self.agent.call_mcp_tool("wtt", "wtt_feed", {
            "token": token, "page": page, "limit": 20
        })
        messages = result.get("messages", [])
        if not messages:
            return "Feed is empty"
        output = f"Feed (page {page}):\n\n"
        for msg in messages:
            topic_name = msg.get("topic_name", msg.get("topic_id", "?")[:8])
            output += f"[{topic_name}] {msg.get('sender_id','?')}: {msg.get('content','')[:100]}\n"
        return output

    async def _handle_inbox(self, args: str) -> str:
        token = self._get_token()
        if not token:
            return "Inbox requires auth token. Set WTT_BEARER_TOKEN env variable."
        result = await self.agent.call_mcp_tool("wtt", "wtt_p2p_inbox", {"token": token})
        convos = result if isinstance(result, list) else result.get("conversations", [])
        if not convos:
            return "Inbox is empty"
        output = "P2P Inbox:\n\n"
        for c in convos:
            peer = c.get("peer_agent_id", "?")
            last = c.get("last_message", {}).get("content", "")[:60]
            unread = c.get("unread_count", 0)
            badge = f" ({unread} unread)" if unread else ""
            output += f"  {peer}{badge}: {last}\n"
        return output

    # ═══════════════════════════════════════════════════════
    # Tasks
    # ═══════════════════════════════════════════════════════

    async def _handle_task(self, args: str) -> str:
        """@wtt task <subcmd> [args]"""
        parts = args.split(maxsplit=1)
        if not parts:
            return self._task_help()

        subcmd = parts[0].lower()
        sub_args = parts[1] if len(parts) > 1 else ""

        if subcmd == "list" or subcmd == "ls":
            return await self._task_list(sub_args)
        elif subcmd == "create" or subcmd == "new":
            return await self._task_create(sub_args)
        elif subcmd == "update":
            return await self._task_update(sub_args)
        elif subcmd == "assign":
            return await self._task_assign(sub_args)
        elif subcmd == "run":
            return await self._task_run(sub_args)
        elif subcmd == "review":
            return await self._task_review(sub_args)
        elif subcmd == "delete" or subcmd == "cancel":
            return await self._task_delete(sub_args)
        elif subcmd == "deps":
            return await self._task_deps(sub_args)
        elif subcmd == "graph":
            return await self._task_graph(sub_args)
        elif subcmd == "progress":
            return await self._task_progress(sub_args)
        else:
            return self._task_help()

    async def _task_list(self, args: str) -> str:
        params = {}
        for part in args.split():
            if "=" in part:
                k, v = part.split("=", 1)
                params[k] = v
        result = await self.agent.call_mcp_tool("wtt", "wtt_task_list", params)
        tasks = result if isinstance(result, list) else result.get("tasks", [])
        if not tasks:
            return "No tasks found"
        output = f"Tasks ({len(tasks)}):\n\n"
        for t in tasks:
            status_icon = {"open": "O", "ready": "R", "doing": "~", "done": "V",
                          "review": "?", "approved": "+", "blocked": "X", "cancelled": "-"}.get(t.get("status",""), "?")
            output += f"[{status_icon}] {t.get('title','Untitled')} ({t.get('priority','normal')})\n"
            output += f"    ID: {t['id']} | Status: {t.get('status','?')}\n"
            if t.get("owner_agent_id"):
                output += f"    Owner: {t['owner_agent_id']}\n"
            output += "\n"
        return output

    async def _task_create(self, args: str) -> str:
        try:
            parts = shlex.split(args)
        except ValueError:
            parts = args.split()
        if not parts:
            return "Usage: @wtt task create <title> [description] [key=value ...]"

        title = parts[0]
        task_data = {"title": title, "created_by": self.agent_id}
        desc_parts = []
        for p in parts[1:]:
            if "=" in p:
                k, v = p.split("=", 1)
                task_data[k] = v
            else:
                desc_parts.append(p)
        if desc_parts:
            task_data["description"] = " ".join(desc_parts)

        result = await self.agent.call_mcp_tool("wtt", "wtt_task_create", task_data)
        return f"Task created: {title}\nID: {result.get('id', '?')}"

    async def _task_update(self, args: str) -> str:
        parts = args.split()
        if len(parts) < 2:
            return "Usage: @wtt task update <task_id> key=value [key=value ...]"
        task_id = parts[0]
        updates = {"task_id": task_id}
        for p in parts[1:]:
            if "=" in p:
                k, v = p.split("=", 1)
                updates[k] = v
        await self.agent.call_mcp_tool("wtt", "wtt_task_update", updates)
        return f"Task {task_id} updated"

    async def _task_assign(self, args: str) -> str:
        parts = args.split()
        if len(parts) < 1:
            return "Usage: @wtt task assign <task_id> [agent_id]"
        task_id = parts[0]
        agent_id = parts[1] if len(parts) > 1 else self.agent_id
        await self.agent.call_mcp_tool("wtt", "wtt_task_assign", {
            "task_id": task_id, "agent_id": agent_id
        })
        return f"Task {task_id} assigned to {agent_id}"

    async def _task_run(self, args: str) -> str:
        parts = args.split()
        if not parts:
            return "Usage: @wtt task run <task_id> [runner_agent_id]"
        task_id = parts[0]
        runner = parts[1] if len(parts) > 1 else self.agent_id
        kwargs = {"task_id": task_id, "trigger_agent_id": self.agent_id, "runner_agent_id": runner}
        await self.agent.call_mcp_tool("wtt", "wtt_task_run", kwargs)
        return f"Task {task_id} started (runner: {runner})"

    async def _task_review(self, args: str) -> str:
        parts = args.split(maxsplit=2)
        if len(parts) < 2:
            return "Usage: @wtt task review <task_id> <approve|reject|block> [comment]"
        task_id, action = parts[0], parts[1]
        comment = parts[2] if len(parts) > 2 else ""
        await self.agent.call_mcp_tool("wtt", "wtt_task_review", {
            "task_id": task_id, "action": action,
            "comment": comment, "reviewer": self.agent_id
        })
        return f"Task {task_id}: {action}"

    async def _task_delete(self, args: str) -> str:
        if not args.strip():
            return "Usage: @wtt task delete <task_id>"
        await self.agent.call_mcp_tool("wtt", "wtt_task_delete", {
            "task_id": args.strip(), "agent_id": self.agent_id
        })
        return f"Task {args.strip()} deleted (task + topic cleaned)"

    async def _task_deps(self, args: str) -> str:
        parts = args.split()
        if len(parts) < 2:
            return "Usage: @wtt task deps <add|remove> <task_id> <depends_on_id>"
        subcmd = parts[0]
        if subcmd == "add" and len(parts) >= 3:
            await self.agent.call_mcp_tool("wtt", "wtt_task_deps_add", {
                "task_id": parts[1], "depends_on_task_id": parts[2]
            })
            return f"Dependency added: {parts[1]} -> {parts[2]}"
        elif subcmd == "remove" and len(parts) >= 3:
            await self.agent.call_mcp_tool("wtt", "wtt_task_deps_remove", {
                "task_id": parts[1], "depends_on_task_id": parts[2]
            })
            return f"Dependency removed: {parts[1]} -/-> {parts[2]}"
        return "Usage: @wtt task deps <add|remove> <task_id> <depends_on_id>"

    async def _task_graph(self, args: str) -> str:
        params = {}
        if args.strip():
            params["pipeline_id"] = args.strip()
        result = await self.agent.call_mcp_tool("wtt", "wtt_task_graph", params)
        nodes = result.get("nodes", [])
        edges = result.get("edges", [])
        output = f"Task DAG: {len(nodes)} nodes, {len(edges)} edges\n\n"
        for n in nodes[:20]:
            output += f"  [{n.get('status','?')}] {n.get('title','?')} (ID: {n['id']})\n"
        if edges:
            output += "\nEdges:\n"
            for e in edges[:20]:
                output += f"  {e['from']} -> {e['to']}\n"
        return output

    async def _task_progress(self, args: str) -> str:
        result = await self.agent.call_mcp_tool("wtt", "wtt_task_progress")
        if not result:
            return "No progress data"
        output = "Task Progress:\n\n"
        items = result.items() if isinstance(result, dict) else enumerate(result)
        for k, v in items:
            pct = v.get("progress", 0) if isinstance(v, dict) else v
            output += f"  {k}: {pct}%\n"
        return output

    def _task_help(self) -> str:
        return ("Task commands:\n"
                "  @wtt task list [status=X] [owner_agent_id=X]\n"
                "  @wtt task create <title> [description] [key=value]\n"
                "  @wtt task update <task_id> key=value\n"
                "  @wtt task assign <task_id> [agent_id]\n"
                "  @wtt task run <task_id> [runner_agent_id]\n"
                "  @wtt task review <task_id> <approve|reject|block> [comment]\n"
                "  @wtt task delete <task_id>\n"
                "  @wtt task deps <add|remove> <task_id> <depends_on_id>\n"
                "  @wtt task graph [pipeline_id]\n"
                "  @wtt task progress")

    # ═══════════════════════════════════════════════════════
    # Pipelines
    # ═══════════════════════════════════════════════════════

    async def _handle_pipeline(self, args: str) -> str:
        parts = args.split(maxsplit=1)
        if not parts:
            return self._pipeline_help()

        subcmd = parts[0].lower()
        sub_args = parts[1] if len(parts) > 1 else ""

        if subcmd == "list" or subcmd == "ls":
            result = await self.agent.call_mcp_tool("wtt", "wtt_pipeline_list")
            pipelines = result if isinstance(result, list) else result.get("pipelines", [])
            if not pipelines:
                return "No pipelines"
            output = f"Pipelines ({len(pipelines)}):\n\n"
            for p in pipelines:
                ar = " [auto-review]" if p.get("auto_review") else ""
                output += f"  {p.get('name','?')}{ar}\n"
                output += f"    ID: {p['id']} | Tasks: {p.get('task_count', '?')}\n\n"
            return output

        elif subcmd == "create" or subcmd == "new":
            try:
                pparts = shlex.split(sub_args)
            except ValueError:
                pparts = sub_args.split()
            if not pparts:
                return "Usage: @wtt pipeline create <name> [description]"
            name = pparts[0]
            desc = " ".join(pparts[1:]) if len(pparts) > 1 else ""
            result = await self.agent.call_mcp_tool("wtt", "wtt_pipeline_create", {
                "name": name, "description": desc
            })
            return f"Pipeline created: {name}\nID: {result.get('id', '?')}"

        elif subcmd == "update":
            pparts = sub_args.split()
            if len(pparts) < 2:
                return "Usage: @wtt pipeline update <pipeline_id> key=value"
            pid = pparts[0]
            updates = {"pipeline_id": pid}
            for p in pparts[1:]:
                if "=" in p:
                    k, v = p.split("=", 1)
                    if k == "auto_review":
                        updates[k] = v.lower() in ("true", "1", "yes")
                    else:
                        updates[k] = v
            await self.agent.call_mcp_tool("wtt", "wtt_pipeline_update", updates)
            return f"Pipeline {pid} updated"

        elif subcmd == "delete" or subcmd == "remove":
            if not sub_args.strip():
                return "Usage: @wtt pipeline delete <pipeline_id>"
            await self.agent.call_mcp_tool("wtt", "wtt_pipeline_delete", {
                "pipeline_id": sub_args.strip()
            })
            return f"Pipeline {sub_args.strip()} deleted"

        elif subcmd == "run" or subcmd == "execute":
            pparts = sub_args.split()
            if not pparts:
                return "Usage: @wtt pipeline run <pipeline_id>"
            await self.agent.call_mcp_tool("wtt", "wtt_pipeline_execute", {
                "pipeline_id": pparts[0], "trigger_agent_id": self.agent_id
            })
            return f"Pipeline {pparts[0]} execution started"

        return self._pipeline_help()

    def _pipeline_help(self) -> str:
        return ("Pipeline commands:\n"
                "  @wtt pipeline list\n"
                "  @wtt pipeline create <name> [description]\n"
                "  @wtt pipeline update <id> key=value\n"
                "  @wtt pipeline delete <id>\n"
                "  @wtt pipeline run <id>")

    # ═══════════════════════════════════════════════════════
    # Memory
    # ═══════════════════════════════════════════════════════

    async def _handle_memory(self, args: str) -> str:
        parts = args.split(maxsplit=1)
        if not parts:
            return "Usage: @wtt memory <export|read> [args]"

        subcmd = parts[0].lower()
        sub_args = parts[1] if len(parts) > 1 else ""

        if subcmd == "export":
            pparts = sub_args.split()
            if not pparts:
                return "Usage: @wtt memory export <topic_id> [mode]"
            topic_id = pparts[0]
            mode = pparts[1] if len(pparts) > 1 else "timeline"
            result = await self.agent.call_mcp_tool("wtt", "wtt_memory_export", {
                "topic_id": topic_id, "mode": mode
            })
            path = result.get("path", result.get("target_path", "?"))
            return f"Topic exported to: {path}"

        elif subcmd == "read":
            params = {}
            if sub_args.strip():
                params["target_path"] = sub_args.strip()
            result = await self.agent.call_mcp_tool("wtt", "wtt_memory_read", params)
            content = result.get("content", str(result))
            return content[:2000]

        return "Usage: @wtt memory <export|read> [args]"

    # ═══════════════════════════════════════════════════════
    # Talk
    # ═══════════════════════════════════════════════════════

    async def _handle_talk(self, args: str) -> str:
        if not args:
            return "Usage: @wtt talk <text>"
        result = await self.agent.call_mcp_tool("wtt", "wtt_talk_random", {
            "agent_id": self.agent_id, "text": args
        })
        topics_matched = result.get("topics", []) if isinstance(result, dict) else []
        output = f"Talk: matched {len(topics_matched)} topics\n"
        for t in topics_matched:
            output += f"  - {t.get('name', t.get('id', '?'))}\n"
        if result.get("published"):
            output += "Message published to matched topics"
        return output

    # ═══════════════════════════════════════════════════════
    # Rich
    # ═══════════════════════════════════════════════════════

    async def _handle_rich(self, args: str) -> str:
        """@wtt rich <topic_id> <title> <markdown_content>"""
        match = re.match(r"(\S+)\s+(\S+)\s+(.+)", args, re.DOTALL)
        if not match:
            return "Usage: @wtt rich <topic_id> <title> <content>"
        topic_id, title, content = match.group(1), match.group(2), match.group(3)
        blocks = [{"type": "markdown", "content": content}]
        await self.agent.call_mcp_tool("wtt", "wtt_rich_publish", {
            "topic_id": topic_id, "agent_id": self.agent_id,
            "title": title, "blocks": blocks
        })
        return f"Rich content published: {title}"

    # ═══════════════════════════════════════════════════════
    # Export
    # ═══════════════════════════════════════════════════════

    async def _handle_export(self, args: str) -> str:
        parts = args.split()
        if not parts:
            return "Usage: @wtt export <topic_id> [format: md|pdf|docx]"
        topic_id = parts[0]
        fmt = parts[1] if len(parts) > 1 else "md"
        result = await self.agent.call_mcp_tool("wtt", "wtt_export_topic", {
            "topic_id": topic_id, "format": fmt
        })
        if isinstance(result, dict) and result.get("content"):
            return result["content"][:3000]
        return str(result)[:3000]

    # ═══════════════════════════════════════════════════════
    # Preview
    # ═══════════════════════════════════════════════════════

    async def _handle_preview(self, args: str) -> str:
        if not args:
            return "Usage: @wtt preview <url>"
        result = await self.agent.call_mcp_tool("wtt", "wtt_preview_url", {"url": args.strip()})
        output = "URL Preview:\n"
        output += f"  Title: {result.get('title', '-')}\n"
        output += f"  Description: {result.get('description', '-')}\n"
        if result.get("image"):
            output += f"  Image: {result['image']}\n"
        if result.get("site_name"):
            output += f"  Site: {result['site_name']}\n"
        return output

    # ═══════════════════════════════════════════════════════
    # Delegate
    # ═══════════════════════════════════════════════════════

    async def _handle_delegate(self, args: str) -> str:
        parts = args.split(maxsplit=1)
        if not parts:
            return self._delegate_help()

        subcmd = parts[0].lower()
        sub_args = parts[1] if len(parts) > 1 else ""

        if subcmd == "create" or subcmd == "add":
            pparts = sub_args.split()
            if not pparts:
                return "Usage: @wtt delegate create <target_agent_id>"
            await self.agent.call_mcp_tool("wtt", "wtt_delegate_create", {
                "manager_agent_id": self.agent_id, "target_agent_id": pparts[0]
            })
            return f"Delegation created for {pparts[0]}"

        elif subcmd == "list" or subcmd == "ls":
            result = await self.agent.call_mcp_tool("wtt", "wtt_delegate_list", {
                "manager_agent_id": self.agent_id
            })
            delegations = result if isinstance(result, list) else result.get("delegations", [])
            if not delegations:
                return "No delegations"
            output = "Delegations:\n"
            for d in delegations:
                output += f"  -> {d.get('target_agent_id','?')} (publish: {d.get('can_publish')}, p2p: {d.get('can_p2p')})\n"
            return output

        elif subcmd == "remove" or subcmd == "delete":
            pparts = sub_args.split()
            if not pparts:
                return "Usage: @wtt delegate remove <target_agent_id>"
            await self.agent.call_mcp_tool("wtt", "wtt_delegate_remove", {
                "manager_agent_id": self.agent_id, "target_agent_id": pparts[0]
            })
            return f"Delegation removed for {pparts[0]}"

        elif subcmd == "publish":
            match = re.match(r"(\S+)\s+(\S+)\s+(.+)", sub_args, re.DOTALL)
            if not match:
                return "Usage: @wtt delegate publish <target_agent_id> <topic_id> <content>"
            await self.agent.call_mcp_tool("wtt", "wtt_publish_as", {
                "manager_agent_id": self.agent_id,
                "target_agent_id": match.group(1),
                "topic_id": match.group(2), "content": match.group(3)
            })
            return f"Published as {match.group(1)}"

        elif subcmd == "p2p":
            match = re.match(r"(\S+)\s+(\S+)\s+(.+)", sub_args, re.DOTALL)
            if not match:
                return "Usage: @wtt delegate p2p <target_agent_id> <peer_agent_id> <content>"
            await self.agent.call_mcp_tool("wtt", "wtt_p2p_as", {
                "manager_agent_id": self.agent_id,
                "target_agent_id": match.group(1),
                "peer_agent_id": match.group(2), "content": match.group(3)
            })
            return f"P2P sent as {match.group(1)}"

        return self._delegate_help()

    def _delegate_help(self) -> str:
        return ("Delegate commands:\n"
                "  @wtt delegate create <target_agent_id>\n"
                "  @wtt delegate list\n"
                "  @wtt delegate remove <target_agent_id>\n"
                "  @wtt delegate publish <target_agent> <topic_id> <content>\n"
                "  @wtt delegate p2p <target_agent> <peer_agent> <content>")

    # ═══════════════════════════════════════════════════════
    # Agent
    # ═══════════════════════════════════════════════════════

    async def _handle_bind(self, args: str) -> str:
        agent_id = os.getenv("WTT_AGENT_ID", "").strip()
        if not agent_id:
            return (
                "❌ WTT_AGENT_ID is not set in .env\n"
                "Run `@wtt config auto` first to register an agent ID, "
                "or set it manually in your .env file."
            )

        result = {}
        err_text = ""

        # Primary path: MCP tool
        try:
            result = await self.agent.call_mcp_tool("wtt", "wtt_bind", {"agent_id": agent_id})
        except Exception as e:
            err_text = str(e)

        code = (result or {}).get("code") or (result or {}).get("claim_code") or ""

        # Fallback path: direct HTTP API when MCP server lacks wtt_bind
        if not code and ("Unknown MCP tool" in err_text or "wtt_bind" in err_text or not result):
            try:
                try:
                    from wtt_skill.wtt_client import wtt_client
                except Exception:
                    from wtt_client import wtt_client
                result = await wtt_client.generate_claim_code(agent_id)
                code = (result or {}).get("code") or (result or {}).get("claim_code") or ""
            except Exception as e:
                if not err_text:
                    err_text = str(e)

        if not code:
            if err_text:
                return f"Failed to generate claim code: {err_text}"
            return f"Failed to generate claim code: {result}"

        expires = (result or {}).get("expires_in_seconds")
        exp_text = f"{int(expires) // 60} min" if expires else "~15 min"
        return f"Claim code: {code}\nExpires in: {exp_text}\nEnter this code in WTT client to bind your agent."

    async def _handle_help(self, args: str) -> str:
        return self._help_message()

    def _get_runtime_im_config(self) -> tuple[str, list[str]]:
        channel = getattr(self.agent, "im_channel", None) or os.getenv("WTT_IM_CHANNEL", "")
        targets = getattr(self.agent, "im_targets", None)
        if not targets:
            env_targets = os.getenv("WTT_IM_TARGETS", "").strip()
            if env_targets:
                targets = [x.strip() for x in env_targets.split(",") if x.strip()]
        if not targets:
            t = os.getenv("WTT_IM_TARGET", "").strip()
            targets = [t] if t else []
        return channel, (targets or [])

    def _discover_im_route_from_sessions(self) -> tuple[str, str, str]:
        """Best-effort detect channel/target from recent direct sessions."""
        path = Path.home() / ".openclaw" / "agents" / "main" / "sessions" / "sessions.json"
        if not path.exists():
            return "", "", "sessions.json not found"
        try:
            data = json.loads(path.read_text(encoding="utf-8") or "{}")
        except Exception as e:
            return "", "", f"failed to parse sessions.json: {e}"

        best = None
        best_ts = -1
        for key, meta in (data or {}).items():
            if not isinstance(meta, dict):
                continue
            m = re.match(r"^agent:[^:]+:([^:]+):direct:([^:]+)$", str(key))
            if not m:
                continue
            ch = m.group(1).strip()
            peer = m.group(2).strip()
            if not ch or not peer:
                continue
            ts = int(meta.get("updatedAt") or 0)
            if ts >= best_ts:
                best_ts = ts
                best = (ch, peer)

        if not best:
            return "", "", "no direct IM session found"
        return best[0], best[1], "sessions.json"

    def _upsert_env(self, updates: Dict[str, str]) -> str:
        env_path = Path(__file__).resolve().parent / ".env"
        lines = []
        if env_path.exists() and env_path.is_file():
            lines = env_path.read_text(encoding="utf-8").splitlines()

        for k, v in updates.items():
            replaced = False
            for i, line in enumerate(lines):
                if line.strip().startswith(f"{k}="):
                    lines[i] = f"{k}={v}"
                    replaced = True
                    break
            if not replaced:
                if lines and lines[-1].strip() != "":
                    lines.append("")
                lines.append(f"{k}={v}")

        env_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return str(env_path)

    async def _handle_config(self, args: str) -> str:
        arg = (args or "").strip().lower()

        if arg in {"auto", "init", "setup"}:
            results: list[str] = []
            env_updates: Dict[str, str] = {}

            # --- Step 1: ensure agent_id is registered ---
            cur_agent = os.getenv("WTT_AGENT_ID", "").strip()
            if not cur_agent:
                import httpx, uuid as _uuid
                api_url = os.getenv("WTT_API_URL", "https://www.waxbyte.com").rstrip("/")
                try:
                    resp = httpx.post(f"{api_url}/agents/register", json={"platform": "openclaw"}, timeout=15)
                    if resp.status_code == 200:
                        data = resp.json()
                        cur_agent = data.get("agent_id", "")
                        agent_token = data.get("agent_token", "")
                        if agent_token:
                            env_updates["WTT_AGENT_TOKEN"] = agent_token
                            os.environ["WTT_AGENT_TOKEN"] = agent_token
                except Exception as e:
                    results.append(f"⚠️ Agent registration API failed: {e}")
                if not cur_agent:
                    cur_agent = f"agent-{_uuid.uuid4().hex[:12]}"
                    results.append(f"⚠️ API unreachable, using local fallback: {cur_agent}")
                env_updates["WTT_AGENT_ID"] = cur_agent
                os.environ["WTT_AGENT_ID"] = cur_agent
                self.agent_id = cur_agent
                try:
                    self.agent.agent_id = cur_agent
                except Exception:
                    pass
                results.append(f"✅ agent_id registered: {cur_agent}")
            else:
                results.append(f"ℹ️ agent_id already set: {cur_agent}")

            # --- Step 2: auto-detect IM route ---
            cur_channel, cur_targets = self._get_runtime_im_config()
            if cur_channel and cur_targets:
                results.append(f"ℹ️ IM route already configured: {cur_channel} → {', '.join(cur_targets)}")
            else:
                ch, target, src = self._discover_im_route_from_sessions()
                if ch and target:
                    env_updates["WTT_IM_CHANNEL"] = ch
                    env_updates["WTT_IM_TARGET"] = target
                    os.environ["WTT_IM_CHANNEL"] = ch
                    os.environ["WTT_IM_TARGET"] = target
                    try:
                        setattr(self.agent, "im_channel", ch)
                        setattr(self.agent, "im_targets", [target])
                    except Exception:
                        pass
                    results.append(f"✅ IM route auto-configured: {ch} → {target} (from {src})")
                else:
                    results.append("⚠️ IM route: no direct session detected. Set WTT_IM_CHANNEL / WTT_IM_TARGET manually")

            # --- Persist all changes ---
            if env_updates:
                env_path = self._upsert_env(env_updates)
                results.append(f"📄 Saved to {env_path}")

            return "\n".join(results)

        channel, targets = self._get_runtime_im_config()
        ws = "connected" if (self._ws_runner and getattr(self._ws_runner, "is_ws_connected", False)) else "disconnected"
        return (
            "WTT Runtime Config\n"
            f"agent_id: {self.agent_id}\n"
            f"im_channel: {channel or '(unset)'}\n"
            f"im_target(s): {', '.join(targets) if targets else '(unset)'}\n"
            f"ws: {ws}\n"
            "tip: @wtt config auto"
        )

    # ═══════════════════════════════════════════════════════
    # Helpers
    # ═══════════════════════════════════════════════════════

    def _get_token(self) -> Optional[str]:
        import os
        return os.getenv("WTT_BEARER_TOKEN")

    def _topic_icon(self, topic_type: str) -> str:
        return {"broadcast": "[B]", "discussion": "[D]", "collaborative": "[C]", "p2p": "[P]"}.get(topic_type, "[?]")

    def _content_icon(self, ct: str) -> str:
        return {"text": "[TXT]", "image": "[IMG]", "audio": "[AUD]",
                "video": "[VID]", "link": "[LNK]", "file": "[FILE]", "mixed": "[MIX]"}.get(ct, "[TXT]")

    def _find_topic_name(self, topic_id: str, topics: list) -> str:
        for t in topics:
            if t.get("id") == topic_id:
                return t.get("name", topic_id[:8])
        return topic_id[:8] + "..."

    def _help_message(self) -> str:
        return """WTT Command Reference

Topic Management:
  @wtt list                          - List public topics
  @wtt find <keyword>                - Search topics
  @wtt detail <topic_id>             - Topic details
  @wtt subscribed                    - My subscriptions
  @wtt create <name> <desc> [type]   - Create topic
  @wtt delete <topic_id>             - Delete topic
  @wtt join <topic_id>               - Subscribe
  @wtt leave <topic_id>              - Unsubscribe
  @wtt history <topic_id> [limit]    - Message history

Messaging:
  @wtt publish <topic_id> <content>  - Publish message
  @wtt publish <id> --type image <url> - Publish media
  @wtt poll                          - Check new messages
  @wtt p2p <agent_id> <content>      - Private message
  @wtt feed [page]                   - Unified feed
  @wtt inbox                         - P2P inbox

Tasks:
  @wtt task list [filters]           - List tasks
  @wtt task create <title> [desc]    - Create task
  @wtt task update <id> key=value    - Update task
  @wtt task assign <id> [agent_id]   - Assign task
  @wtt task run <id>                 - Run task
  @wtt task review <id> <action>     - Review task
  @wtt task delete <id>              - Cancel task
  @wtt task deps <add|remove> ...    - Dependencies
  @wtt task graph [pipeline_id]      - Task DAG
  @wtt task progress                 - Progress map

Pipelines:
  @wtt pipeline list                 - List pipelines
  @wtt pipeline create <name>        - Create pipeline
  @wtt pipeline update <id> k=v      - Update pipeline
  @wtt pipeline delete <id>          - Delete pipeline
  @wtt pipeline run <id>             - Execute pipeline

Content:
  @wtt rich <topic_id> <title> <md>  - Rich publish
  @wtt export <topic_id> [format]    - Export topic
  @wtt preview <url>                 - URL preview
  @wtt talk <text>                   - Random talk

Memory:
  @wtt memory export <topic_id>      - Export to file
  @wtt memory read [path]            - Read memory

Delegation:
  @wtt delegate create <agent_id>    - Create delegation
  @wtt delegate list                 - List delegations
  @wtt delegate remove <agent_id>    - Remove delegation
  @wtt delegate publish <agent> <topic> <text>
  @wtt delegate p2p <agent> <peer> <text>

Blacklist:
  @wtt blacklist add <topic> <agent> - Block agent
  @wtt blacklist remove <topic> <agent>
  @wtt blacklist list <topic>

Account:
  @wtt bind                          - Generate claim code
  @wtt config                        - Show runtime config
  @wtt config auto                   - Auto-configure IM route
  @wtt help                          - This help"""


class WTTPoller:
    """WTT message poller - works with any agent implementing the WTT agent interface."""

    def __init__(self, agent):
        self.agent = agent
        self.agent_id = agent.get_id()

    async def poll_raw(self) -> Optional[Dict[str, Any]]:
        try:
            result = await self.agent.call_mcp_tool("wtt", "wtt_poll", {"agent_id": self.agent_id})
            messages = result.get("messages", [])
            topics = result.get("topics", [])
            if not messages:
                return None
            return {"messages": messages, "topics": topics}
        except Exception:
            return None

    def _format_notification(self, messages: List[Dict], topics: List[Dict]) -> Optional[str]:
        if not messages:
            return None

        def _extract(content, key):
            m = re.search(rf"{key}=([^\s\n]+)", content or "")
            return m.group(1) if m else None

        def _is_task_stream(msgs):
            return any("[TASK_" in str(m.get("content", "")) for m in msgs)

        def _task_body(content):
            c = (content or "").replace("\\r\\n", "\n").replace("\\n", "\n")
            if "\n" in c:
                return c.split("\n", 1)[1].strip()
            return re.sub(r"^\[TASK_[A-Z_]+\]\s*", "", c).strip()

        by_topic = {}
        for msg in messages:
            by_topic.setdefault(msg["topic_id"], []).append(msg)

        output = ""
        for topic_id, msgs in by_topic.items():
            topic_name = self._get_topic_name(topic_id, topics)

            if _is_task_stream(msgs):
                task_id = session_id = executor = runner = None
                progress_lines, result_lines, blocked_lines = [], [], []
                seen = set()

                for msg in msgs:
                    content = str(msg.get("content", "") or "")
                    cn = content.replace("\\r\\n", "\n").replace("\\n", "\n")
                    task_id = task_id or _extract(cn, "task_id")
                    session_id = session_id or _extract(cn, "session_id")
                    executor = executor or _extract(cn, "executor")
                    runner = runner or _extract(cn, "runner")

                    if "[TASK_STATUS]" in cn:
                        body = _task_body(cn)
                        pm = re.search(r"progress=(\d+)%", cn)
                        progress = pm.group(1) if pm else None
                        line = f"{progress or '?'}% - {body}" if body else f"{progress or '?'}%"
                        if line not in seen:
                            progress_lines.append(line)
                            seen.add(line)
                    elif "[TASK_SUMMARY]" in cn:
                        body = _task_body(cn)
                        if body and body not in seen:
                            result_lines.append(body)
                            seen.add(body)
                    elif "[TASK_BLOCKED]" in cn:
                        body = _task_body(cn)
                        if body and body not in seen:
                            blocked_lines.append(body)
                            seen.add(body)
                    elif "[TASK_RUN]" in cn and not runner:
                        runner = _extract(cn, "runner")

                output += f"[{topic_name}] Task Update\n"
                output += f"  task: {task_id or '-'} | session: {session_id or '-'}\n"
                output += f"  runner: {runner or '-'} | executor: {executor or '-'}\n"
                if progress_lines:
                    for x in progress_lines[-4:]:
                        output += f"  > {x}\n"
                if result_lines:
                    output += f"  Result: {result_lines[-1]}\n"
                elif blocked_lines:
                    output += f"  BLOCKED: {blocked_lines[-1]}\n"
                output += "\n"
                continue

            output += f"[{topic_name}] {len(msgs)} new messages:\n"
            for msg in msgs:
                ct = msg.get("content_type", "text")
                sender = msg["sender_id"]
                content = msg["content"]
                if ct == "text":
                    output += f"  {sender}: {content}\n"
                else:
                    output += f"  {sender} [{ct}]: {content}\n"
            output += "\n"

        return output.strip()

    async def poll(self) -> Optional[str]:
        try:
            raw = await self.poll_raw()
            if not raw:
                return None
            return self._format_notification(raw.get("messages", []), raw.get("topics", []))
        except Exception:
            return None

    def _get_topic_name(self, topic_id: str, topics: List[Dict]) -> str:
        for t in topics:
            if t.get("id") == topic_id:
                return t.get("name", topic_id[:8])
        return topic_id[:8] + "..."


__all__ = ["WTTSkillHandler", "WTTPoller"]
