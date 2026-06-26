#!/usr/bin/env python3
"""Backward-compatible wrapper over the unified campaign state store."""
from __future__ import annotations

from campaign_state_store import CampaignStateStore


class CampaignState(CampaignStateStore):
    def __init__(self, campaign_id: str):
        super().__init__(campaign_id)

    # Legacy method names preserved for older scripts.
    def start(self):
        self.data["status"] = "running"
        self.save()

    def end(self):
        self.data["status"] = "completed"
        self.save()

    def add_confirmed(self, blogger_id: str, blogger_info: dict):
        self.record_contacted(blogger_id, blogger_info)
        self.record_reply({"bloggerId": blogger_id, "content": blogger_info.get("content"), "subject": blogger_info.get("subject")}, classification="confirmed")

    def add_contacted(self, blogger_id: str, blogger_info: dict):
        self.record_contacted(blogger_id, blogger_info)

    def add_rejected(self, blogger_id: str, reason: str = ""):
        self.record_reply({"bloggerId": blogger_id, "content": reason, "subject": reason}, classification="rejected")

    def add_discussing(self, blogger_id: str, last_message: str = ""):
        self.record_reply({"bloggerId": blogger_id, "content": last_message, "subject": last_message}, classification="discussing")

    def increment_cycle(self):
        self.data.setdefault("metrics", {})["cyclesCompleted"] = int(self.data.setdefault("metrics", {}).get("cyclesCompleted") or 0) + 1
        self.save()

    def get_confirmed_ids(self) -> set:
        return {
            blogger_id
            for blogger_id, item in (self.data.get("contacted") or {}).items()
            if item.get("status") == "confirmed"
        }
