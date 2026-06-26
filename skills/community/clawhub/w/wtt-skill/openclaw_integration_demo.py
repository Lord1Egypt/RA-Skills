#!/usr/bin/env python3
"""
Complete OpenClaw integration demo for WTT Skill.
Demonstrates:
1) Skill initialization
2) Background polling/runtime start
3) IM push behavior
4) @wtt command handling
"""
import asyncio
import json
import os
from typing import Dict, Any, Optional

try:
    from wtt_skill.runner import WTTSkillRunner
    from wtt_skill.handler import WTTSkillHandler
except ImportError:
    from runner import WTTSkillRunner
    from handler import WTTSkillHandler


class MockOpenClawAgent:
    """Mock OpenClaw agent implementation for local demo/testing."""

    def __init__(self, agent_id: str = "openclaw_demo_agent"):
        self.agent_id = agent_id
        self.api_url = os.getenv("WTT_API_URL", "https://www.waxbyte.com")
        self.im_platform = "telegram"
        self.received_count = 0

    def get_id(self) -> str:
        return self.agent_id

    async def call_mcp_tool(self, server_name: str, tool_name: str, kwargs: Dict[str, Any] = None):
        """Call MCP tools through direct HTTP mapping in this demo."""
        import httpx

        kwargs = kwargs or {}

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
                return response.json() if response.text else {"success": True}

            except Exception as e:
                print(f"MCP call failed [{tool_name}]: {e}")
                return {"error": True, "message": str(e)}

    async def send_to_im(self, message: str):
        """Mock push to IM."""
        self.received_count += 1
        print(f"\n{'='*80}")
        print(f"📱 [{self.im_platform}] IM Push #{self.received_count}")
        print(f"{'='*80}")
        print(message)
        print(f"{'='*80}\n")


class OpenClawWTTIntegration:
    """Wraps WTT skill runtime + command handling for the demo."""

    def __init__(self, agent: MockOpenClawAgent):
        self.agent = agent
        self.runner: Optional[WTTSkillRunner] = None
        self.handler: Optional[WTTSkillHandler] = None

    async def initialize(self):
        """Initialize WTT skill runtime."""
        print("🚀 Initializing WTT Skill...")

        self.runner = WTTSkillRunner(self.agent, interval=30)
        self.handler = WTTSkillHandler(self.agent)

        await self.runner.start()

        print("✅ WTT Skill initialized")

    async def handle_user_message(self, message: str) -> str:
        """Handle incoming user text."""
        if not message.startswith("@wtt"):
            return f"Received non-WTT message: {message}"

        if self.handler:
            return await self.handler.handle_command(message)

        return "WTT Skill is not initialized"

    async def run(self):
        """Run interactive demo loop."""
        print("=" * 80)
        print("WTT + OpenClaw Integration Demo")
        print("=" * 80)

        await self.initialize()

        print("\nType commands:")
        print("  @wtt list")
        print("  @wtt find GitHub")
        print("  @wtt join <topic_id>")
        print("  @wtt poll")
        print("Type 'quit' to exit")

        while True:
            try:
                msg = input("\nYou> ").strip()

                if msg.lower() in ["quit", "exit", "q"]:
                    print("Stopping...")
                    break

                if not msg:
                    continue

                result = await self.handle_user_message(msg)
                print(f"\nAgent> {result}")

            except KeyboardInterrupt:
                print("\n\nInterrupted, exiting...")
                break
            except Exception as e:
                print(f"Runtime error: {e}")

        if self.runner:
            await self.runner.stop()

        print("✅ Demo stopped")


async def run_quick_test():
    """Quick smoke test for key commands."""
    print("=" * 80)
    print("Quick Test")
    print("=" * 80)

    agent = MockOpenClawAgent("openclaw_quick_test")
    integration = OpenClawWTTIntegration(agent)

    await integration.initialize()

    test_commands = [
        "@wtt list",
        "@wtt find GitHub",
        "@wtt help",
    ]

    for cmd in test_commands:
        print(f"\nTesting: {cmd}")
        result = await integration.handle_user_message(cmd)
        print(f"Result:\n{result[:500]}{'...' if len(result) > 500 else ''}")
        await asyncio.sleep(1)

    if integration.runner:
        await integration.runner.stop()

    print("\n✅ Quick test completed")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        asyncio.run(run_quick_test())
    else:
        agent = MockOpenClawAgent()
        integration = OpenClawWTTIntegration(agent)
        asyncio.run(integration.run())
