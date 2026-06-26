#!/usr/bin/env python3
"""LLM-powered extraction of archived transcript content into structured memory.

Usage: extract-llm.py <pre_trim> <trimmed> <sid> <gateway> <state_file> <api_url> <api_token> <mem_enabled> <mem_path>

Guardrails: lockfile, 20K char cap, 60s timeout, dedup via state file.
Exit 0 = success/skip, 2 = LLM failure (caller should fall back).
"""
import json, sys, os, subprocess, fcntl, signal
from datetime import datetime

# Defaults — overridden by config values passed via argv
DEFAULT_MAX_INPUT_CHARS = 20000
DEFAULT_API_TIMEOUT_SECS = 60
DEFAULT_MAX_MEMORIES = 15
DEFAULT_MIN_ARCHIVED = 3
LOCKFILE = "/tmp/session-janitor-extract.lock"
DEFAULT_MODEL = "openclaw"

EXTRACTION_PROMPT = """You are a memory extraction system. Analyze this conversation transcript and extract structured memories.

For each memory, output a JSON object on its own line with these fields:
- "type": one of "fact", "decision", "preference", "task", "risk", "plan", "lesson"
- "salience": 0.1 (trivia) to 1.0 (critical)
- "scene": short label for the topic area (e.g. "infrastructure", "k8s", "personal", "workflow")
- "content": concise statement of the memory (1-2 sentences max)

Rules:
- Extract 3-15 memories. Quality over quantity.
- Focus on: decisions made, facts learned, preferences expressed, tasks assigned, lessons learned, risks identified
- Skip: routine tool output, heartbeat checks, pleasantries, obvious/temporary context
- Each memory should stand alone — readable without the original conversation
- Use present tense for facts/preferences, past tense for events/decisions

Output ONLY the JSON lines, nothing else.

TRANSCRIPT:
"""

def timeout_handler(signum, frame):
    raise TimeoutError("API call exceeded timeout")

def extract_archived_content(pre_trim_file, trimmed_file):
    pre_entries = []
    with open(pre_trim_file) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try: pre_entries.append(json.loads(line))
            except: continue

    kept_ids = set()
    with open(trimmed_file) as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                e = json.loads(line)
                if e.get("id"): kept_ids.add(e["id"])
            except: continue

    archived = []
    for e in pre_entries:
        if e.get("type") != "message": continue
        if e.get("id") in kept_ids: continue
        role = e.get("message", {}).get("role", "")
        if role not in ("user", "assistant"): continue
        content = e.get("message", {}).get("content", "")
        if isinstance(content, list):
            content = " ".join(c.get("text", "") for c in content if c.get("type") == "text")
        content = content.strip()
        if not content or content in ("NO_REPLY", "HEARTBEAT_OK"): continue
        if content.startswith("Read HEARTBEAT"): continue
        archived.append({"role": role, "content": content})
    return archived

def format_for_llm(archived_messages, max_input_chars=DEFAULT_MAX_INPUT_CHARS):
    lines = []
    for msg in archived_messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"[{role}]: {msg['content']}\n")
    text = "".join(lines)
    if len(text) > max_input_chars:
        head = int(max_input_chars * 0.3)
        tail = max_input_chars - head - 50
        text = text[:head] + "\n[... middle truncated ...]\n" + text[-tail:]
    return text

def call_llm(api_url, api_token, transcript_text, model=DEFAULT_MODEL, api_timeout_secs=DEFAULT_API_TIMEOUT_SECS):
    import urllib.request
    payload = {
        "model": model, "max_tokens": 2000, "temperature": 0.3,
        "messages": [{"role": "user", "content": EXTRACTION_PROMPT + transcript_text}]
    }
    req = urllib.request.Request(
        f"{api_url}/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
    )
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(api_timeout_secs)
    try:
        with urllib.request.urlopen(req, timeout=api_timeout_secs) as resp:
            result = json.loads(resp.read())
        signal.alarm(0)
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        signal.alarm(0)
        raise RuntimeError(f"LLM API call failed: {e}")

def parse_memories(llm_output, max_memories=DEFAULT_MAX_MEMORIES):
    memories = []
    for line in llm_output.strip().split("\n"):
        line = line.strip()
        if not line or not line.startswith("{"): continue
        try:
            mem = json.loads(line)
            if not all(k in mem for k in ("type", "salience", "scene", "content")): continue
            if mem["type"] not in ("fact", "decision", "preference", "task", "risk", "plan", "lesson"): continue
            if not (0.0 <= float(mem["salience"]) <= 1.0): continue
            if len(mem["content"]) < 5 or len(mem["content"]) > 500: continue
            memories.append(mem)
        except: continue
    return memories[:max_memories]

# Scene label → file mapping for scene file writes
SCENE_FILE_MAP = {
    "infra": "scene-infrastructure.md",
    "infrastructure": "scene-infrastructure.md",
    "k8s": "scene-infrastructure.md",
    "kubernetes": "scene-infrastructure.md",
    "networking": "scene-infrastructure.md",
    "network": "scene-infrastructure.md",
    "config": "scene-config.md",
    "gateway": "scene-config.md",
    "openclaw": "scene-config.md",
    "configuration": "scene-config.md",
    "projects": "scene-projects.md",
    "project": "scene-projects.md",
    "cyrano": "scene-projects.md",
    "groomer": "scene-projects.md",
    "archy": "scene-projects.md",
    "lessons": "scene-lessons.md",
    "lesson": "scene-lessons.md",
    "commodore": "scene-commodore.md",
    "personal": "scene-commodore.md",
    "preferences": "scene-commodore.md",
    "accounts": "scene-accounts.md",
    "account": "scene-accounts.md",
    "auth": "scene-accounts.md",
}
SCENE_FILE_DEFAULT = "scene-infrastructure.md"

def write_to_scene_files(memories, scene_dir):
    """Append extracted memories to git-backed scene files for durable recovery."""
    if not scene_dir or not os.path.isdir(scene_dir):
        return 0
    from datetime import date
    today = date.today().isoformat()
    written = 0
    for mem in memories:
        scene_label = mem.get("scene", "").lower()
        filename = SCENE_FILE_MAP.get(scene_label, SCENE_FILE_DEFAULT)
        filepath = os.path.join(scene_dir, filename)
        sal = mem.get("salience", 0.5)
        mtype = mem.get("type", "fact")
        content = mem.get("content", "").replace('\n', ' ').strip()
        if not content:
            continue
        line = f"- [{mtype}] (sal: {sal:.1f}) {content}  # janitor {today}\n"
        try:
            with open(filepath, "a") as f:
                f.write(line)
            written += 1
        except Exception as e:
            print(f"scene file write error ({filepath}): {e}", file=sys.stderr)
    return written

def git_commit_scene_files(scene_dir):
    """Commit and push scene file updates to git repo."""
    repo_dir = os.path.dirname(os.path.dirname(scene_dir))  # memory/private/ -> repo root
    try:
        # Check if anything changed
        result = subprocess.run(
            ["git", "-C", repo_dir, "status", "--porcelain", "memory/private/scene-*.md"],
            capture_output=True, text=True, timeout=10
        )
        # Use glob since git status porcelain doesn't expand globs
        import glob
        scene_files = glob.glob(os.path.join(scene_dir, "scene-*.md"))
        changed = []
        for sf in scene_files:
            rel = os.path.relpath(sf, repo_dir)
            r2 = subprocess.run(
                ["git", "-C", repo_dir, "diff", "--quiet", rel],
                capture_output=True, timeout=5
            )
            if r2.returncode != 0:
                changed.append(rel)
        if not changed:
            print("No scene file changes to commit")
            return
        for rel in changed:
            subprocess.run(["git", "-C", repo_dir, "add", rel], timeout=5, check=True)
        from datetime import date
        msg = f"janitor: scene file update {date.today().isoformat()}"
        subprocess.run(["git", "-C", repo_dir, "commit", "-m", msg], timeout=10, check=True)
        subprocess.run(["git", "-C", repo_dir, "push"], timeout=30, check=True)
        print(f"Committed and pushed {len(changed)} scene file(s)")
    except subprocess.CalledProcessError as e:
        print(f"git commit/push failed (non-fatal): {e}", file=sys.stderr)
    except Exception as e:
        print(f"git error (non-fatal): {e}", file=sys.stderr)

def store_memories(memories, mem_enabled, mem_path, scene_dir=None):
    stored = 0
    if mem_enabled:
        for mem in memories:
            try:
                result = subprocess.run(
                    [mem_path, "quick-store", mem["scene"], mem["type"], str(mem["salience"]), mem["content"]],
                    capture_output=True, text=True, timeout=10
                )
                if result.returncode == 0: stored += 1
                else: print(f"mem store failed: {result.stderr.strip()}", file=sys.stderr)
            except Exception as e:
                print(f"mem store error: {e}", file=sys.stderr)
    # Write to scene files (always, if path provided — DB is derived, files are durable)
    scene_written = 0
    if scene_dir:
        scene_written = write_to_scene_files(memories, scene_dir)
        if scene_written > 0:
            git_commit_scene_files(scene_dir)
            print(f"Wrote {scene_written} memories to scene files")
    return stored

def main():
    if len(sys.argv) < 8:
        print("Usage: extract-llm.py <pre_trim> <trimmed> <sid> <gateway> <state> <api_url> <api_token> [mem_enabled] [mem_path]", file=sys.stderr)
        sys.exit(1)

    pre_trim_file, trimmed_file, session_id, gateway = sys.argv[1:5]
    state_file, api_url, api_token = sys.argv[5:8]
    mem_enabled = sys.argv[8].lower() == "true" if len(sys.argv) > 8 else False
    mem_path = sys.argv[9] if len(sys.argv) > 9 else "mem"
    scene_dir = sys.argv[10] if len(sys.argv) > 10 else None
    model = sys.argv[11] if len(sys.argv) > 11 else DEFAULT_MODEL
    max_input_chars = int(sys.argv[12]) if len(sys.argv) > 12 else DEFAULT_MAX_INPUT_CHARS
    api_timeout_secs = int(sys.argv[13]) if len(sys.argv) > 13 else DEFAULT_API_TIMEOUT_SECS
    max_memories = int(sys.argv[14]) if len(sys.argv) > 14 else DEFAULT_MAX_MEMORIES
    min_archived = int(sys.argv[15]) if len(sys.argv) > 15 else DEFAULT_MIN_ARCHIVED

    # Lockfile
    lock_fd = None
    try:
        lock_fd = open(LOCKFILE, "w")
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (IOError, OSError):
        print("Another LLM extraction is running — skipping")
        sys.exit(0)

    try:
        state = {}
        if os.path.exists(state_file):
            try: state = json.load(open(state_file))
            except: pass

        llm_key = f"llm-{session_id}-{os.path.basename(pre_trim_file)}"
        if llm_key in state.get("llm_extracted", {}):
            print(f"Already extracted {llm_key} — skipping")
            sys.exit(0)

        if not os.path.exists(pre_trim_file):
            print(f"Pre-trim file not found: {pre_trim_file}", file=sys.stderr)
            sys.exit(1)

        archived = extract_archived_content(pre_trim_file, trimmed_file)
        if len(archived) < min_archived:
            print(f"Only {len(archived)} archived messages (need {min_archived}) — not enough")
            sys.exit(0)

        transcript_text = format_for_llm(archived, max_input_chars)
        print(f"Sending {len(transcript_text)} chars ({len(archived)} messages) to LLM...")

        try:
            llm_output = call_llm(api_url, api_token, transcript_text, model, api_timeout_secs)
        except Exception as e:
            print(f"LLM extraction failed: {e}", file=sys.stderr)
            sys.exit(2)

        memories = parse_memories(llm_output, max_memories)
        if not memories:
            print("LLM returned no valid memories")
            sys.exit(0)

        stored = store_memories(memories, mem_enabled, mem_path, scene_dir)
        print(f"Extracted {len(memories)} memories, stored {stored} to mem DB")

        # Update dedup state
        llm_extracted = state.get("llm_extracted", {})
        llm_extracted[llm_key] = {
            "timestamp": datetime.now().isoformat(),
            "memories": len(memories),
            "stored": stored,
            "input_chars": len(transcript_text),
        }
        if len(llm_extracted) > 100:
            for k in sorted(llm_extracted, key=lambda k: llm_extracted[k].get("timestamp", ""))[:50]:
                del llm_extracted[k]
        state["llm_extracted"] = llm_extracted
        state["lastLlmRun"] = datetime.now().isoformat()
        json.dump(state, open(state_file, "w"), indent=2)
    finally:
        if lock_fd:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
            try: os.unlink(LOCKFILE)
            except: pass

if __name__ == "__main__":
    main()
