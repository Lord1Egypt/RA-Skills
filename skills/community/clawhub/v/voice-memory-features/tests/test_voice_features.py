
"""Tests for the Voice Memory feature modules (mock BlueColumn, no network)."""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import httpx


# Patch httpx.AsyncClient so tests run without a network/API key
class FakeResp:
    status_code = 200
    def __init__(self, data): self._data = data
    def json(self): return self._data
    @property
    def text(self): return str(self._data)

class FakeClient:
    def __init__(self, **kw): pass
    async def __aenter__(self): return self
    async def __aexit__(self, *a): return False
    async def post(self, url, headers=None, json=None):
        if url.endswith("/agent-recall"):
            return FakeResp({"answer": "Jane prefers email, works EST.", "sources": [{"session_id": "sess_test", "title": "t", "relevance": 0.9}]})
        if url.endswith("/agent-remember"):
            return FakeResp({"session_id": "sess_new", "summary": "stored", "action_items": [], "key_topics": []})
        if url.endswith("/agent-note"):
            return FakeResp({"note_id": "note_new", "queryable": True})
        return FakeResp({})

httpx.AsyncClient = FakeClient

from features import voice_memory as vm
from features import voice_context as vc
from features import voice_journal as vj
from features import voice_crm as cr
from features import voice_meeting as mt
from features import voice_coaching as ch
from features import voice_sales as sl

async def main():
    # core
    assert await vm.remember("Hello world this is a test memory") == "sess_new"
    r = await vm.recall("what do we know about jane")
    assert r["answer"] == "Jane prefers email, works EST."
    assert await vm.note("jane prefers async email") is True

    # context
    ctx = await vc.get_context("pricing question")
    assert "Jane prefers" in ctx["context"]
    assert "sess_test" in [s["session_id"] for s in ctx["sources"]]
    block = vc.build_context_block("ctx")
    assert "🧠 Voice Context" in block
    assert vc.build_context_block("") == ""

    # journal
    assert await vj.journal_entry("Today I felt great about the launch") == "sess_new"
    assert "Jane prefers" in await vj.today_entries()

    # crm
    assert await cr.log_customer_interaction("Acme Corp", "discussed renewal") == "sess_new"
    assert await cr.log_preference("Acme Corp", "email over phone") is True
    assert "Jane prefers" in await cr.customer_profile("Acme Corp")
    assert "Jane prefers" in await cr.open_followups()

    # meeting
    assert await mt.record_meeting("Standup", "Blockers: staging down") == "sess_new"
    assert "Jane prefers" in await mt.summarize_meeting("Standup")
    assert "Jane prefers" in await mt.action_items("Phoenix")

    # coaching
    assert await ch.set_goal("Ship MVP by Sep") == "sess_new"
    assert await ch.log_checkin("Ship MVP", "on track") is True
    assert "Jane prefers" in await ch.goal_status()

    # sales
    assert await sl.log_call("Jane", "discussed pricing", objection="price too high", next_step="send discount") == "sess_new"
    assert await sl.log_objection("Jane", "price too high") is True
    assert await sl.log_followup("Jane", "send proposal Friday") is True
    assert "Jane prefers" in await sl.deal_context("Jane")
    assert "Jane prefers" in await sl.pipeline()

    print("ALL VOICE MEMORY TESTS PASSED ✅")

asyncio.run(main())
