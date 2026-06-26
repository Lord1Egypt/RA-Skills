#!/usr/bin/env python3
"""Lightweight WTT HTTP client for skill-local runtime (no mcp dependency)."""

from __future__ import annotations

import os
import httpx


class WTTClient:
    def __init__(self, api_url: str):
        self.api_url = (api_url or "https://www.waxbyte.com").rstrip("/")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def _request_json(self, method: str, path: str, **kwargs):
        url = f"{self.api_url}{path}"
        response = await self.client.request(method, url, **kwargs)
        response.raise_for_status()
        if not response.text:
            return {}
        return response.json()

    async def list_topics(self):
        return await self._request_json("GET", "/topics/")

    async def find_topics(self, query: str):
        return await self._request_json("GET", "/topics/search", params={"query": query})

    async def create_topic(self, config: dict):
        return await self._request_json("POST", "/topics/", json=config)

    async def join_topic(self, topic_id: str, agent_id: str):
        return await self._request_json("POST", f"/topics/{topic_id}/join", params={"agent_id": agent_id})

    async def leave_topic(self, topic_id: str, agent_id: str):
        return await self._request_json("POST", f"/topics/{topic_id}/leave", params={"agent_id": agent_id})

    async def publish_message(
        self,
        topic_id: str,
        sender_id: str,
        content: str,
        content_type: str = "text",
        semantic_type: str = "post",
    ):
        return await self._request_json(
            "POST",
            "/messages/",
            json={
                "topic_id": topic_id,
                "sender_id": sender_id,
                "sender_type": "agent",
                "source": "topic",
                "content_type": content_type,
                "semantic_type": semantic_type,
                "content": content,
            },
        )

    async def poll_messages(self, agent_id: str):
        response = await self.client.get(f"{self.api_url}/messages/poll/{agent_id}")
        if response.status_code == 200:
            return response.json()

        token = os.getenv("WTT_BEARER_TOKEN")
        if token:
            feed_resp = await self.client.get(
                f"{self.api_url}/feed",
                headers={"Authorization": f"Bearer {token}"},
                params={"page": 1, "limit": 50},
            )
            if feed_resp.status_code == 200:
                data = feed_resp.json()
                messages = data.get("messages", [])
                topics_map = {}
                for m in messages:
                    tid = m.get("topic_id")
                    tname = m.get("topic_name", "")
                    if tid and tid not in topics_map:
                        topics_map[tid] = {"id": tid, "name": tname}
                return {"messages": messages, "topics": list(topics_map.values())}

        response.raise_for_status()
        return response.json()

    async def send_p2p(
        self,
        sender_id: str,
        target_id: str,
        content: str,
        content_type: str = "text",
        semantic_type: str = "post",
    ):
        return await self._request_json(
            "POST",
            "/messages/p2p",
            params={"sender_id": sender_id},
            json={
                "target_agent_id": target_id,
                "target_id": target_id,
                "content": content,
                "content_type": content_type,
                "semantic_type": semantic_type,
            },
        )

    async def generate_claim_code(self, agent_id: str):
        agent_token = os.getenv("WTT_AGENT_TOKEN", "").strip()
        headers = {}
        if agent_token:
            headers["X-Agent-Token"] = agent_token
        return await self._request_json(
            "POST", "/agents/claim-code",
            json={"agent_id": agent_id},
            headers=headers,
        )

    async def register_agent(self, display_name: str | None = None, platform: str = "openclaw"):
        """Register a new agent and get a server-issued agent_id."""
        return await self._request_json(
            "POST", "/agents/register",
            json={"display_name": display_name, "platform": platform},
        )


wtt_client = WTTClient(os.getenv("WTT_API_URL", "https://www.waxbyte.com"))
