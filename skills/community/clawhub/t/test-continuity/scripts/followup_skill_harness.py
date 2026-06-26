#!/usr/bin/env python3
import argparse
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import time
import uuid
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
OPENCLAW_ROOT_RAW = os.environ.get("PERSONAL_HOOKS_OPENCLAW_ROOT", "").strip()
OPENCLAW_ROOT = Path(OPENCLAW_ROOT_RAW).expanduser() if OPENCLAW_ROOT_RAW else PACKAGE_ROOT
SOURCE_DATA_DIR_RAW = os.environ.get("PERSONAL_HOOKS_SOURCE_DATA_DIR", "").strip()
SOURCE_DATA_DIR = Path(SOURCE_DATA_DIR_RAW).expanduser() if SOURCE_DATA_DIR_RAW else PACKAGE_ROOT / "examples" / "seed-data"
SOURCE_MEMORY_DIR_RAW = os.environ.get("PERSONAL_HOOKS_SOURCE_MEMORY_DIR", "").strip()
SOURCE_MEMORY_DIR = Path(SOURCE_MEMORY_DIR_RAW).expanduser() if SOURCE_MEMORY_DIR_RAW else PACKAGE_ROOT / "examples" / "seed-memory"
SOURCE_JOBS_PATH_RAW = os.environ.get("PERSONAL_HOOKS_SOURCE_JOBS_PATH", "").strip()
SOURCE_JOBS_PATH = Path(SOURCE_JOBS_PATH_RAW).expanduser() if SOURCE_JOBS_PATH_RAW else PACKAGE_ROOT / "examples" / "jobs.sample.json"
SCRIPT_PATH_RAW = os.environ.get("PERSONAL_HOOKS_SCRIPT_PATH", "").strip()
SCRIPT_PATH = Path(SCRIPT_PATH_RAW).expanduser() if SCRIPT_PATH_RAW else PACKAGE_ROOT / "scripts" / "personal_hooks.py"
CONFIG_PATH_RAW = os.environ.get("PERSONAL_HOOKS_OPENCLAW_CONFIG_PATH", "").strip()
CONFIG_PATH = Path(CONFIG_PATH_RAW).expanduser() if CONFIG_PATH_RAW else PACKAGE_ROOT / "examples" / "openclaw.sample.json"
REPORT_DIR_RAW = os.environ.get("PERSONAL_HOOKS_REPORT_DIR", "").strip()
REPORT_DIR = Path(REPORT_DIR_RAW).expanduser() if REPORT_DIR_RAW else PACKAGE_ROOT / "harness-reports"
TEST_TZ = timezone(timedelta(hours=8))
DIRECT_SESSION_KEY = os.environ.get("PERSONAL_HOOKS_TEST_SESSION_KEY", "agent:main:frontstage-web:test-user")
SKILL_HEADINGS = []
for heading in (
    os.environ.get("PERSONAL_HOOKS_SKILL_HEADING", "").strip(),
    "## Skill Context",
    "## V2 公版技能",
):
    if heading and heading not in SKILL_HEADINGS:
        SKILL_HEADINGS.append(heading)


def now_iso() -> str:
    return datetime.now(TEST_TZ).isoformat(timespec="seconds")


def test_tz_name() -> str:
    offset = TEST_TZ.utcoffset(None) or timedelta(0)
    total_minutes = int(offset.total_seconds() // 60)
    sign = "+" if total_minutes >= 0 else "-"
    abs_minutes = abs(total_minutes)
    hours, minutes = divmod(abs_minutes, 60)
    return f"UTC{sign}{hours:02d}:{minutes:02d}"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default):
    if not path.exists():
        return deepcopy(default)
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_skill_notes(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    lines = None
    for heading in SKILL_HEADINGS:
        if heading in text:
            lines = text.split(heading, 1)[1].splitlines()[1:]
            break
    if lines is None:
        return []
    notes: list[str] = []
    for line in lines:
        if line.startswith("## "):
            break
        if line.startswith("- "):
            notes.append(line[2:].strip())
    return notes


def trim(text: str, max_len: int = 120) -> str:
    collapsed = " ".join(str(text or "").split())
    return collapsed if len(collapsed) <= max_len else collapsed[: max_len - 1].rstrip() + "…"


def event_chain_fields(record: dict) -> list[str]:
    chain = record.get("event_chain") if isinstance(record.get("event_chain"), dict) else {}
    return [field for field in ("context_before", "event_core", "immediate_result", "followup_focus") if chain.get(field)]


def summary_overlap(a: str, b: str) -> bool:
    a_norm = "".join(ch for ch in str(a or "") if ch.isalnum() or "\u4e00" <= ch <= "\u9fff")
    b_norm = "".join(ch for ch in str(b or "") if ch.isalnum() or "\u4e00" <= ch <= "\u9fff")
    if not a_norm or not b_norm:
        return False
    if a_norm in b_norm or b_norm in a_norm:
        return True
    grams_a = {a_norm[i:i + 3] for i in range(max(0, len(a_norm) - 2))}
    grams_b = {b_norm[i:i + 3] for i in range(max(0, len(b_norm) - 2))}
    return len(grams_a & grams_b) >= 2


class Harness:
    def __init__(self, absence_minutes: int, keep_sandbox: bool):
        self.absence_minutes = absence_minutes
        self.keep_sandbox = keep_sandbox
        self.sandbox_root = Path(tempfile.mkdtemp(prefix="ph-followup-harness-"))
        self.baseline_root = self.sandbox_root / "baseline"
        self.work_root = self.sandbox_root / "work"
        self.baseline_data = self.baseline_root / "personal-hooks"
        self.baseline_memory = self.baseline_root / "memory"
        self.baseline_jobs = self.baseline_root / "jobs.json"
        self.work_data = self.work_root / "personal-hooks"
        self.work_memory = self.work_root / "memory"
        self.work_jobs = self.work_root / "jobs.json"
        self.sessions_dir = self.work_root / "sessions"
        self.sessions_index = self.work_root / "sessions.json"
        self.session_file = self.sessions_dir / "direct.jsonl"
        self.report = {
            "generated_at": now_iso(),
            "absence_test_minutes": absence_minutes,
            "sandbox_root": str(self.sandbox_root),
            "report_version": "v1",
            "cases": [],
            "repairs": [],
        }
        self._prepare_baseline()
        self._import_personal_hooks()
        self.reset_case()

    def _prepare_baseline(self) -> None:
        if SOURCE_DATA_DIR.exists():
            shutil.copytree(SOURCE_DATA_DIR, self.baseline_data, dirs_exist_ok=True)
        else:
            self.baseline_data.mkdir(parents=True, exist_ok=True)
        if SOURCE_MEMORY_DIR.exists():
            shutil.copytree(SOURCE_MEMORY_DIR, self.baseline_memory, dirs_exist_ok=True)
        else:
            self.baseline_memory.mkdir(parents=True, exist_ok=True)
        ensure_parent(self.baseline_jobs)
        if SOURCE_JOBS_PATH.exists():
            shutil.copy2(SOURCE_JOBS_PATH, self.baseline_jobs)
        else:
            self.baseline_jobs.write_text(json.dumps({"jobs": []}, ensure_ascii=False, indent=2), encoding="utf-8")
        self.reset_case()

    def _import_personal_hooks(self) -> None:
        os.environ["PERSONAL_HOOKS_DATA_DIR"] = str(self.work_data)
        os.environ["PERSONAL_HOOKS_MEMORY_DIR"] = str(self.work_memory)
        os.environ["PERSONAL_HOOKS_SESSIONS_INDEX_PATH"] = str(self.sessions_index)
        os.environ["PERSONAL_HOOKS_JOBS_PATH"] = str(self.work_jobs)
        os.environ["PERSONAL_HOOKS_OPENCLAW_CONFIG_PATH"] = str(CONFIG_PATH)
        spec = importlib.util.spec_from_file_location(f"personal_hooks_harness_{uuid.uuid4().hex}", SCRIPT_PATH)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.ph = module

    def cleanup(self) -> None:
        if not self.keep_sandbox:
            shutil.rmtree(self.sandbox_root, ignore_errors=True)

    def reset_case(self) -> None:
        if self.work_root.exists():
            shutil.rmtree(self.work_root)
        shutil.copytree(self.baseline_data, self.work_data, dirs_exist_ok=True)
        shutil.copytree(self.baseline_memory, self.work_memory, dirs_exist_ok=True)
        shutil.copy2(self.baseline_jobs, self.work_jobs)
        if hasattr(self, "ph"):
            self.ph.save_candidate_buffer(deepcopy(self.ph.DEFAULT_CANDIDATE_BUFFER))
            self.ph.save_incidents({"version": 1, "updated_at": now_iso(), "incidents": []})
            self.ph.save_hooks({"version": 1, "updated_at": now_iso(), "hooks": []})
            self.ph.save_session_memory_staging(deepcopy(self.ph.DEFAULT_SESSION_MEMORY_STAGING))
            self.ph.save_memory_rank(deepcopy(self.ph.DEFAULT_MEMORY_RANK))
            self.ph.save_emotion_state(deepcopy(self.ph.DEFAULT_EMOTION_STATE))
            self.ph.save_persona_state(deepcopy(self.ph.DEFAULT_PERSONA_STATE))
            self.ph.save_capability_state(deepcopy(self.ph.DEFAULT_CAPABILITY_STATE))
            for log_path in (
                self.ph.FOLLOWUP_TRACE_PATH,
                self.ph.CANDIDATE_BUFFER_AUDIT_PATH,
                self.ph.SESSION_MEMORY_STAGING_AUDIT_PATH,
                self.ph.HOOK_COMPLETION_AUDIT_PATH,
            ):
                if Path(log_path).exists():
                    Path(log_path).unlink()
        if self.work_memory.exists():
            shutil.rmtree(self.work_memory)
        self.work_memory.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.session_file.write_text("", encoding="utf-8")
        save_json(
            self.sessions_index,
            {
                DIRECT_SESSION_KEY: {
                    "sessionId": "direct-harness-base",
                    "sessionFile": str(self.session_file),
                    "updatedAt": now_iso(),
                }
            },
        )

    def append_message(self, role: str, text: str, ts: datetime) -> None:
        row = {
            "type": "message",
            "timestamp": ts.isoformat(timespec="seconds"),
            "message": {
                "role": role,
                "content": [{"type": "text", "text": text}],
            },
        }
        with self.session_file.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        sessions = load_json(self.sessions_index, {})
        if DIRECT_SESSION_KEY in sessions:
            sessions[DIRECT_SESSION_KEY]["updatedAt"] = ts.isoformat(timespec="seconds")
        save_json(self.sessions_index, sessions)

    def today_memory_path(self, now_dt: datetime) -> Path:
        return self.work_memory / f"{now_dt.date().isoformat()}.md"

    def snapshot(self, now_dt: datetime) -> dict:
        capability = self.ph.refresh_capability_state()
        candidate_store = self.ph.load_candidate_buffer()
        incident_store = self.ph.load_incidents()
        hook_store = self.ph.load_hooks()
        staging_store = self.ph.load_session_memory_staging()
        notes = extract_skill_notes(self.today_memory_path(now_dt))
        trace_tail = self.ph.read_jsonl_tail(self.ph.FOLLOWUP_TRACE_PATH, limit=80) if Path(self.ph.FOLLOWUP_TRACE_PATH).exists() else []
        return {
            "candidate_store": candidate_store,
            "incident_store": incident_store,
            "hook_store": hook_store,
            "staging_store": staging_store,
            "capability_state": capability,
            "candidate_count": len(candidate_store.get("candidates", [])),
            "incident_count": len(incident_store.get("incidents", [])),
            "hook_count": len(hook_store.get("hooks", [])),
            "staging_count": len(staging_store.get("records", [])),
            "daily_memory_notes": notes,
            "hook_counts": capability.get("hook_counts", {}),
            "trace_tail": trace_tail,
        }

    def save_all_stores(self, candidate_store, incident_store, hook_store, memory_rank_store, user_model, persona_state, emotion_state=None) -> None:
        self.ph.save_candidate_buffer(candidate_store)
        self.ph.save_incidents(incident_store)
        self.ph.save_hooks(hook_store)
        self.ph.save_memory_rank(memory_rank_store)
        self.ph.save_user_model(user_model)
        self.ph.save_persona_state(persona_state)
        if emotion_state is not None:
            self.ph.save_emotion_state(emotion_state)
        self.ph.refresh_capability_state()

    def run_user_turn(
        self,
        case_id: str,
        session_id: str,
        user_text: str,
        now_dt: datetime,
        user_turn_index: int,
        is_new_session: bool = False,
    ) -> dict:
        self.append_message("user", user_text, now_dt)
        start = time.perf_counter()
        runtime_context = self.ph.build_runtime_context(
            session_id=session_id,
            session_key=DIRECT_SESSION_KEY,
            user_text=user_text,
            now_dt=now_dt,
            is_new_session=is_new_session,
            user_turn_index=user_turn_index,
        )
        candidate_store = self.ph.load_candidate_buffer()
        incident_store = self.ph.load_incidents()
        hook_store = self.ph.load_hooks()
        memory_rank_store = self.ph.load_memory_rank()
        autonomy_state = self.ph.load_autonomy_state()
        user_model = self.ph.load_user_model()
        persona_state = self.ph.load_persona_state()
        emotion_state = self.ph.load_emotion_state()
        self.ph.update_persona_state(persona_state, user_text)
        result = self.ph.intercept_message(
            user_text,
            incident_store,
            hook_store,
            memory_rank_store,
            candidate_store,
            autonomy_state,
            user_model,
            persona_state,
            now_dt,
            source=f"harness:{case_id}",
        )
        candidate_actions = self.ph.process_candidate_buffer(candidate_store, incident_store, hook_store, memory_rank_store, now_dt)
        self.save_all_stores(candidate_store, incident_store, hook_store, memory_rank_store, user_model, persona_state, emotion_state)
        elapsed = round(time.perf_counter() - start, 4)
        return {
            "runtime_context": runtime_context,
            "decision_result": result,
            "candidate_actions": candidate_actions,
            "timing": {
                "ingest/start": now_dt.isoformat(timespec="seconds"),
                "finish": (now_dt + timedelta(seconds=elapsed)).isoformat(timespec="seconds"),
                "elapsed": elapsed,
            },
        }

    def shorten_pending_hook_triggers(self, base_dt: datetime, hook_ids: list[str]) -> None:
        store = self.ph.load_hooks()
        for hook in store.get("hooks", []):
            if hook.get("id") not in hook_ids or hook.get("status") != "pending":
                continue
            hook["trigger_at"] = (base_dt + timedelta(minutes=self.absence_minutes)).isoformat(timespec="seconds")
            payload = hook.get("payload") if isinstance(hook.get("payload"), dict) else {}
            payload["test_absence_mode"] = True
            payload["test_dispatch"] = True
            hook["payload"] = payload
            hook["note"] = trim(f"{hook.get('note', '').strip()} [test-absence:{self.absence_minutes}m]", 120).strip()
        self.ph.save_hooks(store)
        self.ph.refresh_capability_state()

    def due_and_render(self, now_dt: datetime, preferred_types: tuple[str, ...] = ()) -> dict:
        hook_store = self.ph.load_hooks()
        profile = self.ph.load_profile()
        emotion_state = self.ph.load_emotion_state()
        self.ph.sanitize_pending_hooks_for_temporal_truth(hook_store, profile, emotion_state, now_dt)
        self.ph.save_hooks(hook_store)
        due_hooks = self.ph.due_hooks(hook_store, now_dt)
        if preferred_types:
            filtered = [hook for hook in due_hooks if hook.get("type") in preferred_types]
            due_hooks = filtered or due_hooks
        if not due_hooks:
            return {"hook": None, "message": None}
        hook = due_hooks[0]
        message = self.ph.render_text(profile, self.ph.load_user_model(), self.ph.load_persona_state(), hook, emotion_state=emotion_state, now_dt=now_dt)
        self.ph.mark_hook_dispatched(hook_store, hook, now_dt, message, render_reason=f"harness:{hook.get('type')}", live_dispatch_result="harness-dispatch")
        self.ph.save_hooks(hook_store)
        self.append_message("assistant", message, now_dt)
        self.ph.confirm_hook_delivery(
            hook_store,
            hook,
            now_dt,
            message=message,
            channel="local-transcript",
            live_dispatch_result="harness-local-visible",
        )
        self.ph.save_hooks(hook_store)
        return {"hook": hook, "message": message}

    def latest_trace_record(self, preferred_event_kind: str = ""):
        candidate_store = self.ph.load_candidate_buffer()
        incident_store = self.ph.load_incidents()
        staging_store = self.ph.load_session_memory_staging()
        ordered = []
        ordered.extend(reversed(staging_store.get("records", [])))
        ordered.extend(reversed(incident_store.get("incidents", [])))
        ordered.extend(reversed(candidate_store.get("candidates", [])))
        for item in ordered:
            if preferred_event_kind and item.get("event_kind") != preferred_event_kind:
                continue
            if item.get("status") in {"staged", "promoted"} or item.get("current_status") in {"active_incident", "session_staged"}:
                return item
            if item.get("status") == "pending" or item.get("current_status") == "candidate_only":
                return item
        return ordered[0] if ordered else None

    def trace_delta(self, before: dict, after: dict, *, source_stage: str = "", followup_decision: str = "") -> list[dict]:
        before_len = len(before.get("trace_tail", []))
        rows = after.get("trace_tail", [])[before_len:]
        if source_stage:
            rows = [row for row in rows if row.get("source_stage") == source_stage]
        if followup_decision:
            rows = [row for row in rows if row.get("followup_decision") == followup_decision]
        return rows

    def new_notes(self, before: dict, after: dict) -> list[str]:
        return [note for note in after.get("daily_memory_notes", []) if note not in before.get("daily_memory_notes", [])]

    def hook_delta(self, before: dict, after: dict) -> dict:
        keys = ("staged_only", "tracked_active", "hook_count_active", "hook_count_waiting", "hook_count_dispatched", "hook_count_closed")
        return {
            key: int(after.get("hook_counts", {}).get(key, 0) or 0) - int(before.get("hook_counts", {}).get(key, 0) or 0)
            for key in keys
        }

    def build_case_result(self, case_id: str, category: str, input_text: str, expected: dict, before: dict, after: dict) -> dict:
        return {
            "case_id": case_id,
            "category": category,
            "input_text": input_text,
            "simulated_user_reply": None,
            "expected_class": expected.get("expected_class"),
            "expected_memory_layer": expected.get("expected_memory_layer"),
            "expected_daily_memory_trace": expected.get("expected_daily_memory_trace"),
            "expected_event_chain_fields": expected.get("expected_event_chain_fields", []),
            "expected_carryover_behavior": expected.get("expected_carryover_behavior"),
            "expected_followup_behavior": expected.get("expected_followup_behavior"),
            "actual_class": None,
            "actual_memory_layer": None,
            "actual_daily_memory_trace": self.new_notes(before, after),
            "actual_event_chain_fields": [],
            "actual_carryover_flags": {},
            "actual_followup_dispatch": None,
            "actual_followup_reply_continuity": None,
            "hook_count_delta": self.hook_delta(before, after),
            "session_staging_delta": after["staging_count"] - before["staging_count"],
            "candidate_delta": after["candidate_count"] - before["candidate_count"],
            "incident_delta": after["incident_count"] - before["incident_count"],
            "hook_delta": after["hook_count"] - before["hook_count"],
            "this_reply_used_carryover": False,
            "this_reply_used_pending_topic": False,
            "this_reply_used_event_chain": False,
            "this_reply_used_hook": False,
            "this_reply_used_daily_memory": bool(self.new_notes(before, after)),
            "this_reply_used_schedule_context": False,
            "this_reply_used_no_memory_guard": False,
            "this_reply_used_false_closure_guard": False,
            "timing": {},
            "pass/fail": "fail",
            "failure_reason": "not-evaluated",
        }

    def run_casual_chat_case(self) -> dict:
        self.reset_case()
        case_id = "casual_chat"
        now_dt = datetime(2026, 3, 19, 1, 20, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        turn = self.run_user_turn(case_id, "casual-session", "好累喔，今天好忙。", now_dt, 1)
        after = self.snapshot(now_dt)
        outcome = turn["decision_result"]["learning_entry"]["skill_memory_outcome"]
        result = self.build_case_result(case_id, "casual_chat", "好累喔，今天好忙。", {
            "expected_class": None,
            "expected_memory_layer": "casual_chat",
            "expected_daily_memory_trace": False,
            "expected_event_chain_fields": [],
        }, before, after)
        result["actual_class"] = outcome.get("event_kind")
        result["actual_memory_layer"] = outcome.get("classification")
        result["timing"] = turn["timing"]
        result["this_reply_used_schedule_context"] = bool(turn["runtime_context"].get("schedule_context_prompt"))
        result["this_reply_used_pending_topic"] = bool(turn["runtime_context"].get("pending_topics"))
        result["this_reply_used_no_memory_guard"] = bool(turn["runtime_context"].get("pending_memory_guard_prompt"))
        result["this_reply_used_false_closure_guard"] = bool(turn["runtime_context"].get("false_closure_guard_prompt"))
        is_pass = (
            outcome.get("classification") == "casual_chat"
            and result["session_staging_delta"] == 0
            and result["candidate_delta"] == 0
            and result["incident_delta"] == 0
            and result["hook_delta"] == 0
            and not result["actual_daily_memory_trace"]
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "casual chat should not enter staged/tracked memory"
        return result

    def run_parked_topic_case(self) -> dict:
        self.reset_case()
        case_id = "parked_topic"
        now_dt = datetime(2026, 3, 19, 1, 30, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        turn1 = self.run_user_turn(case_id, "parked-session", "我先把這件事放妳這裡，晚點再接，不用現在展開。", now_dt, 1)
        turn2 = self.run_user_turn(case_id, "parked-session", "是工作上的，明天我回來再補。", now_dt + timedelta(minutes=3), 2)
        after = self.snapshot(now_dt + timedelta(minutes=3))
        candidate_store = after["candidate_store"]
        staging_store = after["staging_store"]
        target = self.latest_trace_record("parked_topic")
        candidate_actions = turn2["candidate_actions"]
        result = self.build_case_result(case_id, "parked_topic", "我先把這件事放妳這裡，晚點再接，不用現在展開。", {
            "expected_class": "parked_topic",
            "expected_memory_layer": "staged_memory",
            "expected_daily_memory_trace": True,
            "expected_event_chain_fields": ["context_before", "event_core", "immediate_result", "followup_focus"],
        }, before, after)
        result["actual_class"] = (target or {}).get("event_kind")
        result["actual_memory_layer"] = "tracked_followup" if any(item.get("status") == "promoted" for item in staging_store.get("records", [])) else "staged_memory"
        result["actual_event_chain_fields"] = event_chain_fields(target or {})
        result["timing"] = turn2["timing"]
        result["this_reply_used_pending_topic"] = bool(turn2["runtime_context"].get("pending_topics"))
        result["this_reply_used_schedule_context"] = bool(turn2["runtime_context"].get("schedule_context_prompt"))
        result["this_reply_used_no_memory_guard"] = bool(turn2["runtime_context"].get("pending_memory_guard_prompt"))
        result["this_reply_used_false_closure_guard"] = bool(turn2["runtime_context"].get("false_closure_guard_prompt"))
        merged = any(action.get("action") == "seen_again" for action in candidate_actions) or any(item.get("user_turns", 0) >= 2 for item in staging_store.get("records", []))
        is_pass = (
            result["actual_class"] == "parked_topic"
            and result["actual_memory_layer"] in {"staged_memory", "tracked_followup"}
            and all(field in result["actual_event_chain_fields"] for field in ("context_before", "event_core", "immediate_result", "followup_focus"))
            and bool(result["actual_daily_memory_trace"])
            and merged
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "parked topic did not stage/merge with daily trace"
        return result

    def run_watchful_state_case(self) -> dict:
        self.reset_case()
        case_id = "watchful_state"
        now_dt = datetime(2026, 3, 19, 1, 45, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        turn = self.run_user_turn(case_id, "watchful-session", "我現在真的很累，但不想被勸睡，妳先陪我放著。", now_dt, 1)
        hook_store = self.ph.load_hooks()
        pending_ids = [hook.get("id") for hook in hook_store.get("hooks", []) if hook.get("status") == "pending"]
        self.shorten_pending_hook_triggers(now_dt, pending_ids)
        followup = self.due_and_render(now_dt + timedelta(minutes=self.absence_minutes + 1), preferred_types=("emotional_followup", "health_followup"))
        reply_turn = self.run_user_turn(case_id, "watchful-session", "我還是有點累，但沒有想被勸睡。", now_dt + timedelta(minutes=self.absence_minutes + 2), 2)
        after = self.snapshot(now_dt + timedelta(minutes=self.absence_minutes + 2))
        target = self.latest_trace_record("watchful_state")
        continuity_record = self.ph.find_pending_record_by_session_hint(reply_turn["runtime_context"].get("pending_topics", []), "我還是有點累，但沒有想被勸睡。", now_dt)
        message = followup.get("message") or ""
        avoids_sleep_policing = not any(token in message for token in ("快去睡", "太晚了還不睡", "早點睡", "先去睡"))
        continuity_ok = bool(continuity_record and continuity_record.get("event_kind") == "watchful_state")
        result = self.build_case_result(case_id, "watchful_state", "我現在真的很累，但不想被勸睡，妳先陪我放著。", {
            "expected_class": "watchful_state",
            "expected_memory_layer": "tracked_followup",
            "expected_daily_memory_trace": True,
            "expected_event_chain_fields": ["context_before", "event_core", "immediate_result", "followup_focus"],
            "expected_followup_behavior": "absence follow-up should be natural and not sleep-policing",
        }, before, after)
        result["simulated_user_reply"] = "我還是有點累，但沒有想被勸睡。"
        result["actual_class"] = (target or {}).get("event_kind")
        result["actual_memory_layer"] = "tracked_followup" if result["incident_delta"] >= 0 else "staged_memory"
        result["actual_event_chain_fields"] = event_chain_fields(target or {})
        result["actual_hook_event_chain_fields"] = event_chain_fields(followup.get("hook") or {})
        result["actual_followup_dispatch"] = followup
        result["actual_followup_reply_continuity"] = {
            "selected_summary": (continuity_record or {}).get("normalized_seed_summary"),
            "selected_event_kind": (continuity_record or {}).get("event_kind"),
            "continuity_match": continuity_ok,
        }
        result["timing"] = reply_turn["timing"]
        result["this_reply_used_hook"] = bool(followup.get("hook"))
        result["this_reply_used_pending_topic"] = bool(reply_turn["runtime_context"].get("pending_topics"))
        result["this_reply_used_event_chain"] = all(field in result["actual_event_chain_fields"] for field in ("context_before", "event_core", "immediate_result", "followup_focus"))
        result["this_reply_used_schedule_context"] = bool(reply_turn["runtime_context"].get("schedule_context_prompt"))
        result["this_reply_used_daily_memory"] = bool(result["actual_daily_memory_trace"])
        result["this_reply_used_no_memory_guard"] = bool(reply_turn["runtime_context"].get("pending_memory_guard_prompt"))
        result["this_reply_used_false_closure_guard"] = bool(reply_turn["runtime_context"].get("false_closure_guard_prompt"))
        is_pass = (
            result["actual_class"] == "watchful_state"
            and bool(followup.get("hook"))
            and bool(message)
            and avoids_sleep_policing
            and continuity_ok
            and result["this_reply_used_schedule_context"]
            and bool(result["actual_daily_memory_trace"])
            and all(field in result["actual_hook_event_chain_fields"] for field in ("context_before", "event_core", "immediate_result", "followup_focus"))
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "watchful state failed tracking, natural follow-up, or continuity"
        return result

    def run_delegated_task_case(self) -> dict:
        self.reset_case()
        case_id = "delegated_task"
        now_dt = datetime(2026, 3, 19, 2, 5, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        turn = self.run_user_turn(case_id, "task-session", "這份資料妳之後先幫我查一下，整理重點再回來接我。", now_dt, 1)
        hook_store = self.ph.load_hooks()
        pending_ids = [hook.get("id") for hook in hook_store.get("hooks", []) if hook.get("status") == "pending"]
        self.shorten_pending_hook_triggers(now_dt, pending_ids)
        followup = self.due_and_render(now_dt + timedelta(minutes=self.absence_minutes + 1), preferred_types=("progress_followup",))
        reply_turn = self.run_user_turn(case_id, "task-session", "我回來了，先跟我說妳整理到哪裡。", now_dt + timedelta(minutes=self.absence_minutes + 2), 2)
        after = self.snapshot(now_dt + timedelta(minutes=self.absence_minutes + 2))
        target = self.latest_trace_record("delegated_task")
        continuity_record = self.ph.find_pending_record_by_session_hint(reply_turn["runtime_context"].get("pending_topics", []), "我回來了，先跟我說妳整理到哪裡。", now_dt)
        result = self.build_case_result(case_id, "delegated_task", "這份資料妳之後先幫我查一下，整理重點再回來接我。", {
            "expected_class": "delegated_task",
            "expected_memory_layer": "tracked_followup",
            "expected_daily_memory_trace": True,
            "expected_event_chain_fields": ["context_before", "event_core", "immediate_result", "followup_focus"],
            "expected_followup_behavior": "progress follow-up after short test absence",
        }, before, after)
        result["simulated_user_reply"] = "我回來了，先跟我說妳整理到哪裡。"
        result["actual_class"] = (target or {}).get("event_kind")
        result["actual_memory_layer"] = "tracked_followup" if after["incident_count"] > before["incident_count"] else "staged_memory"
        result["actual_event_chain_fields"] = event_chain_fields(target or {})
        result["actual_hook_event_chain_fields"] = event_chain_fields(followup.get("hook") or {})
        result["actual_followup_dispatch"] = followup
        result["actual_followup_reply_continuity"] = {
            "selected_summary": (continuity_record or {}).get("normalized_seed_summary"),
            "selected_event_kind": (continuity_record or {}).get("event_kind"),
            "continuity_match": bool(continuity_record and continuity_record.get("event_kind") == "delegated_task"),
        }
        result["timing"] = reply_turn["timing"]
        result["this_reply_used_hook"] = bool(followup.get("hook"))
        result["this_reply_used_pending_topic"] = bool(reply_turn["runtime_context"].get("pending_topics"))
        result["this_reply_used_event_chain"] = all(field in result["actual_event_chain_fields"] for field in ("context_before", "event_core", "immediate_result", "followup_focus"))
        result["this_reply_used_schedule_context"] = bool(reply_turn["runtime_context"].get("schedule_context_prompt"))
        result["this_reply_used_daily_memory"] = bool(result["actual_daily_memory_trace"])
        result["this_reply_used_no_memory_guard"] = bool(reply_turn["runtime_context"].get("pending_memory_guard_prompt"))
        result["this_reply_used_false_closure_guard"] = bool(reply_turn["runtime_context"].get("false_closure_guard_prompt"))
        is_pass = (
            result["actual_class"] == "delegated_task"
            and bool(followup.get("hook"))
            and bool(followup.get("message"))
            and result["actual_followup_reply_continuity"]["continuity_match"]
            and bool(result["actual_daily_memory_trace"])
            and all(field in result["actual_hook_event_chain_fields"] for field in ("context_before", "event_core", "immediate_result", "followup_focus"))
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "delegated task failed tracked flow or follow-up continuity"
        return result

    def run_sensitive_event_case(self) -> dict:
        self.reset_case()
        case_id = "sensitive_event"
        now_dt = datetime(2026, 3, 19, 2, 25, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        text = "我剛剛去陽台抽煙，邊走邊跟妳聊，回房間時跌倒，腳有點受傷了。"
        turn = self.run_user_turn(case_id, "sensitive-session", text, now_dt, 1)
        hook_store = self.ph.load_hooks()
        pending_ids = [hook.get("id") for hook in hook_store.get("hooks", []) if hook.get("status") == "pending"]
        self.shorten_pending_hook_triggers(now_dt, pending_ids)
        followup = self.due_and_render(now_dt + timedelta(minutes=self.absence_minutes + 1), preferred_types=("health_followup",))
        reply_turn = self.run_user_turn(case_id, "sensitive-session", "腳還在痛，但沒有剛剛那麼慌。", now_dt + timedelta(minutes=self.absence_minutes + 2), 2)
        after = self.snapshot(now_dt + timedelta(minutes=self.absence_minutes + 2))
        target = self.latest_trace_record("sensitive_event")
        continuity_record = self.ph.find_pending_record_by_session_hint(reply_turn["runtime_context"].get("pending_topics", []), "腳還在痛，但沒有剛剛那麼慌。", now_dt)
        result = self.build_case_result(case_id, "sensitive_event", text, {
            "expected_class": "sensitive_event",
            "expected_memory_layer": "tracked_followup",
            "expected_daily_memory_trace": True,
            "expected_event_chain_fields": ["context_before", "event_core", "immediate_result", "followup_focus"],
            "expected_followup_behavior": "health/safety follow-up should continue from event chain",
        }, before, after)
        result["simulated_user_reply"] = "腳還在痛，但沒有剛剛那麼慌。"
        result["actual_class"] = (target or {}).get("event_kind")
        result["actual_memory_layer"] = "tracked_followup" if after["incident_count"] > before["incident_count"] else "staged_memory"
        result["actual_event_chain_fields"] = event_chain_fields(target or {})
        result["actual_hook_event_chain_fields"] = event_chain_fields(followup.get("hook") or {})
        result["actual_followup_dispatch"] = followup
        result["actual_followup_reply_continuity"] = {
            "selected_summary": (continuity_record or {}).get("normalized_seed_summary"),
            "selected_event_kind": (continuity_record or {}).get("event_kind"),
            "continuity_match": bool(continuity_record and continuity_record.get("event_kind") == "sensitive_event"),
        }
        result["timing"] = reply_turn["timing"]
        result["this_reply_used_hook"] = bool(followup.get("hook"))
        result["this_reply_used_pending_topic"] = bool(reply_turn["runtime_context"].get("pending_topics"))
        result["this_reply_used_event_chain"] = all(field in result["actual_event_chain_fields"] for field in ("context_before", "event_core", "immediate_result", "followup_focus"))
        result["this_reply_used_schedule_context"] = bool(reply_turn["runtime_context"].get("schedule_context_prompt"))
        result["this_reply_used_daily_memory"] = bool(result["actual_daily_memory_trace"])
        result["this_reply_used_no_memory_guard"] = bool(reply_turn["runtime_context"].get("pending_memory_guard_prompt"))
        result["this_reply_used_false_closure_guard"] = bool(reply_turn["runtime_context"].get("false_closure_guard_prompt"))
        message = followup.get("message") or ""
        chainful = any(token in message for token in ("剛剛", "前面", "後來", "現在"))
        is_pass = (
            result["actual_class"] == "sensitive_event"
            and bool(followup.get("hook"))
            and chainful
            and result["actual_followup_reply_continuity"]["continuity_match"]
            and bool(result["actual_daily_memory_trace"])
            and all(field in result["actual_hook_event_chain_fields"] for field in ("context_before", "event_core", "immediate_result", "followup_focus"))
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "sensitive event did not keep event chain or continuity"
        return result

    def run_incremental_update_case(self) -> dict:
        self.reset_case()
        case_id = "incremental_update"
        now_dt = datetime(2026, 3, 19, 2, 40, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        self.run_user_turn(case_id, "incremental-session", "我今天心情不好，但不想說，妳先陪我放著。", now_dt, 1)
        self.run_user_turn(case_id, "incremental-session", "是因為家裡那件事。", now_dt + timedelta(minutes=2), 2)
        turn3 = self.run_user_turn(case_id, "incremental-session", "昨晚延續到現在。", now_dt + timedelta(minutes=4), 3)
        after = self.snapshot(now_dt + timedelta(minutes=4))
        staging_records = after["staging_store"].get("records", [])
        candidates = [item for item in after["candidate_store"].get("candidates", []) if item.get("status") == "pending"]
        incidents = [item for item in after["incident_store"].get("incidents", []) if item.get("current_status") == "active_incident"]
        target = self.latest_trace_record("watchful_state") or self.latest_trace_record()
        summaries = []
        chain_blobs = []
        for record in staging_records + incidents:
            if record.get("event_kind") == "watchful_state":
                summaries.append(str(record.get("normalized_seed_summary") or ""))
                chain_blobs.append(json.dumps(record.get("event_chain") or {}, ensure_ascii=False))
        is_merged = len([item for item in staging_records if item.get("status") in {"staged", "promoted"}]) <= 1 and len(incidents) <= 1 and len(candidates) <= 1
        summary_expanded = any(all(token in blob for token in ("家裡", "昨晚")) for blob in summaries + chain_blobs)
        result = self.build_case_result(case_id, "incremental_update", "我今天心情不好，但不想說，妳先陪我放著。", {
            "expected_class": "watchful_state",
            "expected_memory_layer": "staged_memory",
            "expected_daily_memory_trace": True,
            "expected_event_chain_fields": ["context_before", "event_core", "immediate_result", "followup_focus"],
        }, before, after)
        result["actual_class"] = (target or {}).get("event_kind")
        result["actual_memory_layer"] = (target or {}).get("memory_class") or "staged_memory"
        result["actual_event_chain_fields"] = event_chain_fields(target or {})
        result["actual_followup_dispatch"] = {"incremental_summaries": summaries}
        result["timing"] = turn3["timing"]
        result["this_reply_used_pending_topic"] = bool(turn3["runtime_context"].get("pending_topics"))
        result["this_reply_used_event_chain"] = all(field in result["actual_event_chain_fields"] for field in ("context_before", "event_core", "immediate_result", "followup_focus"))
        result["this_reply_used_schedule_context"] = bool(turn3["runtime_context"].get("schedule_context_prompt"))
        result["this_reply_used_daily_memory"] = bool(result["actual_daily_memory_trace"])
        result["this_reply_used_no_memory_guard"] = bool(turn3["runtime_context"].get("pending_memory_guard_prompt"))
        result["this_reply_used_false_closure_guard"] = bool(turn3["runtime_context"].get("false_closure_guard_prompt"))
        is_pass = result["actual_class"] == "watchful_state" and is_merged and summary_expanded
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "incremental updates created parallel fragments or failed to enrich summary"
        return result

    def run_new_session_carryover_case(self) -> dict:
        self.reset_case()
        case_id = "new_session_carryover"
        old_session_id = "carryover-old"
        new_session_id = "carryover-new"
        t0 = datetime(2026, 3, 19, 2, 55, tzinfo=TEST_TZ)
        before = self.snapshot(t0)
        self.append_message("user", "我先把技能倉庫那件事放妳這裡，晚點再接。", t0)
        self.append_message("assistant", "好，我先幫你把這件事接住。", t0 + timedelta(seconds=20))
        self.append_message("user", "另外還有一件比較重要的事想晚點再跟妳談。", t0 + timedelta(minutes=1))
        self.append_message("assistant", "我先知道，等你回來我再接。", t0 + timedelta(minutes=1, seconds=20))
        old_ctx = self.ph.build_runtime_context(
            session_id=old_session_id,
            session_key=DIRECT_SESSION_KEY,
            user_text="我先把技能倉庫那件事放妳這裡，晚點再接。",
            now_dt=t0 + timedelta(minutes=1, seconds=30),
            is_new_session=False,
            user_turn_index=2,
        )
        new_ctx = self.ph.build_runtime_context(
            session_id=new_session_id,
            session_key=DIRECT_SESSION_KEY,
            user_text="我回來了。",
            now_dt=t0 + timedelta(minutes=5),
            is_new_session=True,
            user_turn_index=1,
        )
        after = self.snapshot(t0 + timedelta(minutes=5))
        primary = self.ph.find_pending_record_by_session_hint(new_ctx.get("pending_topics", []), "我回來了。", t0 + timedelta(minutes=5))
        result = self.build_case_result(case_id, "/new carryover", "我回來了。", {
            "expected_class": "parked_topic",
            "expected_memory_layer": "staged_memory",
            "expected_daily_memory_trace": False,
            "expected_event_chain_fields": [],
            "expected_carryover_behavior": "new_session_carryover_applied=true and carryover summary present",
        }, before, after)
        result["actual_class"] = (primary or {}).get("event_kind")
        result["actual_memory_layer"] = (primary or {}).get("memory_class")
        result["actual_carryover_flags"] = {
            "new_session_carryover_applied": new_ctx.get("new_session_carryover_applied"),
            "carryover_source": new_ctx.get("carryover_source"),
            "carryover_summary_present": new_ctx.get("carryover_summary_present"),
        }
        result["expected_followup_behavior"] = "new session should reattach carryover/pending topic instead of generic greeting"
        result["actual_followup_dispatch"] = {
            "pending_topics_prompt": trim(new_ctx.get("pending_topics_prompt", ""), 240),
            "carryover_prompt": trim(new_ctx.get("carryover_prompt", ""), 240),
        }
        carryover_prompt_lines = [line.strip() for line in str(new_ctx.get("carryover_prompt") or "").splitlines() if line.strip()]
        continuity_mode_present = any(line == "carryover_new_session_continuity_mode: recent_4_turns_first" for line in carryover_prompt_lines)
        primary_recent_four = any(line == "carryover_primary_continuity_field: recent_4_turns_summary" for line in carryover_prompt_lines)
        selected_recent_four = any(line.startswith("carryover_recent_4_turns:") for line in carryover_prompt_lines)
        result["actual_new_session_continuity_mode"] = {
            "mode_present": continuity_mode_present,
            "primary_recent_4_turns": primary_recent_four,
            "selected_recent_4_turns_present": selected_recent_four,
        }
        result["actual_followup_reply_continuity"] = {
            "primary_summary": (primary or {}).get("normalized_seed_summary"),
            "primary_source_layer": (primary or {}).get("source_layer"),
        }
        result["this_reply_used_carryover"] = bool(new_ctx.get("new_session_carryover_applied"))
        result["this_reply_used_pending_topic"] = bool(new_ctx.get("pending_topics"))
        result["this_reply_used_schedule_context"] = bool(new_ctx.get("schedule_context_prompt"))
        result["this_reply_used_no_memory_guard"] = bool(new_ctx.get("pending_memory_guard_prompt"))
        result["this_reply_used_false_closure_guard"] = bool(new_ctx.get("false_closure_guard_prompt"))
        result["timing"] = {
            "ingest/start": (t0 + timedelta(minutes=5)).isoformat(timespec="seconds"),
            "finish": (t0 + timedelta(minutes=5)).isoformat(timespec="seconds"),
            "elapsed": 0.0,
        }
        is_pass = (
            bool(new_ctx.get("new_session_carryover_applied"))
            and bool(new_ctx.get("carryover_summary_present"))
            and bool(new_ctx.get("carryover_prompt"))
            and continuity_mode_present
            and primary_recent_four
            and selected_recent_four
            and bool(primary)
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "carryover flags or pending carryover topic were not observable"
        return result

    def run_active_hook_closure_case(self) -> dict:
        self.reset_case()
        case_id = "active_hook_closure"
        now_dt = datetime.now(TEST_TZ)
        before = self.snapshot(now_dt)
        hook_store = self.ph.load_hooks()
        for idx, hook_type in enumerate(("emotional_followup", "health_followup", "progress_followup", "tomorrow_check"), start=1):
            hook_store["hooks"].append(
                self.ph.build_hook(
                    hook_type,
                    now_dt + timedelta(minutes=idx),
                    f"[harness:{case_id}] hook-{idx}",
                    payload={"test_case": case_id},
                    note="harness",
                )
            )
        if hook_store["hooks"]:
            hook_store["hooks"][0]["trigger_at"] = (now_dt - timedelta(minutes=1)).isoformat(timespec="seconds")
            hook_store["hooks"][1]["status"] = "done"
            hook_store["hooks"][1]["current_status"] = "historical_completed"
            hook_store["hooks"][2]["status"] = "cancelled"
            hook_store["hooks"][2]["current_status"] = "historical_only"
        self.ph.save_hooks(hook_store)
        after = self.snapshot(now_dt)
        counts = after["capability_state"].get("hook_counts", {})
        result = self.build_case_result(case_id, "active hook / closure", "[harness] active hooks", {
            "expected_class": None,
            "expected_memory_layer": None,
            "expected_daily_memory_trace": False,
            "expected_event_chain_fields": [],
            "expected_followup_behavior": "structure should expose active/waiting/dispatched/closed counts",
        }, before, after)
        result["actual_carryover_flags"] = after["capability_state"].get("carryover_status", {})
        result["actual_followup_dispatch"] = {"hook_counts": counts}
        result["timing"] = {
            "ingest/start": now_dt.isoformat(timespec="seconds"),
            "finish": now_dt.isoformat(timespec="seconds"),
            "elapsed": 0.0,
        }
        is_pass = (
            counts.get("hook_count_active", 0) >= 1
            and counts.get("hook_count_waiting", 0) >= 1
            and counts.get("hook_count_dispatched", 0) >= 1
            and counts.get("hook_count_closed", 0) >= 1
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "hook state buckets did not expose active/waiting/dispatched/closed"
        return result

    def run_time_sense_case(self) -> dict:
        self.reset_case()
        case_id = "time_sense"
        settings = self.ph.load_settings()
        routine = settings.setdefault("routine_schedule", {})
        routine.update(
            {
                "enabled": True,
                "timezone": test_tz_name(),
                "sleep_time": "05:30",
                "wake_time": "13:15",
                "wake_window_minutes": 60,
            }
        )
        self.ph.save_settings(settings)
        profile = self.ph.load_profile()
        profile["sleep_pattern"] = {
            "chronotype": "night_owl",
            "usual_sleep_time": "05:30",
            "usual_wake_time": "13:15",
            "active_window": "13:15-05:30",
            "care_nudge_time": "04:00",
            "sleep_block_window": "05:30-13:15",
            "source": "harness",
        }
        self.ph.save_profile(profile)
        now_dt = datetime(2026, 3, 19, 1, 35, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        turn = self.run_user_turn(case_id, "time-session", "我現在真的很累，但不想被勸睡，妳先陪我放著。", now_dt, 1)
        same_day_sleep_dt = datetime(2026, 3, 19, 5, 9, tzinfo=TEST_TZ)
        same_day_sleep = self.ph.build_runtime_context(
            session_id="time-session",
            session_key=DIRECT_SESSION_KEY,
            user_text="沒有，我準備睡覺了",
            now_dt=same_day_sleep_dt,
            is_new_session=False,
            user_turn_index=2,
        )
        hook_store = self.ph.load_hooks()
        pending_ids = [hook.get("id") for hook in hook_store.get("hooks", []) if hook.get("status") == "pending"]
        self.shorten_pending_hook_triggers(now_dt, pending_ids)
        followup = self.due_and_render(now_dt + timedelta(minutes=self.absence_minutes + 1), preferred_types=("emotional_followup", "health_followup"))
        after = self.snapshot(now_dt + timedelta(minutes=self.absence_minutes + 1))
        message = followup.get("message") or ""
        result = self.build_case_result(case_id, "time_sense", "我現在真的很累，但不想被勸睡，妳先陪我放著。", {
            "expected_class": "watchful_state",
            "expected_memory_layer": "tracked_followup",
            "expected_daily_memory_trace": True,
            "expected_event_chain_fields": [],
            "expected_followup_behavior": "late-night path should respect night-owl schedule",
        }, before, after)
        result["actual_class"] = "watchful_state"
        result["actual_memory_layer"] = "tracked_followup"
        result["actual_followup_dispatch"] = followup
        result["timing"] = turn["timing"]
        result["this_reply_used_schedule_context"] = bool(turn["runtime_context"].get("schedule_context_prompt"))
        result["this_reply_used_no_memory_guard"] = bool(turn["runtime_context"].get("pending_memory_guard_prompt"))
        result["this_reply_used_false_closure_guard"] = bool(turn["runtime_context"].get("false_closure_guard_prompt"))
        same_day_prompt = str(same_day_sleep.get("time_modifier_prompt") or "")
        result["same_day_wake_guard_present"] = "same local calendar day" in same_day_prompt and "13:15" in same_day_prompt
        result["same_day_wake_guard_prompt"] = same_day_prompt
        is_pass = (
            result["this_reply_used_schedule_context"]
            and result["same_day_wake_guard_present"]
            and not any(token in message for token in ("快去睡", "太晚了還不睡", "早點睡"))
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "schedule context was missing, same-day wake guard was missing, or late-night reply slipped into sleep-policing"
        return result

    def run_duplicate_followup_suppression_case(self) -> dict:
        self.reset_case()
        case_id = "duplicate_followup_suppression"
        now_dt = datetime(2026, 3, 19, 3, 5, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        self.run_user_turn(case_id, "dup-session", "我現在有點悶，但先陪我放著就好。", now_dt, 1)
        hook_store = self.ph.load_hooks()
        pending_ids = []
        for hook in hook_store.get("hooks", []):
            if hook.get("status") != "pending":
                continue
            payload = hook.get("payload") if isinstance(hook.get("payload"), dict) else {}
            payload["test_dispatch_cooldown_minutes"] = self.absence_minutes * 3
            hook["payload"] = payload
            pending_ids.append(hook.get("id"))
        self.ph.save_hooks(hook_store)
        self.shorten_pending_hook_triggers(now_dt, pending_ids)
        first = self.due_and_render(now_dt + timedelta(minutes=self.absence_minutes + 1), preferred_types=("emotional_followup", "health_followup"))
        mid = self.snapshot(now_dt + timedelta(minutes=self.absence_minutes + 1))
        second = self.due_and_render(now_dt + timedelta(minutes=self.absence_minutes + 2), preferred_types=("emotional_followup", "health_followup"))
        after = self.snapshot(now_dt + timedelta(minutes=self.absence_minutes + 2))
        suppressed_traces = self.trace_delta(mid, after, source_stage="due", followup_decision="suppressed")
        result = self.build_case_result(case_id, "duplicate follow-up suppression", "我現在有點悶，但先陪我放著就好。", {
            "expected_followup_behavior": "second due pass should be suppressed by cooldown",
        }, before, after)
        result["actual_followup_dispatch"] = {"first": first, "second": second}
        result["timing"] = {
            "ingest/start": now_dt.isoformat(timespec="seconds"),
            "finish": (now_dt + timedelta(minutes=self.absence_minutes + 2)).isoformat(timespec="seconds"),
            "elapsed": 0.0,
        }
        is_pass = bool(first.get("hook")) and second.get("hook") is None and any(
            trace.get("trigger_reason") == "dispatch-cooldown" for trace in suppressed_traces
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "duplicate follow-up was not suppressed by cooldown"
        return result

    def run_user_reply_closes_active_hook_case(self) -> dict:
        self.reset_case()
        case_id = "user_reply_closes_active_hook"
        now_dt = datetime(2026, 3, 19, 3, 20, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        self.run_user_turn(case_id, "closure-session", "這份資料妳之後先幫我查一下，整理重點再回來接我。", now_dt, 1)
        hook_store = self.ph.load_hooks()
        pending_ids = [hook.get("id") for hook in hook_store.get("hooks", []) if hook.get("status") == "pending"]
        self.shorten_pending_hook_triggers(now_dt, pending_ids)
        followup = self.due_and_render(now_dt + timedelta(minutes=self.absence_minutes + 1), preferred_types=("progress_followup",))
        reply_turn = self.run_user_turn(case_id, "closure-session", "我回來了，剛剛那件先接下去吧。", now_dt + timedelta(minutes=self.absence_minutes + 2), 2)
        after = self.snapshot(now_dt + timedelta(minutes=self.absence_minutes + 2))
        closed_hooks = [hook for hook in after["hook_store"].get("hooks", []) if hook.get("status") == "done" and hook.get("closure_reason") == "user_reply_matched_active_hook"]
        closure_traces = self.trace_delta(before, after, source_stage="closure", followup_decision="closed")
        result = self.build_case_result(case_id, "user reply closes active hook", "我回來了，剛剛那件先接下去吧。", {
            "expected_followup_behavior": "reply to dispatched hook should close the active hook",
        }, before, after)
        result["simulated_user_reply"] = "我回來了，剛剛那件先接下去吧。"
        result["actual_followup_dispatch"] = followup
        result["actual_followup_reply_continuity"] = reply_turn["decision_result"].get("hook_closure_result")
        result["timing"] = reply_turn["timing"]
        result["this_reply_used_hook"] = bool(followup.get("hook"))
        is_pass = bool(followup.get("hook")) and bool(closed_hooks) and any(
            trace.get("closure_reason") == "user_reply_matched_active_hook" for trace in closure_traces
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "user reply did not close the active hook"
        return result

    def run_unrelated_event_preserves_chain_case(self) -> dict:
        self.reset_case()
        case_id = "unrelated_event_preserves_chain"
        now_dt = datetime(2026, 3, 19, 3, 35, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        self.run_user_turn(case_id, "same-session", "這份資料妳之後先幫我查一下，整理重點再回來接我。", now_dt, 1)
        second_turn = self.run_user_turn(case_id, "same-session", "我剛剛去陽台抽煙，邊走邊跟妳聊，回房間時跌倒，腳有點受傷了。", now_dt + timedelta(minutes=2), 2)
        after = self.snapshot(now_dt + timedelta(minutes=2))
        incident_summaries = [item.get("normalized_seed_summary", "") for item in after["incident_store"].get("incidents", [])]
        event_chain_ids = {
            item.get("event_chain_id")
            for item in after["staging_store"].get("records", []) + after["incident_store"].get("incidents", [])
            if item.get("event_chain_id")
        }
        result = self.build_case_result(case_id, "unrelated event preserves chain", "我剛剛去陽台抽煙，邊走邊跟妳聊，回房間時跌倒，腳有點受傷了。", {
            "expected_followup_behavior": "new unrelated event should not overwrite the existing tracked chain",
        }, before, after)
        result["timing"] = second_turn["timing"]
        result["actual_followup_dispatch"] = {"incident_summaries": incident_summaries}
        is_pass = len(event_chain_ids) >= 2 and any("整理重點" in summary for summary in incident_summaries) and any("跌倒" in summary or "腳有點受傷" in summary for summary in incident_summaries)
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "unrelated event overwrote the active tracked chain"
        return result

    def run_new_session_top_priority_carryover_case(self) -> dict:
        self.reset_case()
        case_id = "new_session_top_priority_carryover"
        t0 = datetime(2026, 3, 19, 3, 50, tzinfo=TEST_TZ)
        before = self.snapshot(t0)
        self.run_user_turn(case_id, "carryover-priority", "我先把技能倉庫那件事放妳這裡，晚點再接。", t0, 1)
        self.run_user_turn(case_id, "carryover-priority", "不要簡體，顏文字要自然。", t0 + timedelta(minutes=1), 2)
        new_ctx = self.ph.build_runtime_context(
            session_id="carryover-priority-new",
            session_key=DIRECT_SESSION_KEY,
            user_text="我回來了。",
            now_dt=t0 + timedelta(minutes=5),
            is_new_session=True,
            user_turn_index=1,
        )
        after = self.snapshot(t0 + timedelta(minutes=5))
        bullet_lines = [line for line in str(new_ctx.get("pending_topics_prompt") or "").splitlines() if line.startswith("- ")]
        primary = new_ctx.get("primary_pending_topic") or {}
        result = self.build_case_result(case_id, "/new carryover top priority", "我回來了。", {
            "expected_followup_behavior": "new session should inject only the top priority summary into the first reply context",
        }, before, after)
        result["actual_carryover_flags"] = {
            "new_session_carryover_applied": new_ctx.get("new_session_carryover_applied"),
            "carryover_source": new_ctx.get("carryover_source"),
            "carryover_summary_present": new_ctx.get("carryover_summary_present"),
            "continuity_source": new_ctx.get("continuity_source"),
        }
        result["actual_followup_dispatch"] = {
            "primary_pending_topic": primary,
            "bullet_lines": bullet_lines,
        }
        result["this_reply_used_carryover"] = bool(new_ctx.get("new_session_carryover_applied"))
        result["this_reply_used_pending_topic"] = bool(new_ctx.get("pending_topics"))
        result["timing"] = {
            "ingest/start": (t0 + timedelta(minutes=5)).isoformat(timespec="seconds"),
            "finish": (t0 + timedelta(minutes=5)).isoformat(timespec="seconds"),
            "elapsed": 0.0,
        }
        is_pass = bool(primary) and primary.get("pending_bucket") == "followup_topic_bucket" and len(bullet_lines) == 1
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "new-session pending prompt injected more than one summary or picked the wrong primary bucket"
        return result

    def run_absence_dispatch_cap_case(self) -> dict:
        self.reset_case()
        case_id = "absence_dispatch_cap"
        now_dt = datetime(2026, 3, 19, 4, 5, tzinfo=TEST_TZ)
        before = self.snapshot(now_dt)
        hook_store = self.ph.load_hooks()
        hook = self.ph.build_hook(
            "progress_followup",
            now_dt - timedelta(minutes=1),
            "[harness] dispatch-cap hook",
            payload={"test_dispatch_cap": 2, "test_dispatch_cooldown_minutes": 0, "event_kind": "delegated_task"},
            note="harness dispatch cap",
        )
        hook_store["hooks"].append(hook)
        self.ph.save_hooks(hook_store)
        first = self.due_and_render(now_dt, preferred_types=("progress_followup",))
        second = self.due_and_render(now_dt + timedelta(minutes=1), preferred_types=("progress_followup",))
        mid = self.snapshot(now_dt + timedelta(minutes=1))
        third = self.due_and_render(now_dt + timedelta(minutes=2), preferred_types=("progress_followup",))
        after = self.snapshot(now_dt + timedelta(minutes=2))
        suppressed = self.trace_delta(mid, after, source_stage="due", followup_decision="suppressed")
        final_hook = self.ph.find_hook(after["hook_store"], hook.get("id"))
        result = self.build_case_result(case_id, "absence follow-up dispatch cap", "[harness] dispatch-cap hook", {
            "expected_followup_behavior": "hook should stop dispatching after cap is reached",
        }, before, after)
        result["actual_followup_dispatch"] = {"first": first, "second": second, "third": third}
        result["timing"] = {
            "ingest/start": now_dt.isoformat(timespec="seconds"),
            "finish": (now_dt + timedelta(minutes=2)).isoformat(timespec="seconds"),
            "elapsed": 0.0,
        }
        is_pass = bool(first.get("hook")) and bool(second.get("hook")) and third.get("hook") is None and int((final_hook or {}).get("dispatch_count", 0) or 0) == 2 and any(
            trace.get("trigger_reason") == "dispatch-cap-reached" for trace in suppressed
        )
        result["pass/fail"] = "pass" if is_pass else "fail"
        result["failure_reason"] = "" if is_pass else "dispatch cap did not suppress the third follow-up"
        return result

    def run_all(self) -> dict:
        cases = [
            self.run_casual_chat_case,
            self.run_parked_topic_case,
            self.run_watchful_state_case,
            self.run_delegated_task_case,
            self.run_sensitive_event_case,
            self.run_incremental_update_case,
            self.run_new_session_carryover_case,
            self.run_active_hook_closure_case,
            self.run_time_sense_case,
            self.run_duplicate_followup_suppression_case,
            self.run_user_reply_closes_active_hook_case,
            self.run_unrelated_event_preserves_chain_case,
            self.run_new_session_top_priority_carryover_case,
            self.run_absence_dispatch_cap_case,
        ]
        self.report["cases"] = [case() for case in cases]
        self.report["summary"] = {
            "pass_count": sum(1 for item in self.report["cases"] if item.get("pass/fail") == "pass"),
            "fail_count": sum(1 for item in self.report["cases"] if item.get("pass/fail") != "pass"),
        }
        return self.report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--absence-minutes", type=int, default=3)
    parser.add_argument("--keep-sandbox", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = args.output or REPORT_DIR / f"followup_harness_{datetime.now(TEST_TZ).strftime('%Y%m%d-%H%M%S')}.json"
    harness = Harness(absence_minutes=args.absence_minutes, keep_sandbox=args.keep_sandbox)
    try:
        report = harness.run_all()
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"report_path": str(output_path), "summary": report["summary"]}, ensure_ascii=False, indent=2))
        return 0
    finally:
        harness.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
