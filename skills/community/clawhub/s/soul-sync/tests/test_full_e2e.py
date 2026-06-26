#!/usr/bin/env python3
"""
Full End-to-End Test — Simulates a complete soulsync flow from fresh workspace
to personalized files. Tests the entire pipeline.
"""
import os
import sys
import json
import shutil
import tempfile
import subprocess

SKILL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
LIB_DIR = os.path.join(SKILL_DIR, "lib")

passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  ✅ {name}")
        passed += 1
    else:
        print(f"  ❌ {name} — {detail}")
        failed += 1

def run(script, args=None, env_extra=None):
    cmd = [sys.executable, os.path.join(LIB_DIR, script)]
    if args:
        cmd.extend(args)
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=30)
    try:
        return json.loads(r.stdout)
    except:
        return {"_raw": r.stdout, "_err": r.stderr}

# ─── PHASE 1: Fresh workspace detection ──────────────────────────────
print("\n" + "=" * 60)
print("🧪 FULL END-TO-END SOULSYNC TEST")
print("=" * 60)

# Create fresh workspace
tmpdir = tempfile.mkdtemp(prefix="soulsync_e2e_")
import_dir = os.path.join(tmpdir, "_imports")
os.makedirs(import_dir, exist_ok=True)
env = {"OPENCLAW_WORKSPACE": tmpdir}

print(f"\n📁 Test workspace: {tmpdir}")
print(f"📁 Import dir: {import_dir}")

# ─── Phase 1: Detection
print("\n── Phase 1: Workspace Detection ──")
result = run("detector.py", env_extra=env)
test("Detector runs", "level" in result)
test("Detects NEW workspace", result.get("level") == "new", f"got: {result.get('level')}")
test("Lists all gaps", len(result.get("gaps", [])) >= 4)
print(f"  📊 Score: {result.get('score', '?')}, Gaps: {len(result.get('gaps', []))}")

# ─── Phase 2: Conversation Init
print("\n── Phase 2: Conversation Engine Init ──")

# Monkey-patch import dir for conversation engine
conv_env = env.copy()
conv_script = f"""
import sys, os, json
sys.path.insert(0, '{LIB_DIR}')
os.environ['OPENCLAW_WORKSPACE'] = '{tmpdir}'

import conversation
conversation.IMPORT_DIR = '{import_dir}'
conversation.STATE_FILE = os.path.join('{import_dir}', 'conversation.json')

state = conversation.ConversationState()
state.load_imports()
state.save()

result = {{
    "missing": state.get_missing_dimensions(),
    "next_questions": state.get_next_questions(),
    "progress": state.get_progress(),
}}
print(json.dumps(result))
"""
r = subprocess.run([sys.executable, "-c", conv_script], capture_output=True, text=True, timeout=10)
try:
    init_result = json.loads(r.stdout)
except:
    init_result = {"_err": r.stderr, "_raw": r.stdout}

test("Conversation init works", "progress" in init_result)
test("10 dimensions to cover", init_result.get("progress", {}).get("dimensions_total") == 10)
test("0 dimensions covered at start", init_result.get("progress", {}).get("dimensions_covered") == 0)
test("First question is identity", 
     init_result.get("next_questions", [{}])[0].get("dimension") == "identity")

# ─── Phase 3: Simulate conversation
print("\n── Phase 3: Simulated Conversation ──")

conversations = [
    ("identity", "I'm Sarah Chen, but most people call me SC. She/her."),
    ("work", "I'm a product designer at a fintech startup. Been doing UX for about 8 years. Also freelance on the side."),
    ("communication", "Keep it casual and concise. I hate walls of text. Bullet points are great. Don't be overly formal."),
    ("goals", "Help me stay organized, draft emails, research competitors, and remind me about deadlines."),
    ("context", "I'm in Pacific time, Bay Area. Mainly use Mac and iPhone."),
    ("boundaries", "Don't ever post to social media for me. Don't schedule meetings without confirmation. And please don't be sycophantic."),
    ("interests", "Rock climbing, indie games, Japanese food, typography, and sustainability."),
    ("relationships", "My partner Alex, my cat Mochi, and my cofounder Jamie are the main characters."),
    ("technical", "I'm not an engineer but I'm comfortable with Figma, basic HTML/CSS, and I use the terminal sometimes."),
]

for dim, response in conversations:
    conv_record = f"""
import sys, os, json
sys.path.insert(0, '{LIB_DIR}')
os.environ['OPENCLAW_WORKSPACE'] = '{tmpdir}'

import conversation
conversation.IMPORT_DIR = '{import_dir}'
conversation.STATE_FILE = os.path.join('{import_dir}', 'conversation.json')

state = conversation.ConversationState.load()
extracted = state.record_answer('{dim}', '''{response}''')
state.save()

print(json.dumps({{"dim": "{dim}", "extracted": extracted, "progress": state.get_progress()}}))
"""
    r = subprocess.run([sys.executable, "-c", conv_record], capture_output=True, text=True, timeout=10)
    try:
        rec = json.loads(r.stdout)
        extracted_count = len(rec.get("extracted", {}))
        progress = rec.get("progress", {})
        test(f"Record '{dim}' → extracted {extracted_count} fields",
             extracted_count > 0 or dim in ["relationships", "technical"],
             f"extracted: {rec.get('extracted', {})}")
    except:
        test(f"Record '{dim}'", False, f"parse error: {r.stdout[:100]} | {r.stderr[:100]}")

# Check final progress
conv_status = f"""
import sys, os, json
sys.path.insert(0, '{LIB_DIR}')
os.environ['OPENCLAW_WORKSPACE'] = '{tmpdir}'

import conversation
conversation.IMPORT_DIR = '{import_dir}'
conversation.STATE_FILE = os.path.join('{import_dir}', 'conversation.json')

state = conversation.ConversationState.load()
print(json.dumps(state.to_dict()))
"""
r = subprocess.run([sys.executable, "-c", conv_status], capture_output=True, text=True, timeout=10)
try:
    final_state = json.loads(r.stdout)
except:
    final_state = {}

progress = final_state.get("progress", {})
test("All required dimensions covered", progress.get("required_complete", False))
test("Can finish", progress.get("can_finish", False))
test(f"Collected {progress.get('fields_collected', 0)} fields", progress.get("fields_collected", 0) >= 8)
print(f"  📊 {progress.get('dimensions_covered', 0)}/{progress.get('dimensions_total', 0)} dimensions, {progress.get('fields_collected', 0)} fields")

# ─── Phase 4: Simulate importer data
print("\n── Phase 4: Mock Importer Data ──")

mock_github = {
    "source": "github",
    "insights": {
        "technical_skills": "JavaScript, TypeScript, Python — experienced",
        "languages": ["JavaScript", "TypeScript", "Python", "HTML", "CSS"],
        "interests": ["design-systems", "accessibility", "react"],
        "communication_style": "Active open source contributor",
        "profile": {"username": "sarahc", "public_repos": 23, "followers": 150}
    },
    "items_processed": 23
}

mock_spotify = {
    "source": "spotify",
    "insights": {
        "interests": ["indie rock", "lo-fi", "japanese city pop", "ambient"],
        "personality_traits": ["creative", "uses music for focus/productivity", "values downtime and recovery"],
        "top_artists": ["Radiohead", "Nujabes", "Khruangbin", "Tame Impala"],
        "top_genres": ["indie rock", "lo-fi beats", "city pop", "ambient"]
    }
}

mock_reddit = {
    "source": "reddit",
    "insights": {
        "interests": ["climbing", "uxdesign", "indiegaming", "typography", "sustainability"],
        "interest_categories": ["creative", "technology", "lifestyle"],
        "communication_style": "Avg comment: 120 chars. Moderate engagement.",
        "tone": "helpful — gives advice and recommendations, uses humor and casual internet tone",
        "personality_traits": ["commenter > poster — engages more than broadcasts"],
    }
}

for name, data in [("github", mock_github), ("spotify", mock_spotify), ("reddit", mock_reddit)]:
    path = os.path.join(import_dir, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    test(f"Mock {name} data written", os.path.exists(path))

# ─── Phase 5: Synthesis
print("\n── Phase 5: Synthesis ──")

synth_script = f"""
import sys, os, json
sys.path.insert(0, '{LIB_DIR}')
os.environ['OPENCLAW_WORKSPACE'] = '{tmpdir}'

import conversation
conversation.IMPORT_DIR = '{import_dir}'
conversation.STATE_FILE = os.path.join('{import_dir}', 'conversation.json')

# Export conversation data to the import dir so synthesizer can find it
state = conversation.ConversationState.load()
conv_data = state.known
with open(os.path.join('{import_dir}', 'conversation.json'), 'w') as f:
    json.dump(conv_data, f)

import synthesizer
synthesizer.IMPORT_DIR = '{import_dir}'
synthesizer.WORKSPACE = '{tmpdir}'

result = synthesizer.synthesize()
print(json.dumps(result, indent=2))
"""
r = subprocess.run([sys.executable, "-c", synth_script], capture_output=True, text=True, timeout=10)
try:
    synth_result = json.loads(r.stdout)
except:
    synth_result = {"_err": r.stderr, "_raw": r.stdout[:500]}

test("Synthesizer produces output", "files" in synth_result)
test("Sources include conversation + imports",
     len(synth_result.get("sources", [])) >= 2,
     f"sources: {synth_result.get('sources', [])}")

files = synth_result.get("files", {})

# Validate USER.md
user_md = files.get("USER.md", "")
test("USER.md generated", len(user_md) > 50)
test("USER.md has preferred name", "SC" in user_md or "Sarah" in user_md, f"content: {user_md[:200]}")
test("USER.md has timezone", "Pacific" in user_md or "Los_Angeles" in user_md, f"content: {user_md[:300]}")
test("USER.md has work info", "designer" in user_md.lower() or "fintech" in user_md.lower())
test("USER.md has interests", "climbing" in user_md.lower() or "typography" in user_md.lower())

# Validate SOUL.md
soul_md = files.get("SOUL.md", "")
test("SOUL.md generated", len(soul_md) > 100)
test("SOUL.md has communication style", "direct" in soul_md.lower() or "concise" in soul_md.lower() or "casual" in soul_md.lower())
test("SOUL.md has boundaries section", "boundar" in soul_md.lower())

# Validate MEMORY.md
memory_md = files.get("MEMORY.md", "")
test("MEMORY.md generated", len(memory_md) > 50)
test("MEMORY.md seeded with data", "Sarah" in memory_md or "SC" in memory_md or "designer" in memory_md.lower())

# ─── Phase 6: Write files and verify
print("\n── Phase 6: File Writing ──")

for filename, content in files.items():
    path = os.path.join(tmpdir, filename)
    with open(path, "w") as f:
        f.write(content)
    test(f"{filename} written ({len(content)} bytes)", os.path.exists(path) and os.path.getsize(path) > 0)

# ─── Phase 7: Re-detect — should now be established
print("\n── Phase 7: Post-soulsync Detection ──")
result = run("detector.py", env_extra=env)
test("Re-detection works", "level" in result)
test("Workspace now 'partial' or 'established'", 
     result.get("level") in ["partial", "established"],
     f"got: {result.get('level')}")
test("Score improved", result.get("score", 0) > 0.15, f"score: {result.get('score')}")
print(f"  📊 New score: {result.get('score', '?')} (was 0.0)")

# ─── Cleanup
shutil.rmtree(tmpdir)

# ─── Results
print(f"\n{'=' * 60}")
print(f"Results: {passed} passed, {failed} failed")
if failed == 0:
    print("🎉 Full end-to-end test passed!")
else:
    print(f"⚠️  {failed} test(s) need attention")
    sys.exit(1)
