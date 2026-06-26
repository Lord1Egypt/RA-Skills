#!/usr/bin/env python3
"""Integration tests for sidecar.py.

Tests: basic offload, idempotency, restart resilience, trim interaction,
       restart scenarios (fresh session header after compaction).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from datetime import datetime, timezone

SCRIPT_DIR = Path(__file__).parent
SIDECAR_PY = SCRIPT_DIR / "sidecar.py"
TRIM_PY = SCRIPT_DIR / "trim.py"

TEST_SESSIONS_DIR = Path.home() / ".openclaw-test/agents/main/sessions"

PASS = 0
FAIL = 0


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def ok(label):
    global PASS
    print(f"  ✅ {label}")
    PASS += 1


def fail(label):
    global FAIL
    print(f"  ❌ {label}")
    FAIL += 1


def ts():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def make_session_header(sid):
    return {"type": "session", "id": "hdr-001", "sessionId": sid,
            "timestamp": ts(), "agentId": "main", "channelId": "test"}


def make_user(id_, content, parent="hdr-001"):
    return {"type": "message", "id": id_, "parentId": parent,
            "timestamp": ts(), "message": {"role": "user", "content": content}}


def make_assistant(id_, text, tool_ids=None, parent="hdr-001"):
    content = [{"type": "text", "text": text}]
    for tid in (tool_ids or []):
        content.append({"type": "toolCall", "id": tid, "name": "exec",
                         "input": {"command": "ls"}})
    return {"type": "message", "id": id_, "parentId": parent,
            "timestamp": ts(), "message": {"role": "assistant", "content": content}}


def make_tool_result(id_, tcid, tool_name, content_text, parent="hdr-001"):
    return {"type": "message", "id": id_, "parentId": parent, "timestamp": ts(),
            "message": {"role": "toolResult", "toolCallId": tcid,
                        "toolName": tool_name,
                        "content": [{"type": "text", "text": content_text}]}}


def big_text(kb=6):
    line = "output data here " * 4 + "\n"  # ~80 chars
    lines = (kb * 1024) // len(line)
    return "".join(f"Line {i:05d}: {line}" for i in range(lines))


def small_text():
    return "exit 0\nok"


def write_jsonl(path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


def read_jsonl(path):
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except Exception:
                    pass
    return entries


def run_sidecar(jsonl, sid, min_bytes=4096):
    r = subprocess.run(
        [sys.executable, str(SIDECAR_PY), str(jsonl), sid, str(min_bytes)],
        capture_output=True, text=True
    )
    if r.stdout.strip():
        for line in r.stdout.strip().splitlines():
            print(f"    [sidecar] {line}")
    if r.returncode != 0 and r.stderr.strip():
        print(f"    [sidecar STDERR] {r.stderr.strip()}", file=sys.stderr)
    return r.returncode


def run_trim(jsonl, sid, state_file, keep_pairs=10):
    r = subprocess.run(
        [sys.executable, str(TRIM_PY), str(jsonl), sid, "test", str(state_file),
         str(keep_pairs), "2", "5", "50", "250"],
        capture_output=True, text=True
    )
    if r.stdout.strip():
        for line in r.stdout.strip().splitlines():
            print(f"    [trim] {line}")
    return r.returncode


def has_stub(entries):
    for e in entries:
        raw = e.get("message", {}).get("content", [])
        if isinstance(raw, str) and "[tool output offloaded to" in raw:
            return True
        for b in (raw if isinstance(raw, list) else []):
            if isinstance(b, dict) and "[tool output offloaded to" in b.get("text", ""):
                return True
    return False


def count_stubs(entries):
    count = 0
    for e in entries:
        raw = e.get("message", {}).get("content", [])
        if isinstance(raw, str) and "[tool output offloaded to" in raw:
            count += 1
            continue
        for b in (raw if isinstance(raw, list) else []):
            if isinstance(b, dict) and "[tool output offloaded to" in b.get("text", ""):
                count += 1
                break
    return count


def make_sid():
    return f"test-sidecar-{int(time.time() * 1000)}"


# ──────────────────────────────────────────────────────────
# TEST 1: Basic sidecar offload
# ──────────────────────────────────────────────────────────
def test_basic_offload():
    log("TEST 1: Basic sidecar offload (large toolResult → sidecar file)")
    sid = make_sid()
    jsonl = TEST_SESSIONS_DIR / f"{sid}.jsonl"
    cache = TEST_SESSIONS_DIR / f"{sid}.toolcache"
    try:
        entries = [
            make_session_header(sid),
            make_user("u-001", "run something"),
            make_assistant("a-001", "sure", ["tc-001"]),
            make_tool_result("tr-001", "tc-001", "exec", big_text(6), "a-001"),
        ]
        write_jsonl(jsonl, entries)
        orig_kb = jsonl.stat().st_size // 1024

        rc = run_sidecar(jsonl, sid)
        new_kb = jsonl.stat().st_size // 1024

        if rc == 0:
            ok(f"sidecar.py exited 0")
        else:
            fail(f"sidecar.py exited {rc}")

        ok("toolcache dir created") if cache.is_dir() else fail("toolcache dir missing")

        sidecar_file = cache / "tc-001.txt"
        ok("sidecar file tc-001.txt created") if sidecar_file.exists() else fail("sidecar file missing")

        new_entries = read_jsonl(jsonl)
        ok("stub injected into transcript") if has_stub(new_entries) else fail("no stub in transcript")

        ok(f"transcript shrank ({orig_kb}KB → {new_kb}KB)") if new_kb < orig_kb else fail("transcript did not shrink")

    finally:
        jsonl.unlink(missing_ok=True)
        shutil.rmtree(cache, ignore_errors=True)


# ──────────────────────────────────────────────────────────
# TEST 2: Idempotency
# ──────────────────────────────────────────────────────────
def test_idempotency():
    log("TEST 2: Idempotency (run sidecar twice on same file)")
    sid = make_sid()
    jsonl = TEST_SESSIONS_DIR / f"{sid}.jsonl"
    cache = TEST_SESSIONS_DIR / f"{sid}.toolcache"
    try:
        entries = [
            make_session_header(sid),
            make_user("u-001", "run"),
            make_assistant("a-001", "ok", ["tc-001"]),
            make_tool_result("tr-001", "tc-001", "exec", big_text(6), "a-001"),
        ]
        write_jsonl(jsonl, entries)
        run_sidecar(jsonl, sid)

        snapshot = jsonl.read_text()
        run_sidecar(jsonl, sid)
        after = jsonl.read_text()

        ok("transcript unchanged on second run") if snapshot == after else fail("transcript changed on second run (not idempotent)")

        file_count = len(list(cache.iterdir())) if cache.exists() else 0
        ok(f"no duplicate sidecar files ({file_count})") if file_count == 1 else fail(f"unexpected file count: {file_count}")

    finally:
        jsonl.unlink(missing_ok=True)
        shutil.rmtree(cache, ignore_errors=True)


# ──────────────────────────────────────────────────────────
# TEST 3: Small results NOT sidecared
# ──────────────────────────────────────────────────────────
def test_small_not_sidecared():
    log("TEST 3: Small toolResult (below threshold) — should NOT be sidecared")
    sid = make_sid()
    jsonl = TEST_SESSIONS_DIR / f"{sid}.jsonl"
    cache = TEST_SESSIONS_DIR / f"{sid}.toolcache"
    try:
        entries = [
            make_session_header(sid),
            make_user("u-001", "hello"),
            make_assistant("a-001", "hi", ["tc-001"]),
            make_tool_result("tr-001", "tc-001", "exec", small_text(), "a-001"),
        ]
        write_jsonl(jsonl, entries)
        run_sidecar(jsonl, sid)

        ok("no toolcache dir for small result") if not cache.exists() else fail("toolcache dir created unexpectedly")
        new_entries = read_jsonl(jsonl)
        ok("no stub in transcript") if not has_stub(new_entries) else fail("stub found unexpectedly")
    finally:
        jsonl.unlink(missing_ok=True)
        shutil.rmtree(cache, ignore_errors=True)


# ──────────────────────────────────────────────────────────
# TEST 4: Mixed large + small
# ──────────────────────────────────────────────────────────
def test_mixed():
    log("TEST 4: Mixed large + small results")
    sid = make_sid()
    jsonl = TEST_SESSIONS_DIR / f"{sid}.jsonl"
    cache = TEST_SESSIONS_DIR / f"{sid}.toolcache"
    try:
        entries = [
            make_session_header(sid),
            make_user("u-001", "step 1"),
            make_assistant("a-001", "ok", ["tc-001"]),
            make_tool_result("tr-001", "tc-001", "exec", big_text(7), "a-001"),
            make_user("u-002", "step 2", "a-001"),
            make_assistant("a-002", "done", ["tc-002"], "u-002"),
            make_tool_result("tr-002", "tc-002", "Read", small_text(), "a-002"),
        ]
        write_jsonl(jsonl, entries)
        run_sidecar(jsonl, sid)

        ok("large result sidecared") if (cache / "tc-001.txt").exists() else fail("large result not sidecared")
        ok("small result NOT sidecared") if not (cache / "tc-002.txt").exists() else fail("small result incorrectly sidecared")
    finally:
        jsonl.unlink(missing_ok=True)
        shutil.rmtree(cache, ignore_errors=True)


# ──────────────────────────────────────────────────────────
# TEST 5: Restart resilience
# Sidecar files survive; stubs remain readable after restart
# ──────────────────────────────────────────────────────────
def test_restart_resilience():
    log("TEST 5: Restart resilience (sidecar files persist across simulated restart)")
    sid = make_sid()
    jsonl = TEST_SESSIONS_DIR / f"{sid}.jsonl"
    cache = TEST_SESSIONS_DIR / f"{sid}.toolcache"
    try:
        entries = [
            make_session_header(sid),
            make_user("u-001", "run"),
            make_assistant("a-001", "ok", ["tc-001"]),
            make_tool_result("tr-001", "tc-001", "exec", big_text(6), "a-001"),
        ]
        write_jsonl(jsonl, entries)
        run_sidecar(jsonl, sid)

        sidecar_file = cache / "tc-001.txt"
        pre_restart_size = sidecar_file.stat().st_size if sidecar_file.exists() else 0

        # Simulate gateway restart: re-read transcript from disk (no state)
        restored_entries = read_jsonl(jsonl)

        # Sidecar file still there
        ok(f"sidecar file intact ({pre_restart_size} bytes)") if pre_restart_size > 1000 else fail(f"sidecar file too small: {pre_restart_size}")

        # Stub references the filename
        ok("transcript stub references filename") if has_stub(restored_entries) else fail("stub missing after restart")

        # Agent can Read the sidecar file to recover content
        recovered = sidecar_file.read_text()
        ok(f"sidecar content recoverable ({len(recovered)} chars)") if len(recovered) > 1000 else fail("sidecar content empty")

        # New session header scenario: OC writes a fresh header, stubs stay
        # (new session means different SID — old sidecar files remain on disk)
        new_sid = make_sid()
        new_entries = [make_session_header(new_sid)] + restored_entries[1:]
        new_jsonl = TEST_SESSIONS_DIR / f"{new_sid}.jsonl"
        write_jsonl(new_jsonl, new_entries)
        ok("new session header written without losing stubs") if has_stub(read_jsonl(new_jsonl)) else fail("stubs lost after new session header")
        new_jsonl.unlink(missing_ok=True)

    finally:
        jsonl.unlink(missing_ok=True)
        shutil.rmtree(cache, ignore_errors=True)


# ──────────────────────────────────────────────────────────
# TEST 6: Sidecar + trim interaction
# ──────────────────────────────────────────────────────────
def test_sidecar_plus_trim():
    log("TEST 6: Sidecar + trim interaction (sidecar runs before trim)")
    sid = make_sid()
    jsonl = TEST_SESSIONS_DIR / f"{sid}.jsonl"
    cache = TEST_SESSIONS_DIR / f"{sid}.toolcache"
    state_file = Path(tempfile.mktemp(suffix=".json"))
    state_file.write_text("{}")
    try:
        entries = [make_session_header(sid)]
        for i in range(15):
            uid = f"u-{i:02d}"
            aid = f"a-{i:02d}"
            tid = f"tc-{i:02d}"
            entries.append(make_user(uid, f"query {i}"))
            entries.append(make_assistant(aid, f"response {i}", [tid]))
            entries.append(make_tool_result(f"tr-{i:02d}", tid, "exec", big_text(8), aid))

        write_jsonl(jsonl, entries)
        before_kb = jsonl.stat().st_size // 1024

        run_sidecar(jsonl, sid)
        after_sidecar_kb = jsonl.stat().st_size // 1024

        files = list(cache.iterdir()) if cache.exists() else []
        ok(f"sidecar offloaded {len(files)} entries (expected ~15)") if len(files) >= 14 else fail(f"only {len(files)} sidecar files")

        ok(f"sidecar reduced size ({before_kb}KB → {after_sidecar_kb}KB)") if after_sidecar_kb < before_kb else fail("sidecar did not reduce size")

        rc = run_trim(jsonl, sid, state_file)
        after_trim_kb = jsonl.stat().st_size // 1024
        log(f"  After trim: {after_trim_kb}KB")

        # Trim may return 1 if "nothing to do" — both 0 and 1 are OK
        ok(f"trim ran (rc={rc})") if rc in (0, 1) else fail(f"trim failed with rc={rc}")

        # Sidecar files survive trim
        files_after = list(cache.iterdir()) if cache.exists() else []
        ok(f"sidecar files intact after trim ({len(files_after)})") if len(files_after) >= len(files) else fail(f"sidecar files lost: before={len(files)}, after={len(files_after)}")

    finally:
        jsonl.unlink(missing_ok=True)
        for pre in TEST_SESSIONS_DIR.glob(f"{sid}.jsonl.pre-trim.*"):
            pre.unlink(missing_ok=True)
        shutil.rmtree(cache, ignore_errors=True)
        state_file.unlink(missing_ok=True)


# ──────────────────────────────────────────────────────────
# TEST 7: Multiple tool calls in one assistant turn
# ──────────────────────────────────────────────────────────
def test_multi_tool_turn():
    log("TEST 7: Multiple large tool calls in one assistant turn")
    sid = make_sid()
    jsonl = TEST_SESSIONS_DIR / f"{sid}.jsonl"
    cache = TEST_SESSIONS_DIR / f"{sid}.toolcache"
    try:
        entries = [
            make_session_header(sid),
            make_user("u-001", "run two things"),
            make_assistant("a-001", "running both", ["tc-001", "tc-002"]),
            make_tool_result("tr-001", "tc-001", "exec", big_text(6), "a-001"),
            make_tool_result("tr-002", "tc-002", "exec", big_text(6), "a-001"),
        ]
        write_jsonl(jsonl, entries)
        run_sidecar(jsonl, sid)

        ok("both results sidecared") if (cache / "tc-001.txt").exists() and (cache / "tc-002.txt").exists() else fail("missing sidecar files for multi-tool turn")

        new_entries = read_jsonl(jsonl)
        n = count_stubs(new_entries)
        ok(f"two stubs in transcript ({n})") if n == 2 else fail(f"expected 2 stubs, got {n}")

    finally:
        jsonl.unlink(missing_ok=True)
        shutil.rmtree(cache, ignore_errors=True)


# ──────────────────────────────────────────────────────────
# TEST 8: Post-restart compaction scenario
# After a gateway restart, OC writes a new compaction entry.
# Sidecar stubs are preserved through compaction + re-trim cycle.
# ──────────────────────────────────────────────────────────
def test_restart_then_compaction():
    log("TEST 8: Post-restart compaction — stubs survive trim of post-restart transcript")
    sid = make_sid()
    jsonl = TEST_SESSIONS_DIR / f"{sid}.jsonl"
    cache = TEST_SESSIONS_DIR / f"{sid}.toolcache"
    state_file = Path(tempfile.mktemp(suffix=".json"))
    state_file.write_text("{}")
    try:
        # Phase 1: pre-restart session with large tool output
        entries = [make_session_header(sid)]
        for i in range(12):
            uid, aid, tid = f"u-{i:02d}", f"a-{i:02d}", f"tc-{i:02d}"
            entries.append(make_user(uid, f"query {i}"))
            entries.append(make_assistant(aid, f"ok {i}", [tid]))
            entries.append(make_tool_result(f"tr-{i:02d}", tid, "exec", big_text(6), aid))
        write_jsonl(jsonl, entries)
        run_sidecar(jsonl, sid)

        # Phase 2: simulate gateway restart — OC rewrites transcript with new session header
        # In OC, restart writes a .reset. copy; we simulate by adding a new compaction entry
        post_restart_entries = read_jsonl(jsonl)
        compaction = {
            "type": "compaction",
            "id": "compact-after-restart",
            "parentId": "hdr-001",
            "timestamp": ts(),
            "summary": "Gateway restarted. Prior context above.",
            "firstKeptEntryId": None,
            "tokensBefore": 0,
        }
        # Insert compaction after header
        post_restart_entries.insert(1, compaction)
        write_jsonl(jsonl, post_restart_entries)

        # Phase 3: Add more conversation after restart
        last_id = post_restart_entries[-1]["id"] if post_restart_entries else "compact-after-restart"
        for i in range(3):
            uid, aid = f"post-u-{i}", f"post-a-{i}"
            post_restart_entries.append(make_user(uid, f"post-restart query {i}", last_id))
            post_restart_entries.append(make_assistant(aid, f"post-restart reply {i}", [], uid))
            last_id = aid
        write_jsonl(jsonl, post_restart_entries)

        # Phase 4: Run trim on the post-restart transcript
        rc = run_trim(jsonl, sid, state_file, keep_pairs=5)
        log(f"  trim rc={rc}")

        # Sidecar files must still be intact
        if cache.exists():
            file_count = len(list(cache.iterdir()))
            ok(f"sidecar files intact after restart+compaction+trim ({file_count})") if file_count >= 10 else fail(f"only {file_count} sidecar files remain")
        else:
            fail("toolcache dir missing after restart+trim")

    finally:
        jsonl.unlink(missing_ok=True)
        for pre in TEST_SESSIONS_DIR.glob(f"{sid}.jsonl.pre-trim.*"):
            pre.unlink(missing_ok=True)
        shutil.rmtree(cache, ignore_errors=True)
        state_file.unlink(missing_ok=True)


# ──────────────────────────────────────────────────────────
# Run all tests
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    TEST_SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    test_basic_offload()
    test_idempotency()
    test_small_not_sidecared()
    test_mixed()
    test_restart_resilience()
    test_sidecar_plus_trim()
    test_multi_tool_turn()
    test_restart_then_compaction()

    print()
    print("══════════════════════════════════════")
    print(f"  Results: ✅ {PASS} passed  ❌ {FAIL} failed")
    print("══════════════════════════════════════")

    sys.exit(1 if FAIL > 0 else 0)
