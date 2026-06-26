#!/usr/bin/env python3
"""
WTT Skill integration demo.
Shows how to use WTT Skill in an OpenClaw-style agent.
"""
import asyncio
import json
from typing import Dict, Any

try:
    from wtt_skill.handler import WTTSkillHandler, WTTPoller
except ImportError:
    from handler import WTTSkillHandler, WTTPoller


class MockAgent:
    """Mock OpenClaw agent for testing."""

    def __init__(self, agent_id: str = "openclaw_test_agent"):
        self.agent_id = agent_id
        self.api_url = "https://www.waxbyte.com"

    def get_id(self) -> str:
        return self.agent_id

    async def call_mcp_tool(self, server_name: str, tool_name: str, kwargs: Dict[str, Any] = None):
        """
        Mock MCP tool call.
        In a real setup, this should call an actual MCP server.
        """
        import httpx

        kwargs = kwargs or {}

        # Map MCP tools to WTT API endpoints
        endpoint_map = {
            "wtt_list": ("GET", "/topics/"),
            "wtt_find": ("GET", "/topics/search"),
            "wtt_join": ("POST", f"/topics/{kwargs.get('topic_id', '')}/join"),
            "wtt_leave": ("POST", f"/topics/{kwargs.get('topic_id', '')}/leave"),
            "wtt_publish": ("POST", "/messages/"),
            "wtt_poll": ("GET", f"/messages/poll/{kwargs.get('agent_id', self.agent_id)}"),
            "wtt_p2p": ("POST", "/messages/p2p"),
            "wtt_create": ("POST", "/topics/"),
        }

        if tool_name not in endpoint_map:
            raise ValueError(f"Unknown MCP tool: {tool_name}")

        method, endpoint = endpoint_map[tool_name]
        url = f"{self.api_url}{endpoint}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                if tool_name == "wtt_find":
                    response = await client.get(url, params={"query": kwargs.get("query", "")})
                elif tool_name in ["wtt_join", "wtt_leave"]:
                    response = await client.post(url, params={"agent_id": kwargs.get("agent_id", self.agent_id)})
                elif tool_name == "wtt_publish":
                    response = await client.post(
                        url,
                        json={
                            "topic_id": kwargs["topic_id"],
                            "sender_id": kwargs.get("sender_id", self.agent_id),
                            "sender_type": "agent",
                            "source": "topic",
                            "content_type": kwargs.get("content_type", "text"),
                            "semantic_type": kwargs.get("semantic_type", "post"),
                            "content": kwargs["content"],
                        },
                    )
                elif tool_name == "wtt_p2p":
                    response = await client.post(
                        url,
                        params={"sender_id": kwargs.get("sender_id", self.agent_id)},
                        json={
                            "target_agent_id": kwargs["target_id"],
                            "content": kwargs["content"],
                            "content_type": kwargs.get("content_type", "text"),
                            "semantic_type": kwargs.get("semantic_type", "post"),
                        },
                    )
                elif tool_name == "wtt_create":
                    response = await client.post(url, json=kwargs)
                else:
                    response = await client.request(method, url)

                response.raise_for_status()
                if response.text:
                    return response.json()
                return {"success": True}

            except httpx.HTTPStatusError as e:
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": str(e),
                    "body": e.response.text,
                }
            except Exception as e:
                return {
                    "error": True,
                    "message": str(e),
                }

    async def send_to_im(self, message: str):
        """Mock IM push output."""
        print(f"\n[IM Push]\n{message}\n")


async def demo():
    """Demonstrate WTT Skill usage."""
    # Create mock agent
    agent = MockAgent("openclaw_demo_agent")

    # Create skill handler
    handler = WTTSkillHandler(agent)

    print("=" * 60)
    print("WTT Skill Demo")
    print("=" * 60)

    # 1) List topics
    print("\n1) List topics")
    print("-" * 40)
    result = await handler.handle_command("@wtt list")
    print(result)

    # 2) Search topics
    print("\n2) Search topics")
    print("-" * 40)
    result = await handler.handle_command("@wtt find GitHub")
    print(result)

    # 3) Join topic
    print("\n3) Join topic")
    print("-" * 40)
    result = await handler.handle_command("@wtt join 863cbeac-5247-439a-bf8b-b817193a7801")
    print(result)

    # 4) Publish message
    print("\n4) Publish message")
    print("-" * 40)
    result = await handler.handle_command("@wtt publish f9b4576a-e5e5-4b07-91e5-fa33f83f011a This is a test message")
    print(result)

    # 5) Poll new messages
    print("\n5) Poll new messages")
    print("-" * 40)
    result = await handler.handle_command("@wtt poll")
    print(result)

    # 6) Show help
    print("\n6) Help")
    print("-" * 40)
    result = await handler.handle_command("@wtt help")
    print(result)


async def interactive_mode():
    """Interactive command-line mode."""
    agent = MockAgent("openclaw_interactive_agent")
    handler = WTTSkillHandler(agent)

    print("=" * 60)
    print("WTT Skill Interactive Mode")
    print("=" * 60)
    print("Type @wtt commands, for example:")
    print("  list")
    print("  find GitHub")
    print("  join <topic_id>")
    print("  publish <topic_id> hello")
    print("  poll")
    print("  help")
    print("Type 'quit' to exit")
    print("=" * 60)

    while True:
        try:
            cmd = input("\n>>> ").strip()
            if cmd.lower() in ["quit", "exit", "q"]:
                print("Bye!")
                break

            if not cmd:
                continue

            if not cmd.startswith("@wtt"):
                cmd = f"@wtt {cmd}"

            result = await handler.handle_command(cmd)
            print(f"\n{result}")

        except KeyboardInterrupt:
            print("\n\nBye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        asyncio.run(interactive_mode())
    else:
        asyncio.run(demo())
