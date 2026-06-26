#!/usr/bin/env python3
"""
Synapse Layer Python Client for OpenClaw

Simple wrapper around Synapse Layer REST API.
"""

import httpx
import json
from typing import Optional, Dict, List, Any


class SynapseClient:
    """Client for Synapse Layer persistent memory API."""

    def __init__(self, api_key: str, timeout: float = 30.0):
        """
        Initialize Synapse Layer client.

        Args:
            api_key: Your Synapse Layer API key (sk_connect_*)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.client = httpx.Client(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=timeout
        )

    def remember(
        self,
        content: str,
        agent: str = "default",
        memory_type: Optional[str] = None,
        importance: Optional[int] = None,
        tags: Optional[List[str]] = None,
        project: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Store a memory with full security pipeline.

        Args:
            content: Memory content to store
            agent: Agent identifier
            memory_type: Event type (MANUAL, DECISION, MILESTONE, etc.)
            importance: Importance level 1-5
            tags: Tags for categorization
            project: Project identifier

        Returns:
            Dictionary with memory_id, trust_quotient, etc.
        """
        endpoint = "https://forge.synapselayer.org/mcp"
        data = {
            "content": content,
            "agent_id": agent
        }

        if memory_type:
            data["type"] = memory_type
        if importance is not None:
            data["importance"] = importance
        if tags:
            data["tags"] = tags
        if project:
            data["project"] = project

        response = self.client.post(endpoint, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "save_to_synapse",
                "arguments": data
            }
        })

        response.raise_for_status()
        result = response.json()

        if result.get("result") and result["result"].get("content"):
            return json.loads(result["result"]["content"][0]["text"])

        return {}

    def recall(
        self,
        query: str,
        agent: str = "default",
        limit: int = 10,
        mode: str = "auto"
    ) -> Dict[str, Any]:
        """
        Retrieve memories ranked by Trust Quotient.

        Args:
            query: Search query
            agent: Agent identifier
            limit: Maximum memories to return (1-50)
            mode: Recall mode (auto, temporal, semantic, priority, hybrid)

        Returns:
            Dictionary with memories list and metadata
        """
        endpoint = "https://forge.synapselayer.org/mcp"

        response = self.client.post(endpoint, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "recall",
                "arguments": {
                    "query": query,
                    "agent_id": agent,
                    "limit": limit,
                    "mode": mode
                }
            }
        })

        response.raise_for_status()
        result = response.json()

        if result.get("result") and result["result"].get("content"):
            return json.loads(result["result"]["content"][0]["text"])

        return {}

    def search(
        self,
        query: str,
        limit: int = 20,
        agent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cross-agent memory search.

        Args:
            query: Search query
            limit: Maximum results to return (1-50)
            agent_id: Optional agent filter

        Returns:
            Dictionary with search results
        """
        endpoint = "https://forge.synapselayer.org/mcp"

        data = {
            "query": query,
            "limit": limit
        }

        if agent_id:
            data["agent_id"] = agent_id

        response = self.client.post(endpoint, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "search",
                "arguments": data
            }
        })

        response.raise_for_status()
        result = response.json()

        if result.get("result") and result["result"].get("content"):
            return json.loads(result["result"]["content"][0]["text"])

        return {}

    def process_text(
        self,
        text: str,
        agent: str = "default",
        project: Optional[str] = None,
        source: str = "mcp"
    ) -> Dict[str, Any]:
        """
        Extract events from free-form text.

        Args:
            text: Text to process
            agent: Agent identifier
            project: Project identifier
            source: Source identifier

        Returns:
            Dictionary with detected events
        """
        endpoint = "https://forge.synapselayer.org/mcp"

        data = {
            "text": text,
            "agent_id": agent,
            "source": source
        }

        if project:
            data["project"] = project

        response = self.client.post(endpoint, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "process_text",
                "arguments": data
            }
        })

        response.raise_for_status()
        result = response.json()

        if result.get("result") and result["result"].get("content"):
            return json.loads(result["result"]["content"][0]["text"])

        return {}

    def health_check(self) -> Dict[str, Any]:
        """
        Check system health and capabilities.

        Returns:
            Dictionary with status, version, capabilities
        """
        endpoint = "https://forge.synapselayer.org/mcp"

        response = self.client.post(endpoint, json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "health_check",
                "arguments": {}
            }
        })

        response.raise_for_status()
        result = response.json()

        if result.get("result") and result["result"].get("content"):
            return json.loads(result["result"]["content"][0]["text"])

        return {}

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# Convenience function for quick usage
def create_client(api_key: str) -> SynapseClient:
    """Create a Synapse Layer client with default settings."""
    return SynapseClient(api_key)
