#!/usr/bin/env python3
"""
Basic integration test for Taichi Framework.
Requires Redis running on localhost:6379.
"""
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import redis.asyncio as redis


async def test_basic_pipeline():
    """Test the full centralized pipeline: user.request -> dispatch.completed."""
    r = await redis.from_url("redis://localhost:6379", decode_responses=True)

    test_request = {
        "type": "user.request",
        "from": "test_client",
        "to": "PlannerAgent",
        "correlation_id": "test-001",
        "payload": {"text": "分析日志文件 app.log"},
    }

    # Subscribe to orchestrator for final result
    pubsub = r.pubsub()
    await pubsub.subscribe("agent.orchestrator")

    # Publish test request
    await r.publish("agent.PlannerAgent", json.dumps(test_request))
    print(f"[Test] Published request: {test_request['correlation_id']}")

    # Wait for dispatch.completed
    timeout = 30
    received = False
    try:
        async for msg in pubsub.listen():
            if msg["type"] == "message":
                data = json.loads(msg["data"])
                if (
                    data.get("correlation_id") == "test-001"
                    and data.get("type") == "dispatch.completed"
                ):
                    print(f"[Test] Received result: {data['payload']}")
                    received = True
                    break
    except asyncio.TimeoutError:
        pass

    await pubsub.unsubscribe()
    await pubsub.aclose()
    await r.aclose()

    if received:
        print("[Test] PASSED")
        return 0
    else:
        print("[Test] TIMEOUT - check Redis and agents are running")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(test_basic_pipeline()))
