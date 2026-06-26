#!/usr/bin/env python3
"""
Soulsync E2E Test — Simulates a fresh workspace and runs the full soulsync pipeline.
Creates a temp workspace, runs detector → importers → synthesizer, validates output.
"""
import os
import sys
import json
import shutil
import tempfile
import subprocess

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_PASSED = 0
TESTS_FAILED = 0

def test(name, condition, detail=""):
    global TESTS_PASSED, TESTS_FAILED
    if condition:
        print(f"  ✅ {name}")
        TESTS_PASSED += 1
    else:
        print(f"  ❌ {name} — {detail}")
        TESTS_FAILED += 1

def run_script(script, env=None, args=None):
    """Run a Python script and return parsed JSON output."""
    cmd = [sys.executable, os.path.join(SKILL_DIR, script)]
    if args:
        cmd.extend(args)
    
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    
    result = subprocess.run(cmd, capture_output=True, text=True, env=full_env, timeout=30)
    try:
        return json.loads(result.stdout), result.returncode
    except json.JSONDecodeError:
        return {"raw_output": result.stdout, "stderr": result.stderr}, result.returncode

def test_detector_new():
    """Test detector with completely empty workspace."""
    print("\n🔍 Test: Detector — Empty workspace (new user)")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result, code = run_script("lib/detector.py", env={"OPENCLAW_WORKSPACE": tmpdir})
        
        test("Returns valid JSON", isinstance(result, dict) and "level" in result)
        test("Detects 'new' level", result.get("level") == "new", f"got: {result.get('level')}")
        test("Score is low", result.get("score", 1) < 0.2, f"got: {result.get('score')}")
        test("Lists gaps", len(result.get("gaps", [])) > 0)

def test_detector_partial():
    """Test detector with partial workspace."""
    print("\n🔍 Test: Detector — Partial workspace")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create minimal files
        with open(os.path.join(tmpdir, "SOUL.md"), "w") as f:
            f.write("# SOUL.md\n_You're not a chatbot._\nBe helpful.")
        with open(os.path.join(tmpdir, "USER.md"), "w") as f:
            f.write("Name: Test User\nTimezone: UTC")
        
        result, code = run_script("lib/detector.py", env={"OPENCLAW_WORKSPACE": tmpdir})
        
        test("Returns valid JSON", isinstance(result, dict) and "level" in result)
        test("Detects 'partial' or 'new'", result.get("level") in ["partial", "new"], f"got: {result.get('level')}")
        test("SOUL.md detected as default", result["details"]["soul_md"]["score"] < 0.5)

def test_detector_established():
    """Test detector with rich workspace."""
    print("\n🔍 Test: Detector — Established workspace")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create rich files
        with open(os.path.join(tmpdir, "SOUL.md"), "w") as f:
            f.write("# SOUL.md\n\n" + "Detailed personality description. " * 50)
        with open(os.path.join(tmpdir, "USER.md"), "w") as f:
            f.write("Name: Power User\n\n" + "Detailed background info. " * 50)
        with open(os.path.join(tmpdir, "MEMORY.md"), "w") as f:
            f.write("# Long-term Memory\n\n" + "Important memory entry. " * 40)
        with open(os.path.join(tmpdir, "IDENTITY.md"), "w") as f:
            f.write("name: TestBot\n")
        
        # Create memory day files
        mem_dir = os.path.join(tmpdir, "memory")
        os.makedirs(mem_dir)
        for i in range(10):
            with open(os.path.join(mem_dir, f"2026-03-{i+10:02d}.md"), "w") as f:
                f.write(f"# Day {i}\nStuff happened.\n")
        
        result, code = run_script("lib/detector.py", env={"OPENCLAW_WORKSPACE": tmpdir})
        
        test("Returns valid JSON", isinstance(result, dict) and "level" in result)
        test("Detects 'established'", result.get("level") == "established", f"got: {result.get('level')}")
        test("Score is high", result.get("score", 0) >= 0.6, f"got: {result.get('score')}")
        test("Few or no gaps", len(result.get("gaps", [])) <= 1)

def test_synthesizer():
    """Test synthesizer with mock data."""
    print("\n🧪 Test: Synthesizer — Mock data")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        import_dir = os.path.join(tmpdir, "imports")
        os.makedirs(import_dir)
        
        # Create mock importer outputs
        gmail_data = {
            "source": "gmail",
            "insights": {
                "communication_style": "concise, uses bullet points",
                "key_contacts": ["alice@example.com", "bob@example.com"],
                "interests": ["AI", "Bitcoin", "Photography"],
                "work_patterns": "Most active: 9:00, 14:00, 21:00; Rarely works weekends",
                "tone": "Direct but friendly"
            }
        }
        with open(os.path.join(import_dir, "gmail.json"), "w") as f:
            json.dump(gmail_data, f)
        
        github_data = {
            "source": "github",
            "insights": {
                "technical_skills": "Python, JavaScript, TypeScript developer — experienced",
                "languages": ["Python", "JavaScript", "TypeScript"],
                "interests": ["web-development", "machine-learning"],
                "communication_style": "Active open source contributor"
            }
        }
        with open(os.path.join(import_dir, "github.json"), "w") as f:
            json.dump(github_data, f)
        
        conversation_data = {
            "name": "Test User",
            "preferred_name": "Testy",
            "pronouns": "They/Them",
            "timezone": "America/Chicago",
            "email": "test@example.com",
            "work": "Software engineer and entrepreneur",
            "interests": ["Bitcoin", "AI", "3D printing"],
            "boundaries": ["Don't send emails without asking", "Respect quiet hours after 11pm"],
            "goals": ["Build a personal AI agent", "Learn about hardware"],
            "communication_style": "Direct, concise, no fluff",
            "tone": "Casual but competent",
        }
        with open(os.path.join(import_dir, "conversation.json"), "w") as f:
            json.dump(conversation_data, f)
        
        # Monkey-patch the import dir
        import importlib.util
        spec = importlib.util.spec_from_file_location("synthesizer", os.path.join(SKILL_DIR, "lib", "synthesizer.py"))
        synth = importlib.util.module_from_spec(spec)
        
        # Override IMPORT_DIR
        original_import_dir = os.path.join(SKILL_DIR, "lib")
        env = os.environ.copy()
        env["OPENCLAW_WORKSPACE"] = tmpdir
        
        # Run synthesizer with our mock import dir
        result = subprocess.run(
            [sys.executable, "-c", f"""
import sys, os, json
sys.path.insert(0, '{os.path.join(SKILL_DIR, "lib")}')
import synthesizer
synthesizer.IMPORT_DIR = '{import_dir}'
synthesizer.WORKSPACE = '{tmpdir}'
result = synthesizer.synthesize()
print(json.dumps(result, indent=2))
"""],
            capture_output=True, text=True, env=env, timeout=10
        )
        
        try:
            output = json.loads(result.stdout)
        except:
            output = {}
            print(f"  ⚠️  Synthesizer output: {result.stdout[:200]}")
            print(f"  ⚠️  Stderr: {result.stderr[:200]}")
        
        test("Returns valid output", "files" in output)
        test("Generates USER.md", "USER.md" in output.get("files", {}))
        test("Generates SOUL.md", "SOUL.md" in output.get("files", {}))
        test("Generates MEMORY.md", "MEMORY.md" in output.get("files", {}))
        
        user_md = output.get("files", {}).get("USER.md", "")
        test("USER.md contains name", "Test User" in user_md, f"content: {user_md[:100]}")
        test("USER.md contains interests", "Bitcoin" in user_md or "AI" in user_md)
        
        soul_md = output.get("files", {}).get("SOUL.md", "")
        test("SOUL.md is non-empty", len(soul_md) > 100)
        
        memory_md = output.get("files", {}).get("MEMORY.md", "")
        test("MEMORY.md seeds from data", "Test User" in memory_md or "Software" in memory_md)

def test_github_importer():
    """Test GitHub importer with a known public profile."""
    print("\n🐙 Test: GitHub importer — Public profile")
    
    result, code = run_script("lib/importers/github.py", args=["torvalds"])
    
    test("Returns valid JSON", isinstance(result, dict) and "source" in result)
    test("Source is github", result.get("source") == "github")
    test("Has insights", "insights" in result)
    test("Detected languages", len(result.get("insights", {}).get("languages", [])) > 0,
         f"got: {result.get('insights', {}).get('languages', [])}")
    test("Has profile data", result.get("insights", {}).get("profile", {}).get("username") == "torvalds")

if __name__ == "__main__":
    print("🚀 Soulsync Skill — End-to-End Tests")
    print("=" * 50)
    
    test_detector_new()
    test_detector_partial()
    test_detector_established()
    test_synthesizer()
    test_github_importer()
    
    print(f"\n{'=' * 50}")
    print(f"Results: {TESTS_PASSED} passed, {TESTS_FAILED} failed")
    
    if TESTS_FAILED > 0:
        sys.exit(1)
    else:
        print("🎉 All tests passed!")
