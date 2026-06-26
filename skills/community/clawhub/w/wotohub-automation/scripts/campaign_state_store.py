#!/usr/bin/env python3
from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

from common import state_file


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


class CampaignStateStore:
    """Unified campaign state store for cron-friendly campaign automation.

    Canonical sections:
    - contacted: outreach attempts / sent emails
    - replies: inbound reply records
    - replyActions: preview / auto-send / human-review decisions
    - metrics: cumulative counters across cycles
    """

    CURRENT_VERSION = 2

    def __init__(self, campaign_id: str, path: Optional[Union[str, Path]]= None):
        self.campaign_id = campaign_id
        self.path = Path(path) if path else state_file(f"campaign_{campaign_id}.json")
        self.data = self._load()

    def _default_state(self) -> dict[str, Any]:
        return {
            "version": self.CURRENT_VERSION,
            "campaignId": self.campaign_id,
            "createdAt": _now_iso(),
            "updatedAt": _now_iso(),
            "status": "idle",
            "targetCount": 30,
            "contacted": {},
            "replies": {},
            "replyActions": {},
            "metrics": {
                "cyclesCompleted": 0,
                "totalContacted": 0,
                "totalReplies": 0,
                "totalReplyActions": 0,
                "confirmed": 0,
                "discussing": 0,
                "rejected": 0,
                "autoRepliesSent": 0,
                "humanReviewRequired": 0,
            },
            "history": {
                "cycles": [],
            },
            "legacy": {
                "confirmed_partners": [],
                "contacted_bloggers": [],
                "rejected_bloggers": [],
                "discussing_bloggers": [],
                "total_invited": 0,
                "cycles_completed": 0,
                "start_time": None,
                "end_time": None,
            },
        }

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return self._default_state()
        raw = json.loads(self.path.read_text())
        if raw.get("version") == self.CURRENT_VERSION and "metrics" in raw:
            return raw
        return self._migrate_legacy(raw)

    def _migrate_legacy(self, raw: dict[str, Any]) -> dict[str, Any]:
        state = self._default_state()
        state["createdAt"] = raw.get("created_at") or raw.get("createdAt") or state["createdAt"]
        state["status"] = raw.get("status") or state["status"]
        state["targetCount"] = int(raw.get("target_count") or raw.get("targetCount") or 30)
        state["legacy"]["start_time"] = raw.get("start_time")
        state["legacy"]["end_time"] = raw.get("end_time")

        for item in raw.get("contacted_bloggers", []):
            blogger_id = str(item.get("bloggerId") or "")
            if blogger_id:
                state["contacted"][blogger_id] = {
                    "bloggerId": blogger_id,
                    "status": "contacted",
                    "contactedAt": item.get("contacted_at") or _now_iso(),
                    "lastContact": item.get("info") or {},
                }
        for item in raw.get("confirmed_partners", []):
            blogger_id = str(item.get("bloggerId") or "")
            if blogger_id:
                entry = state["contacted"].setdefault(blogger_id, {"bloggerId": blogger_id})
                entry.update({
                    "status": "confirmed",
                    "confirmedAt": item.get("confirmed_at") or _now_iso(),
                    "lastReply": item.get("info") or {},
                })
        for item in raw.get("discussing_bloggers", []):
            blogger_id = str(item.get("bloggerId") or "")
            if blogger_id:
                entry = state["contacted"].setdefault(blogger_id, {"bloggerId": blogger_id})
                entry.update({
                    "status": "discussing",
                    "lastMessage": item.get("last_message") or "",
                    "updatedAt": item.get("updated_at") or _now_iso(),
                })
        for item in raw.get("rejected_bloggers", []):
            blogger_id = str(item.get("bloggerId") or "")
            if blogger_id:
                entry = state["contacted"].setdefault(blogger_id, {"bloggerId": blogger_id})
                entry.update({
                    "status": "rejected",
                    "rejectedAt": item.get("rejected_at") or _now_iso(),
                    "rejectReason": item.get("reason") or "",
                })

        state["metrics"]["cyclesCompleted"] = int(raw.get("cycles_completed") or 0)
        state["metrics"]["totalContacted"] = len(state["contacted"])
        state["metrics"]["confirmed"] = len([x for x in state["contacted"].values() if x.get("status") == "confirmed"])
        state["metrics"]["discussing"] = len([x for x in state["contacted"].values() if x.get("status") == "discussing"])
        state["metrics"]["rejected"] = len([x for x in state["contacted"].values() if x.get("status") == "rejected"])
        state["legacy"].update({
            "confirmed_partners": raw.get("confirmed_partners", []),
            "contacted_bloggers": raw.get("contacted_bloggers", []),
            "rejected_bloggers": raw.get("rejected_bloggers", []),
            "discussing_bloggers": raw.get("discussing_bloggers", []),
            "total_invited": int(raw.get("total_invited") or len(raw.get("contacted_bloggers", []))),
            "cycles_completed": int(raw.get("cycles_completed") or 0),
        })
        self._sync_legacy_views(state)
        return state

    def save(self) -> None:
        self.data["updatedAt"] = _now_iso()
        self._sync_legacy_views(self.data)
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2))

    def _sync_legacy_views(self, state: dict[str, Any]) -> None:
        confirmed = []
        contacted = []
        rejected = []
        discussing = []
        for blogger_id, item in (state.get("contacted") or {}).items():
            base = {"bloggerId": blogger_id}
            if item.get("contactedAt"):
                contacted.append({**base, "info": item.get("lastContact") or {}, "contacted_at": item.get("contactedAt")})
            if item.get("status") == "confirmed":
                confirmed.append({**base, "info": item.get("lastReply") or {}, "confirmed_at": item.get("confirmedAt") or state.get("updatedAt")})
            elif item.get("status") == "discussing":
                discussing.append({**base, "last_message": item.get("lastMessage") or "", "updated_at": item.get("updatedAt") or state.get("updatedAt")})
            elif item.get("status") == "rejected":
                rejected.append({**base, "reason": item.get("rejectReason") or "", "rejected_at": item.get("rejectedAt") or state.get("updatedAt")})
        legacy = state.setdefault("legacy", {})
        legacy.update({
            "confirmed_partners": confirmed,
            "contacted_bloggers": contacted,
            "rejected_bloggers": rejected,
            "discussing_bloggers": discussing,
            "total_invited": len(contacted),
            "cycles_completed": state.get("metrics", {}).get("cyclesCompleted", 0),
        })

    def start_cycle(self, mode: str = "single_cycle", metadata: Optional[dict[str, Any]]= None) -> dict[str, Any]:
        cycle_no = int(self.data["metrics"].get("cyclesCompleted") or 0) + 1
        self.data["status"] = "running"
        cycle = {
            "cycle": cycle_no,
            "mode": mode,
            "startedAt": _now_iso(),
            "endedAt": None,
            "metadata": metadata or {},
            "search": {},
            "send": {},
            "replies": {},
            "replyActions": {},
        }
        self.data.setdefault("history", {}).setdefault("cycles", []).append(cycle)
        self.save()
        return cycle

    def finish_cycle(self, cycle_no: int, summary: Optional[dict[str, Any]]= None) -> dict[str, Any]:
        for cycle in reversed(self.data.setdefault("history", {}).setdefault("cycles", [])):
            if int(cycle.get("cycle") or 0) == int(cycle_no):
                cycle["endedAt"] = _now_iso()
                if summary:
                    cycle["summary"] = summary
                break
        self.data["metrics"]["cyclesCompleted"] = max(int(self.data["metrics"].get("cyclesCompleted") or 0), int(cycle_no))
        self.data["status"] = "idle"
        self.save()
        return self.data

    def update_cycle_section(self, cycle_no: int, section: str, payload: dict[str, Any]) -> None:
        for cycle in reversed(self.data.setdefault("history", {}).setdefault("cycles", [])):
            if int(cycle.get("cycle") or 0) == int(cycle_no):
                cycle[section] = payload
                break
        self.save()

    def set_target_count(self, target_count: int) -> None:
        self.data["targetCount"] = int(target_count)
        self.save()

    def record_contacted(self, blogger_id: str, info: dict[str, Any]) -> None:
        blogger_id = str(blogger_id or "")
        if not blogger_id:
            return
        current = self.data.setdefault("contacted", {}).get(blogger_id, {"bloggerId": blogger_id})
        if not current.get("contactedAt"):
            current["contactedAt"] = _now_iso()
        current["status"] = current.get("status") or "contacted"
        current["lastContact"] = deepcopy(info)
        self.data["contacted"][blogger_id] = current
        self._refresh_metrics()
        self.save()

    def record_reply(self, reply: dict[str, Any], classification: Optional[str]= None) -> None:
        reply_id = str(reply.get("emailId") or reply.get("id") or reply.get("replyId") or "")
        blogger_id = str(reply.get("bloggerId") or "")
        if not reply_id:
            return
        item = deepcopy(reply)
        item["replyId"] = reply_id
        if classification:
            item["classification"] = classification
        item["recordedAt"] = _now_iso()
        self.data.setdefault("replies", {})[reply_id] = item
        if blogger_id:
            contacted = self.data.setdefault("contacted", {}).setdefault(blogger_id, {"bloggerId": blogger_id})
            contacted["lastReply"] = item
            if classification in {"confirmed", "discussing", "rejected"}:
                contacted["status"] = classification
                stamp_key = {"confirmed": "confirmedAt", "rejected": "rejectedAt"}.get(classification, "updatedAt")
                contacted[stamp_key] = _now_iso()
                if classification == "discussing":
                    contacted["lastMessage"] = str(reply.get("content") or reply.get("cleanContent") or reply.get("subject") or "")
        self._refresh_metrics()
        self.save()

    def record_reply_action(self, reply_id: Union[str, int], action: dict[str, Any]) -> None:
        rid = str(reply_id)
        action_item = deepcopy(action)
        action_item["replyId"] = rid
        action_item["recordedAt"] = _now_iso()
        self.data.setdefault("replyActions", {})[rid] = action_item
        self._refresh_metrics()
        self.save()

    # P0-2: 持久化自生成的 reply_model_analysis，供下个周期注入使用
    def save_reply_model_analysis(self, analysis: dict[str, Any], source: str = "rule_based_fallback_self_generated") -> None:
        self.data["replyModelAnalysis"] = deepcopy(analysis)
        self.data["replyModelAnalysisGeneratedAt"] = _now_iso()
        self.data["replyModelAnalysisMeta"] = {
            "source": source,
            "generatedAt": self.data["replyModelAnalysisGeneratedAt"],
            "scope": "campaign",
            "version": 1,
        }
        self.save()

    def get_saved_reply_model_analysis(self) -> Optional[dict[str, Any]]:
        return deepcopy(self.data.get("replyModelAnalysis"))

    def get_saved_reply_model_analysis_meta(self) -> Optional[dict[str, Any]]:
        return deepcopy(self.data.get("replyModelAnalysisMeta"))

    def _refresh_metrics(self) -> None:
        contacted = self.data.get("contacted") or {}
        statuses = [item.get("status") for item in contacted.values()]
        metrics = self.data.setdefault("metrics", {})
        metrics["totalContacted"] = len(contacted)
        metrics["totalReplies"] = len(self.data.get("replies") or {})
        metrics["totalReplyActions"] = len(self.data.get("replyActions") or {})
        metrics["confirmed"] = sum(1 for s in statuses if s == "confirmed")
        metrics["discussing"] = sum(1 for s in statuses if s == "discussing")
        metrics["rejected"] = sum(1 for s in statuses if s == "rejected")
        actions = list((self.data.get("replyActions") or {}).values())
        metrics["autoRepliesSent"] = sum(1 for a in actions if a.get("status") == "sent" and a.get("deliveryMode") == "auto_send")
        metrics["humanReviewRequired"] = sum(1 for a in actions if a.get("reviewRequired") is True)

    def get_contacted_ids(self) -> set[str]:
        return {blogger_id for blogger_id in (self.data.get("contacted") or {}).keys() if blogger_id}

    def get_progress(self) -> dict[str, Any]:
        metrics = self.data.get("metrics") or {}
        target = int(self.data.get("targetCount") or 30)
        confirmed = int(metrics.get("confirmed") or 0)
        return {
            "confirmed": confirmed,
            "target": target,
            "remaining": max(0, target - confirmed),
            "contacted": int(metrics.get("totalContacted") or 0),
            "discussing": int(metrics.get("discussing") or 0),
            "rejected": int(metrics.get("rejected") or 0),
            "cycles": int(metrics.get("cyclesCompleted") or 0),
            "total_invited": int(metrics.get("totalContacted") or 0),
            "totalReplies": int(metrics.get("totalReplies") or 0),
            "humanReviewRequired": int(metrics.get("humanReviewRequired") or 0),
        }

    def is_target_reached(self) -> bool:
        progress = self.get_progress()
        return progress["confirmed"] >= progress["target"]
